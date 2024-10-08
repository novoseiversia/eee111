# SPDX-FileCopyrightText: Copyright (C) Nile Jocson <novoseiversia@gmail.com>
# SPDX-License-Identifier: 0BSD

from dataclasses import dataclass
from enum import Enum
from math import ceil
from os import path
from typing import Any, Optional, Self



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
		"""
		Allow construction of a CommandType from its name. Case-insensitive.

		Returns
		-------
		Any
			A member of the enum corresponding to the string. INVALID if none matched.
		"""
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
	"""
	Prompts the user to input a space-separated list.
	"""
	return input(prompt).split()



def parse_rules(input_rules: InputRules, output_rules: OutputRules, args: list[str]) -> Optional[list[Any]]:
	"""
	Parses the given arguments based on input and output rules.

	Parameters
	----------
	input_rules : InputRules
		If the rule is a type, tries to convert the corresponding argument into that type.
		If the rule is a string, compares the corresponding argument with that string.
		If any of these fail, the argument list is immediately invalid.
	output_rules : OutputRules
		Takes the element of the converted arguments and appends them into the list to be returned,
		converting them again if a type is specified.
	args : list[str]
		The arguments to parse.

	Returns
	-------
	Optional[list[Any]]
		None is returned if the list is invalid; i.e. if the lengths of args and input_rules mismatch,
		or if any of the input_rules weren't followed.
		Otherwise, the converted and reordered arguments are returned.

	Notes
	-----
	Given the command specification:
		<file_name> needed_in <X>
	The docopt string can be inferred:
		<file_name:str> needed_in <X:int>
	The input_rules can then be created from this:
		[str, "needed_in", int]

	Using these rules, the following args are invalid:
		["needed_in", "3"]
		["Hospital1.csv", "needed_in"]
		["Hospital1.csv", "needed_in", "a"]

	Only arguments that satisfy all input_rules are valid, such as:
		["Hospital1.csv", "needed_in", "3"]
	This is then converted based on the input_rules:
		["Hospital1.csv", "needed_in", 3]

	In order to rearrange and further convert the arguments, output_rules should be specified:
		[(1, CommandType), 0, 2]
	The final output can then be calculated:
		[CommandType.NEEDED_IN, "Hospital1.csv", 3]
	"""
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
	"""
	Tries to parse the arguments with the given rulesets, and returns the first valid parse.

	Parameters
	----------
	rules : list[RuleSet]
		The list of RuleSets to try (a RuleSet is a pair of InputRules and OutputRules).
	args : list[str]
		The arguments to parse.
	default: list[Any]
		The default value returned if no valid parses were made.

	Returns
	-------
	list[Any]
		The first valid parse from the given list of rules, or default if no valid parses were made.
	"""
	for input_rules, output_rules in rules:
		if parsed := parse_rules(input_rules, output_rules, args):
			return parsed
	return default



def parse_args(command: list[str]) -> list[Any]:
	"""
	Parse the given arguments into a command.

	Parameters
	----------
	command : list[str]
		The arguments to parse.

	Returns
	-------
	list[Any]
		The command type and its arguments parsed from the given list of rules.
		INVALID if no rules were satisfied.

	Notes
	-----
	This tries to parse the arguments into the following docopt strings:
		<file_name:str> "needed_now"
		<file_name:str> "needed_in" <X:int>
		<file_name:str> "runs_out"
		<file_name:str> <N:int> "run_outs"
		"help"
		"exit"
	"""
	return parse_rules_any(
		[
			([str, "needed_now"    ], [(1, CommandType), 0   ]),
			([str, "needed_in", int], [(1, CommandType), 0, 2]),
			([str, "runs_out"      ], [(1, CommandType), 0   ]),
			([str, int, "run_outs" ], [(2, CommandType), 0, 1]),
			(["help"               ], [(0, CommandType)      ]),
			(["exit"               ], [(0, CommandType)      ])
		],
		command,
		[CommandType.INVALID]
	)



def parse_database(filename: str) -> SupplyDatabase:
	"""
	Parses the given csv file as a SupplyDatabase.

	Raises
	------
	RuntimeError
		If the csv file could not be parsed as a SupplyDatabase.

	Notes
	-----
	This tries to parse each line of the csv file using the following docopt string:
		<item_name:str> <quantity:int> <daily_usage:int>
	"""
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
	"""
	Removes the file extension from the given filename.
	"""
	return path.splitext(filename)[0]



def get_sorted_remaining_days_deficit(database: SupplyDatabase) -> list[RemainingInfo]:
	remaining_days_deficit: list[RemainingInfo] = []
	for item, stock_info in database.items():
		remaining_days = ceil(stock_info.quantity / stock_info.daily_usage)
		deficit = stock_info.daily_usage * remaining_days - stock_info.quantity
		remaining_days_deficit.append(RemainingInfo(item, remaining_days, deficit))

	sort_name    = sorted(remaining_days_deficit, key=lambda i: i.name)
	sort_deficit = sorted(sort_name, key=lambda i: i.deficit, reverse=True)
	sort_days    = sorted(sort_deficit, key=lambda i: i.remaining_days)

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

	remaining_days_deficit = get_sorted_remaining_days_deficit(database)
	print(f"{ remaining_days_deficit[0].name } will run out in { remaining_days_deficit[0].remaining_days } day/s")

def run_outs(name: str, database: SupplyDatabase, n_items: int) -> None:
	print(f"For { name }:")

	remaining_days_deficit = get_sorted_remaining_days_deficit(database)
	for item in remaining_days_deficit[:n_items]:
		print(f"{ item.name } will run out in { item.remaining_days } day/s")



def help(info: Optional[str] = None) -> None:
	if info != None:
		info += "\n"
	else:
		info = ""

	print(f"""{ info }Usage:
	<file_name:str> needed_now        Gets amount of items needed immediately for the day.
	<file_name:str> needed_in <X:int> Gets amount of items needed in X days.
	<file_name:str> runs_out          Prints the first item to run out, as well as how many days it will last.
	<file_name:str> <N:int> run_outs  Prints the first N items to run out, as well as how many days they will last.
	help                              Prints this message.
	exit                              Exits the program."""
	)



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
			case CommandType.HELP:
				help()
			case CommandType.EXIT:
				break
			case _:
				help("Invalid arguments provided.")
		print("")

	return



__main__()
