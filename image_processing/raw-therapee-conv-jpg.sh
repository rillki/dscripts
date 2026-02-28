#!/usr/bin/env bash

INPUT_DIR="."
OUTPUT_DIR="./optimized"

while [[ $# -gt 0 ]]; do
  case "$1" in
    -i|--input)  INPUT_DIR="$2";  shift 2 ;;
    -o|--output) OUTPUT_DIR="$2"; shift 2 ;;
    -h|--help)
      echo "Usage: $(basename "$0") [-i INPUT_DIR] [-o OUTPUT_DIR]"
      echo "  -i, --input   Input directory (default: current directory)"
      echo "  -o, --output  Output directory (default: ./optimized)"
      exit 0
      ;;
    *)
      echo "Unknown option: $1" >&2
      exit 1
      ;;
  esac
done

echo "Input:  $INPUT_DIR"
echo "Output: $OUTPUT_DIR"
read -rp "Start conversion? [Y/n] " answer
answer="${answer:-y}"

if [[ ! "${answer,,}" == "y" ]]; then
  echo "Aborted."
  exit 0
fi

mkdir -p "$OUTPUT_DIR"

for file in "$INPUT_DIR"/*.jpg "$INPUT_DIR"/*.JPG; do
  [ -f "$file" ] || continue
  rawtherapee-cli -o "$OUTPUT_DIR" -j90 -Y -c "$file"
done


