# SPDX-FileCopyrightText: Copyright (C) Nile Jocson <novoseiversia@gmail.com>
# SPDX-License-Identifier: 0BSD



def absv(x: int) -> int:
	if x > 0:
		return x
	else:
		return -x



# Using euclidean algorithm
def gcf(a: int, b: int) -> int:
	if b > a:
		a, b = b, a
	while b != 0:
		a, b = b, a % b
	return a



# Derived from gcd
def lcm(a: int, b: int) -> int:
	# Guaranteed to return an integer
	return int(absv(a * b) / gcf(a, b))



def print_squares(a: int, b: int) -> None:
	lower = gcf(a, b)
	upper = lcm(a, b)
	i = 0
	square = 0
	while square < upper:
		square = i * i
		if lower < square < upper:
			print(square)
		i += 1



# MAIN CODE
### Avoid changing anything below this line.

X = int(input("Enter 1st key: "))
Y = int(input("Enter 2nd key: "))

print("Your Security Code is:")
print(gcf(X, Y))
print_squares(X, Y)
print(lcm(X, Y))



# REFERENCES
# https://en.wikipedia.org/wiki/Greatest_common_divisor
