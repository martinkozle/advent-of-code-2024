#!/usr/bin/env sh

# Useful if changing common code that may affect previous days

for i in $(seq 1 25); do
    DAY=$(printf "%02d" "$i")
    INPUT=inputs/day_${DAY}.txt
    if [ ! -f "$INPUT" ]; then
        echo "# DAY=${DAY} No input"
        continue
    fi

    for PART in $(seq 1 2); do

        INPUT=inputs/day_${DAY}.txt

        OUTPUT=$(python -m src.days.day_"${DAY}".part"${PART}" <"$INPUT" 2>/dev/null)

        OUTPUT_FILE="outputs/day_${DAY}.part${PART}.txt"

        # Compare output with previous output
        if [ -f "$OUTPUT_FILE" ]; then
            PREVIOUS_OUTPUT=$(cat "$OUTPUT_FILE")
            if [ "$OUTPUT" != "$PREVIOUS_OUTPUT" ]; then
                echo "# DAY=${DAY} PART=${PART} Output differs from previous output"
                echo "# Previous output:"
                echo "$PREVIOUS_OUTPUT"
                echo "# Current output:"
                echo "$OUTPUT"
            else
                echo "# DAY=${DAY} PART=${PART} OK"
            fi
        else
            echo "# DAY=${DAY} PART=${PART} No previous output"
        fi
    done
done
