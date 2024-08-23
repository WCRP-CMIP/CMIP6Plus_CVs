



for file in *.json; do jq 'with_entries(.key |= sub("^[^:]+:"; ""))' "$file" > tmp.$file && mv tmp.$file "$file"; done



for file in *.json; do jq 'with_entries(if .key | startswith("@") then . else .key |= "prefix_" + . end)' "$file" > tmp.$file && mv tmp.$file "$file"; done


find ../../ -type f -name "*.jsonld.json" -exec bash -c 'mv "$1" "${1%.jsonld.json}.jsonld"' _ {} \;



# linkml-convert -s instituitons.yaml cams.yaml -t json-ld  --context {} | jq 'with_entries(.key |= "prefix:" + .)' | perl -pe 's/"prefix:(id|type)":/"@\1":/g;'


# https://jmespath.org/
# https://jmespath.org/tutorial.html