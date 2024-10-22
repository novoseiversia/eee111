# SPDX-FileCopyrightText: Copyright (C) Nile Jocson <novoseiversia@gmail.com>
# SPDX-License-Identifier: 0BSD



def input_int(prompt: str) -> int:
	while True:
		try:
			parsed = int(input(prompt))
		except ValueError:
			print("Please enter a valid integer.")
		else:
			return parsed



def binary_ndigit_z(n: int, z: int) -> list[str]:
	if n == 1:
		if z == 0:
			return ["1"]
		elif z == 1:
			return ["0"]
		else:
			return []

	out: list[str] = []
	for b in binary_ndigit_z(n - 1, z):
		out.append(b + "1")

	for b in binary_ndigit_z(n - 1, z - 1):
		out.append(b + "0")

	return out



n = input_int("Input n: ")
z = input_int("Input z: ")

print(f"All { n }-digit binary numbers with { z } zero/es:")
for b in binary_ndigit_z(n, z):
	print(b)
