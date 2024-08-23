#!/bin/bash

# ./combine_graphs.sh compiled/graph_data .. graph ../miptables
# ./combine_graphs.sh compiled/data_request ../miptables graph none
# ./combine_graphs.sh compiled/versioning .. version none

# Check if the correct number of arguments is provided
if [ "$#" -lt 4 ]; then
    echo "Usage: $0 <output_file_name> <directory_to_search> <file_name> <skip_dir1> [<skip_dir2> ...]"
    exit 1
fi

# Assign arguments to variables
OUTPUT_FILE="$1.json"
MINIFIED_OUTPUT_FILE="${OUTPUT_FILE%.*}.min.json"
SEARCH_DIR="$2"
FILE_NAME="$3.jsonld"
shift 3
SKIP_DIRS=("$@")

# Function to check if a directory is in the skip list
function is_skipped {
    local dir=$1
    for skip in "${SKIP_DIRS[@]}"; do
        if [[ "$dir" == *"$skip"* ]]; then
            return 0
        fi
    done
    return 1
}

# Remove the output files if they exist
[ -f "$OUTPUT_FILE" ] && rm "$OUTPUT_FILE"
[ -f "$MINIFIED_OUTPUT_FILE" ] && rm "$MINIFIED_OUTPUT_FILE"

# Initialize/clear the output files and start the JSON array
echo "[" > "$OUTPUT_FILE"
echo "[" > "$MINIFIED_OUTPUT_FILE"

# Variable to track if an entry has been added (to handle commas correctly)
first_entry=true

# Find all specified JSON files, skipping directories in SKIP_DIRS
find "$SEARCH_DIR" -type f -name "$FILE_NAME" | while read -r file; do
    dir=$(dirname "$file")
    if ! is_skipped "$dir"; then
        if [ "$first_entry" = true ]; then
            first_entry=false
        else
            echo "," >> "$OUTPUT_FILE"
        fi
        echo "Found: $file"
        cat "$file" >> "$OUTPUT_FILE"
    fi
done

# Close the JSON array
echo "]" >> "$OUTPUT_FILE"

# Create a minified version of the concatenated file
jq -c . "$OUTPUT_FILE" > "$MINIFIED_OUTPUT_FILE"

echo "All $FILE_NAME files have been concatenated into $OUTPUT_FILE"
echo "A minified version has been created as $MINIFIED_OUTPUT_FILE"
