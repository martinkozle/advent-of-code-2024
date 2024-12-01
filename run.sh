#!/usr/bin/env sh

DAY=$(printf "%02d" $1)
PART=$2

if [[ -n "$3" && "$3" == "in" ]]; then
    python -m src.days.day_${DAY}.part${PART} <&0
else
    python -m src.days.day_${DAY}.part${PART} < inputs/day_${DAY}.txt
fi
