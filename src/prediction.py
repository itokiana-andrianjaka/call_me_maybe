#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   prediction.py                                        :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: tiana-an <tiana-an@student.42antananarivo.   +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/09/01 10:26:00 by tiana-an            #+#    #+#            #
#   Updated: 2026/09/05 11:02:20 by tiana-an           ###   ########.fr      #
#                                                                             #
# ########################################################################### #

from .parsing import Parser
from .print_err import print_error

try:
    from llm_sdk import Small_LLM_Model
except ModuleNotFoundError as err:
    print_error(f"[Error]: {err}")


class FunctionPredictor:
    """Gestionnaire de prédiction de fonctions sous contraintes pour LLM."""

    def __init__(self, llm: Small_LLM_Model, parser: Parser):
        self.llm = llm
        self.parser = parser

        # Récupération des noms de fonctions et des prompts
        self._available_fn = [func.name for func in parser.functions]
        self._prompts = [call.prompt for call in parser.callings]
        self._prompt_tokens = {
            prompt: self.llm.encode(f'"{prompt}"')[0].tolist()
            for prompt in self._prompts
        }
        self._functions_by_name = {
            func.name: func for func in parser.functions
        }

        self._model_ex = ""
        self._build_model_example()
        # print(self._model_ex)

        # Encodage de base (few-shot uniquement) — on le sauvegarde pour le réutiliser
        encoded_ex = self.llm.encode(self._model_ex)[0]
        self._base_encoded = encoded_ex.tolist()
        self._encoded = self._base_encoded[:]

        self._utils_tokens = {}
        for char in ['{', '}', '\n', ',', ' ', '"', ':']:
            enc_char = self.llm.encode(char)[0]
            self._utils_tokens[char] = enc_char.tolist()[0]
        self._utils_tokens['====='] = self.llm.encode("=====")[0].tolist()

        self._flag_tokens = {}
        flags = ['\t"prompt": ', '\t"name": ', ',\n\t"parameters": {']
        for flag in flags:
            enc_flag = self.llm.encode(flag)[0]
            self._flag_tokens[flag] = enc_flag.tolist()

        self._parameter_tokens = {
            func.name: {
                name: self.llm.encode(name)[0].tolist()
                for name in func.parameters
            }
            for func in parser.functions
        }

        # Encodage des noms de fonctions + pré-calcul des tokens autorisés par position
        self.f_tokens = []
        max_len = 0
        for func in self.parser.functions:
            func_enc = self.llm.encode(func.name)[0]
            token_list = func_enc.tolist()
            self.f_tokens.append(token_list)
            if len(token_list) > max_len:
                max_len = len(token_list)

        self._allowed_by_pos = []
        for index in range(max_len + 1):
            allowed = set()
            for token_list in self.f_tokens:
                if index < len(token_list):
                    allowed.add(token_list[index])
                else:
                    allowed.add(self._utils_tokens['"'])
            self._allowed_by_pos.append(allowed)

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


        self._model_ex += '{\n\t"prompt": "get "total score" from 2% = 5",'
        self._model_ex += '\n\t"name": "fn_find_total",'
        self._model_ex += '\n\t"parameters": '
        self._model_ex += '{"goal": "total score", "percent": 2.0, "value": 5.0}\n}\n'

    def _select_best_ftoken(self, index: int, logits: list[float]) -> int:
        if index < len(self._allowed_by_pos):
            allowed = self._allowed_by_pos[index]
        else:
            allowed = {self._utils_tokens['"']}

        best_id = self._utils_tokens['"']
        best_val = float("-inf")
        vocab_size = len(logits)

        for token_id in allowed:
            if token_id < vocab_size and logits[token_id] > best_val:
                best_val = logits[token_id]
                best_id = token_id

        return best_id

    def _fname_predictor(self) -> str | None:
        """Génère soit le nom de fonction (contraint), soit les paramètres JSON."""
        # Ouverture du guillemet pour le nom
        name_start = len(self._encoded)
        self._encoded.append(self._utils_tokens['"'])
        index = 0
        max_name_tokens = len(self._allowed_by_pos)

        while index < max_name_tokens:
            logits = self.llm.get_logits_from_input_ids(self._encoded)
            next_token_id = self._select_best_ftoken(index, logits)
            self._encoded.append(next_token_id)

            # Fin dès qu'on génère le guillemet de fermeture
            if next_token_id == self._utils_tokens['"']:
                break
            index += 1

        return self.llm.decode(self._encoded[name_start:]).strip('"')

    def _predict_parameter_value(self) -> None:
        """Génère une valeur jusqu'au séparateur JSON suivant."""
        for _ in range(self._max_param_tokens):
            logits = self.llm.get_logits_from_input_ids(self._encoded)
            best_token_id = max(range(len(logits)), key=logits.__getitem__)
            self._encoded.append(best_token_id)

            token_text = self.llm.decode([best_token_id])
            # print(token_text)
            if "," in token_text or "}" in token_text:
                return

        raise RuntimeError("Unable to terminate the parameter value")

    def _get_function(self, function_name: str):
        return self._functions_by_name.get(function_name)

    def res_predict(self) -> None:
        """Lance la prédiction pour tous les prompts (avec reset du contexte)."""
        for prompt in self._prompts:
            self._encoded = self._base_encoded[:]

            self._encoded.extend(self._utils_tokens['====='])
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
                function = next(
                    (func for func in self.parser.functions if func.name == self._available_fn[0]),
                    None,
                )
            self._encoded.extend(self._flag_tokens[',\n\t"parameters": {'])

            for index, parameter_name in enumerate(function.parameters):
                if index:
                    self._encoded.append(self._utils_tokens[' '])
                self._encoded.append(self._utils_tokens['"'])
                self._encoded.extend(
                    self._parameter_tokens[function.name][parameter_name]
                )
                self._encoded.append(self._utils_tokens['"'])
                self._encoded.append(self._utils_tokens[':'])
                self._predict_parameter_value()

            self._encoded.append(self._utils_tokens['}'])

            # Affichage du résultat
            full_text = self.llm.decode(self._encoded)
            print(full_text.split("=====")[-1].strip())
