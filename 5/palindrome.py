# SPDX-FileCopyrightText: Copyright (C) Nile Jocson <novoseiversia@gmail.com>
# SPDX-License-Identifier: 0BSD



def is_palindrome(s: str) -> bool:
	return s.lower() == s[::-1].lower()



s = input("Enter a string: ")

if is_palindrome(s):
	print(f"\"{ s }\" is a palindrome.")
else:
	print(f"\"{ s }\" is NOT a palindrome.")
