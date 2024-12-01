#!/usr/bin/env sh

OUTPUT=$(./run.sh $@)

aoc submit --year 2024 --day $1 $2 $OUTPUT
