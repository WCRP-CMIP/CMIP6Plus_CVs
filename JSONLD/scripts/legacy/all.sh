#! /bin/bash 

python update_new.py $@;

./combine_graphs.sh compiled/graph_data .. graph ../scripts 

# if using flags.



# # Directory containing the files
# DIR="node_scripts"

# # Loop through each file in the directory
# for FILE in "$DIR"/*
# do
#   # Check if it is a file (not a directory)
#   if [ -f "$FILE" ]; then
#     # Run your command here, e.g., print the file name
    
#     echo -e "\033[94m Processing file: $FILE \033[90m"
#     # skip files that start with x
#         if [[ "$filename" != x* ]]; then
#     node $FILE
#     fi
    
#      echo -e "\033[0m"
#     # Example command: Run a script or command with the file as an argument
#     # ./your_command "$FILE"
#   fi
# done

