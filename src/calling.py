#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   calling.py                                           :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: tiana-an <tiana-an@student.42antananarivo.   +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/08/27 09:04:05 by tiana-an            #+#    #+#            #
#   Updated: 2026/08/27 15:38:47 by tiana-an           ###   ########.fr      #
#                                                                             #
# ########################################################################### #

from .print_err import print_error

try:
    from pydantic import BaseModel, Field
except ModuleNotFoundError as err:
    print_error(f"[Error]: {err}")


class Calling(BaseModel):
    prompt: str = Field(min_length=1)
