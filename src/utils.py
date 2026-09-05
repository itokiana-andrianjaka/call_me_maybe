#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   utils.py                                             :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: tiana-an <tiana-an@student.42antananarivo.   +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/09/04 11:15:17 by tiana-an            #+#    #+#            #
#   Updated: 2026/09/04 11:15:18 by tiana-an           ###   ########.fr      #
#                                                                             #
# ########################################################################### #

def last_quoted(string: str) -> str | None:
    parts = string.split('"')
    if len(parts) < 3 or len(parts) % 2 == 0:
        return None
    return parts[-2]
