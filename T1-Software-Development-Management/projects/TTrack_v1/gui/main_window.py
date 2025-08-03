from PyQt5.QtWidgets import QMainWindow, QMessageBox, QTableWidget, QLabel, QProgressBar
from PyQt5.QtCore import Qt

from ui import helpers
from services.database import DatabaseManager
from core.data_processor import DataProcessor
from controllers.theme_manager import ThemeManager
from controllers.tab_controller import TabController

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Main color scheme
        self.main_color = "#4ecdc4"  # Teal color for accent elements
        
        # Store helpers
        self.helpers = helpers
        
        # Initialize component managers
        self.theme_manager = ThemeManager(self)
        self.tab_controller = TabController(self)
        self.data_processor = DataProcessor(self)
        self.database_manager = DatabaseManager(self)
        
        # Initialize UI
        self.init_ui()
    
    def init_ui(self):
        """Initialize the main UI components"""
        self.setWindowTitle("TTrack – Degree Tracker")
        self.setGeometry(100, 100, 1200, 800)

        # Initialize tabs through the tab controller
        self.tabs = self.tab_controller.initialize_tabs()
        
        # Store references to UI elements for easier access
        self.input_tab = self.tab_controller.get_input_tab()
        self.results_tab = self.tab_controller.get_results_tab()
        self.login_tab = self.tab_controller.get_login_tab()
        
        # Set up the required tables
        self.results_table = self.results_tab.findChild(QTableWidget)
        self.summary_table = self.results_tab.findChildren(QTableWidget)[1] if len(self.results_tab.findChildren(QTableWidget)) > 1 else None
        self.electives_table = self.results_tab.findChildren(QTableWidget)[2] if len(self.results_tab.findChildren(QTableWidget)) > 2 else None
        
        # Set central widget
        self.setCentralWidget(self.tabs)
    
    @property
    def is_dark_mode(self):
        """Property to get dark mode status from theme manager"""
        return self.theme_manager.is_dark_mode
    
    def update_theme(self):
        """Update all theme colors based on current mode"""
        # Delegate to theme manager
        self.theme_manager.update_theme()
    
    def toggle_theme(self):
        """Toggle between dark and light mode"""
        self.theme_manager.toggle_theme()
        
        # Force update text colors in input tab for all labeled elements
        title = self.input_tab.findChild(QLabel, "title_label")
        subtitle = self.input_tab.findChild(QLabel, "subtitle_label")
        credit = self.input_tab.findChild(QLabel, "credit_label")
        
        # Update title text color
        if title:
            title.setStyleSheet("color: #000000; font-weight: bold; padding: 5px;" if not self.theme_manager.is_dark_mode else "color: #ffffff; font-weight: bold; padding: 5px;")
        
        # Update subtitle text color
        if subtitle:
            subtitle.setStyleSheet("color: #333333; font-size: 13px;" if not self.theme_manager.is_dark_mode else "color: #ffffff; font-size: 13px;")
            
        # Update credit text color
        if credit:
            credit.setStyleSheet("color: #444444; font-size: 11px; font-style: italic;" if not self.theme_manager.is_dark_mode else "color: #dddddd; font-size: 11px; font-style: italic;")
        
        # Update results tab elements
        if hasattr(self, 'results_tab'):
            # Update header and subheader
            if hasattr(self, 'header_label'):
                self.header_label.setStyleSheet("""
                    font-size: 22px; 
                    font-weight: bold; 
                    color: %s;
                    margin-bottom: 4px;
                """ % ('#4ecdc4' if self.theme_manager.is_dark_mode else '#1a7d6f'))
            
            if hasattr(self, 'sub_header'):
                self.sub_header.setStyleSheet("""
                    font-size: 14px;
                    color: %s;
                    margin-bottom: 15px;
                """ % ('#ffffff' if self.theme_manager.is_dark_mode else '#333333'))
            
            # Update progress label
            progress_label = self.results_tab.findChild(QLabel, "progress_label")
            if progress_label:
                progress_label.setStyleSheet(
                    "color: %s; font-size: 12px;" % ('#dddddd' if self.theme_manager.is_dark_mode else '#444444')
                )
    
    def process_data(self):
        """Process the loaded data and display results"""
        # Delegate to data processor
        success = self.data_processor.process_data()
        
        # Enable results tab if processing was successful
        if success:
            self.tab_controller.enable_results_tab()

    def _save_to_database(self):
        """
        Save processed session data to database (triggered from UI)
        """
        from PyQt5.QtWidgets import QMessageBox
        
        # Check if data is available
        if not hasattr(self.data_processor, 'results_df') or self.data_processor.results_df is None:
            QMessageBox.warning(self, "No Data", "No processed data to save. Please process data first.")
            return
        
        # Delegate to DataProcessor
        success = self.data_processor.save_session_to_database()
        
        if success:
            QMessageBox.information(
                self,
                "Data Saved",
                f"Processed data saved successfully!"
            )
        else:
            QMessageBox.warning(self, "Save Failed", "Failed to save session data to database.")