#!/usr/bin/env bash
# ------------------------------------------------------------
# Run the Python pipeline for every DOI listed in a text file.
#
# Expected layout of the DOI file (one DOI per line):
#   10.1234/abcde1
#   10.5678/fghij2
# ------------------------------------------------------------

# Path to the file that holds the DOIs
DOI_FILE="data/dois_for_asi_test1.txt"

# Make sure the file exists before we start
if [[ ! -f "$DOI_FILE" ]]; then
    echo "Error: DOI list file not found at '$DOI_FILE'" >&2
    exit 1
fi

# Iterate over each line (each DOI) in the file.
# Using `while IFS= read -r` preserves whitespace and avoids word‑splitting.
while IFS= read -r DOI; do
    # Skip empty lines (optional, but handy)
    [[ -z "$DOI" ]] && continue

    echo "Processing DOI: $DOI"

    # Add DOI prefix
    DOI="doi:10.17026/$DOI"

    # Run the Python module. Adjust the import path if necessary.
    python3 -m src.pipeline --doi "$DOI"

    # Check the exit status of the Python command – useful for debugging.
    if [[ $? -ne 0 ]]; then
        echo "Warning: Python script failed for DOI $DOI" >&2
    else
        echo "Finished processing DOI: $DOI"
    fi
done < "$DOI_FILE"