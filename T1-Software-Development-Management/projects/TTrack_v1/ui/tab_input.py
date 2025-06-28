from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QLabel, QTableView, QFileDialog, QLineEdit
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

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
    title.setFont(QFont("Arial", 20, QFont.Bold))
    title.setStyleSheet(f"color: {'#ffffff' if parent.is_dark_mode else '#2c3e50'};")
    
    # Add theme toggle button
    theme_icon = "🌙" if not parent.is_dark_mode else "☀️"
    parent.theme_toggle_btn = QPushButton(theme_icon)
    parent.theme_toggle_btn.setFixedSize(50, 50)
    parent.theme_toggle_btn.setToolTip(
        "Switch to Dark Mode" if not parent.is_dark_mode else "Switch to Light Mode"
    )
    parent.theme_toggle_btn.setStyleSheet(f"""
        QPushButton {{
            border: 2px solid {'#2c3e50' if not parent.is_dark_mode else '#ffffff'};
            border-radius: 25px;
            font-size: 24px;
            background-color: {'#f0f0f0' if not parent.is_dark_mode else '#2d2d2d'};
            color: {'#2c3e50' if not parent.is_dark_mode else '#ffffff'};
            padding: 0;
            margin: 0;
        }}
        QPushButton:hover {{
            background-color: {'#e0e0e0' if not parent.is_dark_mode else '#3d3d3d'};
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
    subtitle.setStyleSheet(f"color: {'#bbbbbb' if parent.is_dark_mode else '#555555'}; font-size: 13px;")
    subtitle.setAlignment(Qt.AlignCenter)

    credit = QLabel("Guided by Dr. Atif Qureshi – Software Development Management, 2025")
    credit.setStyleSheet(f"color: {'#999999' if parent.is_dark_mode else '#777777'}; font-size: 11px; font-style: italic;")
    credit.setAlignment(Qt.AlignCenter)

    layout.addWidget(subtitle)
    layout.addWidget(credit)
    layout.addSpacing(20)

    # Upload Section
    button_layout = QHBoxLayout()
    
    # Create buttons
    parent.transcript_btn = QPushButton("📄 Upload Transcript")
    parent.curriculum_btn = QPushButton("📚 Upload Curriculum")
    parent.process_btn = QPushButton("🔍 Process Data")
    
    # Connect signals
    parent.transcript_btn.clicked.connect(lambda: load_file(parent, is_transcript=True))
    parent.curriculum_btn.clicked.connect(lambda: load_file(parent, is_transcript=False))
    parent.process_btn.clicked.connect(parent.process_data)
    parent.process_btn.setEnabled(False)
    
    # Style buttons
    from .helpers import set_button_style
    set_button_style(parent.transcript_btn, parent.main_color, parent.is_dark_mode)
    set_button_style(parent.curriculum_btn, parent.main_color, parent.is_dark_mode)
    set_button_style(parent.process_btn, "#27ae60", parent.is_dark_mode)
    
    # Add buttons to layout
    button_layout.addWidget(parent.transcript_btn)
    button_layout.addWidget(parent.curriculum_btn)
    button_layout.addStretch()
    button_layout.addWidget(parent.process_btn)
    layout.addLayout(button_layout)

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
            parent.transcript_df = parent.helpers.model_to_dataframe(model)
        else:
            parent.curriculum_table.setModel(model)
            parent.curriculum_df = parent.helpers.model_to_dataframe(model)
            
        # Enable process button if both files are loaded
        if parent.transcript_df is not None and parent.curriculum_df is not None:
            parent.process_btn.setEnabled(True)