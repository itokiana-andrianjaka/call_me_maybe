#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   parsing.py                                           :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: tiana-an <tiana-an@student.42antananarivo.   +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/08/27 09:04:18 by tiana-an            #+#    #+#            #
#   Updated: 2026/09/01 14:56:56 by tiana-an           ###   ########.fr      #
#                                                                             #
# ########################################################################### #

from .functions import Function
from .calling import Calling
from .print_err import print_error
from typing import Any

try:
    from pydantic import BaseModel, Field, ValidationError, model_validator
    from json import JSONDecodeError, load
    from pathlib import Path
except ModuleNotFoundError as err:
    print_error(f"[Error]: {err}")


class Parser(BaseModel):
    functions: list[Function] = []
    callings: list[Calling] = []
    fdef_path: str = Field(
        default=str(
            Path(__file__).resolve().parent / "../data/input/functions_definition.json"
        )
    )
    fcall_path: str = Field(
        default=str(
            Path(__file__).resolve().parent
            / "../data/input/function_calling_tests.json"
        )
    )

    def _process_function(self, function_data: dict[str, Any]) -> Function:
        name: str = function_data["name"]
        description: str = function_data["description"]
        params_to_manage: dict[str, dict[str, str]] = function_data["parameters"]
        parameters: dict[str, str] = {}
        for param in params_to_manage:
            parameters[param] = params_to_manage[param]["type"]

        returns_to_manage: dict[str, str] = function_data["returns"]
        return_type: str = returns_to_manage["type"]

        return Function(
            name=name,
            description=description,
            parameters=parameters,
            return_type=return_type,
        )

    def _process_calling(self, call_data: dict[str, str]) -> Calling:
        return Calling(prompt=call_data["prompt"])

    @model_validator(mode="after")
    def parsing_function_def(self) -> "Parser":
        try:
            with open(self.fdef_path, "r", encoding="utf-8") as file:
                json_fdata = load(file)
            for function_data in json_fdata:
                self.functions.append(self._process_function(function_data))

        except (
            ValueError,
            KeyError,
            ValidationError,
            JSONDecodeError,
            FileNotFoundError,
            OSError,
        ) as err:
            if err.__class__.__name__ == "KeyError":
                raise Exception(
                    f"[Error]: Wrong key in the JSON data, it must be '{err.args[0]}'"
                )
            raise Exception(str(err))

        return self

    @model_validator(mode="after")
    def parsing_calling(self) -> "Parser":
        try:
            with open(self.fcall_path, "r", encoding="utf-8") as file:
                json_calldata = load(file)
            for call_data in json_calldata:
                self.callings.append(self._process_calling(call_data))

        except (
            ValueError,
            KeyError,
            ValidationError,
            JSONDecodeError,
            FileNotFoundError,
            OSError,
        ) as err:
            if err.__class__.__name__ == "KeyError":
                raise Exception(
                    f"[Error]: Wrong key in the JSON data, it must be '{err.args[0]}'"
                )
            raise Exception(str(err))

        return self
