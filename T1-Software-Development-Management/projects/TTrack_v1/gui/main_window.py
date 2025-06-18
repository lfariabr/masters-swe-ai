from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QPushButton,
    QFileDialog, QLabel, QTableView, QHBoxLayout, QTabWidget, QTableWidget, QTableWidgetItem, QMessageBox
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from resolvers.engine import match_transcript_with_curriculum, generate_progress_summary, suggest_electives

# Import UI modules
from ui.tab_input import setup_input_tab
from ui.tab_results import setup_results_tab
from ui import helpers

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Initialize theme
        self.is_dark_mode = self.check_dark_mode()
        self.main_color = "#2c3e50" if not self.is_dark_mode else "#ffffff"
        self.sub_color = "#555555" if not self.is_dark_mode else "#bbbbbb"
        self.credit_color = "#777777" if not self.is_dark_mode else "#999999"
        
        # Store dataframes
        self.transcript_df = None
        self.curriculum_df = None
        self.results_df = None
        
        # Store helpers
        self.helpers = helpers
        
        # Initialize UI
        self.init_ui()
    
    def init_ui(self):
        """Initialize the main UI components"""
        self.setWindowTitle("TTrack – Degree Tracker")
        self.setGeometry(100, 100, 1100, 700)

        # Create tab widget
        self.tabs = QTabWidget()
        
        # Create and add tabs
        self.input_tab = setup_input_tab(self)
        self.results_tab = setup_results_tab(self)
        
        # Add tabs to the tab widget
        self.tabs.addTab(self.input_tab, "Input")
        self.tabs.addTab(self.results_tab, "Results")
        
        # Initially disable results tab
        self.tabs.setTabEnabled(1, False)
        
        # Set central widget
        self.setCentralWidget(self.tabs)
    
    def check_dark_mode(self):
        """Check if system is in dark mode"""
        from PyQt5.QtGui import QGuiApplication
        from PyQt5.QtCore import QSettings
        
        # Try to get system dark mode setting
        try:
            settings = QSettings()
            return settings.value("darkMode", False, type=bool)
        except:
            # Fallback to checking system palette
            palette = QGuiApplication.palette()
            return palette.window().color().lightness() < 128
    
    def process_data(self):
        """Process the loaded data and display results"""
        if self.transcript_df is None or self.curriculum_df is None:
            return
            
        try:
            # Process the data using engine functions
            self.results_df = match_transcript_with_curriculum(
                self.transcript_df, self.curriculum_df)
            summary_df = generate_progress_summary(self.results_df)
            electives_df = suggest_electives(self.results_df)
            
            # Populate tables using helpers
            self.helpers.populate_table(self.results_table, self.results_df)
            self.helpers.populate_table(self.summary_table, summary_df)
            self.helpers.populate_table(self.electives_table, electives_df)
            
            # Enable and switch to results tab
            self.tabs.setTabEnabled(1, True)
            self.tabs.setCurrentIndex(1)
            
        except Exception as e:
            QMessageBox.critical(
                self, 
                "Error", 
                f"Failed to process data: {str(e)}\n\nPlease ensure your files are in the correct format."
            )
            raise