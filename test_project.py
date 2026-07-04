"""Tests for the Baza Drzew CS50P final project.

Each test function is named exactly after the function it tests, prepended
with test_, as required by the CS50P final project specification. Edge cases
are folded into each test as additional assertions.

Run with:  pytest
"""

import pytest

from project import (
    add_tree,
    search_by_species,
    filter_by_condition,
    needs_inspection,
    compute_stats,
    calculate_distance,
    save_trees,
    load_trees,
)


def sample_trees():
    """A small reusable inventory for the read-only tests."""
    return [
        add_tree("Oak", "healthy", 52.0, 18.0),
        add_tree("Birch", "poor", 52.1, 18.1),
        add_tree("oak", "dead", 52.2, 18.2),
    ]


def test_add_tree():
    # A valid call returns a normalised dictionary.
    tree = add_tree("Maple", "Fair", "52.5", "18.5")
    assert tree == {
        "species": "Maple",
        "condition": "fair",
        "latitude": 52.5,
        "longitude": 18.5,
    }
    # Whitespace is stripped and the condition is lower-cased.
    pine = add_tree("  Pine  ", "  HEALTHY  ", 0, 0)
    assert pine["species"] == "Pine"
    assert pine["condition"] == "healthy"
    # Invalid input is rejected.
    with pytest.raises(ValueError):
        add_tree("   ", "healthy", 0, 0)          # empty species
    with pytest.raises(ValueError):
        add_tree("Oak", "burned", 0, 0)           # bad condition
    with pytest.raises(ValueError):
        add_tree("Oak", "healthy", "north", "east")  # non-numeric coords
    with pytest.raises(ValueError):
        add_tree("Oak", "healthy", 200, 0)        # latitude out of range
    with pytest.raises(ValueError):
        add_tree("Oak", "healthy", 0, 200)        # longitude out of range


def test_search_by_species():
    trees = sample_trees()
    # Matching is case-insensitive, so "OAK" finds both "Oak" and "oak".
    assert len(search_by_species(trees, "OAK")) == 2
    # A species that is not present yields an empty list.
    assert search_by_species(trees, "Willow") == []


def test_filter_by_condition():
    trees = sample_trees()
    assert len(filter_by_condition(trees, "poor")) == 1
    assert filter_by_condition(trees, "healthy")[0]["species"] == "Oak"
    assert filter_by_condition(trees, "fair") == []


def test_needs_inspection():
    assert needs_inspection(add_tree("Oak", "poor", 0, 0)) is True
    assert needs_inspection(add_tree("Oak", "dead", 0, 0)) is True
    assert needs_inspection(add_tree("Oak", "healthy", 0, 0)) is False
    assert needs_inspection(add_tree("Oak", "fair", 0, 0)) is False


def test_compute_stats():
    stats = compute_stats(sample_trees())
    assert stats["total"] == 3
    assert stats["needs_inspection"] == 2
    assert stats["by_condition"]["healthy"] == 1
    assert stats["by_condition"]["poor"] == 1
    assert stats["by_condition"]["dead"] == 1
    assert stats["by_condition"]["fair"] == 0
    # An empty inventory reports zeros, not errors.
    empty = compute_stats([])
    assert empty["total"] == 0
    assert empty["needs_inspection"] == 0
    assert all(count == 0 for count in empty["by_condition"].values())


def test_calculate_distance():
    # The distance from a point to itself is zero.
    here = add_tree("Oak", "healthy", 52.0, 18.0)
    assert calculate_distance(here, here) == 0.0
    # One degree of latitude is roughly 111 km anywhere on Earth.
    north = add_tree("Birch", "healthy", 53.0, 18.0)
    assert calculate_distance(here, north) == pytest.approx(111.0, abs=1.0)


def test_save_trees(tmp_path):
    trees = sample_trees()
    path = tmp_path / "trees.csv"
    save_trees(trees, str(path))
    # The file exists and starts with the expected header row.
    contents = path.read_text(encoding="utf-8")
    assert contents.startswith("species,condition,latitude,longitude")


def test_load_trees(tmp_path):
    trees = sample_trees()
    path = tmp_path / "trees.csv"
    save_trees(trees, str(path))
    # Saving then loading returns an identical inventory.
    assert load_trees(str(path)) == trees
    # Loading a file that does not exist raises FileNotFoundError.
    with pytest.raises(FileNotFoundError):
        load_trees(str(tmp_path / "missing.csv"))
