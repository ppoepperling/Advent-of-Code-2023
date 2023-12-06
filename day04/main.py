import argparse
import time


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("path")
    return parser.parse_args()


def parse_game_row(row: str):
    _, games = row.split(":")
    winning_numbers, player_numbers = games.split(" | ")
    winning_numbers = [
        int(num) for num in winning_numbers.split(" ") if num.isnumeric()
    ]
    player_numbers = [int(num) for num in player_numbers.split(" ") if num.isnumeric()]
    return winning_numbers, player_numbers


def find_matched_winning_numbers(winning_numbers: list, player_numbers: list):
    return [num for num in player_numbers if num in winning_numbers]


def calculate_score(winning_numbers: list, player_numbers: list):
    matched_winning_numbers = find_matched_winning_numbers(
        winning_numbers, player_numbers
    )
    if len(matched_winning_numbers) == 0:
        return 0
    return 2 ** (len(matched_winning_numbers) - 1)


def read_file(path: str):
    with open(path, "r") as f:
        rows = f.readlines()
    return [line.strip() for line in rows]


if __name__ == "__main__":
    start = time.perf_counter()
    args = parse_arguments()
    data = read_file(args.path)
    games = [parse_game_row(row) for row in data]
    number_of_games = len(games)
    total_score = 0
    number_of_cards = {i: 1 for i in range(len(games))}
    num_matching_winning_numbers = {}
    for i, (winning_numbers, player_numbers) in enumerate(games):
        for _ in range(number_of_cards[i]):
            if i not in num_matching_winning_numbers:
                num_matching_winning_numbers[i] = len(
                    find_matched_winning_numbers(winning_numbers, player_numbers)
                )
            for k in range(num_matching_winning_numbers[i]):
                number_of_cards[i + 1 + k] += 1

        game_score = calculate_score(winning_numbers, player_numbers)
        total_score += game_score
    print(f"Part 1: Total score: {total_score}")
    print(f"Part 2: Total number of cards: {sum(number_of_cards.values())}")
    end = time.perf_counter()
    print(f"Runtime of the program is {end - start}")
