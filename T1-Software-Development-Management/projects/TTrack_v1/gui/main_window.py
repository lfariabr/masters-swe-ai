from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget, 
    QVBoxLayout, 
    QPushButton,
    QFileDialog, 
    QLabel, 
    QTableView, 
    QHBoxLayout, 
    QTabWidget, 
    QTableWidget, 
    QTableWidgetItem, 
    QMessageBox, 
    QProgressBar, 
    QLineEdit
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
        self.update_theme()
        
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
        self.setGeometry(100, 100, 1200, 800)

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
    
    def update_theme(self):
        """Update all theme colors based on current mode"""
        if self.is_dark_mode:
            self.setStyleSheet("""
                QMainWindow, QWidget {
                    background-color: #1e1e1e;
                    color: #ffffff;
                }
                QLabel {
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
                QPushButton:disabled {
                    background-color: #2d2d2d;
                    color: #666666;
                }
            """)
        else:
            self.setStyleSheet("""
                QMainWindow, QWidget {
                    background-color: #f5f5f5;
                    color: #333333;
                }
                QLabel {
                    color: #333333;
                }
                QTableView {
                    background-color: #ffffff;
                    color: #333333;
                    gridline-color: #dddddd;
                    border: 1px solid #cccccc;
                }
                QHeaderView::section {
                    background-color: #f0f0f0;
                    color: #333333;
                    padding: 5px;
                    border: 1px solid #dddddd;
                }
                QTabBar::tab {
                    background: #f0f0f0;
                    color: #555555;
                    padding: 8px 20px;
                    border: 1px solid #cccccc;
                    border-bottom: none;
                    border-top-left-radius: 4px;
                    border-top-right-radius: 4px;
                }
                QTabBar::tab:selected {
                    background: #ffffff;
                    color: #2c3e50;
                    border-bottom: 2px solid #27ae60;
                }
                QTabWidget::pane {
                    border: 1px solid #cccccc;
                    top: -1px;
                }
                QPushButton {
                    background-color: #f0f0f0;
                    color: #333333;
                    border: 1px solid #cccccc;
                    padding: 8px 16px;
                    border-radius: 4px;
                }
                QPushButton:hover {
                    background-color: #e0e0e0;
                }
                QPushButton:disabled {
                    background-color: #f5f5f5;
                    color: #aaaaaa;
                }
            """)
        
        # Update color variables
        self.main_color = "#2c3e50" if not self.is_dark_mode else "#ffffff"
        self.sub_color = "#555555" if not self.is_dark_mode else "#bbbbbb"
        self.credit_color = "#777777" if not self.is_dark_mode else "#999999"
        
        # Update UI elements if they exist
        if hasattr(self, 'tabs'):
            self.tabs.setStyleSheet("")
            self.tabs.setStyleSheet(self.styleSheet())
            
        # Update theme toggle button if it exists
        if hasattr(self, 'theme_toggle_btn'):
            self.theme_toggle_btn.setText("🌙" if not self.is_dark_mode else "☀️")
    
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
    
    def process_data(self):
        """Process the loaded data and display results"""
        if self.transcript_df is None or self.curriculum_df is None:
            return
        
        # Extract student info from transcript dataframe if available
        try:
            # Check if metadata columns exist - common formats for transcript data
            if 'Student Name' in self.transcript_df.columns:
                self.student_name = self.transcript_df['Student Name'].iloc[0]
            elif 'Name' in self.transcript_df.columns:
                self.student_name = self.transcript_df['Name'].iloc[0]
            else:
                self.student_name = "Student"
                
            if 'University' in self.transcript_df.columns:
                self.university = self.transcript_df['University'].iloc[0]
            elif 'Institution' in self.transcript_df.columns:
                self.university = self.transcript_df['Institution'].iloc[0]
            else:
                self.university = "Torrens University"
        except (AttributeError, IndexError, KeyError):
            # Fallback to defaults if extraction fails
            self.student_name = "Student"
            self.university = "Torrens University"
            
        print(f"Using student info: {self.student_name} @ {self.university}")
            
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
            
            # Update header labels with student info
            header_label = self.results_tab.findChild(QLabel, "header_label")
            sub_header = self.results_tab.findChild(QLabel, "sub_header")
            
            if header_label:
                header_label.setText(f"Results for {self.student_name}")
                print(f"Updated header with student name: {self.student_name}")
            
            if sub_header:
                sub_header.setText(f"@ {self.university}")
                print(f"Updated sub-header with university: {self.university}")
            
            # Update progress bar if present
            for progress_bar in self.results_tab.findChildren(QProgressBar):
                done_count = len(self.results_df[self.results_df['Status'] == 'Done'])
                total_count = len(self.results_df)
                progress = int(done_count / total_count * 100) if total_count > 0 else 0
                progress_bar.setValue(progress)
                print(f"Updated progress bar: {progress}%")
                break
                
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