#!/bin/bash

# URL of the PNG image
IMAGE_URL="https://img.freepik.com/free-photo/lightning-hit-house_1204-219.jpg?t=st=1725995160~exp=1725998760~hmac=8352dc291722d1ccabe8c74294d491218303baff301c7920ec749bd806f8b470&w=1060"

# Output file name
OUTPUT_FILE="dark-sky-thunder.png"

# Fetch the image file
curl -o "$OUTPUT_FILE" "$IMAGE_URL"

# Get the directory of the output file
FILE_DIR=$(dirname "$(realpath "$OUTPUT_FILE")")

# Get the filename from the output file path
FILE_NAME=$(basename "$OUTPUT_FILE")

# Encode the file to base64 and remove newlines
ENCODED_IMAGE=$(base64 "$FILE_DIR/$FILE_NAME" | tr -d '\n')
echo "$ENCODED_IMAGE" > encoded_file.txt

# Perform the curl request
curl -X POST "https://api.runpod.ai/v2/a4gv71qdr31by4/runsync" \
-H "accept: application/json" \
-H "content-type: application/json" \
-d '{
  "input": {
    "prompt": "Hello World",
    "model_name": "sketch_to_image_stochastic",
    "model_path": "",
    "use_fp16": true,
    "low_threshold": 100,
    "high_threshold": 200,
    "gamma": 0.4,
    "seed": 42
  }
}'
