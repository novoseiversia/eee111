# SPDX-FileCopyrightText: Copyright (C) Nile Jocson <novoseiversia@gmail.com>
# SPDX-License-Identifier: 0BSD



def input_list_int(prompt: str) -> list[int]:
	while True:
		try:
			parsed = [int(s) for s in input(prompt).split()]
		except ValueError:
			print("Please enter a valid list of integers.")
		else:
			return parsed



def sum_integers(integers: list[int]) -> int:
	accum = 0
	for i in integers:
		accum += i
	return accum

def avg_integers(integers: list[int]) -> int:
	return int(sum_integers(integers) / len(integers))



integers = input_list_int("Enter a space-separated list of integers: ")

integers_sum = sum_integers(integers)
integers_avg = avg_integers(integers)

print(f"Sum = { integers_sum }\tAvg = { integers_avg }")
