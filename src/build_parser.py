#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   build_parser.py                                      :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: tiana-an <tiana-an@student.42antananarivo.   +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/09/08 16:13:09 by tiana-an            #+#    #+#            #
#   Updated: 2026/09/11 12:44:44 by tiana-an           ###   ########.fr      #
#                                                                             #
# ########################################################################### #

"""Provide a function to build an argument parser for the program."""

import argparse
from pathlib import Path


def build_parser() -> argparse.ArgumentParser:
    """Build and returns an argument parser for the program.

    Returns:
        argparse.ArgumentParser: The built argument parser.
    """
    parser: argparse.ArgumentParser = argparse.ArgumentParser(
        description="Predict function calls from prompts."
    )
    parser.add_argument(
        "--functions_definition",
        type=Path,
        default=Path(__file__).resolve().parent
        / "../data/input/functions_definition.json",
        help="Path to the function definitions JSON file.",
    )
    parser.add_argument(
        "--input",
        type=Path,
        default=Path(__file__).resolve().parent
        / "../data/input/function_calling_tests.json",
        help="Path to the prompts JSON file.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(__file__).resolve().parent
        / "../data/output/function_calling_results.json",
        help="Write predictions to this file instead of stdout.",
    )
    parser.add_argument(
        "--model",
        type=str,
        default="Qwen/Qwen3-0.6B",
        help="The model to use for predictions.",
    )
    return parser
