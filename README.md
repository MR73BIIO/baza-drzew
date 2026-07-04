# Baza Drzew — Tree Inventory and Arborist Verification Tool

#### Video Demo: <PASTE YOUR UNLISTED YOUTUBE LINK HERE>

#### Description

Baza Drzew (Polish for "tree database") is a command-line tool for keeping a
small inventory of trees and flagging the ones that need a safety inspection.
It grew out of real arborist work: when you survey a plot, every tree has a
species, a condition, and a position, and you need to find specific trees
again, know which ones are dangerous, and measure how far apart they are.

The program runs an interactive menu. From it you can add a tree, search the
inventory by species, filter by condition, list every tree that needs an
inspection, see summary statistics, measure the great-circle distance between
two trees, and save or load the whole inventory as a CSV file.

## Files

- **`project.py`** — the program. It contains `main()`, which drives the
  interactive menu, and a set of independent helper functions that do the
  actual work. Every helper is pure where it can be (it takes data in and
  returns data out), which keeps the logic testable and the menu thin.
- **`test_project.py`** — the test suite, run with `pytest`. There is at least
  one test per core function, plus tests for the edge cases that matter:
  invalid input, empty inventory, an exact known distance, and a save/load
  round-trip.
- **`README.md`** — this file.

## Functions

- **`add_tree(species, condition, latitude, longitude)`** validates all four
  fields and returns one tree as a dictionary. It rejects a blank species, a
  condition outside the allowed set, non-numeric coordinates, and coordinates
  outside the legal ranges (latitude −90…90, longitude −180…180). Because it
  validates instead of trusting the caller, a bad entry can never enter the
  inventory in the first place.
- **`search_by_species(trees, species)`** returns every matching tree,
  case-insensitively, so "Oak" and "oak" are treated as the same species.
- **`filter_by_condition(trees, condition)`** returns every tree recorded with
  a given condition.
- **`needs_inspection(tree)`** returns `True` when a tree's condition is `poor`
  or `dead` — the cases an arborist would not leave unchecked.
- **`compute_stats(trees)`** returns a summary: the total count, a breakdown by
  condition (every condition is reported, even at zero), and how many trees
  need inspection.
- **`calculate_distance(tree_a, tree_b)`** returns the distance between two
  trees in kilometres.
- **`save_trees` / `load_trees`** write the inventory to a CSV file and read it
  back, converting coordinates to and from floats so a loaded tree behaves
  exactly like one entered by hand.

## Design decisions

**Why a dictionary per tree instead of a class.** A tree is just a record of
four fields with no behaviour of its own, so a dictionary is the simplest thing
that works and keeps the functions easy to test without constructing objects.

**Why the haversine formula for distance.** Latitude and longitude are angles on
a sphere, not points on a flat grid. Treating them as flat would understate
distances, badly at high latitudes. The haversine formula accounts for the
Earth's curvature, which is why one degree of latitude correctly comes out near
111 km regardless of where on the globe the trees are.

**Why validation lives inside `add_tree`.** Putting all the checks in one place
means the rest of the program — and the saved CSV — can assume every tree is
already well-formed. Bad input is rejected at the door instead of being handled
everywhere downstream.

**Why a fixed set of conditions.** Free-text conditions would make filtering and
statistics unreliable ("Healthy" vs "healthy" vs "good"). A small controlled
vocabulary (`healthy`, `fair`, `poor`, `dead`) keeps the data consistent and
makes the inspection rule unambiguous.

## Usage

Run the program:

```
python project.py
```

Then follow the numbered menu. Run the tests with:

```
pytest test_project.py
```
