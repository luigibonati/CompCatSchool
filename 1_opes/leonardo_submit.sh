#!/bin/bash
set -euo pipefail

SBATCH_FILE="leonardo.sbatch"

for TEMP in 700; do
    for BIAS in OPES_METAD OPES_METAD_EXPLORE; do

        if [[ "$BIAS" == "OPES_METAD_EXPLORE" ]]; then
            BARRIER=0.6
            LABEL="explore"
        else
            BARRIER=1.0
            LABEL="metad"
        fi

        JOB_NAME="${TEMP}K-${LABEL}"

        sbatch \
            -J "$JOB_NAME" \
            --export=NONE,TEMP="$TEMP",BIAS="$BIAS",BARRIER="$BARRIER" \
            "$SBATCH_FILE"

    done
done