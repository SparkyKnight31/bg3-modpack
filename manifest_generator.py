#!/usr/bin/env python3
import os
import json
import argparse
import hashlib
from datetime import datetime

def generate_manifest(mods_dir, base_url, output_file, name="BG3 Gayming Modpack"):
    """
    Generate a manifest.json file for all mods in the specified directory.
    
    Args:
        mods_dir (str): Path to the directory containing mod files
        base_url (str): Base URL where mods will be hosted (e.g., 'https://username.github.io/bg3-modpack/mods/')
        output_file (str): Path where the manifest.json will be saved
        name (str): Name of the modpack
    """
    if not os.path.exists(mods_dir):
        print(f"Error: Mods directory '{mods_dir}' does not exist.")
        return False
    
    # Ensure the base_url ends with a slash
    if not base_url.endswith('/'):
        base_url += '/'
    
    mods = []
    
    print(f"Scanning directory: {mods_dir}")
    
    # List all files in the mods directory
    for filename in os.listdir(mods_dir):
        file_path = os.path.join(mods_dir, filename)
        
        # Skip directories
        if os.path.isdir(file_path):
            continue
        
        # Skip hidden files
        if filename.startswith('.'):
            continue
        
        # Only include zip, rar, and 7z files (common mod formats)
        if not filename.lower().endswith(('.zip', '.rar', '.7z')):
            print(f"Skipping non-archive file: {filename}")
            continue
        
        # Get file size and last modified time
        file_size = os.path.getsize(file_path)
        last_modified = datetime.fromtimestamp(os.path.getmtime(file_path))
        
        # Generate MD5 hash for the file (useful for version checking)
        md5_hash = calculate_md5(file_path)
        
        # Extract mod name from filename (remove extension)
        mod_name = os.path.splitext(filename)[0]
        
        # Create mod entry
        mod_entry = {
            "name": mod_name,
            "fileName": filename,
            "version": last_modified.strftime("%Y.%m.%d"),  # Use date as version
            "size": file_size,
            "md5": md5_hash,
            "downloadUrl": f"{base_url}{filename}"
        }
        
        mods.append(mod_entry)
        print(f"Added mod: {mod_name}")
    
    if not mods:
        print("No mod files found in the specified directory.")
        return False
    
    # Create the manifest
    manifest = {
        "name": name,
        "version": datetime.now().strftime("%Y.%m.%d"),
        "lastUpdated": datetime.now().isoformat(),
        "modCount": len(mods),
        "mods": mods
    }
    
    # Write the manifest to the output file
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(manifest, f, indent=2)
    
    print(f"Manifest generated successfully with {len(mods)} mods.")
    print(f"Saved to: {output_file}")
    return True

def calculate_md5(file_path):
    """Calculate MD5 hash for a file."""
    md5_hash = hashlib.md5()
    with open(file_path, "rb") as f:
        # Read file in chunks to handle large files
        for chunk in iter(lambda: f.read(4096), b""):
            md5_hash.update(chunk)
    return md5_hash.hexdigest()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate a manifest.json file for a BG3 modpack.")
    parser.add_argument("--mods-dir", default="./mods", help="Directory containing mod files (default: ./mods)")
    parser.add_argument("--base-url", required=True, help="Base URL where mods will be hosted (e.g., 'https://username.github.io/bg3-modpack/mods/')")
    parser.add_argument("--output", default="./manifest.json", help="Output file path (default: ./manifest.json)")
    parser.add_argument("--name", default="BG3 Gayming Modpack", help="Name of the modpack (default: 'BG3 Gayming Modpack')")
    
    args = parser.parse_args()
    
    generate_manifest(args.mods_dir, args.base_url, args.output, args.name)