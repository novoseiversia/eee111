# SPDX-FileCopyrightText: Copyright (C) Nile Jocson <novoseiversia@gmail.com>
# SPDX-License-Identifier: 0BSD

from dataclasses import dataclass
from enum import Enum
from math import ceil
from os import path
from typing import Any



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
class StockInfo:
	quantity      : int
	daily_usage   : int
	remaining_days: int
	deficit       : int

type InputRules = list[type | str]
type OutputRules = list[int | tuple[int, type]]
type RuleSet = tuple[InputRules, OutputRules]

type SupplyDatabase = dict[str, StockInfo]
type SortedSupplyDatabase = list[tuple[str, StockInfo]]



def input_list(prompt: str) -> list[str]:
	return input(prompt).split()



def parse_rules(input_rules: InputRules, output_rules: OutputRules, args: list[str]) -> list[Any] | None:
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

def parse_rulesets(rulesets: list[RuleSet], args: list[str], default: list[Any]) -> list[Any]:
	for input_rules, output_rules in rulesets:
		if parsed := parse_rules(input_rules, output_rules, args):
			return parsed
	return default

def parse_args(args: list[str]) -> list[Any]:
	return parse_rulesets(
		[
			([str, "needed_now"    ], [(1, CommandType), 0   ]),
			([str, "needed_in", int], [(1, CommandType), 0, 2]),
			([str, "runs_out"      ], [(1, CommandType), 0   ]),
			([str, int, "run_outs" ], [(2, CommandType), 0, 1]),
			(["help"               ], [(0, CommandType)      ]),
			(["exit"               ], [(0, CommandType)      ])
		],
		args,
		[CommandType.INVALID]
	)



def parse_database(filename: str) -> SupplyDatabase:
	file = open(filename, "r")
	database: SupplyDatabase = {}

	for line in file:
		if parsed := parse_rules(
			[str, int, int],
			[0, 1, 2],
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



def get_sorted_supply_database(database: SupplyDatabase) -> SortedSupplyDatabase:
	sort_name    = sorted(database.items(), key=lambda i: i[0])
	sort_deficit = sorted(sort_name, key=lambda i: i[1].deficit, reverse=True)
	sort_days    = sorted(sort_deficit, key=lambda i: i[1].remaining_days)

	return sort_days



def needed_now(name: str, database: SupplyDatabase) -> None:
	print(f"Needed Items now for { name }:")

	for item, stock_info in database.items():
		if stock_info.quantity >= stock_info.daily_usage:
			continue
		else:
			print(f"{ stock_info.daily_usage - stock_info.quantity } x { item }")

def needed_in(name: str, database: SupplyDatabase, days: int) -> None:
	print(f"Needed Items in { days } day/s for { name }:")

	for item, stock_info in database.items():
		needed = stock_info.daily_usage * days
		if stock_info.quantity >= needed:
			continue
		else:
			print(f"{ needed - stock_info.quantity } x { item }")

def runs_out(name: str, database: SupplyDatabase) -> None:
	print(f"For { name }:")

	sorted_database = get_sorted_supply_database(database)

	item = sorted_database[0]
	print(f"{ item[0] } will run out in { item[1].remaining_days } day/s")

def run_outs(name: str, database: SupplyDatabase, n_items: int) -> None:
	print(f"For { name }:")

	sorted_database = get_sorted_supply_database(database)
	for item in sorted_database[:n_items]:
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



def __main__():
	while True:
		command = parse_args(input_list(""))
		try:
			match command[0]:
				case CommandType.NEEDED_NOW:
					needed_now(remove_extension(command[1]), parse_database(command[1]))
				case CommandType.NEEDED_IN:
					needed_in(remove_extension(command[1]), parse_database(command[1]), command[2])
				case CommandType.RUNS_OUT:
					runs_out(remove_extension(command[1]), parse_database(command[1]))
				case CommandType.RUN_OUTS:
					run_outs(remove_extension(command[1]), parse_database(command[1]), command[2])
				case CommandType.HELP:
					help_string()
				case CommandType.EXIT:
					break
				case _:
					help_string("Invalid arguments provided.")
		except Exception as e:
			print(e)
		print("")

	return



__main__()
