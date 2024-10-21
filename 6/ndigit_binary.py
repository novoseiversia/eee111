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



print(ndigit_binary(int(input())))
