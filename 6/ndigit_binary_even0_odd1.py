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



def ndigit_binary_z(n: int, z: int) -> list[str]:
	if n == 1:
		if z == 0:
			return ["1"]
		elif z == 1:
			return ["0"]
		else:
			return []

	out: list[str] = []
	for b in ndigit_binary_z(n - 1, z):
		out.append(b + "1")

	for b in ndigit_binary_z(n - 1, z - 1):
		out.append(b + "0")

	return out



def ndigit_binary_even0_odd1(n: int, z: int | None = None) -> list[str]:
	if n % 2 == 0:
		return []
	if z == None:
		return ndigit_binary_even0_odd1(n, n - 1)
	if z == 0:
		return ndigit_binary_z(n, 0)

	return ndigit_binary_z(n, z) + ndigit_binary_even0_odd1(n, z - 2)



n = input_int("Input n: ")

print(f"All { n }-digit binary numbers with an even amount of zeroes and an odd amount of ones:")
for b in ndigit_binary_even0_odd1(n):
	print(b)
