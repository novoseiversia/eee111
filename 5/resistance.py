# SPDX-FileCopyrightText: Copyright (C) Nile Jocson <novoseiversia@gmail.com>
# SPDX-License-Identifier: 0BSD



from typing import List



valid_colors = ["black", "brown", "red", "orange", "yellow", "green", "blue", "violet", "grey", "white", "gold", "silver"]

def color(s: str) -> str:
	lower_s = s.lower()
	if lower_s in valid_colors:
		return lower_s
	else:
		raise ValueError(f"Invalid color: { lower_s }")



def input_list_colors(prompt: str) -> List[str]:
	while True:
		try:
			parsed = [color(s) for s in input(prompt).split()]
		except ValueError:
			print("Please enter a valid list of colors.")
		else:
			return parsed



def get_band_digit(color: str) -> int | None:
	digits = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, None, None]
	band_digits = dict(zip(valid_colors, digits, strict = True))
	return band_digits[color]

def get_band_multiplier(color: str) -> float | None:
	exponents = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, -1, -2]
	band_exponents = dict(zip(valid_colors, exponents, strict = True))
	return 10**band_exponents[color]

def get_band_tolerance(color: str) -> float | None:
	tolerances = [None, 1, 2, 3, 4, 0.5, 0.25, 0.10, 0.05, None, 5, 10]
	band_tolerances = dict(zip(valid_colors, tolerances, strict = True))
	return band_tolerances[color]

def get_resistance_from_colors(colors: List[str]) -> str:
	first_digit  = get_band_digit(colors[0])
	second_digit = get_band_digit(colors[1])
	multiplier   = get_band_multiplier(colors[2])
	tolerance    = get_band_tolerance(colors[3])

	if first_digit == None:
		return f"Invalid first digit color \"{ colors[0] }\""
	if second_digit == None:
		return f"Invalid second digit color \"{ colors[1] }\""
	if multiplier == None:
		return f"Invalid multiplier color \"{ colors[2] }\""
	if tolerance == None:
		return f"Invalid tolerance color \"{ colors[3] }\""

	resistance = (10 * first_digit + second_digit) * multiplier

	return f"{ resistance } +/- { tolerance }%"



def __main__():
	colors = input_list_colors("Enter your 4-band resistor colors: ")

	if len(colors) != 4:
		print("Please enter a color combination for a 4-band resistor.")
		return

	resistance = get_resistance_from_colors(colors)

	print(resistance)



__main__()
