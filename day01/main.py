import sys
import argparse


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("path")
    parser.add_argument("--debug", action="store_true")
    return parser.parse_args()


def extract_digits(row: str, replace=False, debug=False) -> int:
    if replace:
        digits_to_pattern = {
            "one": "one1one",
            "two": "two2two",
            "three": "three3three",
            "four": "four4four",
            "five": "five5five",
            "six": "six6six",
            "seven": "seven7seven",
            "eight": "eight8eight",
            "nine": "nine9nine",
        }

        for digit, pattern in digits_to_pattern.items():
            row = row.replace(digit, pattern)

    digits_only_as_str = "".join([digit for digit in row if digit.isdigit()])

    out = int(f"{digits_only_as_str[0]}{digits_only_as_str[-1]}")

    if debug:
        print(f"{row} -> {out}")

    return out


def read_file(path: str):
    with open(path, "r") as f:
        rows = f.readlines()
    return rows


if __name__ == "__main__":
    args = parse_arguments()

    rows = read_file(args.path)
    digits_problem_1 = [
        extract_digits(row, replace=False, debug=args.debug) for row in rows
    ]
    digits_problem_2 = [
        extract_digits(row, replace=True, debug=args.debug) for row in rows
    ]

    print(f"Solution problem 1: {sum(digits_problem_1)}")
    print(f"Solution problem 2: {sum(digits_problem_2)}")
