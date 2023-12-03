import argparse
from typing import Optional


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("path")
    return parser.parse_args()


def replace_char_with_indicator(row: str, replace_gears: bool = False):
    out = []
    for char in row:
        if char == ".":
            out.append("d")
        elif char.isnumeric():
            out.append("n")
        elif char == "*" and replace_gears:
            out.append("g")
        else:
            out.append("s")

    return out


def get_full_number_of_digit(position, row, raw_row):
    # Expanding to left and right to find the full number
    left_position, right_position = position, position
    while left_position > 0 and row[left_position - 1] == "n":
        left_position -= 1
    while right_position < len(row) - 1 and row[right_position + 1] == "n":
        right_position += 1
    return (
        left_position,
        right_position,
        int(f"{raw_row[left_position:right_position+1]}"),
    )


def invalid_distance(pos_1, pos_2):
    return abs(pos_1 - pos_2) > 1


def process_row_part_1(
    row: Optional[list],
    adjacent_symbol: str,
    position_of_nums_in_row: list,
    positions_of_adjacent_symbols: list,
):
    position_of_symbols = [i for i, x in enumerate(row) if x == adjacent_symbol]
    for num_position in position_of_nums_in_row:
        for symbol_position in position_of_symbols:
            if invalid_distance(num_position, symbol_position):
                continue
            positions_of_adjacent_symbols.append(num_position)
            break


def check_for_adjacent_symbol(
    row_with_indicators: list,
    row_above_with_indicators: Optional[list],
    row_below_with_indicators: Optional[list],
    original_row: str = None,
):
    position_of_nums_in_row = [i for i, x in enumerate(row_with_indicators) if x == "n"]

    positions_of_adjacent_symbols = []

    process_row_part_1(
        row_with_indicators,
        "s",
        position_of_nums_in_row,
        positions_of_adjacent_symbols,
    )

    if row_above_with_indicators is not None:
        process_row_part_1(
            row_above_with_indicators,
            "s",
            position_of_nums_in_row,
            positions_of_adjacent_symbols,
        )

    if row_below_with_indicators is not None:
        process_row_part_1(
            row_below_with_indicators,
            "s",
            position_of_nums_in_row,
            positions_of_adjacent_symbols,
        )

    out = {}
    for position in positions_of_adjacent_symbols:
        left_position, right_position, full_number = get_full_number_of_digit(
            position, row_with_indicators, original_row
        )
        out[f"{left_position}-{right_position}"] = full_number

    return sum(out.values())


def process_row_part_2(
    row: list,
    original_row: str,
    position_of_potential_gear: int,
    adjacent_nums: dict,
    row_label,
):
    for num_position in [i for i, x in enumerate(row) if x == "n"]:
        if invalid_distance(num_position, position_of_potential_gear):
            continue
        left_position, right_position, full_number = get_full_number_of_digit(
            num_position, row, original_row
        )
        adjacent_nums[f"{left_position}-{right_position}-{row_label}"] = full_number


# Part 2
def check_for_adjacent_numbers(
    row: list,
    row_above: Optional[list],
    row_below: Optional[list],
    original_row: Optional[str] = None,
    original_row_above: Optional[str] = None,
    original_row_below: Optional[str] = None,
):
    # A gear is a * that is adjacent to exactly 2 numbers.
    position_of_potential_gears_in_row = [i for i, x in enumerate(row) if x == "g"]

    row_result = 0
    for position_of_potential_gear in position_of_potential_gears_in_row:
        adjacent_nums = {}
        process_row_part_2(
            row,
            original_row,
            position_of_potential_gear,
            adjacent_nums,
            "same_row",
        )

        if row_above is not None:
            process_row_part_2(
                row_above,
                original_row_above,
                position_of_potential_gear,
                adjacent_nums,
                "above_row",
            )
        if row_below is not None:
            process_row_part_2(
                row_below,
                original_row_below,
                position_of_potential_gear,
                adjacent_nums,
                "below_row",
            )

        if len(adjacent_nums) == 2:
            factor_1 = adjacent_nums[list(adjacent_nums.keys())[0]]
            factor_2 = adjacent_nums[list(adjacent_nums.keys())[1]]
            gear_result = (
                adjacent_nums[list(adjacent_nums.keys())[0]]
                * adjacent_nums[list(adjacent_nums.keys())[1]]
            )
            row_result += gear_result
        elif len(adjacent_nums) > 2:
            pass
        else:
            pass

    return row_result


def read_file(path: str):
    with open(path, "r") as f:
        rows = f.readlines()
    return [line.strip() for line in rows]


def get_adjacent_rows(row_number, rows):
    previous_row = rows[row_number - 1] if row_number > 0 else None
    next_row = rows[row_number + 1] if row_number < len(rows) - 1 else None
    return previous_row, next_row


if __name__ == "__main__":
    args = parse_arguments()

    raw_rows = read_file(args.path)
    indicator_rows_part_1 = [replace_char_with_indicator(row) for row in raw_rows]
    result = 0
    for i, indicator_row in enumerate(indicator_rows_part_1):
        previous_row, next_row = get_adjacent_rows(i, indicator_rows_part_1)
        row_result = check_for_adjacent_symbol(
            indicator_row,
            previous_row,
            next_row,
            raw_rows[i],
        )

        result += row_result

    print(f"Part 1 - Sum of all part_numbers: {result}")

    indicator_rows_part_2 = [replace_char_with_indicator(row, True) for row in raw_rows]
    result = 0
    for i, indicator_row in enumerate(indicator_rows_part_2):
        previous_row, next_row = get_adjacent_rows(i, indicator_rows_part_2)
        previous_raw_row, next_raw_row = get_adjacent_rows(i, raw_rows)

        row_result = check_for_adjacent_numbers(
            indicator_row,
            previous_row,
            next_row,
            raw_rows[i],
            previous_raw_row,
            next_raw_row,
        )

        result += row_result

    print(f"Part 2 - Sum of all gears: {result}")
