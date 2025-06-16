from PyQt5.QtWidgets import (QMainWindow, QLabel, QVBoxLayout, QHBoxLayout, 
                             QWidget, QTabWidget, QStatusBar, QMenuBar, QMenu, 
                             QAction, QToolBar, QMessageBox)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon

from data_loader.curriculum_loader import CurriculumLoader
from data_loader.transcript_loader import TranscriptLoader
from gui.upload_widget import UploadWidget
from gui.widgets.progress_widget import ProgressWidget
from analysis.progress_analyzer import ProgressAnalyzer

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("TTrack – Smart Subject Requirement Checker")
        self.setMinimumSize(1000, 700)
        
        # Initialize application state
        self.transcript_path = None
        self.curriculum_path = None
        self.progress_widget = None
        
        self.init_ui()
        self.create_actions()
        self.create_menus()
        self.create_toolbar()
        self.create_statusbar()
    
    def init_ui(self):
        """Initialize the main UI components."""
        # Create central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(10, 10, 10, 10)
        
        # Create tab widget for different views
        self.tabs = QTabWidget()
        main_layout.addWidget(self.tabs)
        
        # Add upload widget to the first tab
        self.upload_widget = UploadWidget()
        self.tabs.addTab(self.upload_widget, "Upload Files")
        
        # Add progress widget (initially disabled)
        self.progress_widget = ProgressWidget()
        self.tabs.addTab(self.progress_widget, "Progress")
        self.tabs.setTabEnabled(1, False)  # Disable progress tab initially
        
        # Connect signals
        self.upload_widget.transcript_uploaded.connect(self.on_transcript_uploaded)
        self.upload_widget.curriculum_uploaded.connect(self.on_curriculum_uploaded)
    
    def create_actions(self):
        """Create actions for menus and toolbars."""
        # File actions
        self.new_action = QAction("&New", self)
        self.new_action.setShortcut("Ctrl+N")
        self.new_action.triggered.connect(self.new_file)
        
        self.open_action = QAction("&Open...", self)
        self.open_action.setShortcut("Ctrl+O")
        self.open_action.triggered.connect(self.open_file)
        
        self.exit_action = QAction("E&xit", self)
        self.exit_action.setShortcut("Ctrl+Q")
        self.exit_action.triggered.connect(self.close)
        
        # Help actions
        self.about_action = QAction("&About", self)
        self.about_action.triggered.connect(self.show_about)
    
    def create_menus(self):
        """Create the menu bar."""
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu("&File")
        file_menu.addAction(self.new_action)
        file_menu.addAction(self.open_action)
        file_menu.addSeparator()
        file_menu.addAction(self.exit_action)
        
        # Help menu
        help_menu = menubar.addMenu("&Help")
        help_menu.addAction(self.about_action)
    
    def create_toolbar(self):
        """Create the main toolbar."""
        toolbar = QToolBar("Main Toolbar")
        self.addToolBar(toolbar)
        
        toolbar.addAction(self.new_action)
        toolbar.addAction(self.open_action)
        toolbar.addSeparator()
    
    def create_statusbar(self):
        """Create the status bar."""
        self.statusBar().showMessage("Ready")
    
    def on_transcript_uploaded(self, path):
        """Handle transcript file upload."""
        self.transcript_path = path
        self.statusBar().showMessage(f"Transcript loaded: {path}", 3000)
        self.process_uploaded_files()
    
    def on_curriculum_uploaded(self, path):
        """Handle curriculum file upload."""
        self.curriculum_path = path
        self.statusBar().showMessage(f"Curriculum loaded: {path}", 3000)
        self.process_uploaded_files()
    
    def process_uploaded_files(self):
        """Process both uploaded files when ready."""
        if not self.transcript_path or not self.curriculum_path:
            return  # Wait for both files
        
        try:
            # Show loading message
            self.statusBar().showMessage("Processing files...")
            
            # Load and process files
            curriculum = CurriculumLoader.load(self.curriculum_path)
            academic_record = TranscriptLoader.load(self.transcript_path)
            
            # Analyze progress
            analyzer = ProgressAnalyzer(curriculum, academic_record)
            progress_result = analyzer.analyze_progress()
            
            # Update progress widget
            self.progress_widget.update_progress(progress_result)
            
            # Enable and switch to progress tab
            self.tabs.setTabEnabled(1, True)
            self.tabs.setCurrentIndex(1)
            
            self.statusBar().showMessage("Analysis complete!", 3000)
            
        except Exception as e:
            QMessageBox.critical(
                self,
                "Error",
                f"Failed to process files: {str(e)}\n\nPlease ensure you've selected valid files."
            )
            self.statusBar().showMessage("Error processing files", 3000)
    
    def new_file(self):
        """Handle new file action."""
        # Reset the application state
        self.transcript_path = None
        self.curriculum_path = None
        self.upload_widget.reset()
        self.tabs.setTabEnabled(1, False)  # Disable progress tab
        self.tabs.setCurrentIndex(0)  # Switch to upload tab
        self.statusBar().showMessage("New session started", 2000)
    
    def open_file(self):
        """Handle open file action."""
        # TODO: Implement file opening logic
        pass
    
    def show_about(self):
        """Show about dialog."""
        QMessageBox.about(self, "About TTrack",
                        "<b>TTrack - Smart Subject Requirement Checker</b><br><br>"
                        "Version: 1.0.0<br>"
                        "A tool for tracking and validating subject requirements.<br><br>"
                        " 2025 SDM Group Project<br>"
                        "Prof. Dr. Atif")
    
    def closeEvent(self, event):
        """Handle window close event."""
        # Add any cleanup or save confirmation here
        reply = QMessageBox.question(
            self, 'Exit',
            'Are you sure you want to exit?',
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()
