# ui/tab_results.py
from PyQt5.QtWidgets import (
    QVBoxLayout,
    QHBoxLayout,
    QTableWidget,
    QWidget,
    QLabel,
    QFrame,
    QProgressBar
)

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

    student_name = getattr(parent, 'student_name', 'Student')
    university = getattr(parent, 'university', 'University')

    # Main header
    header_label = QLabel(f"Results for {student_name}")
    header_label.setObjectName("header_label")
    header_label.setStyleSheet(f"""
        font-size: 22px; 
        font-weight: bold; 
        color: {'#4ecdc4' if parent.is_dark_mode else '#2a9d8f'};
        margin-bottom: 4px;
    """)

    # Sub header with university
    sub_header = QLabel(f"@ {university}")
    sub_header.setObjectName("sub_header")
    sub_header.setStyleSheet(f"""
        font-size: 14px;
        color: {'#bbbbbb' if parent.is_dark_mode else '#555555'};
        margin-bottom: 15px;
    """)

    # Progress indicator
    progress_container = QWidget()
    progress_layout = QHBoxLayout(progress_container)
    progress_layout.setContentsMargins(0, 0, 0, 0)

    progress_bar = QProgressBar()
    # TODO: Update progress bar
    progress_bar.setValue(0)
        
    progress_bar.setStyleSheet(f"""
        QProgressBar {{
            border: none;
            border-radius: 10px;
            text-align: center;
            background: {'#444444' if parent.is_dark_mode else '#e9ecef'};
            height: 8px;
        }}
        QProgressBar::chunk {{
            background-color: {'#4ecdc4' if parent.is_dark_mode else '#2a9d8f'};
            border-radius: 10px;
        }}
    """)

    progress_label = QLabel(f"Degree Progress")
    progress_label.setStyleSheet(f"color: {'#bbbbbb' if parent.is_dark_mode else '#666666'}; font-size: 12px;")

    progress_layout.addWidget(progress_label, 1)
    progress_layout.addWidget(progress_bar, 3)

    # Add all elements to header
    header_layout.addWidget(header_label)
    header_layout.addWidget(sub_header)
    header_layout.addWidget(progress_container)

    # Add a separator line
    separator = QFrame()
    separator.setFrameShape(QFrame.HLine)
    separator.setFrameShadow(QFrame.Sunken)
    separator.setStyleSheet(f"background-color: {'#444444' if parent.is_dark_mode else '#e9ecef'};")
    header_layout.addWidget(separator)

    # Add header to main layout
    layout.addWidget(header_container)
    
    # Add to layout with section headers
    layout.addWidget(create_section_header("📘 Subject Matching Results"))
    layout.addWidget(parent.results_table)
    
    layout.addWidget(create_section_header("📊 Progress Summary"))
    layout.addWidget(parent.summary_table)
    
    layout.addWidget(create_section_header("🧠 Suggested Electives"))
    layout.addWidget(parent.electives_table)
    
    # Push everything to the top
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