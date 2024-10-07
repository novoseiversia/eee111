# SPDX-FileCopyrightText: Copyright (C) Nile Jocson <novoseiversia@gmail.com>
# SPDX-License-Identifier: 0BSD

from typing import Optional



def input_float(prompt: str, *, noexcept: bool = False) -> Optional[float]:
	while True:
		try:
			parsed = float(input(prompt))
		except ValueError:
			if noexcept:
				return None
			print("Please enter a valid number.")
		else:
			return parsed




def nthroot(x: float, n: float = 2) -> float:
	return x ** (1/n)



x = input_float("Input x: ")
n = input_float("Input n (default: 2): ", noexcept = True)

print("")

if x != None:
	if n == None:
		root = nthroot(x)
		print(f"root({ x }) = { root }")
	else:
		root = nthroot(x, n)
		print(f"root({ x }, { n }) = { root }")
