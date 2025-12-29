# FILE-MOVING

A Python script to automatically organize files in a specific directory into subfolders based on their file extensions.

## Purpose

This script organizes files in `C:\Users\Signature Edition\Downloads\THE REPAIR GUY` by moving them into categorized subfolders based on their file extensions.

## Features

- **Automatic folder creation**: Creates subfolders (Images, PDF, Spreadsheets, Word, JSON) as needed
- **File conflict resolution**: If a file with the same name already exists in the destination folder, the script automatically renames the incoming file by appending `-1`, `-2`, etc. before the extension
- **Safe operation**: Only processes files in the specified directory, leaving all other directories untouched
- **Case-insensitive**: Handles file extensions regardless of case (e.g., `.JPG`, `.jpg`, `.Jpg`)

## Supported File Types

The script organizes files with the following extensions:

| Extension(s) | Destination Folder |
|-------------|-------------------|
| `.jpg` | Images |
| `.pdf` | PDF |
| `.csv`, `.xlsx` | Spreadsheets |
| `.doc`, `.docx` | Word |
| `.json` | JSON |

Files with other extensions are left in place and not moved.

## Usage

### Running the Script

```bash
python organize_files.py
```

The script will:
1. Check if the target directory exists
2. Scan all files in the root of the target directory (not subdirectories)
3. Create necessary subfolders if they don't exist
4. Move files to their appropriate subfolders
5. Handle naming conflicts automatically
6. Display a summary of operations

### Example Output

```
Organizing files in: C:\Users\Signature Edition\Downloads\THE REPAIR GUY
------------------------------------------------------------
Moved: photo.jpg → Images/photo.jpg
Moved: document.pdf → PDF/document.pdf
Moved: data.csv → Spreadsheets/data.csv
Moved (renamed): report.pdf → PDF/report-1.pdf
Skipped (unhandled extension): readme.txt
------------------------------------------------------------
Summary: 4 files moved, 1 files skipped
```

## Testing

Run the test suite to verify functionality:

```bash
python test_organize_files.py -v
```

The test suite includes:
- Extension mapping tests
- Filename conflict resolution tests
- Full file organization tests
- Edge case handling

## Requirements

- Python 3.6 or higher
- Standard library only (no external dependencies)

## How It Works

1. **Directory Scanning**: The script scans only the top-level files in the target directory
2. **Extension Detection**: Each file's extension is checked against the supported extensions
3. **Folder Creation**: If a destination subfolder doesn't exist, it's created automatically
4. **Conflict Resolution**: If a file with the same name exists in the destination, the script generates a unique name by appending a number (e.g., `file.jpg` becomes `file-1.jpg`)
5. **File Moving**: The file is moved to its destination subfolder
6. **Reporting**: The script outputs detailed information about each operation

## Safety Features

- Only processes files in the specified directory path
- Never modifies files in subdirectories or parent directories
- Preserves all existing files by using rename strategy for conflicts
- Validates directory existence before processing
- Handles permission errors gracefully
