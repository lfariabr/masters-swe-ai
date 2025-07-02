"""
Tests for the UI tab components.
"""
import pytest
from PyQt5.QtWidgets import QApplication, QFileDialog
from PyQt5.QtCore import Qt
from unittest.mock import patch, MagicMock

# Import the UI components to test
from ui.tab_input import setup_input_tab

class TestInputTab:
    """Test cases for the input tab functionality."""
    
    def test_input_tab_initialization(self, qtbot):
        """Test that the input tab initializes with the correct widgets."""
        from PyQt5.QtWidgets import QWidget, QPushButton
        
        # Create a parent widget with necessary attributes
        parent = MagicMock()
        parent.transcript_table = MagicMock()
        parent.curriculum_table = MagicMock()
        parent.transcript_df = None
        parent.curriculum_df = None
        parent.process_btn = MagicMock()
        
        # Import here to avoid circular imports
        from ui.tab_input import setup_input_tab
        
        # Set up the input tab
        tab = setup_input_tab(parent)
        
        # Verify tab is created
        assert tab is not None
    
    @patch('ui.tab_input.QFileDialog.getOpenFileName')
    @patch('gui.utils.load_excel_as_model')
    def test_file_loading(self, mock_load_excel, mock_file_dialog, qtbot):
        """Test file loading functionality."""
        from PyQt5.QtWidgets import QWidget, QPushButton
        
        # Setup mocks
        mock_file = "test_file.xlsx"
        mock_file_dialog.return_value = (mock_file, "Excel Files (*.xlsx)")
        mock_load_excel.return_value = MagicMock()
        
        # Create a parent widget with necessary attributes
        parent = MagicMock()
        parent.transcript_table = MagicMock()
        parent.curriculum_table = MagicMock()
        parent.transcript_df = None
        parent.curriculum_df = None
        parent.process_btn = MagicMock()
        
        # Import here to avoid circular imports
        from ui.tab_input import load_file
        
        # Test transcript loading
        load_file(parent, is_transcript=True)
        mock_file_dialog.assert_called_once()
        mock_load_excel.assert_called_once()
        parent.transcript_table.setModel.assert_called_once()
        
        # Reset mocks
        mock_file_dialog.reset_mock()
        mock_load_excel.reset_mock()
        
        # Test curriculum loading
        load_file(parent, is_transcript=False)
        mock_file_dialog.assert_called_once()
        mock_load_excel.assert_called_once()
        parent.curriculum_table.setModel.assert_called_once()

class TestResultsTabs:
    """Test cases for the results tabs."""
    
    def test_results_tab_initialization(self, qtbot):
        """Test that results tabs initialize correctly."""
        # Import here to avoid Qt import issues
        from ui.tab_results import setup_results_tab
        
        # Create a parent widget with necessary attributes
        parent = MagicMock()
        
        # Set up results tab
        results_tab = setup_results_tab(parent)
        
        # Verify tab is created
        assert results_tab is not None

# Fixture for Qt bot
@pytest.fixture
def qtbot(qapp):
    """Fixture providing a Qt bot for testing Qt applications."""
    from pytestqt.qtbot import QtBot
    return QtBot(qapp)
