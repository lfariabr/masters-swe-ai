"""
Tests for file handling and data loading functionality.
"""
import os
import tempfile
import pytest
import pandas as pd
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QStandardItemModel

# Import the functions to test
from gui.utils import load_excel_as_model, is_dark_mode

class TestExcelLoading:
    """Test cases for Excel file loading functionality."""
    
    def test_load_valid_excel(self, qtbot):
        """Test loading a valid Excel file."""
        # Create a temporary Excel file
        with tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False) as tmp:
            # Create a sample DataFrame
            test_data = {
                'Subject Code': ['MATH101', 'PHYS101'],
                'Subject Name': ['Calculus I', 'Physics I'],
                'Grade': ['A', 'B+']
            }
            df = pd.DataFrame(test_data)
            df.to_excel(tmp.name, index=False, engine='openpyxl')
            
            try:
                # Test loading the Excel file
                model = load_excel_as_model(tmp.name)
                
                # Verify the model was created with correct data
                assert isinstance(model, QStandardItemModel)
                assert model.rowCount() == 2  # 2 rows of data
                assert model.columnCount() == 3  # 3 columns
                
                # Verify header data
                for col, header in enumerate(test_data.keys()):
                    assert model.headerData(col, Qt.Horizontal) == header
                
                # Verify cell data
                for row in range(model.rowCount()):
                    for col in range(model.columnCount()):
                        index = model.index(row, col)
                        value = model.data(index, Qt.DisplayRole)
                        expected = str(test_data[list(test_data.keys())[col]][row])
                        assert value == expected
                        
            finally:
                # Clean up the temporary file
                os.unlink(tmp.name)
    
    def test_load_nonexistent_file(self):
        """Test loading a non-existent file should raise an exception."""
        with pytest.raises(FileNotFoundError):
            load_excel_as_model("nonexistent_file.xlsx")
    
    def test_load_invalid_excel(self, tmp_path):
        """Test loading an invalid Excel file."""
        # Create a non-Excel file
        invalid_file = tmp_path / "invalid.xlsx"
        invalid_file.write_text("This is not an Excel file")
        
        with pytest.raises(ValueError):
            load_excel_as_model(str(invalid_file))

class TestThemeDetection:
    """Test cases for theme detection functionality."""
    
    def test_is_dark_mode(self, qapp):
        """Test dark mode detection."""
        # This test is somewhat limited since we can't easily change the system theme
        # Just verify the function runs and returns a boolean
        result = is_dark_mode()
        assert isinstance(result, bool)

# Note: Using pytest's built-in tmp_path fixture instead of defining our own

# Fixture for sample Excel file
@pytest.fixture
def sample_excel_file():
    """Fixture providing a sample Excel file for testing."""
    with tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False) as tmp:
        # Create a sample DataFrame
        test_data = {
            'Subject Code': ['MATH101', 'PHYS101'],
            'Subject Name': ['Calculus I', 'Physics I'],
            'Grade': ['A', 'B+']
        }
        df = pd.DataFrame(test_data)
        df.to_excel(tmp.name, index=False, engine='openpyxl')
        yield tmp.name
        # Clean up
        try:
            os.unlink(tmp.name)
        except:
            pass
