#!/usr/bin/env sh

DAY=$(printf "%02d" $1)
PART=$2

# Check if input should be stdin
if [[ -n "$3" && "$3" == "in" ]]; then
    INPUT=/dev/stdin
else
    INPUT=inputs/day_${DAY}.txt
fi

OUTPUT=$(python -m src.days.day_${DAY}.part${PART} < $INPUT)

echo "# OUTPUT:"
echo $OUTPUT

if [ ! -d "outputs" ]; then
    mkdir "outputs"
fi

OUTPUT_FILE="outputs/day_${DAY}.part${PART}.txt"

# Compare output with previous output
if [ "$INPUT" != "/dev/stdin" ] && [ -f "$OUTPUT_FILE" ]; then
    PREVIOUS_OUTPUT=$(cat $OUTPUT_FILE)
    if [ "$OUTPUT" != "$PREVIOUS_OUTPUT" ]; then
        echo "# Output differs from previous output:"
        echo $PREVIOUS_OUTPUT
    fi
fi


echo $OUTPUT > $OUTPUT_FILE
