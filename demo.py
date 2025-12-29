#!/usr/bin/env python3
"""
Demo script to show how the file organizer works.
Creates a temporary test directory, populates it with sample files, and runs the organizer.
"""

import os
import shutil
import tempfile
from pathlib import Path

import organize_files


def create_demo():
    """Create a demo environment and run the file organizer."""
    # Create a temporary directory
    demo_dir = tempfile.mkdtemp(prefix="file_organizer_demo_")
    demo_path = Path(demo_dir)
    
    print("=" * 70)
    print("FILE ORGANIZER DEMO")
    print("=" * 70)
    print(f"\nCreated demo directory: {demo_dir}\n")
    
    # Create sample files
    sample_files = [
        "vacation_photo.jpg",
        "family_picture.jpg",
        "contract.pdf",
        "invoice.pdf",
        "budget.xlsx",
        "contacts.csv",
        "report.docx",
        "letter.doc",
        "config.json",
        "data.json",
        "readme.txt",  # This should be skipped
        "video.mp4",   # This should be skipped
    ]
    
    print("Creating sample files:")
    print("-" * 70)
    for filename in sample_files:
        file_path = demo_path / filename
        # Create file with some dummy content
        with open(file_path, 'w') as f:
            f.write(f"This is a sample {filename} file.\n")
        print(f"  ✓ {filename}")
    
    print("\n" + "=" * 70)
    print("BEFORE ORGANIZATION")
    print("=" * 70)
    print("\nDirectory structure:")
    list_directory_structure(demo_path)
    
    print("\n" + "=" * 70)
    print("RUNNING FILE ORGANIZER")
    print("=" * 70)
    print()
    
    # Run the organizer
    organize_files.organize_files(str(demo_path))
    
    print("\n" + "=" * 70)
    print("AFTER ORGANIZATION")
    print("=" * 70)
    print("\nDirectory structure:")
    list_directory_structure(demo_path)
    
    print("\n" + "=" * 70)
    print("TESTING CONFLICT RESOLUTION")
    print("=" * 70)
    print("\nCreating a duplicate 'vacation_photo.jpg' file...")
    
    # Create a duplicate file to test conflict resolution
    duplicate_file = demo_path / "vacation_photo.jpg"
    with open(duplicate_file, 'w') as f:
        f.write("This is a DUPLICATE vacation_photo.jpg file.\n")
    print("  ✓ vacation_photo.jpg created")
    
    print("\nRunning organizer again...")
    organize_files.organize_files(str(demo_path))
    
    print("\nDirectory structure:")
    list_directory_structure(demo_path)
    
    print("\n" + "=" * 70)
    print("DEMO COMPLETE")
    print("=" * 70)
    print(f"\nDemo directory preserved at: {demo_dir}")
    print("You can inspect the results manually or run this script again.")
    print(f"To clean up: rm -rf {demo_dir}")
    print()
    
    return demo_dir


def list_directory_structure(path: Path, indent: int = 0):
    """
    Recursively list directory structure.
    
    Args:
        path: Path to list
        indent: Indentation level
    """
    try:
        items = sorted(path.iterdir())
        
        for item in items:
            prefix = "  " * indent
            if item.is_dir():
                print(f"{prefix}📁 {item.name}/")
                list_directory_structure(item, indent + 1)
            else:
                size = item.stat().st_size
                print(f"{prefix}📄 {item.name} ({size} bytes)")
    except PermissionError:
        print(f"{'  ' * indent}[Permission denied]")


if __name__ == "__main__":
    create_demo()
