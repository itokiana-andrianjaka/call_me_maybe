#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   prediction.py                                        :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: tiana-an <tiana-an@student.42antananarivo.   +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/09/01 10:26:00 by tiana-an            #+#    #+#            #
#   Updated: 2026/09/05 11:49:23 by tiana-an           ###   ########.fr      #
#                                                                             #
# ########################################################################### #

from .parsing import Parser
from .print_err import print_error
import json
from typing import Any

try:
    from llm_sdk import Small_LLM_Model
except ModuleNotFoundError as err:
    print_error(f"[Error]: {err}")


class FunctionPredictor:
    """Gestionnaire de prédiction de fonctions sous contraintes pour LLM."""

    def __init__(self, llm: Small_LLM_Model, parser: Parser):
        self.llm = llm
        self.parser = parser

        self._utils_tokens = {}
        for char in ['{', '}', '\n', ',', ' ', '"', ':', '.', '-', '+']:
            enc_char = self.llm.encode(char)[0]
            self._utils_tokens[char] = enc_char.tolist()[0]

        self._prompts = [call.prompt for call in parser.callings]
        self._prompt_tokens = {
            prompt: self.llm.encode(f'"{prompt}"')[0].tolist()
            for prompt in self._prompts
        }
        #ilaina b
        self._fn_by_name = {
            func.name: func for func in parser.functions
        }

        self._parameter_tokens = {
            func.name: {
                name: self.llm.encode(name)[0].tolist()
                for name in func.parameters
            }
            for func in parser.functions
        }

        self._model_ex = ""
        self._build_model_example()
        # print(self._model_ex)

        encoded_ex = self.llm.encode(self._model_ex)[0]
        self._base_encoded = encoded_ex.tolist()
        self._encoded = self._base_encoded[:]

        # Encodage des noms de fonctions
        self.f_tokens: dict[str, list[int]] = {}
        for func in self.parser.functions:
            func_enc = self.llm.encode(func.name)[0]
            token_list = func_enc.tolist()
            self.f_tokens[func] = token_list

        self._maxlen_ftokens = len(
            max(self.f_tokens.values(), key=len)
        )

        self._func_avoid = set()

        # Limite de sécurité pour la génération des paramètres
        self._max_param_tokens = 100

    def _build_model_example(self) -> None:
        self._model_ex += '(\n"fn_find_total" - '
        self._model_ex += '[Calculate the total from a known percentage value.]\n'
        self._model_ex += '"parameters": '
        self._model_ex += '{"goal": string, "percent": float, "value": float}\n)\n'

        for f in self.parser.functions:
            self._model_ex += f'(\n"{f.name}" - '
            self._model_ex += f'[{f.description}]\n'
            self._model_ex += f'"parameters": {f.parameters}\n)\n'


        self._model_ex += '\n"get \\"total score\\" from 2% = 5"'
        self._model_ex += '\n"fn_find_total",\n'
        self._model_ex += '{"goal": "total score"}\n'
        self._model_ex += '{"percent": 2.0}\n'
        self._model_ex += '{"value": 5.0}\n'

    def _select_best_ftoken(self, index: int, logits: list[float]) -> int:
        choice = []

        for func in self.f_tokens:
            if func in self._func_avoid:
                continue

            tokens = self.f_tokens[func]
            choice.append(tokens[index])

        best = max(choice, key=lambda token_id: logits[token_id])

        for func in self.f_tokens:
            if self.f_tokens[func][index] != best:
                self._func_avoid.add(func)

        return best

    def _fname_predictor(self) -> str | None:
        name_start = len(self._encoded)
        self._encoded.append(self._utils_tokens['"'])

        for index in range(self._maxlen_ftokens):
            logits = self.llm.get_logits_from_input_ids(self._encoded)
            next_token_id = self._select_best_ftoken(index, logits)
            self._encoded.append(next_token_id)
    
            if next_token_id == self._utils_tokens['"']:
                name = self.llm.decode(
                    self._encoded[name_start:]
                )
                try:
                    to_validate = f'{name}'
                    json.loads(to_validate)
                except json.JSONDecodeError:
                    continue
                f_name = name.strip('"')
                return f_name if f_name in self._fn_by_name else None

        raise ValueError("Function name exceeds maximum token length")

    def _predict_parameter_value(self, key: str) -> Any:
        self._encoded.append(self._utils_tokens['{'])
        self._encoded.extend(
            self.llm.encode(f'"{key}": ')[0].tolist()
        )
    
        val_start = len(self._encoded)
    
        for _ in range(self._max_param_tokens):
            logits = self.llm.get_logits_from_input_ids(self._encoded)
            best_token_id = max(range(len(logits)), key=logits.__getitem__)
            self._encoded.append(best_token_id)
    
            if best_token_id == self._utils_tokens['}']:
                value = self.llm.decode(
                    self._encoded[val_start:-1]
                )
    
                try:
                    return json.loads(value)
                except json.JSONDecodeError:
                    continue
    
        raise RuntimeError("Unable to terminate the parameter value")

    def _get_function(self, function_name: str):
        return self._functions_by_name.get(function_name)

    def res_predict(self) -> None:
        """Lance la prédiction pour tous les prompts (avec reset du contexte)."""
        full_res = []
        for count, prompt in enumerate(self._prompts):
            self._encoded = self._base_encoded[:]

            # Construction de la structure JSON
            self._encoded.append(self._utils_tokens['{'])
            self._encoded.append(self._utils_tokens['\n'])
            self._encoded.extend(self._flag_tokens['\t"prompt": '])

            self._encoded.extend(self._prompt_tokens[prompt])

            self._encoded.append(self._utils_tokens[','])
            self._encoded.append(self._utils_tokens['\n'])

            # Génération contrainte du nom de fonction
            self._encoded.extend(self._flag_tokens['\t"name": '])
            function_name = self._fname_predictor()

            function = self._get_function(function_name)
            if function is None:
                function = next(iter(self._fn_by_name))

            self._encoded.extend(self._flag_tokens[',\n\t"parameters": {'])

            for index, parameter in enumerate(function.parameters):
                if index:
                    self._encoded.append(self._utils_tokens[' '])
                self._encoded.append(self._utils_tokens['"'])
                self._encoded.extend(
                    self._parameter_tokens[function.name][parameter]
                )
                self._encoded.append(self._utils_tokens['"'])
                self._encoded.append(self._utils_tokens[':'])
                self._predict_parameter_value()

            self._encoded.append(self._utils_tokens['}'])
            if count < len(self._prompts) - 1:
                self._encoded.append(self._utils_tokens[','])
                self._encoded.append(self._utils_tokens['\n'])
            full_res.extend(self._encoded[len(self._base_encoded):])

        # Affichage du résultat
        print(self.llm.decode(full_res))
