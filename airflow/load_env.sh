#!/bin/bash

# Script to load environment variables from a .env file. Must be run using source function.
# Usage: source ./load_env.sh [path_to_env_file]
# or: . ./load_env.sh [path_to_env_file]

# Default .env file path
ENV_FILE="${1:-.env}"

# Check if file exists
if [ ! -f "$ENV_FILE" ]; then
    echo "Error: .env file '$ENV_FILE' not found!"
    return 1 2>/dev/null || exit 1
fi

# Read .env file and export variables
echo "Loading environment variables from: $ENV_FILE"

while IFS= read -r line; do
    # Skip empty lines and comments
    if [[ -z "$line" || "$line" =~ ^[[:space:]]*# ]]; then
        continue
    fi
    
    # Remove leading/trailing whitespace
    line=$(echo "$line" | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')
    
    # Check if line contains an equals sign
    if [[ "$line" == *"="* ]]; then
        # Extract key and value
        key=$(echo "$line" | cut -d'=' -f1)
        value=$(echo "$line" | cut -d'=' -f2-)
        
        # Remove quotes if present
        value=$(echo "$value" | sed 's/^"\(.*\)"$/\1/; s/^'"'"'\(.*\)'"'"'$/\1/')
        
        # Export the variable
        export "$key=$value"
        echo "Exported: $key"
    fi
done < "$ENV_FILE"

echo "Environment variables loaded successfully!"
echo "Note: These variables are now available in your current shell session."
