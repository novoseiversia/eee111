# SPDX-FileCopyrightText: Copyright (C) Nile Jocson <novoseiversia@gmail.com>
# SPDX-License-Identifier: 0BSD

from enum import Enum
from typing import Any, List, Self



class CommandType(Enum):
	NEEDED_NOW =  0,
	NEEDED_IN  =  1,
	RUNS_OUT   =  2,
	RUN_OUTS   =  3,
	EXIT       =  4,
	INVALID    = -1,

	@classmethod
	def _missing_(cls, value: object) -> Any:
		value = value.upper()
		for member in cls:
			if member.name == value:
				return member
		return cls.INVALID



def input_list(prompt: str) -> List[str]:
	return [s for s in input(prompt).split()]

def parse_rules(
		input_rules: List[type | str],
		output_rules: List[int | tuple[int, type]],
		args: List[str]
) -> List[Any] | None:
	if len(args) != len(input_rules):
		return None

	parsed_args = []
	for rule, arg in zip(input_rules, args):
		if isinstance(rule, str):
			if not isinstance(arg, str):
				return None
			if rule != arg:
				return None
			else:
				parsed_args.append(arg)
		else:
			try:
				parsed_args.append(rule(arg))
			except:
				return None

	output_args = []
	for rule in output_rules:
		if isinstance(rule, int):
			output_args.append(parsed_args[rule])
		else:
			output_args.append(rule[1](parsed_args[rule[0]]))

	return output_args



def parse_args(command: List[str]) -> List[Any]:
	if parsed := parse_rules(
		[str, "needed_now"],
		[(1, CommandType), 0],
		command
	):
		return parsed

	elif parsed := parse_rules(
		[str, "needed_in", int],
		[(1, CommandType), 0, 2],
		command
	):
		return parsed

	elif parsed := parse_rules(
		[str, "runs_out"],
		[(1, CommandType), 0],
		command
	):
		return parsed

	elif parsed := parse_rules(
		[str, int, "runouts"],
		[(2, CommandType), 0, 1],
		command
	):
		return parsed

	elif parsed := parse_rules(
		["exit"],
		[(0, CommandType)],
		command
	):
		return parsed

	else:
		return [CommandType.INVALID]



def __main__():
	print(parse_args(input_list("Input your command:")))
	return



__main__()
