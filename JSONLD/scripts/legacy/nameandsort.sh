#! /bin/bash

# Find and process each JSON file
# Change the id to lowercase and hyphenated
# sort keys alphabetically. 

find "$@" -type f -name "*.json" | while read -r file; do
    echo "Processing: $file"
    jq 'walk(
        if type == "object" then
            with_entries(
                if .key == "@id" then
                    .key = "@id",
                    .value |= (if type == "string" then ascii_downcase | gsub("_"; "-") else . end)
                else
                    .key |= (if type == "string" then ascii_downcase | gsub("_"; "-") else . end)
                end
                    
            )
        else
            .
        end
    )' "$file" | jq -S '.' > "${file}.tmp" && mv "${file}.tmp" "$file"
done