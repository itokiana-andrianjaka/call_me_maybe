#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   calling.py                                           :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: tiana-an <tiana-an@student.42antananarivo.   +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/08/27 09:04:05 by tiana-an            #+#    #+#            #
#   Updated: 2026/09/09 16:22:30 by tiana-an           ###   ########.fr      #
#                                                                             #
# ########################################################################### #

"""Define the Calling class, which represents a function call with a prompt."""

from .print_err import print_error

try:
    from pydantic import BaseModel, Field, model_validator
except ModuleNotFoundError as err:
    print_error(f"[Error]: {err}")


class Calling(BaseModel):
    """Represents a function call with a prompt."""

    prompt: str = Field(min_length=1)

    @model_validator(mode="after")
    def validate_prompt(self) -> "Calling":
        """Validate the prompt field.

        Returns:
            Calling: The validated Calling instance.
        """
        self.prompt = self.prompt.lstrip()
        if len(self.prompt) == 0:
            raise ValueError("Prompt cannot be empty or whitespace only.")
        return self
