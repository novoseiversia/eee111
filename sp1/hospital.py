# SPDX-FileCopyrightText: Copyright (C) Nile Jocson <novoseiversia@gmail.com>
# SPDX-License-Identifier: 0BSD

from dataclasses import dataclass
from functools import cmp_to_key
from math import ceil
from os import path
from typing import Any, Callable



@dataclass
class Transform:
	convert : type | Callable
	position: int

@dataclass
class Rule:
	transforms : list[Transform]
	find_string: str | None = None

@dataclass
class CommandSpec:
	rules   : list[Rule]
	callback: Callable[[list[Any]], bool]



@dataclass
class Item:
	name          : str
	quantity      : int
	daily_usage   : int
	remaining_days: int
	deficit       : int

type SupplyDatabase = list[Item]



def input_list(prompt: str) -> list[str]:
	return input(prompt).split()



def parse_rules(rules: list[Rule], args: list[str]) -> list[Any] | None:
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

def try_commandspecs(specs: list[CommandSpec], args: list[str], default: Callable[[], bool]) -> bool:
	for spec in specs:

		if (parsed := parse_rules(spec.rules, args)) != None:
			return spec.callback(parsed)

	return default()



def parse_database(filename: str) -> SupplyDatabase:
	file = open(filename, "r")
	database: SupplyDatabase = []

	for line in file:
		if parsed := parse_rules(
			[Rule([Transform(str, 0)]), Rule([Transform(int, 1)]), Rule([Transform(int, 2)])],
			line.split(",")
		):
			name = parsed[0]
			quantity = parsed[1]
			daily_usage = parsed[2]
			remaining_days = ceil(quantity / daily_usage)
			deficit = daily_usage * remaining_days - quantity

			database.append(Item(name, quantity, daily_usage, remaining_days, deficit))

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

def supply_database_compare(left: Item, right: Item) -> int:

	if (compare_days := left.remaining_days - right.remaining_days) != 0:
		return compare_days

	if (compare_deficit := right.deficit - left.deficit) != 0:
		return compare_deficit

	return strcmp(left.name, right.name)

def sort_supply_database(database: SupplyDatabase) -> SupplyDatabase:
	return sorted(database, key=cmp_to_key(supply_database_compare))



def needed_now(args: list[Any]) -> bool:
	database = args[0]
	name = args[1]

	print(f"Needed Items now for { name }:")

	for item in database:
		if item.quantity >= item.daily_usage:
			continue

		else:
			print(f"{ item.daily_usage - item.quantity } x { item.name }")

	return True

def needed_in(args: list[Any]) -> bool:
	database = args[0]
	name = args[1]
	x = args[2]

	print(f"Needed Items in { x } day/s for { name }:")

	for item in database:
		needed = item.daily_usage * x
		if item.quantity >= needed:
			continue

		else:
			print(f"{ needed - item.quantity } x { item.name }")

	return True

def runs_out(args: list[Any]) -> bool:
	database = args[0]
	name = args[1]

	print(f"For { name }:")

	sorted_database = sort_supply_database(database)
	item = sorted_database[0]
	print(f"{ item.name } will run out in { item.remaining_days } day/s")

	return True

def run_outs(args: list[Any]) -> bool:
	database = args[0]
	name = args[1]
	n = args[2]

	print(f"For { name }:")

	sorted_database = sort_supply_database(database)
	for item in sorted_database[:n]:
		print(f"{ item.name } will run out in { item.remaining_days } day/s")

	return True

def help_string(info: str | None = None) -> bool:
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

	return True



def	run_command(args: list[str]) -> bool:
	return try_commandspecs(
		[
			CommandSpec(
				[
					Rule([Transform(parse_database, 0), Transform(remove_extension, 1)]),
					Rule([], "needed_now")
				],
				needed_now
			),

			CommandSpec(
				[
					Rule([Transform(parse_database, 0), Transform(remove_extension, 1)]),
					Rule([], "needed_in"),
					Rule([Transform(int, 2)])
				],
				needed_in
			),

			CommandSpec(
				[
					Rule([Transform(parse_database, 0), Transform(remove_extension, 1)]),
					Rule([], "runs_out")
				],
				runs_out
			),

			CommandSpec(
				[
					Rule([Transform(parse_database, 0), Transform(remove_extension, 1)]),
					Rule([Transform(int, 2)]),
					Rule([], "run_outs")
				],
				run_outs
			),

			CommandSpec(
				[
					Rule([], "help")
				],
				lambda _: help_string()
			),

			CommandSpec(
				[
					Rule([], "exit")
				],
				lambda _: False
			)
		],
		args,
		lambda: help_string("Invalid arguments provided.")
	)



def __main__():
	while True:
		args = input_list("")

		try:
			if run_command(args) == False:
				return

		except Exception as e:
			print(e)

		print("")



__main__()
