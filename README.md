# 🌳 Baza Drzew — Tree Inventory and Arborist Verification Tool

**Video Demo:** [https://youtu.be/wu61kIDfXBk](https://youtu.be/wu61kIDfXBk)

![Python Version](https://img.shields.io/badge/python-3.6+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Status](https://img.shields.io/badge/status-active-brightgreen.svg)

## 📖 Description

Baza Drzew (Polish for "tree database") is a command-line tool for keeping a small inventory of trees and flagging the ones that need a safety inspection. It grew out of real arborist work: when you survey a plot, every tree has a species, a condition, and a position, and you need to find specific trees again, know which ones are dangerous, and measure how far apart they are.

The program runs an interactive menu. From it you can add a tree, search the inventory by species, filter by condition, list every tree that needs an inspection, see summary statistics, measure the great-circle distance between two trees, and save or load the whole inventory as a CSV file.

## ✨ Features

- ✅ Add trees with species, condition, and GPS coordinates
- 🔍 Search inventory by species (case-insensitive)
- 📊 Filter trees by condition (good, poor, dead, excellent)
- ⚠️ Flag trees that need inspection (poor/dead condition)
- 📈 View summary statistics of your inventory
- 📏 Calculate great-circle distance between any two trees
- 💾 Save and load inventory as CSV files

## 📁 Files

- **`project.py`** — the program. It contains `main()`, which drives the interactive menu, and a set of independent helper functions that do the actual work. Every helper is pure where it can be (it takes data in and returns data out), which keeps the logic testable and the menu thin.
- **`test_project.py`** — the test suite, run with `pytest`. There is at least one test per core function, plus tests for the edge cases that matter: invalid input, empty inventory, an exact known distance, and a save/load round-trip.
- **`README.md`** — this file.

## 🛠️ Installation

```bash
# Clone the repository
git clone https://github.com/MR73BIIO/baza-drzew.git
cd baza-drzew

# (Optional) Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Linux/Mac
# or venv\Scripts\activate  # On Windows

# Install dependencies (if any)
pip install -r requirements.txt
