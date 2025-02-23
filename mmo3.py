#!/usr/bin/env python3

import os
import shutil
import argparse
import json
from pathlib import Path
import filecmp
import time

# Set default paths
HOME = str(Path.home())
MANIFEST_DIR = f"{HOME}/.manifests"
O3DE_MANIFEST = os.path.join(HOME, ".o3de", "o3de_manifest.json")


# Helper function to get a list of all manifest files in the manifest directory
def list_manifests():
    # List all .json files in the ~/.manifests directory
    manifests = [f for f in os.listdir(MANIFEST_DIR) if f.endswith('.json')]

    # Function to determine if two manifest files are identical
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

        # First pass: Print the "in_use" manifest
        for manifest in manifests:
            manifest_path = os.path.join(MANIFEST_DIR, manifest)
            if os.path.exists(O3DE_MANIFEST) and is_same_manifest_by_content(O3DE_MANIFEST, manifest_path):
                print(f"\n  - [active] {manifest}\n")
                break  # Only one manifest can be "in_use"

        # Second pass: Print all other manifests except the "in_use" one
        for manifest in manifests:
            manifest_path = os.path.join(MANIFEST_DIR, manifest)
            if os.path.exists(O3DE_MANIFEST) and is_same_manifest_by_content(O3DE_MANIFEST, manifest_path):
                continue  # Skip the "in_use" manifest
            print(f"  - {manifest}")

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


# Show the status of the current manifest
def show_status():
    # Check if the current manifest exists
    if not os.path.exists(O3DE_MANIFEST):
        print("No active manifest found in ~/.o3de")
        return

    # Get the last modified time of the current manifest
    modified_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(os.path.getmtime(O3DE_MANIFEST)))

    # Load the current manifest
    with open(O3DE_MANIFEST, 'r') as f:
        current_manifest_data = json.load(f)

    engine_version = current_manifest_data.get("engines", "Unknown")
    projects = current_manifest_data.get("projects", [])

    # Determine the name of the manifest being used by comparing with ~/.manifests
    manifest_name = "Unknown"
    for manifest in os.listdir(MANIFEST_DIR):
        manifest_path = os.path.join(MANIFEST_DIR, manifest)
        if filecmp.cmp(O3DE_MANIFEST, manifest_path, shallow=False):
            manifest_name = manifest
            break

    # Print the status
    print(f"Manifest status:")
    print(f"  Last Modified: {modified_time}")
    print(f"  O3DE Version: {engine_version}")
    print(f"  Projects: {projects}")
    print(f"  Current Manifest: {manifest_name}")


# Main function to handle arguments
def main():
    parser = argparse.ArgumentParser(description="MMO3 Manifest Manager")

    parser.add_argument('-list', '-ls', action="store_true", help="List all manifests")
    parser.add_argument('-set', '-s', type=str, help="Set the active manifest")
    parser.add_argument('-new', '-n', type=str, help="Create a new manifest")
    parser.add_argument('-open', '-o', nargs='?', const='', help="Open manifest in text editor (nano)")
    parser.add_argument('-duplicate', '-d', type=str, help="Duplicate an existing manifest")
    parser.add_argument('-status', '-st', action="store_true", help="Show the status of the active manifest")
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

    if args.status:
        show_status()

    if args.version:
        print("mmo3 - O3DE Manifest Manager - version 1.1")


if __name__ == '__main__':
    main()