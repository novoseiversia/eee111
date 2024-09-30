# SPDX-FileCopyrightText: Copyright (C) Nile Jocson <novoseiversia@gmail.com>
# SPDX-License-Identifier: 0BSD



a = input("Input a: ")
b = input("Input b: ")
print(f"Before swap: a = { a }, b = { b }")

a, b = b, a
print(f"After swap: a = { a }, b = { b }")
