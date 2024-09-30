# SPDX-FileCopyrightText: Copyright (C) Nile Jocson <novoseiversia@gmail.com>
# SPDX-License-Identifier: 0BSD



def input_float(prompt: str) -> float:
	while True:
		try:
			parsed = float(input(prompt))
		except ValueError:
			print("Please enter a valid number.")
		else:
			return parsed



a = input_float("Input a: ")
b = input_float("Input b: ")
c = input_float("Input c: ")

sum = a + b + c
product = a * b * c
average = sum / 3

print("")
print(f"Sum: { sum }")
print(f"Product: { product }")
print(f"Average: { average }")
