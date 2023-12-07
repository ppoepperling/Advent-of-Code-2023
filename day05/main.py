import argparse
from tqdm import tqdm


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("path")
    return parser.parse_args()


def read_file(path: str):
    with open(path, "r") as f:
        rows = f.readlines()
    return [line.strip() for line in rows]


def parse_input(data: list, part=1):
    if part == 1:
        seeds = [int(num) for num in data[0].split(" ") if num.isnumeric()]
    else:
        seeds = []
        seed_info = [int(num) for num in data[0].split(" ") if num.isnumeric()]
        for i in range(0, len(seed_info), 2):
            seeds.extend(range(seed_info[i], seed_info[i] + seed_info[i + 1]))

    mappings = {}
    current_seed_name = ""
    for i in range(1, len(data)):
        if len(data[i]) > 0 and not data[i][0].isnumeric():
            current_seed_name = data[i].split(" ")[0]
            mappings[current_seed_name] = []
        elif len(data[i]) > 0 and data[i][0].isnumeric():
            destination_range_start, source_range_start, range_length = [
                int(num) for num in data[i].split(" ") if num.isnumeric()
            ]

            mappings[current_seed_name].append(
                {
                    "destination_range_start": destination_range_start,
                    "source_range_start": source_range_start,
                    "range_length": range_length,
                }
            )
    return seeds, mappings


def parse_mappings(mappings, num):
    total_mapping = []
    for maps in mappings:
        total_mapping.append(
            {
                "destination_range_start": maps["destination_range_start"],
                "destination_range_end": maps["destination_range_start"]
                + maps["range_length"],
                "source_range_start": maps["source_range_start"],
                "source_range_end": maps["source_range_start"] + maps["range_length"],
            }
        )
    # Check if the number is in the range of any of the mappings
    for mapping in total_mapping:
        if mapping["source_range_start"] <= num < mapping["source_range_end"]:
            return mapping["destination_range_start"] + (
                num - mapping["source_range_start"]
            )
    return num


def process(mappings, seed):
    mapping_sequence = [
        "seed-to-soil",
        "soil-to-fertilizer",
        "fertilizer-to-water",
        "water-to-light",
        "light-to-temperature",
        "temperature-to-humidity",
        "humidity-to-location",
    ]

    for mapping_name in mapping_sequence:
        seed = parse_mappings(mappings[mapping_name], seed)

    return seed


if __name__ == "__main__":
    args = parse_arguments()
    data = read_file(args.path)
    seeds, mappings = parse_input(data)
    min_location = float("inf")
    for seed in seeds:
        location = process(mappings, seed)
        if location < min_location:
            min_location = location

    print(f"Part 1: Lowest location: {min_location}")

    seeds, mappings = parse_input(data, part=2)
    min_location = float("inf")
    seeds, mappings = parse_input(data, part=2)
    min_location = float("inf")
    for seed in seeds:
        location = process(mappings, seed)
        if location < min_location:
            min_location = location

    print(f"Part 2: Lowest location: {min_location}")
