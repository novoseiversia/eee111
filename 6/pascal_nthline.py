# SPDX-FileCopyrightText: Copyright (C) Nile Jocson <novoseiversia@gmail.com>
# SPDX-License-Identifier: 0BSD



def pascal_nthline(n: int) -> list[int]:
	if n == 1:
		return [1]

	last = pascal_nthline(n - 1)
	out: list[int] = []

	out.append(1)
	for x, y in zip(last[:-1], last[1:]):
		out.append(x + y)
	out.append(1)

	return out



print(pascal_nthline(int(input())))
