#!/usr/bin/env python3
r"""
File organizer script that moves files in a specific directory into subfolders
based on their file extensions.

Only processes files in: C:\Users\Signature Edition\Downloads\THE REPAIR GUY
"""

import os
import shutil
from pathlib import Path
from typing import Dict, List


# Configuration
TARGET_DIRECTORY = r"C:\Users\Signature Edition\Downloads\THE REPAIR GUY"

# Extension to folder mapping
EXTENSION_MAPPING: Dict[str, List[str]] = {
    "Images": ["jpg"],
    "PDF": ["pdf"],
    "Spreadsheets": ["csv", "xlsx"],
    "Word": ["doc", "docx"],
    "JSON": ["json"]
}


def get_unique_filename(target_dir: Path, filename: str) -> str:
    """
    Generate a unique filename by appending -1, -2, etc. if file already exists.
    
    Args:
        target_dir: Target directory path
        filename: Original filename
        
    Returns:
        Unique filename that doesn't conflict with existing files
    """
    target_path = target_dir / filename
    
    if not target_path.exists():
        return filename
    
    # Split filename into name and extension
    stem = Path(filename).stem
    suffix = Path(filename).suffix
    
    counter = 1
    while True:
        new_filename = f"{stem}-{counter}{suffix}"
        new_path = target_dir / new_filename
        
        if not new_path.exists():
            return new_filename
        
        counter += 1


def get_folder_for_extension(extension: str) -> str | None:
    """
    Get the folder name for a given file extension.
    
    Args:
        extension: File extension (without dot)
        
    Returns:
        Folder name or None if extension is not in mapping
    """
    extension_lower = extension.lower()
    
    for folder_name, extensions in EXTENSION_MAPPING.items():
        if extension_lower in extensions:
            return folder_name
    
    return None


def organize_files(target_directory: str = TARGET_DIRECTORY) -> None:
    """
    Organize files in the target directory into subfolders based on extensions.
    
    Args:
        target_directory: Path to the directory to organize
    """
    target_path = Path(target_directory)
    
    # Validate target directory exists
    if not target_path.exists():
        print(f"Error: Target directory does not exist: {target_directory}")
        return
    
    if not target_path.is_dir():
        print(f"Error: Target path is not a directory: {target_directory}")
        return
    
    print(f"Organizing files in: {target_directory}")
    print("-" * 60)
    
    # Track statistics
    files_moved = 0
    files_skipped = 0
    
    # Get all files in the target directory (not subdirectories)
    try:
        items = list(target_path.iterdir())
    except PermissionError:
        print(f"Error: Permission denied to access directory: {target_directory}")
        return
    
    for item in items:
        # Only process files, not directories
        if not item.is_file():
            continue
        
        # Get file extension (without the dot)
        extension = item.suffix.lstrip('.')
        
        if not extension:
            # Skip files without extension
            files_skipped += 1
            print(f"Skipped (no extension): {item.name}")
            continue
        
        # Get target folder for this extension
        target_folder_name = get_folder_for_extension(extension)
        
        if target_folder_name is None:
            # Skip files with extensions we don't handle
            files_skipped += 1
            print(f"Skipped (unhandled extension): {item.name}")
            continue
        
        # Create target folder if it doesn't exist
        target_folder = target_path / target_folder_name
        target_folder.mkdir(exist_ok=True)
        
        # Get unique filename to avoid conflicts
        unique_filename = get_unique_filename(target_folder, item.name)
        target_file = target_folder / unique_filename
        
        # Move the file
        try:
            shutil.move(str(item), str(target_file))
            files_moved += 1
            
            if unique_filename != item.name:
                print(f"Moved (renamed): {item.name} → {target_folder_name}/{unique_filename}")
            else:
                print(f"Moved: {item.name} → {target_folder_name}/{unique_filename}")
        except Exception as e:
            print(f"Error moving {item.name}: {e}")
            files_skipped += 1
    
    print("-" * 60)
    print(f"Summary: {files_moved} files moved, {files_skipped} files skipped")


def main():
    """Main entry point for the script."""
    organize_files()


if __name__ == "__main__":
    main()
