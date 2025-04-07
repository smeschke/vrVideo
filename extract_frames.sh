#!/bin/bash

# Create directories and extract first 1000 frames from each .MP4 file
for file in *.MP4; do
    if [[ -f "$file" ]]; then
        # Get filename without extension
        filename="${file%.MP4}"
        
        # Create a folder with the same name as the file
        mkdir -p "$filename"
        
        # Extract first 1000 frames and save as images
        ffmpeg -i "$file" -vf "scale=1920:1080" -vframes 1000 "$filename/frame_%04d.png"
    fi
done
