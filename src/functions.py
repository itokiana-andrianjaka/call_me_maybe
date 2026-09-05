#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   functions.py                                         :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: tiana-an <tiana-an@student.42antananarivo.   +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/08/27 09:04:09 by tiana-an            #+#    #+#            #
#   Updated: 2026/09/05 06:50:12 by tiana-an           ###   ########.fr      #
#                                                                             #
# ########################################################################### #

from .print_err import print_error

try:
    from pydantic import BaseModel, Field, model_validator
except ModuleNotFoundError as err:
    print_error(f"[Error]: {err}")


class Function(BaseModel):
    name: str = Field(min_length=1)
    description: str = Field(min_length=1)
    parameters: dict[str, str] = Field(min_length=1)
    return_type: str = Field(min_length=1)

    @model_validator(mode="after")
    def num_to_float(self) -> "Function":
        for param in self.parameters:
            if self.parameters[param] in ["number", "num"]:
                self.parameters[param] = "float"
        if self.return_type in ["number", "num"]:
            self.return_type = "float"
        return self
