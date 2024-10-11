#!/bin/bash

# Define paths
MANIFEST_DIR="$HOME/.manifests"
MMO3_PATH="/usr/local/bin/mmo3"

# Step 1: Check if ~/.manifests directory exists, if not, create it
if [ ! -d "$MANIFEST_DIR" ]; then
    echo "Creating directory $MANIFEST_DIR..."
    mkdir -p "$MANIFEST_DIR"
    echo "Directory $MANIFEST_DIR created."
else
    echo "Directory $MANIFEST_DIR already exists."
fi

# Step 2: Copy mmo3.py to /usr/local/bin/mmo3
if [ -f "./mmo3.py" ]; then
    echo "Installing mmo3 script..."
    sudo cp mmo3.py $MMO3_PATH
    sudo chmod +x $MMO3_PATH
    echo "mmo3 has been installed as a global command."
else
    echo "mmo3.py not found! Make sure you're in the right directory where mmo3.py exists."
    exit 1
fi

# Step 3: Check if mmo3 is in the user's PATH and executable
if command -v mmo3 > /dev/null 2>&1; then
    echo "Installation complete! You can now use 'mmo3' from the command line."
    echo "Type mmo3 --help or -h to view available commands."
else
    echo "Installation failed: mmo3 is not available in your PATH. Please check manually."
fi
