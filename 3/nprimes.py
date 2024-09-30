# SPDX-FileCopyrightText: Copyright (C) Nile Jocson <novoseiversia@gmail.com>
# SPDX-License-Identifier: 0BSD

from typing import List



def input_int(prompt: str, *, noexcept: bool = False) -> int:
	while True:
		try:
			parsed = int(input(prompt))
		except ValueError:
			if noexcept:
				return None
			print("Please enter a valid integer.")
		else:
			return parsed



def prime(x: int) -> bool:
	for i in range(2, x):
		if x % i == 0:
			return False
	return True

def nprimes(n: int) -> List[int]:
	x = 2
	primes = []
	while len(primes) < n:
		if prime(x):
			primes.append(x)
		x += 1

	return primes



n = input_int("Input n: ")

print("")
print(f"First { n } primes: { nprimes(n) }")
