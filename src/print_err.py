#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   print_err.py                                         :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: tiana-an <tiana-an@student.42antananarivo.   +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/08/27 09:04:22 by tiana-an            #+#    #+#            #
#   Updated: 2026/08/27 15:38:55 by tiana-an           ###   ########.fr      #
#                                                                             #
# ########################################################################### #

"""Module used to print each error."""

import sys
from typing import NoReturn

COLORS = {
    "BLUE": "\033[36m",
    "RESET": "\033[0m",
}


def print_error(msg: str) -> NoReturn:
    """Print an error message and exit the program.

    Args:
        msg (str): The error message to be printed.

    Returns:
        NoReturn: This function does not return; it exits the program.
    """
    print(
        f"{COLORS['BLUE']}\n{msg}\n{COLORS['RESET']}",
        file=sys.stderr,
    )

    sys.exit()
