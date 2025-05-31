#!/usr/bin/env python3
"""
Course Materials Organizer

This script helps organize course materials into the appropriate directories
based on file type and naming conventions.
"""

import os
import shutil
import re
from pathlib import Path

# Configuration
COURSES = {
    'sd': 'T1-Software-Development-Management',
    'sep': 'T1-Software-Engineering-Principles'
}

FILE_TYPES = {
    'lecture': ['lecture', 'slide', 'week', 'w\d+'],
    'assignment': ['assignment', 'hw', 'a\d+'],
    'reading': ['reading', 'paper', 'chapter', 'book'],
    'reference': ['ref', 'cheatsheet', 'guide']
}

def get_target_directory(file_name, course_code):
    """Determine the target directory based on file name and type."""
    file_name_lower = file_name.lower()
    
    # Check for course code
    for code, course_dir in COURSES.items():
        if code in file_name_lower:
            base_dir = Path(course_dir) / 'raw'
            break
    else:
        base_dir = Path('.')
    
    # Determine file type
    for file_type, keywords in FILE_TYPES.items():
        if any(keyword in file_name_lower for keyword in keywords):
            return base_dir / file_type
    
    # Default to references if type not determined
    return base_dir / 'references'

def organize_files(directory='.'):
    """Organize files in the given directory."""
    directory = Path(directory)
    
    for item in directory.iterdir():
        if item.is_file() and item.name not in ['.DS_Store', 'README.md']:
            target_dir = get_target_directory(item.name, '')
            target_dir.mkdir(parents=True, exist_ok=True)
            
            # Handle naming conflicts
            target_path = target_dir / item.name
            counter = 1
            while target_path.exists():
                target_path = target_dir / f"{item.stem}_{counter}{item.suffix}"
                counter += 1
            
            # Move the file
            shutil.move(str(item), str(target_path))
            print(f"Moved: {item.name} -> {target_path}")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        organize_files(sys.argv[1])
    else:
        organize_files()

    print("\nOrganization complete!")
    print("\nNext steps:")
    print("1. Review the moved files")
    print("2. Manually move any files that weren't categorized correctly")
    print("3. Update the FILE_TYPES dictionary in the script for better organization in the future")
