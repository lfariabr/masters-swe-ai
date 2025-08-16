from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
    QLabel, QTableView, QFileDialog, QLineEdit,
    QGroupBox, QGridLayout
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
import os

def setup_input_tab(parent):
    """
    Set up the input tab with file uploads and tables
    
    Args:
        parent: The main window instance that will contain this tab
        
    Returns:
        QWidget: The configured input tab widget
    """
    # Create the main widget and layout
    tab = QWidget()
    layout = QVBoxLayout()
    layout.setSpacing(20)
    layout.setContentsMargins(30, 30, 30, 30)

    # Title Section
    title_layout = QHBoxLayout()
    title = QLabel("🎓 TTrack – Torrens Degree Tracker")
    title.setObjectName("title_label") # Add object name for identification
    title.setFont(QFont("Arial", 40, QFont.Bold))
    # Force black color in light mode, white in dark mode
    title.setStyleSheet("color: #000000; font-weight: bold; padding: 5px;" if not parent.theme_manager.is_dark_mode else "color: #ffffff; font-weight: bold; padding: 5px;")

    
    # Add theme toggle button
    theme_icon = "🌙" if not parent.theme_manager.is_dark_mode else "☀️"
    parent.theme_toggle_btn = QPushButton(theme_icon)
    parent.theme_toggle_btn.setFixedSize(50, 50)
    parent.theme_toggle_btn.setToolTip(
        "Switch to Dark Mode" if not parent.theme_manager.is_dark_mode else "Switch to Light Mode"
    )
    parent.theme_toggle_btn.setStyleSheet(f"""
        QPushButton {{
            border: 2px solid {'#2c3e50' if not parent.theme_manager.is_dark_mode else '#ffffff'};
            border-radius: 25px;
            font-size: 24px;
            background-color: {'#f0f0f0' if not parent.theme_manager.is_dark_mode else '#2d2d2d'};
            color: {'#2c3e50' if not parent.theme_manager.is_dark_mode else '#ffffff'};
            padding: 0;
            margin: 0;
        }}
        QPushButton:hover {{
            background-color: {'#e0e0e0' if not parent.theme_manager.is_dark_mode else '#3d3d3d'};
        }}
    """)
    parent.theme_toggle_btn.clicked.connect(parent.toggle_theme)
    
    # Add title and theme button to layout
    title_layout.addStretch()
    title_layout.addWidget(title)
    title_layout.addStretch()
    title_layout.addWidget(parent.theme_toggle_btn)
    
    layout.addLayout(title_layout)

    subtitle = QLabel("Built by students for academic advisors at Torrens University Australia.")
    subtitle.setObjectName("subtitle_label")
    subtitle.setStyleSheet("color: #ffffff; font-size: 16px;" if parent.theme_manager.is_dark_mode else "color: #333333; font-size: 16px;")
    subtitle.setAlignment(Qt.AlignCenter)

    credit = QLabel("Guided by Dr. Atif Qureshi – Software Development Management, 2025")
    credit.setObjectName("credit_label")
    credit.setStyleSheet("color: #dddddd; font-size: 14px; font-style: italic;" if parent.theme_manager.is_dark_mode else "color: #444444; font-size: 14px; font-style: italic;")
    credit.setAlignment(Qt.AlignCenter)

    layout.addWidget(subtitle)
    layout.addWidget(credit)
    layout.addSpacing(20)

    # Create main buttons
    from ui.helpers import set_button_style
    parent.transcript_btn = QPushButton("📄 Upload Transcript")
    parent.curriculum_btn = QPushButton("📚 Upload Curriculum")
    parent.process_btn = QPushButton("🔍 Process Data")
    
    # Style buttons
    set_button_style(parent.transcript_btn, parent.main_color, parent.theme_manager.is_dark_mode)
    set_button_style(parent.curriculum_btn, parent.main_color, parent.theme_manager.is_dark_mode)
    set_button_style(parent.process_btn, "#27ae60", parent.theme_manager.is_dark_mode)
    
    # Connect buttons
    parent.transcript_btn.clicked.connect(lambda: load_file(parent, is_transcript=True))
    parent.curriculum_btn.clicked.connect(lambda: load_file(parent, is_transcript=False))
    parent.process_btn.clicked.connect(parent.process_data)
    parent.process_btn.setEnabled(False)
    
    # Create helper buttons
    parent.sample_transcript_btn = QPushButton("🧪 Try with Sample Data")
    parent.sample_curriculum_btn = QPushButton("🧪 Try with Sample Data")
    parent.download_transcript_btn = QPushButton("📦 Download the Template")
    parent.download_curriculum_btn = QPushButton("📦 Download the Template")
    
    # Style helper buttons
    sample_button_color = "#27AE60"  # Green
    download_button_color = "#2471A3"  # Blue
    set_button_style(parent.sample_transcript_btn, sample_button_color, parent.theme_manager.is_dark_mode, smaller=True)
    set_button_style(parent.sample_curriculum_btn, sample_button_color, parent.theme_manager.is_dark_mode, smaller=True)
    set_button_style(parent.download_transcript_btn, download_button_color, parent.theme_manager.is_dark_mode, smaller=True)
    set_button_style(parent.download_curriculum_btn, download_button_color, parent.theme_manager.is_dark_mode, smaller=True)
    
    # Connect helper buttons
    ## Transcript = Student's Progress in Courses
    parent.sample_transcript_btn.clicked.connect(lambda: load_sample_file(parent, is_transcript=True))
    parent.download_transcript_btn.clicked.connect(lambda: download_sample_file(parent, is_transcript=True))

    ## Curriculum = Academic Course Requirements
    parent.sample_curriculum_btn.clicked.connect(lambda: load_sample_file_hardcoded(parent, is_transcript=False)) #TODO: load_sample_file_hardcoded
    parent.download_curriculum_btn.clicked.connect(lambda: download_sample_file(parent, is_transcript=False))
    
    # Create clear column headers
    transcript_label = QLabel("Transcript")
    transcript_label.setAlignment(Qt.AlignCenter)
    transcript_label.setStyleSheet("font-weight: bold;")
    
    curriculum_label = QLabel("Curriculum")
    curriculum_label.setAlignment(Qt.AlignCenter)
    curriculum_label.setStyleSheet("font-weight: bold;")
    
    # Create action grid layout
    action_grid = QGridLayout()
    
    # Add column headers
    action_grid.addWidget(transcript_label, 0, 0)
    action_grid.addWidget(curriculum_label, 0, 1)
    
    # Add main buttons
    action_grid.addWidget(parent.transcript_btn, 1, 0)
    action_grid.addWidget(parent.curriculum_btn, 1, 1)
    
    # Add helper buttons
    action_grid.addWidget(parent.sample_transcript_btn, 2, 0)
    action_grid.addWidget(parent.sample_curriculum_btn, 2, 1)
    
    action_grid.addWidget(parent.download_transcript_btn, 3, 0)
    action_grid.addWidget(parent.download_curriculum_btn, 3, 1)
    
    # Add process button centered at the bottom
    process_layout = QHBoxLayout()
    process_layout.addStretch()
    process_layout.addWidget(parent.process_btn)
    process_layout.addStretch()
    
    # Add layouts to main layout
    layout.addLayout(action_grid)
    layout.addSpacing(15)
    layout.addLayout(process_layout)

    # Display Section
    layout.addSpacing(15)
    tables_layout = QHBoxLayout()
    
    # Transcript Section
    transcript_group = QVBoxLayout()
    transcript_group.addWidget(QLabel("Transcript Table"))
    parent.transcript_table = QTableView()
    parent.transcript_table.setSortingEnabled(True)
    transcript_group.addWidget(parent.transcript_table)
    
    # Curriculum Section
    curriculum_group = QVBoxLayout()
    curriculum_group.addWidget(QLabel("Curriculum Table"))
    parent.curriculum_table = QTableView()
    parent.curriculum_table.setSortingEnabled(True)
    curriculum_group.addWidget(parent.curriculum_table)
    
    # Add tables to layout
    tables_layout.addLayout(transcript_group, 1)
    tables_layout.addLayout(curriculum_group, 1)
    
    # Add to main layout
    layout.addLayout(tables_layout, 1)
    tab.setLayout(layout)
    
    return tab

