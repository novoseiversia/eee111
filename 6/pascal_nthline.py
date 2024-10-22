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



def pascal_nthline(n: int) -> list[int]:
	if n == 0:
		return [1]

	last = pascal_nthline(n - 1)
	out: list[int] = []

	out.append(1)
	for x, y in zip(last[:-1], last[1:]):
		out.append(x + y)
	out.append(1)

	return out



n = input_int("Input n: ")

for x in pascal_nthline(n):
	print(x, end = " ")
