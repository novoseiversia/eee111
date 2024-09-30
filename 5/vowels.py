# SPDX-FileCopyrightText: Copyright (C) Nile Jocson <novoseiversia@gmail.com>
# SPDX-License-Identifier: 0BSD



def print_vowels(s: str) -> None:
	vowels = []
	for c in s:
		if c in "AEIOUaeiou":
			vowels.append(c)
	print(f"The string \"{ s }\" contains the vowels: { vowels }")



s = input("Enter a string: ")
print_vowels(s)
