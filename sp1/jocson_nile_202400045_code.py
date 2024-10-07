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

	def make(self, *args: Any) -> tuple[Self, List[Any]]:
		return (self, list(args))

	@classmethod
	def _missing_(cls, value: object) -> Any:
		value = value.upper()
		for member in cls:
			if member.name == value:
				return member
		return cls.INVALID

type Command = tuple[CommandType, List[Any]]



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
			else:
				parsed_args.append(arg)
		else:
			parsed_args.append(rule(arg))

	output_args = []
	for rule in output_rules:
		if isinstance(rule, int):
			output_args.append(parsed_args[rule])
		else:
			output_args.append(rule[1](parsed_args[rule[0]]))

	return output_args



def parse_args(command: List[str]) -> Command:
	if command[1] == "needed_now":
		return CommandType.NEEDED_NOW.make(command[0])
	elif command[1] == "needed_in":
		return CommandType.NEEDED_IN.make(command[0], command[2])
	elif command[1] == "runs_out":
		return CommandType.RUNS_OUT.make(command[0])
	elif command[2] == "run_outs":
		return CommandType.RUN_OUTS.make(command[0], command[1])
	elif command[0] == "exit":
		return CommandType.EXIT.make()
	else:
		return CommandType.INVALID.make()



def __main__():
	print(parse_args(input_list("Input your command:")))
	return



__main__()
