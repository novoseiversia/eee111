# SPDX-FileCopyrightText: Copyright (C) Nile Jocson <novoseiversia@gmail.com>
# SPDX-License-Identifier: 0BSD

from dataclasses import dataclass
from enum import Enum
from functools import cmp_to_key
from math import ceil
from os import path
from typing import Any, Callable



class CommandType(Enum):
	NEEDED_NOW =  0,
	NEEDED_IN  =  1,
	RUNS_OUT   =  2,
	RUN_OUTS   =  3,
	HELP       =  4,
	EXIT       =  5,
	INVALID    = -1,

	@classmethod
	def _missing_(cls, value: object) -> Any:
		value = str(value).upper()
		for member in cls:
			if member.name == value:
				return member
		return cls.INVALID



@dataclass
class TransformInfo:
	convert : type | Callable
	position: int

@dataclass
class ParseRule:
	transforms : list[TransformInfo]
	find_string: str | None = None



@dataclass
class StockInfo:
	quantity      : int
	daily_usage   : int
	remaining_days: int
	deficit       : int

type SupplyDatabase = dict[str, StockInfo]
type SortedSupplyDatabase = list[tuple[str, StockInfo]]



def input_list(prompt: str) -> list[str]:
	return input(prompt).split()



def parse_rules(rules: list[ParseRule], args: list[str]) -> list[Any] | None:
	if len(args) != len(rules):
		return None

	outputs = 0
	for rule in rules:
		outputs += len(rule.transforms)

	parsed: list[Any] = [None] * outputs

	for rule, arg in zip(rules, args):
		if rule.find_string != None and rule.find_string != arg:
			return None

		try:
			for transform in rule.transforms:
				parsed[transform.position] = transform.convert(arg)

		except:
			return None

	return parsed

def parse_rulesets(rulesets: list[list[ParseRule]], args: list[str], default: list[Any]) -> list[Any]:
	for rules in rulesets:

		if parsed := parse_rules(rules, args):
			return parsed

	return default

def parse_args(args: list[str]) -> list[Any]:
	return parse_rulesets(
		[
			[
				ParseRule([TransformInfo(parse_database, 1), TransformInfo(remove_extension, 2)]),
				ParseRule([TransformInfo(CommandType, 0)], "needed_now")
			],
			[
				ParseRule([TransformInfo(parse_database, 1), TransformInfo(remove_extension, 2)]),
				ParseRule([TransformInfo(CommandType, 0)], "needed_in"),
				ParseRule([TransformInfo(int, 3)])
			],
			[
				ParseRule([TransformInfo(parse_database, 1), TransformInfo(remove_extension, 2)]),
				ParseRule([TransformInfo(CommandType, 0)], "runs_out")
			],
			[
				ParseRule([TransformInfo(parse_database, 1), TransformInfo(remove_extension, 2)]),
				ParseRule([TransformInfo(int, 3)]),
				ParseRule([TransformInfo(CommandType, 0)], "run_outs")
			],
			[
				ParseRule([TransformInfo(CommandType, 0)], "help")
			],
			[
				ParseRule([TransformInfo(CommandType, 0)], "exit")
			],
		],
		args,
		[CommandType.INVALID]
	)



def parse_database(filename: str) -> SupplyDatabase:
	file = open(filename, "r")
	database: SupplyDatabase = {}

	for line in file:
		if parsed := parse_rules(
			[ParseRule([TransformInfo(str, 0)]), ParseRule([TransformInfo(int, 1)]), ParseRule([TransformInfo(int, 2)])],
			line.split(",")
		):
			name = parsed[0]
			quantity = parsed[1]
			daily_usage = parsed[2]
			remaining_days = ceil(quantity / daily_usage)
			deficit = daily_usage * remaining_days - quantity

			database[name] = StockInfo(quantity, daily_usage, remaining_days, deficit)

		else:
			raise RuntimeError("Invalid hospital supply database format.")

	file.close()
	return database

def remove_extension(filename: str) -> str:
	return path.splitext(filename)[0]



def strcmp(left: str, right: str) -> int:
	if left < right:
		return -1

	elif left > right:
		return 1

	else:
		return 0

def supply_database_compare(left: tuple[str, StockInfo], right: tuple[str, StockInfo]) -> int:
	left_name, left_info = left
	right_name, right_info = right

	if (compare_days := left_info.remaining_days - right_info.remaining_days) != 0:
		return compare_days

	if (compare_deficit := right_info.deficit - left_info.deficit) != 0:
		return compare_deficit

	return strcmp(left_name, right_name)

def get_sorted_supply_database(database: SupplyDatabase) -> SortedSupplyDatabase:
	return sorted(database.items(), key=cmp_to_key(supply_database_compare))



def needed_now(args: list[Any]) -> None:
	database = args[1]
	name = args[2]

	print(f"Needed Items now for { name }:")

	for item, info in database.items():
		if info.quantity >= info.daily_usage:
			continue

		else:
			print(f"{ info.daily_usage - info.quantity } x { item }")

def needed_in(args: list[Any]) -> None:
	database = args[1]
	name = args[2]
	x = args[3]

	print(f"Needed Items in { x } day/s for { name }:")

	for item, info in database.items():
		needed = info.daily_usage * x
		if info.quantity >= needed:
			continue

		else:
			print(f"{ needed - info.quantity } x { item }")

def runs_out(args: list[Any]) -> None:
	database = args[1]
	name = args[2]

	print(f"For { name }:")

	sorted_database = get_sorted_supply_database(database)
	item = sorted_database[0]
	print(f"{ item[0] } will run out in { item[1].remaining_days } day/s")

def run_outs(args: list[Any]) -> None:
	database = args[1]
	name = args[2]
	n = args[3]

	print(f"For { name }:")

	sorted_database = get_sorted_supply_database(database)
	for item in sorted_database[:n]:
		print(f"{ item[0] } will run out in { item[1].remaining_days } day/s")

def help_string(info: str | None = None) -> None:
	if info != None:
		info += "\n"

	else:
		info = ""

	print(f"""{ info }Usage:
	<file_name:str> needed_now        Gets amount of items needed immediately for the day.
	<file_name:str> needed_in <X:int> Gets amount of items needed in X days.
	<file_name:str> runs_out          Prints the first item to run out, and in how many days.
	<file_name:str> <N:int> run_outs  Prints the first N items to run out, and in how many days.
	help                              Prints this message.
	exit                              Exits the program."""
	)



def run_command(args: list[Any]) -> bool:
	match args[0]:
		case CommandType.NEEDED_NOW:
			needed_now(args)

		case CommandType.NEEDED_IN:
			needed_in(args)

		case CommandType.RUNS_OUT:
			runs_out(args)

		case CommandType.RUN_OUTS:
			run_outs(args)

		case CommandType.HELP:
			help_string()

		case CommandType.EXIT:
			return False

		case _:
			help_string("Invalid arguments provided.")

	return True



def __main__():
	while True:
		args = parse_args(input_list(""))

		try:
			if not run_command(args):
				return

		except Exception as e:
			print(e)

		print("")



__main__()
