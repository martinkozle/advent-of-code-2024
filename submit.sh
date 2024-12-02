#!/usr/bin/env sh

# shellcheck source=/dev/null
. ./.env

OUTPUT=$(./run.sh "$@")

echo "$OUTPUT"

aoc submit --year "$YEAR" --day "$1" "$2" "$OUTPUT"
