#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   utils.py                                             :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: tiana-an <tiana-an@student.42antananarivo.   +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/09/04 11:15:17 by tiana-an            #+#    #+#            #
#   Updated: 2026/09/09 17:33:45 by tiana-an           ###   ########.fr      #
#                                                                             #
# ########################################################################### #

"""Provide utility functions for the program."""

from typing import Any

from .functions import Function
from .print_wcolors import print_with_colors


def format_result(
    prompt: str,
    function_name: str,
    parameters: dict[str, Any],
    corresp_fn: Function,
) -> dict[str, Any]:
    """Format the result of a function call.

    Args:
        prompt (str): The prompt that led to the function call.
        function_name (str): The name of the function being called.
        parameters (dict[str, Any]): The parameters for the function call.
        corresp_fn (Function): The corresponding Function object.

    Returns:
        dict[str, Any]: A dictionary containing the formatted result.
    """
    result: dict[str, Any] = {
        "prompt": prompt,
        "name": function_name,
        "parameters": parameters,
    }
    for param, value in result["parameters"].items():
        if corresp_fn.parameters[param] in ["float", "int", "bool"]:
            try:
                if corresp_fn.parameters[param] == "int":
                    result["parameters"][param] = int(round(value))
                elif corresp_fn.parameters[param] == "float":
                    floated = float(value)
                    result["parameters"][param] = floated
                else:
                    result["parameters"][param] = value

            except (ValueError, TypeError):
                result["parameters"][param] = value
            print_with_colors(f". {param}: {str(result['parameters'][param])}")
        else:
            print_with_colors(
                f'. {param}: "{str(result["parameters"][param])}"'
            )
    return result
