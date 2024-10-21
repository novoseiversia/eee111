# SPDX-FileCopyrightText: Copyright (C) Nile Jocson <novoseiversia@gmail.com>
# SPDX-License-Identifier: 0BSD



def ndigit_binary(n: int) -> list[str]:
	if n == 1:
		return ["0", "1"]

	out = []
	for b in ndigit_binary(n - 1):
		out.append(b + "0")
		out.append(b + "1")

	return out



def ndigit_binary_z(n: int, z: int) -> list[str]:
	if n == 1:
		if z == 0:
			return ["1"]
		elif z == 1:
			return ["0"]
		else:
			return []

	out = []
	for b in ndigit_binary_z(n - 1, z):
		out.append(b + "1")

	for b in ndigit_binary_z(n - 1, z - 1):
		out.append(b + "0")

	return out

n = int(input("> "))
z = int(input("> "))
print(ndigit_binary_z(n, z))
