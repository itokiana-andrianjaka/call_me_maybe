#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   print_wcolors.py                                     :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: tiana-an <tiana-an@student.42antananarivo.   +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/09/04 11:15:21 by tiana-an            #+#    #+#            #
#   Updated: 2026/09/09 04:45:57 by tiana-an           ###   ########.fr      #
#                                                                             #
# ########################################################################### #

"""Provide a function to print text with colors using the rich library."""

from typing import Literal
from rich import print as rich_print


def print_with_colors(
    text: str = "",
    prompt_fname: Literal["prompt", "fname", "end"] | None = None,
) -> None:
    """Print text with colors based on the provided prompt_fname.

    Args:
        text: The message to print. Defaults to "".
        prompt_fname: The type to print. Defaults to None.
    """
    if prompt_fname is not None:
        if prompt_fname == "prompt":
            rich_print("[bold magenta]Prompt:[/bold magenta]", end=" ")
            rich_print(f"[cyan]{text}[/cyan]")

        elif prompt_fname == "fname":
            rich_print("[bold magenta]Corresponding Function:[/bold magenta]")
            rich_print("[bold yellow]\tName:[/bold yellow]", end=" ")
            print(text)
            rich_print("[bold yellow]\tParameters:[/bold yellow]", end="")

        elif prompt_fname == "end":
            rich_print("\n\n")

        else:
            raise ValueError(f"Invalid value for prompt_fname: {prompt_fname}")

    else:
        if text.startswith("."):
            print("\n\t\t", end="")
            print("\U00002022", end="")
            print(text[1:], end="")
