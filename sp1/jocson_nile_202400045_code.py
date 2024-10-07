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
	EXIT       =  4,
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
	quantity: int
	daily_usage: int

@dataclass
class RemainingInfo:
	name: str
	remaining_days: int
	deficit: int



type InputRules = list[type | str]
type OutputRules = list[int | tuple[int, type]]
type RuleSet = tuple[InputRules, OutputRules]

type SupplyDatabase = dict[str, StockInfo]



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

def parse_rules_any(rules: list[RuleSet], args: list[str], default: list[Any]) -> list[Any]:
	for input_rules, output_rules in rules:
		if parsed := parse_rules(input_rules, output_rules, args):
			return parsed
	return default

def parse_args(command: list[str]) -> list[Any]:
	return parse_rules_any(
		[
			([str, "needed_now"    ], [(1, CommandType), 0   ]),
			([str, "needed_in", int], [(1, CommandType), 0, 2]),
			([str, "runs_out"      ], [(1, CommandType), 0   ]),
			([str, int, "run_outs" ], [(2, CommandType), 0, 1]),
			(["exit"               ], [(0, CommandType)      ])
		],
		command,
		[CommandType.INVALID]
	)



def parse_database(filename: str) -> SupplyDatabase:
	file = open(filename, "r")
	deserialized: SupplyDatabase = {}
	for line in file:
		if parsed := parse_rules(
			[str, int, int],
			[0, 1, 2],
			line.split(",")
		):
			deserialized[parsed[0]] = StockInfo(parsed[1], parsed[2])
		else:
			raise RuntimeError("Invalid hospital supply database format.")
	file.close()
	return deserialized

def remove_extension(filename: str) -> str:
	return path.splitext(filename)[0]



def get_sorted_remaining_days_deficit(database: SupplyDatabase) -> list[RemainingInfo]:
	remaining_days_deficit: dict[str, tuple[int, int]] = {}
	for item, stock_info in database.items():
		remaining_days = ceil(stock_info.quantity / stock_info.daily_usage)
		deficit = stock_info.daily_usage * remaining_days - stock_info.quantity
		remaining_days_deficit[item] = (remaining_days, deficit)

	sort_name     = sorted(remaining_days_deficit.items(), key=lambda kv: kv[0])
	sort_shortage = sorted(sort_name, key=lambda kv: kv[1][1], reverse=True)
	sort_days     = sorted(sort_shortage, key=lambda kv: kv[1][0])

	return [RemainingInfo(item, info[0], info[1]) for item, info in sort_days]



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

	remaining_days_deficit = get_sorted_remaining_days_deficit(database)
	print(f"{ remaining_days_deficit[0].name } will run out in { remaining_days_deficit[0].remaining_days } day/s")

def run_outs(name: str, database: SupplyDatabase, n_items: int) -> None:
	print(f"For { name }:")

	remaining_days_deficit = get_sorted_remaining_days_deficit(database)
	for item in remaining_days_deficit[:n_items]:
		print(f"{ item.name } will run out in { item.remaining_days } day/s")



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
