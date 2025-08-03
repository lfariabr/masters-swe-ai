from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QSettings


class ThemeManager:
    """
    Manages application theming, including dark/light mode toggles and style application.
    """
    
    def __init__(self, parent):
        """
        Initialize the theme manager
        
        Args:
            parent: The main window instance this manager is attached to
        """
        self.parent = parent
        self.is_dark_mode = self.detect_system_theme()
        self.main_color = "#4ecdc4"  # Teal color for accent elements
        self.update_theme()
        
    def detect_system_theme(self):
        """
        Detect if the system is using dark mode
        
        Returns:
            bool: True if system is in dark mode, False otherwise
        """
        # For now, always default to light mode to match the OS
        # This ensures text visibility while we debug the actual issue
        return False
            
    def check_dark_mode(self):
        """
        Check if current mode is dark mode
        
        Returns:
            bool: Current dark mode state
        """
        return self.is_dark_mode
            
    def update_theme(self):
        """Update all theme colors based on current mode"""
        if self.is_dark_mode:
            self.parent.setStyleSheet("""
                QMainWindow, QWidget {
                    background-color: #1e1e1e;
                    color: #ffffff;
                }
                QTableView {
                    background-color: #2d2d2d;
                    color: #ffffff;
                    gridline-color: #3e3e3e;
                    border: 1px solid #3e3e3e;
                }
                QHeaderView::section {
                    background-color: #2d2d2d;
                    color: #ffffff;
                    padding: 5px;
                    border: 1px solid #3e3e3e;
                }
                QTabBar::tab {
                    background: #2d2d2d;
                    color: #aaaaaa;
                    padding: 8px 20px;
                    border: 1px solid #3e3e3e;
                    border-bottom: none;
                    border-top-left-radius: 4px;
                    border-top-right-radius: 4px;
                }
                QTabBar::tab:selected {
                    background: #1e1e1e;
                    color: #ffffff;
                    border-bottom: 2px solid #27ae60;
                }
                QTabWidget::pane {
                    border: 1px solid #3e3e3e;
                    top: -1px;
                }
                QPushButton {
                    background-color: #2d2d2d;
                    color: #ffffff;
                    border: 1px solid #3e3e3e;
                    padding: 8px 16px;
                    border-radius: 4px;
                }
                QPushButton:hover {
                    background-color: #3d3d3d;
                }
                QPushButton:pressed {
                    background-color: #4d4d4d;
                }
                QPushButton:disabled {
                    background-color: #2d2d2d;
                    color: #777777;
                    border: 1px solid #3e3e3e;
                }
                QLineEdit {
                    background-color: #2d2d2d;
                    color: #ffffff;
                    border: 1px solid #3e3e3e;
                    padding: 5px;
                    border-radius: 2px;
                }
                QProgressBar {
                    border: none;
                    border-radius: 10px;
                    text-align: center;
                    background: #444444;
                    height: 8px;
                }
                QProgressBar::chunk {
                    background-color: #4ecdc4;
                    border-radius: 10px;
                }
            """)
        else:
            self.parent.setStyleSheet("""
                QMainWindow, QWidget {
                    background-color: #ffffff;
                    color: #333333;
                }
                QTableView {
                    background-color: #fafafa;
                    color: #333333;
                    gridline-color: #dddddd;
                    border: 1px solid #dddddd;
                }
                QHeaderView::section {
                    background-color: #f0f0f0;
                    color: #333333;
                    padding: 5px;
                    border: 1px solid #dddddd;
                }
                QTabBar::tab {
                    background: #f0f0f0;
                    color: #777777;
                    padding: 8px 20px;
                    border: 1px solid #dddddd;
                    border-bottom: none;
                    border-top-left-radius: 4px;
                    border-top-right-radius: 4px;
                }
                QTabBar::tab:selected {
                    background: #ffffff;
                    color: #333333;
                    border-bottom: 2px solid #27ae60;
                }
                QTabWidget::pane {
                    border: 1px solid #dddddd;
                    top: -1px;
                }
                QPushButton {
                    background-color: #f0f0f0;
                    color: #333333;
                    border: 1px solid #dddddd;
                    padding: 8px 16px;
                    border-radius: 4px;
                }
                QPushButton:hover {
                    background-color: #e0e0e0;
                }
                QPushButton:pressed {
                    background-color: #d0d0d0;
                }
                QPushButton:disabled {
                    background-color: #f0f0f0;
                    color: #aaaaaa;
                    border: 1px solid #dddddd;
                }
                QLineEdit {
                    background-color: #fafafa;
                    color: #333333;
                    border: 1px solid #dddddd;
                    padding: 5px;
                    border-radius: 2px;
                }
                QProgressBar {
                    border: none;
                    border-radius: 10px;
                    text-align: center;
                    background: #e9ecef;
                    height: 8px;
                }
                QProgressBar::chunk {
                    background-color: #2a9d8f;
                    border-radius: 10px;
                }
            """)
        
        # Update UI elements if they exist
        if hasattr(self.parent, 'tabs'):
            self.parent.tabs.setStyleSheet("")
            self.parent.tabs.setStyleSheet(self.parent.styleSheet())
            
        # Update theme toggle button if it exists
        if hasattr(self.parent, 'theme_toggle_btn'):
            self.parent.theme_toggle_btn.setText("🌙" if not self.is_dark_mode else "☀️")
    
    def toggle_theme(self):
        """Toggle between light and dark theme"""
        self.is_dark_mode = not self.is_dark_mode
        self.update_theme()
        
        # Save the preference
        try:
            settings = QSettings()
            settings.setValue("darkMode", self.is_dark_mode)
        except:
            pass  # If settings can't be saved, continue with in-memory toggle
