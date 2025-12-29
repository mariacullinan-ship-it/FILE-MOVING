#!/usr/bin/env python3
"""
Tests for the file organizer script.
"""

import os
import shutil
import tempfile
import unittest
from pathlib import Path

# Import the module to test
import organize_files


class TestFileOrganizer(unittest.TestCase):
    """Test cases for file organizer functionality."""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        # Create a temporary directory for testing
        self.test_dir = tempfile.mkdtemp()
        self.test_path = Path(self.test_dir)
    
    def tearDown(self):
        """Clean up test fixtures after each test method."""
        # Remove the temporary directory
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
    
    def test_get_folder_for_extension(self):
        """Test that extensions map to correct folder names."""
        self.assertEqual(organize_files.get_folder_for_extension("jpg"), "Images")
        self.assertEqual(organize_files.get_folder_for_extension("JPG"), "Images")
        self.assertEqual(organize_files.get_folder_for_extension("pdf"), "PDF")
        self.assertEqual(organize_files.get_folder_for_extension("csv"), "Spreadsheets")
        self.assertEqual(organize_files.get_folder_for_extension("xlsx"), "Spreadsheets")
        self.assertEqual(organize_files.get_folder_for_extension("doc"), "Word")
        self.assertEqual(organize_files.get_folder_for_extension("docx"), "Word")
        self.assertEqual(organize_files.get_folder_for_extension("json"), "JSON")
        self.assertIsNone(organize_files.get_folder_for_extension("txt"))
        self.assertIsNone(organize_files.get_folder_for_extension("mp4"))
    
    def test_get_unique_filename_no_conflict(self):
        """Test unique filename generation when no conflict exists."""
        filename = organize_files.get_unique_filename(self.test_path, "test.jpg")
        self.assertEqual(filename, "test.jpg")
    
    def test_get_unique_filename_with_conflict(self):
        """Test unique filename generation when conflicts exist."""
        # Create a file that will conflict
        (self.test_path / "test.jpg").touch()
        
        filename = organize_files.get_unique_filename(self.test_path, "test.jpg")
        self.assertEqual(filename, "test-1.jpg")
        
        # Create another conflict
        (self.test_path / "test-1.jpg").touch()
        
        filename = organize_files.get_unique_filename(self.test_path, "test.jpg")
        self.assertEqual(filename, "test-2.jpg")
    
    def test_get_unique_filename_with_multiple_conflicts(self):
        """Test unique filename generation with multiple conflicts."""
        # Create multiple conflicting files
        (self.test_path / "document.pdf").touch()
        (self.test_path / "document-1.pdf").touch()
        (self.test_path / "document-2.pdf").touch()
        
        filename = organize_files.get_unique_filename(self.test_path, "document.pdf")
        self.assertEqual(filename, "document-3.pdf")
    
    def test_organize_files_basic(self):
        """Test basic file organization."""
        # Create test files
        (self.test_path / "photo.jpg").touch()
        (self.test_path / "document.pdf").touch()
        (self.test_path / "data.csv").touch()
        (self.test_path / "spreadsheet.xlsx").touch()
        (self.test_path / "letter.docx").touch()
        (self.test_path / "report.doc").touch()
        (self.test_path / "config.json").touch()
        
        # Run organizer
        organize_files.organize_files(str(self.test_path))
        
        # Verify folders were created
        self.assertTrue((self.test_path / "Images").exists())
        self.assertTrue((self.test_path / "PDF").exists())
        self.assertTrue((self.test_path / "Spreadsheets").exists())
        self.assertTrue((self.test_path / "Word").exists())
        self.assertTrue((self.test_path / "JSON").exists())
        
        # Verify files were moved
        self.assertTrue((self.test_path / "Images" / "photo.jpg").exists())
        self.assertTrue((self.test_path / "PDF" / "document.pdf").exists())
        self.assertTrue((self.test_path / "Spreadsheets" / "data.csv").exists())
        self.assertTrue((self.test_path / "Spreadsheets" / "spreadsheet.xlsx").exists())
        self.assertTrue((self.test_path / "Word" / "letter.docx").exists())
        self.assertTrue((self.test_path / "Word" / "report.doc").exists())
        self.assertTrue((self.test_path / "JSON" / "config.json").exists())
        
        # Verify original files were removed
        self.assertFalse((self.test_path / "photo.jpg").exists())
        self.assertFalse((self.test_path / "document.pdf").exists())
    
    def test_organize_files_with_conflicts(self):
        """Test file organization with name conflicts."""
        # Create target folder with existing file
        images_folder = self.test_path / "Images"
        images_folder.mkdir()
        (images_folder / "photo.jpg").touch()
        
        # Create new file with same name in source
        (self.test_path / "photo.jpg").touch()
        
        # Run organizer
        organize_files.organize_files(str(self.test_path))
        
        # Verify both files exist with different names
        self.assertTrue((images_folder / "photo.jpg").exists())
        self.assertTrue((images_folder / "photo-1.jpg").exists())
    
    def test_organize_files_skips_unhandled_extensions(self):
        """Test that files with unhandled extensions are skipped."""
        # Create files with various extensions
        (self.test_path / "test.txt").touch()
        (self.test_path / "video.mp4").touch()
        (self.test_path / "photo.jpg").touch()
        
        # Run organizer
        organize_files.organize_files(str(self.test_path))
        
        # Verify unhandled files remain in place
        self.assertTrue((self.test_path / "test.txt").exists())
        self.assertTrue((self.test_path / "video.mp4").exists())
        
        # Verify handled file was moved
        self.assertFalse((self.test_path / "photo.jpg").exists())
        self.assertTrue((self.test_path / "Images" / "photo.jpg").exists())
    
    def test_organize_files_skips_directories(self):
        """Test that subdirectories are not processed."""
        # Create a subdirectory
        subdir = self.test_path / "existing_subfolder"
        subdir.mkdir()
        (subdir / "photo.jpg").touch()
        
        # Create a file in root
        (self.test_path / "photo.jpg").touch()
        
        # Run organizer
        organize_files.organize_files(str(self.test_path))
        
        # Verify subdirectory still exists and wasn't processed
        self.assertTrue(subdir.exists())
        self.assertTrue((subdir / "photo.jpg").exists())
        
        # Verify root file was moved
        self.assertTrue((self.test_path / "Images" / "photo.jpg").exists())
    
    def test_organize_files_case_insensitive_extensions(self):
        """Test that file extensions are handled case-insensitively."""
        # Create files with various case extensions
        (self.test_path / "photo.JPG").touch()
        (self.test_path / "document.PDF").touch()
        (self.test_path / "data.CSV").touch()
        
        # Run organizer
        organize_files.organize_files(str(self.test_path))
        
        # Verify files were moved correctly
        self.assertTrue((self.test_path / "Images" / "photo.JPG").exists())
        self.assertTrue((self.test_path / "PDF" / "document.PDF").exists())
        self.assertTrue((self.test_path / "Spreadsheets" / "data.CSV").exists())


if __name__ == "__main__":
    unittest.main()
