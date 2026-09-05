#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   print_wcolors.py                                     :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: tiana-an <tiana-an@student.42antananarivo.   +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/09/04 11:15:21 by tiana-an            #+#    #+#            #
#   Updated: 2026/09/04 11:15:22 by tiana-an           ###   ########.fr      #
#                                                                             #
# ########################################################################### #

import sys


class Color:
    FUCHSIA = "\033[38;5;201m"
    YELLOW = "\033[93m"
    RESET = "\033[0m"


def print_with_colors(text: str) -> None:
    if '"prompt":' in text and '"name":' in text:
        part_prompt, part_name = text.split('"name":', 1)
        before_prompt, prompt_val = part_prompt.split('"prompt":', 1)

        sys.stdout.write(f"{Color.RESET}{before_prompt}")
        sys.stdout.write(f'{Color.FUCHSIA}"prompt":{Color.RESET}')
        sys.stdout.write(f"{Color.YELLOW}{prompt_val}{Color.RESET}")

        sys.stdout.write(f'{Color.FUCHSIA}"name":{Color.RESET}')
        sys.stdout.write(f"{Color.RESET}{part_name}")

    elif '"prompt":' in text:
        before_prompt, prompt_val = text.split('"prompt":', 1)
        sys.stdout.write(f"{Color.RESET}{before_prompt}")
        sys.stdout.write(f'{Color.FUCHSIA}"prompt":{Color.RESET}')
        sys.stdout.write(f"{Color.YELLOW}{prompt_val}{Color.RESET}")

    elif '"name"' in text or '"parameters"' in text:
        flag = '"name"' if '"name"' in text else '"parameters"'
        before_flag, after_flag = text.split(flag, 1)
        sys.stdout.write(f"{Color.RESET}{before_flag}")
        sys.stdout.write(f"{Color.FUCHSIA}{flag}{Color.RESET}")
        sys.stdout.write(f"{Color.RESET}{after_flag}")

    else:
        sys.stdout.write(f"{Color.RESET}{text}")

    sys.stdout.flush()