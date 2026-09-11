#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   parsing.py                                           :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: tiana-an <tiana-an@student.42antananarivo.   +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/08/27 09:04:18 by tiana-an            #+#    #+#            #
#   Updated: 2026/09/11 08:59:21 by tiana-an           ###   ########.fr      #
#                                                                             #
# ########################################################################### #

"""Provide a parser for function definitions, calls from JSON files."""

from typing import Any
from json import load
from pathlib import Path

from .functions import Function
from .calling import Calling
from .print_err import print_error

try:
    from pydantic import BaseModel, Field, model_validator
except ModuleNotFoundError as err:
    print_error(f"[Error]: {err}")


class Parser(BaseModel):
    """Parses function definitions and function calls from JSON files."""

    functions: list[Function] = Field(default_factory=list)
    callings: list[Calling] = Field(default_factory=list)
    fdef_path: str = Field(min_length=len(".json") + 1)
    fcall_path: str = Field(min_length=len(".json") + 1)

    def _process_function(self, function_data: dict[str, Any]) -> Function:
        """Process a function definition from a dictionary.

        Args:
            function_data: A dict containing the function definition data.

        Returns:
            Function: The processed function.
        """
        if len(function_data) != 4:
            raise ValueError(
                "[Error]: Function definition must contain 4 keys:\n"
                "'name', 'description', 'parameters', and 'returns'."
            )
        name: str = function_data["name"]
        description: str = function_data["description"]
        params_to_manage: dict[str, dict[str, str]] = function_data[
            "parameters"
        ]
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
        """Process a function call from a dictionary.

        Args:
            call_data: A dictionary containing the function call data.

        Returns:
            Calling: The processed function call.
        """
        if len(call_data) != 1:
            raise ValueError(
                "[Error]: Function call must contain only prompt key."
            )
        return Calling(prompt=call_data["prompt"])

    def _parsing_function_def(self) -> None:
        """Parse function definitions from the JSON file."""
        try:
            with open(self.fdef_path, "r", encoding="utf-8") as file:
                json_fdata = load(file)
            for function_data in json_fdata:
                self.functions.append(self._process_function(function_data))

        except (
            ValueError,
            TypeError,
            KeyError,
            OSError,
        ) as e:
            if isinstance(e, KeyError):
                raise KeyError(
                    f"[Error]: Wrong key in the JSON data -> '{e.args[0]}'"
                )
            raise ValueError(f"Invalid function definitions:\n{e}")

    def _parsing_calling(self) -> None:
        """Parse function calls from the JSON file."""
        try:
            with open(self.fcall_path, "r", encoding="utf-8") as file:
                json_calldata = load(file)
            for call_data in json_calldata:
                self.callings.append(self._process_calling(call_data))

        except (
            ValueError,
            TypeError,
            KeyError,
            OSError,
        ) as e:
            if isinstance(e, KeyError):
                raise KeyError(
                    f"[Error]: Wrong key in the JSON data -> '{e.args[0]}'"
                )
            raise ValueError(f"Invalid function calls:\n{e}")

    @model_validator(mode="after")
    def _validate_paths(self) -> "Parser":
        """Validate the paths for function definitions and function calls.

        Returns:
            Parser: The validated Parser instance.
        """
        if not self.fdef_path.endswith(
            ".json"
        ) or not self.fcall_path.endswith(".json"):
            raise ValueError("[Error]: \
Function definition/calling file must be a JSON file.")

        if (
            not Path(self.fdef_path).is_file()
            or not Path(self.fcall_path).is_file()
        ):
            raise FileNotFoundError(
                "[Error]: Function definition/calling file not found."
            )

        self._parsing_function_def()
        self._parsing_calling()

        if not self.functions:
            raise ValueError(
                f"[Error]: No functions found in '{self.fdef_path}'."
            )

        if not self.callings:
            raise ValueError(
                f"[Error]: No callings found in '{self.fcall_path}'."
            )

        return self
