json_files=$(grep -rl '"version_metadata"' *.json)

# Iterate over each JSON file and update the 'checksum' element
for json_file in $json_files; do
  jq '.version_metadata.checksum = "reset"' "$json_file" > "$json_file.tmp" && mv "$json_file.tmp" "$json_file"
done


json_files=$(grep -rl '"version_metadata"' Auxillary*/*.json)

# Iterate over each JSON file and update the 'checksum' element
for json_file in $json_files; do
  jq '.version_metadata.checksum = "reset"' "$json_file" > "$json_file.tmp" && mv "$json_file.tmp" "$json_file"
done

git add -A 
git commit -m 'reset_checksum'
git push


# make sure your commit message is 'reset_checksum'