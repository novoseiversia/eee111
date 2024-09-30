# SPDX-FileCopyrightText: Copyright (C) Nile Jocson <novoseiversia@gmail.com>
# SPDX-License-Identifier: 0BSD



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



x = input_int("Input x: ")

print("")
if prime(x):
	print(f"{ x } is prime")
else:
	print(f"{ x } is not prime")
