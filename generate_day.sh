#!/usr/bin/env sh

# Generate new module for the given day
# Usage: ./generate_module.sh <day>
# Example: ./generate_module.sh 1

# check if the day is given
if [ -z "$1" ]; then
    echo "Usage: ./generate_module.sh <day>"
    exit 1
fi

# check if the day is a number
if ! [[ "$1" =~ ^[0-9]+$ ]]; then
    echo "Day must be a number"
    exit 1
fi

# check if the day is in the range
if [ "$1" -lt 1 ] || [ "$1" -gt 25 ]; then
    echo "Day must be in the range 1-25"
    exit 1
fi

# generate module only if the day is not already generated
if [ ! -d "src/days/day_$(printf "%02d" "$1")" ]; then
    # create the directory in src/days/day_n with 2 digits
    mkdir -p "src/days/day_$(printf "%02d" "$1")"

    # create the part1.py and part2.py files containing template.py
    cp template.py "src/days/day_$(printf "%02d" "$1")/part1.py"
    cp template.py "src/days/day_$(printf "%02d" "$1")/part2.py"

    # create the __init__.py file
    touch "src/days/day_$(printf "%02d" "$1")/__init__.py"
fi

if [ ! -d "inputs" ]; then
    mkdir "inputs"
fi

# use aoc cli to download just the input to inputs/day_{n:02d}.txt
aoc download --year 2024 --day "$1" --input-only --input-file "inputs/day_$(printf "%02d" "$1").txt"
