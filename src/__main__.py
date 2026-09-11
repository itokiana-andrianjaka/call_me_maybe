#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   __main__.py                                          :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: tiana-an <tiana-an@student.42antananarivo.   +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/08/27 09:04:13 by tiana-an            #+#    #+#            #
#   Updated: 2026/09/11 12:46:38 by tiana-an           ###   ########.fr      #
#                                                                             #
# ########################################################################### #

"""The entrypoint of the program."""

from typing import Any

from .parsing import Parser
from .prediction import FunctionPredictor
from .build_parser import build_parser
from .giving_output import giving_output
from .print_err import print_error

try:
    from pydantic import ValidationError
    from llm_sdk import Small_LLM_Model
except ModuleNotFoundError as err:
    print_error(f"[Error]: {err}")


def main() -> None:
    """Execute all logic of the program.

    raises:
        BaseException: If any error occurs during the execution of the program.
    """
    arguments = build_parser().parse_args()
    try:
        llm: Small_LLM_Model = Small_LLM_Model(
            model_name=arguments.model
        )

        parser: Parser = Parser(
            fdef_path=str(arguments.functions_definition),
            fcall_path=str(arguments.input),
        )
        generator: FunctionPredictor = FunctionPredictor(llm, parser)
        final_result: list[dict[str, Any]] = generator.res_predict()
        giving_output(final_result, str(arguments.output))

    except ValidationError as err:
        error = ""
        for e in err.errors():
            msg = e["msg"]
            error += f"{msg}\n"
        print_error(error)

    except BaseException as err:
        if err.__class__.__name__ == "KeyboardInterrupt":
            print_error("[Interrupted]")
        else:
            print_error(str(err))


if __name__ == "__main__":
    main()
