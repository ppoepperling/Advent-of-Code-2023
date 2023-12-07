import argparse
import math


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("path")
    return parser.parse_args()


def read_file(path: str):
    with open(path, "r") as f:
        rows = f.readlines()
    return [line.strip() for line in rows]


def parse_input(data: list):
    times = []
    distances = []
    # Times are on line 1, distances are on line 2
    for i in data[0].split(" "):
        if i.isnumeric():
            times.append(int(i))
    for i in data[1].split(" "):
        if i.isnumeric():
            distances.append(int(i))

    time_distances_pairs = list(zip(times, distances))
    return time_distances_pairs


def parse_input_part_2(data: list):
    time = ""
    distance = ""
    for i in data[0].split(" "):
        if i.isnumeric():
            time += i
    for i in data[1].split(" "):
        if i.isnumeric():
            distance += i
    return int(time), int(distance)


def shift_integer_solutions(sol1, sol2):
    if sol1.is_integer():
        sol1 += -1 if sol1 > sol2 else 1
    if sol2.is_integer():
        sol2 += -1 if sol2 > sol1 else 1
    return sol1, sol2


def get_winning_times(record_distance, race_time):
    a = -1
    b = race_time
    c = -record_distance

    d = b**2 - 4 * a * c

    sol1 = (-b - math.sqrt(d)) / (2 * a)
    sol2 = (-b + math.sqrt(d)) / (2 * a)

    # If any of the solutions are an integer, we need to add/subtract 1
    # to beat the record instead of just equaling it.
    sol1, sol2 = shift_integer_solutions(sol1, sol2)

    return sol1, sol2


if __name__ == "__main__":
    args = parse_arguments()
    data = read_file(args.path)
    time_distances_pairs = parse_input(data)
    all_solutions = []
    for race_time, record_distance in time_distances_pairs:
        winning_time_range = get_winning_times(record_distance, race_time)
        integers_in_range = int(winning_time_range[0]) - int(winning_time_range[1])
        all_solutions.append(integers_in_range)

    # Calculate the product of all solutions
    print(f"Part 1 - Product of all solutions: {math.prod(all_solutions)}")

    # Part 2
    time, distance = parse_input_part_2(data)
    winning_time_range = get_winning_times(distance, time)
    num_soutions = int(winning_time_range[0]) - int(winning_time_range[1])
    print(f"Part 2 - Number of solutions: {num_soutions}")
