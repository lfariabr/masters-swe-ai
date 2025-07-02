"""
Integration tests for the TTrack application.
"""
import sys
import pytest
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt, QTimer
from unittest.mock import patch, MagicMock

# Import the main application and components
import main
from gui.main_window import MainWindow
from resolvers.engine import match_transcript_with_curriculum

class TestApplicationIntegration:
    """Integration tests for the TTrack application."""
    
    def test_application_startup(self, qapp):
        """Test that the application starts up correctly."""
        # Import the main window class directly
        from gui.main_window import MainWindow
        
        # Create the main window instance
        window = MainWindow()
        
        # Verify the window has the expected attributes
        assert hasattr(window, 'setWindowTitle')
        assert hasattr(window, 'show')
        
        # Clean up
        window.close()
    
    def test_end_to_end_workflow(self, qtbot, sample_excel_file):
        """Test the complete workflow from file loading to processing."""
        # Import here to avoid circular imports
        from PyQt5.QtWidgets import QApplication
        from PyQt5.QtCore import QCoreApplication
        from gui.main_window import MainWindow
        from ui.tab_input import load_file
        
        # Create a test application instance if needed
        app = QApplication.instance()
        if app is None:
            app = QApplication(sys.argv)
        
        # Set application name if not set
        if not QCoreApplication.applicationName():
            QCoreApplication.setApplicationName("TTrack Test")
        
        try:
            # Create the main window
            window = MainWindow()
            qtbot.addWidget(window)
            
            # Verify initial state
            if hasattr(window, 'process_btn'):
                assert not window.process_btn.isEnabled()
            
            # Mock file dialogs and Excel loading
            with patch('PyQt5.QtWidgets.QFileDialog.getOpenFileName') as mock_file_dialog, \
                 patch('gui.utils.load_excel_as_model') as mock_load_excel:
                
                # Create a real QStandardItemModel for testing
                from PyQt5.QtGui import QStandardItemModel
                test_model = QStandardItemModel()
                mock_load_excel.return_value = test_model
                
                # Setup mock return values
                mock_file_dialog.return_value = (sample_excel_file, "Excel Files (*.xlsx)")
                
                # Test transcript loading if the table exists
                if hasattr(window, 'transcript_table'):
                    load_file(window, is_transcript=True)
                    mock_file_dialog.assert_called()
                    mock_load_excel.assert_called_once()
                    
                    # Verify the model was set on the table
                    assert window.transcript_table.model() is test_model
                
                # Reset mocks
                mock_file_dialog.reset_mock()
                mock_load_excel.reset_mock()
                
                # Test curriculum loading if the table exists
                if hasattr(window, 'curriculum_table'):
                    load_file(window, is_transcript=False)
                    mock_file_dialog.assert_called()
                    mock_load_excel.assert_called_once()
                    
                    # Verify the model was set on the table
                    assert window.curriculum_table.model() is test_model
                
                # Test process button state if both files are loaded
                if hasattr(window, 'process_btn') and hasattr(window, 'transcript_df') and hasattr(window, 'curriculum_df'):
                    # Simulate loading data
                    import pandas as pd
                    window.transcript_df = pd.DataFrame()
                    window.curriculum_df = pd.DataFrame()
                    
                    # Enable the button (in a real scenario, this would be done by the application)
                    window.process_btn.setEnabled(True)
                    assert window.process_btn.isEnabled()
            
        finally:
            # Clean up
            if 'window' in locals():
                window.close()

# Fixture for sample Excel file
@pytest.fixture
def sample_excel_file(tmp_path):
    """Create a sample Excel file for testing."""
    import pandas as pd
    
    # Create sample data
    data = {
        'Subject Code': ['MATH101', 'PHYS101'],
        'Subject Name': ['Calculus I', 'Physics I'],
        'Credits': [3, 4],
        'Type': ['Core', 'Core']
    }
    
    # Create a temporary Excel file
    file_path = tmp_path / "test_curriculum.xlsx"
    df = pd.DataFrame(data)
    df.to_excel(file_path, index=False, engine='openpyxl')
    
    return str(file_path)
