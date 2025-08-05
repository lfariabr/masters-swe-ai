# ui/tab_results.py
from PyQt5.QtWidgets import (
    QVBoxLayout,
    QHBoxLayout,
    QTableWidget,
    QWidget,
    QLabel,
    QFrame,
    QProgressBar,
    QPushButton
)
from core.data_processor import DataProcessor
from services.database import DatabaseManager

def setup_results_tab(parent):
    """
    Set up the results tab with tables for different result views
    
    Args:
        parent: The main window instance that will contain this tab
        
    Returns:
        QWidget: The configured results tab widget
    """
    # Main widget + layout
    tab = QWidget()
    layout = QVBoxLayout()
    layout.setSpacing(20)
    layout.setContentsMargins(30, 30, 30, 30)
    
    ## 1. Results Table
    parent.results_table = QTableWidget()
    parent.results_table.setColumnCount(4)
    parent.results_table.setHorizontalHeaderLabels(
        ["Subject Code", "Subject Name", "Type", "Status"]
    )
    parent.results_table.setSortingEnabled(True)
    
    ## 2. Summary Table
    parent.summary_table = QTableWidget()
    parent.summary_table.setSortingEnabled(True)
    
    ## 3. Electives Table
    parent.electives_table = QTableWidget()
    parent.electives_table.setColumnCount(4)
    parent.electives_table.setHorizontalHeaderLabels(
        ["Subject Code", "Subject Name", "Type", "Status"]
    )
    parent.electives_table.setSortingEnabled(True)

    # Header with student info
    header_container = QWidget()
    header_layout = QVBoxLayout(header_container)
    header_layout.setContentsMargins(0, 0, 0, 20)

    # Replace local labels with parent attributes
    parent.header_label = QLabel("")
    parent.header_label.setObjectName("header_label")
    # Use direct conditional styling for header label
    parent.header_label.setStyleSheet("""
        font-size: 22px; 
        font-weight: bold; 
        color: %s;
        margin-bottom: 4px;
    """ % ('#4ecdc4' if parent.theme_manager.is_dark_mode else '#1a7d6f'))

    parent.sub_header = QLabel("")
    parent.sub_header.setObjectName("sub_header")
    # Use direct conditional styling with proper contrasting colors
    parent.sub_header.setStyleSheet("""
        font-size: 14px;
        color: %s;
        margin-bottom: 15px;
    """ % ('#ffffff' if parent.theme_manager.is_dark_mode else '#333333'))

    # Progress indicator
    progress_container = QWidget()
    progress_layout = QHBoxLayout(progress_container)
    progress_layout.setContentsMargins(0, 0, 0, 0)

    parent.progress_bar = QProgressBar()
    parent.progress_bar.setValue(0)
    parent.progress_bar.setStyleSheet(f"""
        QProgressBar {{
            border: none;
            border-radius: 10px;
            text-align: center;
            background: {'#444444' if parent.theme_manager.is_dark_mode else '#e9ecef'};
            height: 8px;
        }}
        QProgressBar::chunk {{
            background-color: {'#4ecdc4' if parent.theme_manager.is_dark_mode else '#2a9d8f'};
            border-radius: 10px;
        }}
    """)

    progress_label = QLabel("Degree Progress")
    progress_label.setObjectName("progress_label") # Add object name for identification
    progress_label.setStyleSheet(
        "color: %s; font-size: 12px;" % ('#dddddd' if parent.theme_manager.is_dark_mode else '#444444')
    )

    progress_layout.addWidget(progress_label, 1)
    progress_layout.addWidget(parent.progress_bar, 3)

    # Add widgets to header
    header_layout.addWidget(parent.header_label)
    header_layout.addWidget(parent.sub_header)
    header_layout.addWidget(progress_container)

    # Add "Save" button
    from ui.helpers import set_button_style
    save_button = QPushButton("💾 Save This Data")
    save_button.clicked.connect(parent._save_to_database)
    set_button_style(save_button, "#27ae60", parent.theme_manager.is_dark_mode)
    header_layout.addWidget(save_button)

    # Add a separator line
    separator = QFrame()
    separator.setFrameShape(QFrame.HLine)
    separator.setFrameShadow(QFrame.Sunken)
    separator.setStyleSheet(
        f"background-color: {'#444444' if parent.theme_manager.is_dark_mode else '#e9ecef'};"
    )
    header_layout.addWidget(separator)

    layout.addWidget(header_container)
    
    # Add to layout with section headers
    layout.addWidget(create_section_header("📘 Subject Matching Results"))
    layout.addWidget(parent.results_table)
    
    layout.addWidget(create_section_header("📊 Progress Summary"))
    layout.addWidget(parent.summary_table)
    
    layout.addWidget(create_section_header("🧠 Suggested Electives"))
    layout.addWidget(parent.electives_table)
    
    layout.addStretch()
    
    tab.setLayout(layout)
    return tab

def create_section_header(text):
    """Create a styled section header"""
    label = QLabel(text)
    label.setStyleSheet("""
        QLabel {
            font-weight: bold;
            font-size: 14px;
            margin-top: 15px;
            margin-bottom: 5px;
        }
    """)
    return label