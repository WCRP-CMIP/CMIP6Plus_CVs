#!/bin/bash

# Root directory containing JSON files
root_directory=".."

# Check if jq is installed
if ! command -v jq &> /dev/null; then
    echo "jq is not installed. Please install jq (https://stedolan.github.io/jq/) to proceed."
    exit 1
fi

# Check if Perl is installed
if ! command -v perl &> /dev/null; then
    echo "Perl is not installed. Please install Perl to proceed."
    exit 1
fi

# Process each JSON file recursively
find "$root_directory" -type f -name "*.json" -print0 | while IFS= read -r -d $'\0' file; do
    echo "Processing file: $file"

    # Replace instances of "cmip:" with "mip:" using Perl
    perl -i.bak -pe 's/"cmip:/"mip:/g' "$file"

    # Remove @set section but keep its contents using jq
    jq 'walk(if type == "object" then with_entries(if .value | type == "object" and has("@nest") then .value = .value["@nest"] else . end) else . end)' "$file" > "$file.tmp"

    # Replace original file with modified one
    mv "$file.tmp" "$file"

    # Optionally, remove the backup file created by Perl
    # rm "${file}.bak"
done

echo "All JSON files in '$root_directory' processed."

