# SPDX-FileCopyrightText: Copyright (C) Nile Jocson <novoseiversia@gmail.com>
# SPDX-License-Identifier: 0BSD



def input_float_none(prompt: str, *, none: bool = False) -> float | None:
	while True:
		try:
			parsed = float(input(prompt))
		except ValueError:
			if none:
				return None
			print("Please enter a valid number.")
		else:
			return parsed



def nthroot(x: float, n: float = 2) -> float:
	return x ** (1/n)



x = input_float_none("Input x: ")
n = input_float_none("Input n (default: 2): ", none = True)

print("")

if x != None:
	if n == None:
		root = nthroot(x)
		print(f"root({ x }) = { root }")
	else:
		root = nthroot(x, n)
		print(f"root({ x }, { n }) = { root }")
