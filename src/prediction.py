#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   prediction.py                                        :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: tiana-an <tiana-an@student.42antananarivo.   +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/09/01 10:26:00 by tiana-an            #+#    #+#            #
#   Updated: 2026/09/11 11:15:58 by tiana-an           ###   ########.fr      #
#                                                                             #
# ########################################################################### #

"""Provide the FunctionPredictor class."""

import json
from typing import Any

from .parsing import Parser
from .utils import format_result
from .giving_model import build_model_example
from .functions import Function
from .print_wcolors import print_with_colors
from .print_err import print_error

try:
    from llm_sdk import Small_LLM_Model
except ModuleNotFoundError as err:
    print_error(f"[Error]: {err}")


class FunctionPredictor:
    """Predict function calls based on prompts using a language model."""

    def __init__(self, llm: Small_LLM_Model, parser: Parser) -> None:
        """Initialize the FunctionPredictor.

        Args:
            llm: The language model used for predictions.
            parser: The parser containing function definitions and prompts.
        """
        self._llm: Small_LLM_Model = llm
        self._parser: Parser = parser
        self._encode_cache: dict[str, list[int]] = {}

        self._utils_tokens: dict[str, int] = {}
        for char in ["{", "}", "\n", '"']:
            self._utils_tokens[char] = self._encode_cached(char)[0]
        self._bool_tokens: dict[str, list[int]] = {}
        for value in ["true}", "false}"]:
            self._bool_tokens[value] = self._encode_cached(value)

        self._prompts: list[str] = [
            call.prompt for call in self._parser.callings
        ]
        self._fn_by_name: dict[str, Function] = {
            func.name: func for func in self._parser.functions
        }

        self._model_ex: str = build_model_example(self._parser, self._llm)
        encoded = self._llm.encode(self._model_ex)[0]
        self._base_encoded: list[int] = encoded.tolist()
        self._encoded: list[int] = self._base_encoded[:]

        self._f_tokens: dict[str, list[int]] = {}
        for func in self._parser.functions:
            self._f_tokens[func.name] = self._encode_cached(func.name)

        self._maxlen_ftokens: int = (
            len(max(self._f_tokens.values(), key=len)) + 1
        )
        self._func_available: set[str] = set(self._f_tokens)

    def _encode_cached(self, text: str) -> list[int]:
        """Encode text once and reuse its token IDs.

        Args:
            text (str): The text to be encoded.
        """
        if text not in self._encode_cache:
            self._encode_cache[text] = self._llm.encode(text)[0].tolist()
        return self._encode_cache[text]

    def _function_token(self, function_name: str, index: int) -> int:
        """Return a function token or its closing quote token.

        Args:
            function_name (str): The name of the function.
            index (int): The index of the token to return.

        Returns:
            int: The token ID.
        """
        tokens = self._f_tokens[function_name]
        if index < len(tokens):
            return tokens[index]
        return self._utils_tokens['"']

    def _select_best_ftoken(
        self, index: int, logits: list[float]
    ) -> int | None:
        """Select the best function token based on the logits.

        Args:
            index (int): The index of the token to select.
            logits (list[float]): The logits from the language model.

        Returns:
            int | None: The best token ID if available, otherwise None.
        """
        choices = [
            self._function_token(function_name, index)
            for function_name in self._func_available
        ]

        if not choices:
            return None

        best = max(choices, key=lambda token_id: logits[token_id])

        self._func_available = {
            function_name
            for function_name in self._func_available
            if self._function_token(function_name, index) == best
        }

        return best

    def _fname_predictor(self) -> str | None:
        """Predict the function name based on the encoded input.

        Returns:
            str | None: The predicted f_name if available, otherwise None.
        """
        self._func_available = set(self._f_tokens)

        for index in range(self._maxlen_ftokens):
            if len(self._func_available) == 1:
                func = next(iter(self._func_available))
                self._encoded.extend(self._f_tokens[func][index:])
                self._encoded.append(self._utils_tokens['"'])
                return func

            logits = self._llm.get_logits_from_input_ids(self._encoded)
            next_token_id = self._select_best_ftoken(index, logits)
            if next_token_id is None:
                for _ in range(index):
                    self._encoded.pop()
                return None

            self._encoded.append(next_token_id)

        raise ValueError("Function name exceeds maximum token length")

    def _predict_param_value(self, param_name: str, function: Function) -> Any:
        """Predict the value of a parameter.

        Args:
            param_name (str): The name of the parameter to predict.
            function (Function): The function to which the parameter belongs.

        Returns:
            Any: The predicted value of the parameter.
        """
        start = len(self._encoded)
        self._encoded.append(self._utils_tokens["{"])
        self._encoded.extend(self._encode_cached(f'"{param_name}": '))

        for token_index in range(50):
            logits = self._llm.get_logits_from_input_ids(self._encoded)
            if function.parameters[param_name] == "bool":
                best_value = max(
                    self._bool_tokens,
                    key=lambda value: logits[self._bool_tokens[value][0]],
                )
                self._encoded.extend(
                    self._bool_tokens[best_value]
                )
            else:
                best_token_id = max(range(len(logits)), key=logits.__getitem__)
                self._encoded.append(best_token_id)

            closes_object = False
            text_dict = self._llm.decode(self._encoded[start:]).lstrip()
            try:
                if text_dict.endswith(","):
                    text_dict = text_dict[:-1] + "}"
                    closes_object = True
                parsed, _ = json.JSONDecoder().raw_decode(text_dict)
            except json.JSONDecodeError:
                continue

            if isinstance(parsed, dict) and param_name in parsed:
                if closes_object:
                    self._encoded.append(self._utils_tokens["}"])
                return parsed[param_name]

            if token_index == 48:
                self._encoded.append(self._utils_tokens["}"])

        raise RuntimeError(
            "Failed to predict parameter value within 50 tokens"
        )

    def _predict_parameters(self, function: Function) -> dict[str, Any]:
        """Predict all parameters for a given function.

        Args:
            function (Function): The function for which to predict parameters.
        Returns:
            dict[str, Any]: A dictionary containing the predicted parameters.
        """
        res = {}

        self._encoded.extend(self._encode_cached("\nParameters: "))
        for param in function.parameters:
            res[param] = self._predict_param_value(param, function)
        self._encoded.append(self._utils_tokens["\n"])
        return res

    def _prepare_prompt(self, prompt: str) -> None:
        """Prepare the prompt for encoding.

        Args:
            prompt (str): The prompt to be prepared.
        """
        self._encoded = self._base_encoded[:]
        encoded_prompt = json.dumps(prompt, ensure_ascii=False)
        self._encoded.extend(
            self._llm.encode(
                f"\nUser request: {encoded_prompt}\n"
            )[0].tolist()
        )
        print_with_colors(f'"{prompt}"', "prompt")
        self._encoded.extend(self._encode_cached('Function name: "'))

    def _select_function(self) -> str:
        """Select the function to be called.

        Returns:
            str: The name of the selected function.
        """
        function_name = self._fname_predictor()
        if function_name is None:
            function_name = next(iter(self._fn_by_name))
            self._encoded.extend(self._encode_cached(f'{function_name}"'))
        print_with_colors(f'"{function_name}"', "fname")
        return function_name

    def res_predict(self) -> list[dict[str, Any]]:
        """Predict the results for the given prompts.

        Returns:
            list[dict[str, Any]]: List of predicted results for each prompt.
        """
        final_results: list[dict[str, Any]] = []
        for prompt in self._prompts:
            self._prepare_prompt(prompt)
            function_name = self._select_function()

            function = self._fn_by_name.get(function_name)
            if function is None:
                raise RuntimeError(f"Unknown function: {function_name}")

            parameters = self._predict_parameters(function)
            res = format_result(prompt, function_name, parameters, function)
            print_with_colors("", "end")
            final_results.append(res)
        return final_results
