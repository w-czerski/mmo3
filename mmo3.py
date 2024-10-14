#!/usr/bin/env python3

import os
import shutil
import argparse
import json
from pathlib import Path
import filecmp

# Set default paths
HOME = str(Path.home())
MANIFEST_DIR = f"{HOME}/.manifests"
O3DE_MANIFEST = os.path.join(HOME, ".o3de", "o3de_manifest.json")

# Helper function to get a list of all manifest files in the manifest directory
def list_manifests():
    # List all .json files in the ~/.manifests directory
    manifests = [f for f in os.listdir(MANIFEST_DIR) if f.endswith('.json')]

    # Load the current ~/.o3de/o3de_manifest.json
    if os.path.exists(O3DE_MANIFEST):
        with open(O3DE_MANIFEST, 'r') as f:
            current_manifest_data = json.load(f)
    else:
        current_manifest_data = None

    # Function to check if two manifest files are identical
    def is_same_manifest_by_content(manifest_a_path, manifest_b_path):
        try:
            # Compare the file contents directly
            return filecmp.cmp(manifest_a_path, manifest_b_path, shallow=False)
        except Exception as e:
            print(f"Error comparing {manifest_a_path} with {manifest_b_path}: {e}")
            return False

    # Check if there are any available manifest files
    if len(manifests) > 0:
        print("Available manifests:")
        for manifest in manifests:
            manifest_path = os.path.join(MANIFEST_DIR, manifest)
            in_use = ""

            # Directly compare the content of the current ~/.o3de manifest with the manifest in ~/.manifests
            if os.path.exists(O3DE_MANIFEST) and is_same_manifest_by_content(O3DE_MANIFEST, manifest_path):
                in_use = " <-- currently used"

            print(f"  - {manifest}{in_use}")
    else:
        print("Currently, there are no available manifests to switch on."
              "\nPlease create or copy manifests into the path: ", MANIFEST_DIR)


# Set the current manifest to the chosen one
def set_manifest(manifest_name):
    manifest_path = os.path.join(MANIFEST_DIR, manifest_name)
    if os.path.exists(manifest_path):
        shutil.copy(manifest_path, O3DE_MANIFEST)
        print(f"The manifest '{manifest_name}' is now set as the active one.")
    else:
        print(f"Manifest '{manifest_name}' does not exist.")


# Create a new manifest
def create_manifest(manifest_name):
    new_manifest_path = os.path.join(MANIFEST_DIR, manifest_name)
    if not manifest_name.endswith('.json'):
        manifest_name += '.json'

    if os.path.exists(new_manifest_path):
        print(f"A manifest with the name '{manifest_name}' already exists.")
    else:
        default_manifest = {
            "engine_version": "",
            "projects": []
        }
        with open(new_manifest_path, 'w') as f:
            json.dump(default_manifest, f, indent=4)
        print(f"Created new manifest -'{manifest_name}'")


# Open a manifest in the default editor (nano)
def open_manifest(manifest_name=None):
    if manifest_name:
        manifest_path = os.path.join(MANIFEST_DIR, manifest_name)
    else:
        manifest_path = O3DE_MANIFEST

    if os.path.exists(manifest_path):
        os.system(f"nano {manifest_path}")
    else:
        print(f"Manifest '{manifest_name}' does not exist.")


# Duplicate an existing manifest
def duplicate_manifest(manifest_name):
    manifest_path = os.path.join(MANIFEST_DIR, manifest_name)
    if os.path.exists(manifest_path):
        new_name = input("Enter the name for the duplicate manifest: ")
        if not new_name.endswith('.json'):
            new_name += '.json'
        shutil.copy(manifest_path, os.path.join(MANIFEST_DIR, new_name))
        print(f"Manifest duplicated as '{new_name}'")
    else:
        print(f"Manifest '{manifest_name}' does not exist.")


# Main function to handle arguments
def main():
    parser = argparse.ArgumentParser(description="MMO3 Manifest Manager")

    parser.add_argument('-list', '-ls', action="store_true", help="List all manifests")
    parser.add_argument('-set', '-s', type=str, help="Set the active manifest")
    parser.add_argument('-new', '-n', type=str, help="Create a new manifest")
    parser.add_argument('-open', '-o', nargs='?', const='', help="Open manifest in text editor (nano)")
    parser.add_argument('-duplicate', '-d', type=str, help="Duplicate an existing manifest")
    parser.add_argument("-version", "-v", action="store_true", help="Show the application version")

    args = parser.parse_args()

    if args.list:
        list_manifests()

    if args.set:
        set_manifest(args.set)

    if args.new:
        create_manifest(args.new)

    if args.open is not None:
        open_manifest(args.open)

    if args.duplicate:
        duplicate_manifest(args.duplicate)

    if args.version:
        print("mmo3 - O3DE Manifest Manager - version 1.0")


if __name__ == '__main__':
    main()