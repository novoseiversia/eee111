# SPDX-FileCopyrightText: Copyright (C) Nile Jocson <novoseiversia@gmail.com>
# SPDX-License-Identifier: 0BSD



def is_anagram(a: str, b: str) -> bool:
	sorted_lower_a = sorted(a.lower())
	sorted_lower_b = sorted(b.lower())

	return sorted_lower_a == sorted_lower_b



a = input("Enter your first string: ")
b = input("Enter your second string: ")

if is_anagram(a, b):
	print(f"\"{ a }\" and \"{ b }\" are anagrams of each other.")
else:
	print(f"\"{ a }\" and \"{ b }\" are NOT anagrams of each other.")
