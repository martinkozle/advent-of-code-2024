#!/usr/bin/env sh

source ./.env

OUTPUT=$(./run.sh $@)

echo $OUTPUT

aoc submit --year $YEAR --day $1 $2 $OUTPUT
