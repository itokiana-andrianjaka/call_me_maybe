#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   functions.py                                         :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: tiana-an <tiana-an@student.42antananarivo.   +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/08/27 09:04:09 by tiana-an            #+#    #+#            #
#   Updated: 2026/09/11 11:13:44 by tiana-an           ###   ########.fr      #
#                                                                             #
# ########################################################################### #

"""Define all functions with their signature."""

from .print_err import print_error

try:
    from pydantic import BaseModel, Field
    from llm_sdk import Small_LLM_Model
except ModuleNotFoundError as err:
    print_error(f"[Error]: {err}")


class Function(BaseModel):
    """Represents a function with its signature."""

    name: str = Field(min_length=1)
    description: str = Field(min_length=1)
    parameters: dict[str, str] = Field(min_length=1)
    return_type: str = Field(min_length=1)

    def ajust_type(self, llm: Small_LLM_Model) -> None:
        """Adjust the types of parameters based on the LLM model.

        Args:
            llm (Small_LLM_Model): The LLM model used for type adjustment.
        """
        type_token = {
            "int": llm.encode("int")[0].tolist(),
            "float": llm.encode("float")[0].tolist(),
            "str": llm.encode("str")[0].tolist(),
            "bool": llm.encode("bool")[0].tolist(),
        }
        large_type = {
            "digits": "int",
            "integer": "int",
            "string": "str",
            "sentence": "str",
            "boolean": "bool",
            "number": "float",
        }

        encoded = llm.encode("sentences=str, digit=int, ")[0].tolist()
        for param, param_type in self.parameters.items():
            if param_type in large_type:
                self.parameters[param] = large_type[param_type]
            elif param_type not in type_token:
                encoded.extend(llm.encode(f"{param}=")[0].tolist())
                logits = llm.get_logits_from_input_ids(encoded)
                probably = max(
                    type_token,
                    key=lambda type_name: logits[type_token[type_name][0]],
                )
                self.parameters[param] = probably
