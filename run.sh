#!/usr/bin/env sh

DAY=$(printf "%02d" $1)
PART=$2

if [[ -n "$3" && "$3" == "in" ]]; then
    python -m src.days.day_${DAY}.part$2 <&0
else
    python -m src.days.day_${DAY}.part$2 < inputs/day_${DAY}.txt
fi
