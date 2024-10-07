# SPDX-FileCopyrightText: Copyright (C) Nile Jocson <novoseiversia@gmail.com>
# SPDX-License-Identifier: 0BSD

from enum import Enum
from typing import Any, List



class CommandType(Enum):
	NEEDED_NOW =  0,
	NEEDED_IN  =  1,
	RUNS_OUT   =  2,
	RUN_OUTS   =  3,
	EXIT       =  4,
	INVALID    = -1,



def input_list(prompt: str) -> List[str]:
	return [s for s in input(prompt).split]

def parse_command(command: List[str]) -> tuple[CommandType, List[Any]]:
	if command[1] == "needed_now":
		return (CommandType.NEEDED_NOW, [command[0]])
	elif command[1] == "needed_in":
		return (CommandType.NEEDED_IN, [command[0], command[2]])
	elif command[1] == "runs_out":
		return (CommandType.RUNS_OUT, [command[0]])
	elif command[2] == "run_outs":
		return (CommandType.RUN_OUTS, [command[0], command[1]])
	elif command[0] == "exit":
		return (CommandType.EXIT, [])
	else:
		return (CommandType.INVALID, [])



def __main__():
	return



__main__()