def load_file(parent, is_transcript=True):
    """
    Handle file loading for both transcript and curriculum
    
    Args:
        parent: The main window instance
        is_transcript: Boolean indicating if loading transcript (True) or curriculum (False)
    """
    file_type = "Transcript" if is_transcript else "Curriculum"
    file_path, _ = QFileDialog.getOpenFileName(
        parent, f"Open {file_type}", "", "Excel Files (*.xlsx)")
        
    if file_path:
        from gui.utils import load_excel_as_model
        model = load_excel_as_model(file_path)
        
        if is_transcript:
            parent.transcript_table.setModel(model)
            parent.data_processor.set_transcript_data(parent.helpers.model_to_dataframe(model))
        else:
            parent.curriculum_table.setModel(model)
            parent.data_processor.set_curriculum_data(parent.helpers.model_to_dataframe(model))
            
        # Enable process button if both files are loaded
        if parent.data_processor.transcript_df is not None and parent.data_processor.curriculum_df is not None:
            parent.process_btn.setEnabled(True)


def load_sample_file(parent, is_transcript=True):
    """
    Load sample data files for transcript or curriculum
    
    Args:
        parent: The main window instance
        is_transcript: Boolean indicating if loading transcript (True) or curriculum (False)
    """
    # Get base directory path
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # Define the sample file path based on type
    file_name = "sample_academic_transcript_v2.xlsx" if is_transcript else "sample_prescribed_curriculum_v2.xlsx"
    file_path = os.path.join(base_dir, "services/data", file_name)
    
    # Check if file exists
    if not os.path.exists(file_path):
        from PyQt5.QtWidgets import QMessageBox
        QMessageBox.warning(parent, "File Not Found", 
                           f"Sample {('transcript' if is_transcript else 'curriculum')} file not found at {file_path}")
        return
    
    # Load the sample file
    try:
        from gui.utils import load_excel_as_model
        model = load_excel_as_model(file_path)
        
        if is_transcript:
            parent.transcript_table.setModel(model)
            parent.data_processor.set_transcript_data(parent.helpers.model_to_dataframe(model))
            parent.statusBar().showMessage(f"Loaded sample transcript from {file_name}", 3000)
        else:
            parent.curriculum_table.setModel(model)
            parent.data_processor.set_curriculum_data(parent.helpers.model_to_dataframe(model))
            parent.statusBar().showMessage(f"Loaded sample curriculum from {file_name}", 3000)
        
        # Enable process button if both files are loaded
        if parent.data_processor.transcript_df is not None and parent.data_processor.curriculum_df is not None:
            parent.process_btn.setEnabled(True)
            
    except Exception as e:
        from PyQt5.QtWidgets import QMessageBox
        QMessageBox.critical(parent, "Error Loading Sample Data", 
                           f"Error loading sample {('transcript' if is_transcript else 'curriculum')}:\n{str(e)}")

