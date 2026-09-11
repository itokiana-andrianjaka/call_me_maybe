#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   giving_model.py                                      :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: tiana-an <tiana-an@student.42antananarivo.   +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/09/09 13:11:51 by tiana-an            #+#    #+#            #
#   Updated: 2026/09/11 09:14:44 by tiana-an           ###   ########.fr      #
#                                                                             #
# ########################################################################### #

"""Provide the build_model_example function."""

from .print_err import print_error
from .parsing import Parser
import json

try:
    from llm_sdk import Small_LLM_Model
except ImportError as err:
    print_error(f"[Error]: {err}")


def build_model_example(parser: Parser, llm: Small_LLM_Model) -> str:
    """Build a model example based on the parser and language model.

    Args:
        parser: The parser containing function definitions and prompts.
        llm: The language model used for type adjustment.

    Returns:
        str: A string representing the model example.
    """
    model_ex = (
        "Choose the function that best matches each user request.\n"
        "Return the function name in quotes, followed by a JSON object "
        "containing its parameters.\n"
        "Available functions:\n"
    )

    for f in parser.functions:
        f.ajust_type(llm)
        func_repr = {
            "name": f.name,
            "description": f.description,
            "parameters": f.parameters,
        }
        model_ex += (
            json.dumps(func_repr, ensure_ascii=False, indent=2) + "\n\n"
        )

    return model_ex
