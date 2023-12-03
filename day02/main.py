import sys
import argparse


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("path")
    parser.add_argument("--debug", action="store_true")
    return parser.parse_args()


def read_file(path: str):
    with open(path, "r") as f:
        rows = f.readlines()
    return rows


def get_number_of_marbles_per_round(round: str):
    colors = ["blue", "red", "green"]
    marbles = {color: 0 for color in colors}

    for color in colors:
        if color in round:
            try:
                marbles[color] = int(round.split(color)[0].split()[-1])
            except ValueError:
                pass

    return marbles


def get_game_number_and_rounds(row: str):
    game_number = row.split(":")[0].split(" ")[-1]
    rounds = row.split(";")
    return game_number, rounds


def check_game_validity(row: str, debug=False):
    game_number, rounds = get_game_number_and_rounds(row)
    for round in rounds:
        num_marbles_per_round = get_number_of_marbles_per_round(round)
        if not num_marbles_per_round:
            return 0
        # A game is valid if it has now more than 12 red cubes, 13 green cubes, and 14 blue cubes
        max_marbles = {"blue": 14, "red": 12, "green": 13}
        for color in max_marbles.keys():
            if num_marbles_per_round[color] > max_marbles[color]:
                return 0

    return int(game_number)


def get_min_needed_marbels(row: str):
    _, rounds = get_game_number_and_rounds(row)
    min_blue = 0
    min_red = 0
    min_green = 0
    for round in rounds:
        num_marbles_per_round = get_number_of_marbles_per_round(round)
        if not num_marbles_per_round:
            return 0
        blue_marbels = num_marbles_per_round["blue"]
        red_marbels = num_marbles_per_round["red"]
        green_marbels = num_marbles_per_round["green"]
        if blue_marbels > min_blue:
            min_blue = blue_marbels
        if red_marbels > min_red:
            min_red = red_marbels
        if green_marbels > min_green:
            min_green = green_marbels

    return min_blue * min_red * min_green


if __name__ == "__main__":
    args = parse_arguments()

    rows = read_file(args.path)

    valid_games = []
    for row in rows:
        valid_games.append(check_game_validity(row, debug=args.debug))

    print(f"Sum of valid games: {sum(valid_games)}")
    print(
        f"Min number of marbels needed: {sum(get_min_needed_marbels(row) for row in rows)}"
    )
