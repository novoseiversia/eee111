# SPDX-FileCopyrightText: Copyright (C) Nile Jocson <novoseiversia@gmail.com>
# SPDX-License-Identifier: 0BSD

from enum import Enum
from typing import List



class CommandType(Enum):
	NEEDED_IN  =  0,
	NEEDED_NOW =  1,
	RUNS_OUT   =  2,
	RUN_OUTS   =  3,
	EXIT       =  4,
	INVALID    = -1,



def input_list(prompt: str) -> List[str]:
	return [s for s in input(prompt).split]



def __main__():
	return



__main__()
