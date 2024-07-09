#!/bin/bash

# Directory containing the zip files
# dir="data_dump/New Data Collection 040424 BTEC/zip exports"

# # Loop over all zip files in the directory
# for i in "$dir"/*.zip; do
#     # Run the command on each zip file
#     python3 pycorn-bin.py -e xlsx "$i"
#     # python pycorn-bin.py -t "$i"
# done

dir="data_dump/New Data Collection 040424 BTEC_annex/all"

# Loop over all zip files in the directory and its subdirectories
find "$dir" -name "*.zip" | while read i; do
    # Run the command on each zip file
    python3 pycorn-bin.py -e xlsx "$i"
    # python pycorn-bin.py -t "$i"
done