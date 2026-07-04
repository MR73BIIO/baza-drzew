"""
Baza Drzew — a tree inventory and arborist verification tool.

CS50P final project by Marcin Ruszczak (GitHub/edX: MR73BIIO).

The program manages a small database of trees. For each tree it stores the
species, its condition, and its GPS coordinates. From there it can search,
filter, flag trees that need a safety inspection, compute statistics, measure
the distance between two trees on the surface of the Earth, and save or load
the inventory as a CSV file.
"""

import csv
import sys
from math import radians, sin, cos, sqrt, atan2

# Conditions an arborist would record in the field, from best to worst.
VALID_CONDITIONS = ("healthy", "fair", "poor", "dead")

# A tree counts as needing inspection if its condition is one of these.
INSPECTION_CONDITIONS = ("poor", "dead")

# Mean radius of the Earth in kilometres, used by the haversine formula.
EARTH_RADIUS_KM = 6371.0


def main():
    """Run an interactive menu over an in-memory tree inventory."""
    trees: list[dict] = []
    print("Baza Drzew — tree inventory and arborist verification tool")

    while True:
        print(
            "\n[1] Add tree   [2] Search by species   [3] Filter by condition"
            "\n[4] Trees needing inspection   [5] Statistics"
            "\n[6] Distance between two trees   [7] Save   [8] Load   [9] Quit"
        )
        choice = input("> ").strip()

        if choice == "1":
            try:
                tree = add_tree(
                    input("Species: "),
                    input(f"Condition {VALID_CONDITIONS}: "),
                    input("Latitude: "),
                    input("Longitude: "),
                )
            except ValueError as error:
                print(f"Could not add tree: {error}")
            else:
                trees.append(tree)
                print(f"Added: {format_tree(tree)}")

        elif choice == "2":
            matches = search_by_species(trees, input("Species to find: "))
            print_trees(matches)

        elif choice == "3":
            matches = filter_by_condition(trees, input("Condition to filter: "))
            print_trees(matches)

        elif choice == "4":
            flagged = [t for t in trees if needs_inspection(t)]
            print_trees(flagged)

        elif choice == "5":
            stats = compute_stats(trees)
            print(f"Total trees: {stats['total']}")
            print(f"Needing inspection: {stats['needs_inspection']}")
            for condition, count in stats["by_condition"].items():
                print(f"  {condition}: {count}")

        elif choice == "6":
            if len(trees) < 2:
                print("Need at least two trees to measure a distance.")
                continue
            print_trees(trees)
            try:
                first = trees[int(input("Index of first tree: "))]
                second = trees[int(input("Index of second tree: "))]
            except (ValueError, IndexError):
                print("Invalid tree index.")
            else:
                km = calculate_distance(first, second)
                print(f"Distance: {km} km")

        elif choice == "7":
            save_trees(trees, input("Filename to save (e.g. trees.csv): ").strip())
            print("Saved.")

        elif choice == "8":
            try:
                trees = load_trees(input("Filename to load: ").strip())
            except FileNotFoundError:
                print("No such file.")
            else:
                print(f"Loaded {len(trees)} tree(s).")

        elif choice == "9":
            print("Goodbye.")
            sys.exit(0)

        else:
            print("Please choose a number from 1 to 9.")


def add_tree(species: str, condition: str, latitude, longitude) -> dict:
    """
    Validate the supplied fields and return a single tree as a dictionary.

    Raises ValueError if the species is blank, the condition is not one of
    VALID_CONDITIONS, or the coordinates fall outside the legal ranges for
    latitude (-90..90) and longitude (-180..180).
    """
    species = species.strip()
    if not species:
        raise ValueError("species must not be empty")

    condition = condition.strip().lower()
    if condition not in VALID_CONDITIONS:
        raise ValueError(f"condition must be one of {VALID_CONDITIONS}")

    try:
        latitude = float(latitude)
        longitude = float(longitude)
    except (TypeError, ValueError):
        raise ValueError("coordinates must be numbers")

    if not -90.0 <= latitude <= 90.0:
        raise ValueError("latitude must be between -90 and 90")
    if not -180.0 <= longitude <= 180.0:
        raise ValueError("longitude must be between -180 and 180")

    return {
        "species": species,
        "condition": condition,
        "latitude": latitude,
        "longitude": longitude,
    }


def search_by_species(trees: list[dict], species: str) -> list[dict]:
    """Return every tree whose species matches, case-insensitively."""
    target = species.strip().lower()
    return [tree for tree in trees if tree["species"].lower() == target]


def filter_by_condition(trees: list[dict], condition: str) -> list[dict]:
    """Return every tree recorded with the given condition."""
    target = condition.strip().lower()
    return [tree for tree in trees if tree["condition"] == target]


def needs_inspection(tree: dict) -> bool:
    """Return True if a tree's condition flags it for a safety inspection."""
    return tree["condition"] in INSPECTION_CONDITIONS


def compute_stats(trees: list[dict]) -> dict:
    """
    Summarise the inventory.

    Returns a dictionary with the total number of trees, a count broken down
    by condition (every valid condition is present, even when zero), and the
    number of trees flagged as needing inspection.
    """
    by_condition = {condition: 0 for condition in VALID_CONDITIONS}
    for tree in trees:
        by_condition[tree["condition"]] += 1

    return {
        "total": len(trees),
        "by_condition": by_condition,
        "needs_inspection": sum(1 for tree in trees if needs_inspection(tree)),
    }


def calculate_distance(tree_a: dict, tree_b: dict) -> float:
    """
    Return the great-circle distance in kilometres between two trees.

    Uses the haversine formula so the curvature of the Earth is accounted for,
    rather than treating latitude/longitude as a flat plane. The result is
    rounded to three decimal places (metre-level precision).
    """
    lat1, lon1 = radians(tree_a["latitude"]), radians(tree_a["longitude"])
    lat2, lon2 = radians(tree_b["latitude"]), radians(tree_b["longitude"])

    delta_lat = lat2 - lat1
    delta_lon = lon2 - lon1

    a = sin(delta_lat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(delta_lon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    return round(EARTH_RADIUS_KM * c, 3)


def save_trees(trees: list[dict], path: str) -> None:
    """Write the inventory to a CSV file with a header row."""
    fieldnames = ["species", "condition", "latitude", "longitude"]
    with open(path, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(trees)


def load_trees(path: str) -> list[dict]:
    """
    Read an inventory back from a CSV file.

    Coordinates are converted back to floats so loaded trees behave exactly
    like ones added during the session. Raises FileNotFoundError if the file
    does not exist.
    """
    trees = []
    with open(path, newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            trees.append(
                {
                    "species": row["species"],
                    "condition": row["condition"],
                    "latitude": float(row["latitude"]),
                    "longitude": float(row["longitude"]),
                }
            )
    return trees


def format_tree(tree: dict) -> str:
    """Return a single tree as a one-line human-readable string."""
    return (
        f"{tree['species']} ({tree['condition']}) "
        f"at {tree['latitude']}, {tree['longitude']}"
    )


def print_trees(trees: list[dict]) -> None:
    """Print a numbered list of trees, or a notice if the list is empty."""
    if not trees:
        print("No trees found.")
        return
    for index, tree in enumerate(trees):
        print(f"[{index}] {format_tree(tree)}")


if __name__ == "__main__":
    main()
