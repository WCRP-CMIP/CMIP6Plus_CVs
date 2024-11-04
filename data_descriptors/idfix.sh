find . -type f -name "*-*.json" | while read -r file; do
    new_file=$(echo "$file" | sed 's/-/_/g')
    mv "$file" "$new_file"
done

find . -type f -name "*.json" | while read -r file; do
    # Extract the filename without path and extension
    filename=$(basename "$file" .json)
    
    # Update the "id" field inside the JSON to match the new filename
    perl -i -pe "s/\"id\" *: *\"[^\"]+\"/\"id\": \"$filename\"/" "$file"
    
    # Change permissions to make the file readable for others but not writable
    chmod 644 "$file"
done

rm -f */*.json-E