def load_sample_file_hardcoded(parent, is_transcript=True):
    """
    This will be responsible to load the hardcoded sample course structure when the user clicks on the "Try with Sample Data" button
    """
    # Import course data loader
    from gui.utils import load_as_model_hardcoded
    model = load_as_model_hardcoded(is_transcript=is_transcript)
    
    if is_transcript:
        parent.transcript_table.setModel(model)
        parent.data_processor.set_transcript_data(parent.helpers.model_to_dataframe(model))
        parent.statusBar().showMessage(f"Loaded sample transcript from hardcoded data", 3000)
    else:
        parent.curriculum_table.setModel(model)
        parent.data_processor.set_curriculum_data(parent.helpers.model_to_dataframe(model))
        parent.statusBar().showMessage(f"Loaded sample curriculum from hardcoded data", 3000)
    
    # Enable Process when both are present
    if parent.data_processor.transcript_df is not None and parent.data_processor.curriculum_df is not None:
        parent.process_btn.setEnabled(True)

def download_sample_file(parent, is_transcript=True):
    """
    Download sample data files for transcript or curriculum to user-specified location
    
    Args:
        parent: The main window instance
        is_transcript: Boolean indicating if downloading transcript (True) or curriculum (False)
    """
    # Get base directory path
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # Define the sample file path based on type
    file_name = "sample_academic_transcript_v2.xlsx" if is_transcript else "sample_prescribed_curriculum_v2.xlsx"
    file_path = os.path.join(base_dir, "services/data", file_name)
    
    # Check if file exists
    if not os.path.exists(file_path):
        from PyQt5.QtWidgets import QMessageBox
        QMessageBox.warning(parent, "File Not Found", 
                          f"Sample {('transcript' if is_transcript else 'curriculum')} file not found at {file_path}")
        return
    
    # Ask user where to save the file
    file_type = "Transcript" if is_transcript else "Curriculum"
    from PyQt5.QtWidgets import QFileDialog
    save_path, _ = QFileDialog.getSaveFileName(
        parent, 
        f"Save {file_type} Template", 
        file_name,
        "Excel Files (*.xlsx)"
    )
    
    if save_path:
        try:
            # Use shutil to copy the file
            import shutil
            shutil.copy2(file_path, save_path)
            parent.statusBar().showMessage(f"Downloaded {file_type} template to {save_path}", 3000)
        except Exception as e:
            from PyQt5.QtWidgets import QMessageBox
            QMessageBox.critical(parent, "Error Saving File", 
                              f"Error saving {file_type} template: {str(e)}")