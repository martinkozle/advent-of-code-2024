#!/usr/bin/env sh

DAY=$(printf "%02d" "$1")
PART=$2

# Check if input should be stdin
if [ -n "$3" ] && [ "$3" = "in" ]; then
    INPUT=/dev/stdin
else
    INPUT=inputs/day_${DAY}.txt
fi

OUTPUT=$(python -m src.days.day_"${DAY}".part"${PART}" <"$INPUT")
RETURN_CODE=$?

echo "# OUTPUT:" >/dev/stderr
echo "$OUTPUT"

if [ ! -d "outputs" ]; then
    mkdir "outputs"
fi

OUTPUT_FILE="outputs/day_${DAY}.part${PART}.txt"

if [ $RETURN_CODE -eq 0 ] && [ -n "$OUTPUT" ]; then
    # Compare output with previous output
    if [ "$INPUT" != "/dev/stdin" ] && [ -f "$OUTPUT_FILE" ]; then
        PREVIOUS_OUTPUT=$(cat "$OUTPUT_FILE")
        if [ "$OUTPUT" != "$PREVIOUS_OUTPUT" ]; then
            echo "# Output differs from previous output:" >/dev/stderr
            echo "$PREVIOUS_OUTPUT" >/dev/stderr
        fi
    fi

    echo "$OUTPUT" >"$OUTPUT_FILE"
fi
