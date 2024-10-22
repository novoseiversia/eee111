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



def binary_ndigit(n: int) -> list[str]:
	if n == 1:
		return ["0", "1"]

	out: list[str] = []
	for b in binary_ndigit(n - 1):
		out.append(b + "0")
		out.append(b + "1")

	return out



n = input_int("Input n: ")

print(f"All { n }-digit binary numbers:")
for b in binary_ndigit(n):
	print(b)
