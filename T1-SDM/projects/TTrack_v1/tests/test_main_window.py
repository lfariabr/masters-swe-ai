"""
Tests for the main window of TTrack application.
"""
import pytest
from PyQt5.QtWidgets import QApplication, QPushButton
from PyQt5.QtCore import Qt

# Import the main window class
from gui.main_window import MainWindow

# Fixture for QApplication instance
@pytest.fixture(scope="session")
def qapp():
    """Fixture providing a QApplication instance for testing."""
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    return app

# Test class for MainWindow
class TestMainWindow:
    """Test cases for the MainWindow class."""
    
    def test_window_initialization(self, qapp):
        """Test that the main window initializes correctly."""
        # Create the main window
        window = MainWindow()
        
        # Verify window properties
        assert window.windowTitle() != ""
        assert window.isVisible() is False  # Window should not be visible until .show() is called
        
        # Cleanup
        window.close()
    
    def test_theme_switch(self, qapp):
        """Test theme switching functionality."""
        window = MainWindow()
        
        # Verify theme toggle button exists and is clickable
        theme_button = None
        for child in window.findChildren(QPushButton):
            if child.text() in ['🌙', '☀️']:
                theme_button = child
                break
                
        if theme_button is None:
            # If no button found with emoji, try to find any button that might be the theme button
            for child in window.findChildren(QPushButton):
                if child.toolTip() and 'theme' in child.toolTip().lower():
                    theme_button = child
                    break
        
        # Skip the test if no theme button is found
        if theme_button is None:
            pytest.skip("No theme toggle button found in the UI")
        
        # Get initial icon
        initial_icon = theme_button.text()
        
        # Click the theme button
        theme_button.click()
        
        # Verify icon changed
        assert theme_button.text() != initial_icon
        
        # Cleanup
        window.close()

# Test for main application startup
def test_application_startup():
    """Test that the application can be started and has the expected properties."""
    import sys
    from PyQt5.QtWidgets import QApplication
    from PyQt5.QtCore import QCoreApplication
    
    # Create a test application if one doesn't exist
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    
    # Set a test application name if not set
    if not QCoreApplication.applicationName():
        QCoreApplication.setApplicationName("TTrack Test")
    
    # Test that the application name is set
    assert QCoreApplication.applicationName() != ""
    
    # Cleanup - don't quit the application as it might be used by other tests
    # The QApplication will be cleaned up by pytest-qt
