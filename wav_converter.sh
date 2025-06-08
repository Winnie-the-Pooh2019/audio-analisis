#!/bin/bash

# Directory containing .m4a files (default is current directory)
INPUT_DIR="./music"
OUTPUT_DIR="./wav"

# Create output directory if it doesn't exist
mkdir -p "$OUTPUT_DIR"

# Loop through all .m4a files in input directory
for file in "$INPUT_DIR"/*.m4a; do
    # Check if there are actually .m4a files
    if [ -e "$file" ]; then
        filename=$(basename "$file" .m4a)
        echo "Converting '$file' to '${filename}.wav'..."
        ffmpeg -i "$file" "$OUTPUT_DIR/${filename}.wav"
    else
        echo "No .m4a files found in '$INPUT_DIR'"
        exit 1
    fi
done

echo "Conversion complete! WAV files saved in '$OUTPUT_DIR'"