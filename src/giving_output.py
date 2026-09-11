#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   giving_output.py                                     :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: tiana-an <tiana-an@student.42antananarivo.   +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/09/08 16:16:12 by tiana-an            #+#    #+#            #
#   Updated: 2026/09/09 04:24:45 by tiana-an           ###   ########.fr      #
#                                                                             #
# ########################################################################### #

"""Provide a function to write the final result to a JSON file."""

from typing import Any
from pathlib import Path
import json


def giving_output(
    final_result: list[dict[str, Any]], output_path: str
) -> None:
    """Write the final result to a JSON file.

    Args:
        final_result: The final result to be written to the JSON file.
        output_path: The path to the output JSON file.
    """
    if not output_path.endswith(".json"):
        raise ValueError("[Error]: Output file must be a JSON file.")

    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)

    try:
        with output_file.open("w", encoding="utf-8") as file:
            json.dump(final_result, file, indent=2, ensure_ascii=False)
            file.write("\n")

    except OSError as err:
        raise OSError(f"Failed to write to output file:\n{err}")
