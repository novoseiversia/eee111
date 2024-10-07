# SPDX-FileCopyrightText: Copyright (C) Nile Jocson <novoseiversia@gmail.com>
# SPDX-License-Identifier: 0BSD

from enum import Enum
from math import ceil
from os import path
from typing import Any, List



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
	return input(prompt).split()



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

def parse_rules_any(
		rules: List[tuple[List[type | str], List[int | tuple[int | type]]]],
		args: List[str],
		default: List[Any]
) -> List[Any]:
	for input_rules, output_rules in rules:
		if parsed := parse_rules(input_rules, output_rules, args):
			return parsed

	return default

def parse_args(command: List[str]) -> List[Any]:
	needed_now_rules = ([str, "needed_now"], [(1, CommandType), 0])
	needed_in_rules  = ([str, "needed_in", int], [(1, CommandType), 0, 2])
	runs_out_rules   = ([str, "runs_out"], [(1, CommandType), 0])
	run_outs_rules   = ([str, int, "run_outs"], [(2, CommandType), 0, 1])
	exit_rules       = (["exit"], [(0, CommandType)])

	return parse_rules_any(
		[needed_now_rules, needed_in_rules, runs_out_rules, run_outs_rules, exit_rules],
		command,
		[CommandType.INVALID]
	)



def parse_database(filename: str) -> dict[str, tuple[int, int]]:
	file = open(filename, "r")
	deserialized = {}
	for line in file:
		if parsed := parse_rules(
			[str, int, int],
			[0, 1, 2],
			line.split(",")
		):
			deserialized[parsed[0]] = (parsed[1], parsed[2])
		else:
			raise RuntimeError("Invalid hospital supply database format.")

	return deserialized

def remove_extension(filename: str) -> str:
	return path.splitext(filename)[0]



def get_sorted_days_shortage(database: dict[str, tuple[int, int]]) -> List[tuple]:
	days_shortage = {}
	for item, (quantity, daily_usage) in database.items():
		runs_out_in = ceil(quantity / daily_usage)
		shortage = daily_usage * runs_out_in - quantity
		days_shortage[item] = (runs_out_in, shortage)

	sort_name     = sorted(days_shortage.items(), key=lambda kv: kv[0])
	sort_shortage = sorted(sort_name, key=lambda kv: kv[1][1], reverse=True)
	sort_days     = sorted(sort_shortage, key=lambda kv: kv[1][0])

	return sort_days



def needed_now(name: str, database: dict[str, tuple[int, int]]) -> None:
	print(f"Needed Items now for { name }:")

	for item, (quantity, daily_usage) in database.items():
		if quantity >= daily_usage:
			continue
		else:
			print(f"{ daily_usage - quantity } x { item }")

def needed_in(name: str, database: dict[str, tuple[int, int]], days: int) -> None:
	print(f"Needed Items in { days } day/s for { name }:")

	for item, (quantity, daily_usage) in database.items():
		needed = daily_usage * days
		if quantity >= needed:
			continue
		else:
			print(f"{ needed - quantity } x { item }")

def runs_out(name: str, database: dict[str, tuple[int, int]]) -> None:
	print(f"For { name }:")

	days_shortage = get_sorted_days_shortage(database)
	print(f"{ days_shortage[0][0] } will run out in { days_shortage[0][1][0] } day/s")

def run_outs(name: str, database: dict[str, tuple[int, int]], n_items: int) -> None:
	print(f"For { name }:")

	days_shortage = get_sorted_days_shortage(database)
	for item in days_shortage[:n_items]:
		print(f"{ item[0] } will run out in { item[1][0] } day/s")



def __main__():
	while True:
		command = parse_args(input_list(""))
		match command[0]:
			case CommandType.NEEDED_NOW:
				needed_now(remove_extension(command[1]), parse_database(command[1]))
			case CommandType.NEEDED_IN:
				needed_in(remove_extension(command[1]), parse_database(command[1]), command[2])
			case CommandType.RUNS_OUT:
				runs_out(remove_extension(command[1]), parse_database(command[1]))
			case CommandType.RUN_OUTS:
				run_outs(remove_extension(command[1]), parse_database(command[1]), command[2])
			case CommandType.EXIT:
				break
		print("")

	return



__main__()
