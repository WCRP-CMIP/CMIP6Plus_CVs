#!/bin/bash

# Define the branch and files to be removed from history
BRANCH_NAME="your-branch-name"
FILES=(
  "JSONLD/miptables/variables/table-specific/graph.json"
  "JSONLD/scripts/data_request"
  "JSONLD/scripts/graph_data.json"
)

# Backup your repository before proceeding
git clone --mirror https://github.com/PCMDI/mip-cmor-tables.git mip-cmor-tables-backup
cd mip-cmor-tables-backup

# Loop through each file and remove it from history for the specified branch
for FILE in "${FILES[@]}"; do
  git filter-branch --index-filter "git rm --cached --ignore-unmatch '$FILE'" -- $BRANCH_NAME
done

# Force push the changes to update the remote repository
git push --force origin $BRANCH_NAME

# Clean up
cd ..
rm -rf mip-cmor-tables-backup

