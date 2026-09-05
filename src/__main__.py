#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   __main__.py                                          :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: tiana-an <tiana-an@student.42antananarivo.   +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/08/27 09:04:13 by tiana-an            #+#    #+#            #
#   Updated: 2026/09/04 22:27:57 by tiana-an           ###   ########.fr      #
#                                                                             #
# ########################################################################### #

import time
from .print_err import print_error
from .parsing import Parser
from .prediction import FunctionPredictor

try:
    from llm_sdk import Small_LLM_Model
except ModuleNotFoundError as err:
    print_error(f"[Error]: {err}")

if __name__ == "__main__":

    start_time = time.time()

    all_func: str = ""
    all_prompt: list[str] = []
    try:
        parser: Parser = Parser()
        llm = Small_LLM_Model()
        generator = FunctionPredictor(llm, parser)
        generator.res_predict()

    except BaseException as err:
        print_error(f"Failure: {err}")
    finally:
        end_time = time.time()
        diff_time = end_time - start_time
        print(f"Execution time: {diff_time:.2f} seconds")
