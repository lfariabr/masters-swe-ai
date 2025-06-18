# ui/tab_results.py
from PyQt5.QtWidgets import (
    QVBoxLayout, QLabel, QTableWidget, QWidget
)

def setup_results_tab(parent):
    """
    Set up the results tab with tables for different result views
    
    Args:
        parent: The main window instance that will contain this tab
        
    Returns:
        QWidget: The configured results tab widget
    """
    # Create the main widget and layout
    tab = QWidget()
    layout = QVBoxLayout()
    layout.setSpacing(20)
    layout.setContentsMargins(30, 30, 30, 30)
    
    # Results Table
    parent.results_table = QTableWidget()
    parent.results_table.setColumnCount(4)
    parent.results_table.setHorizontalHeaderLabels(
        ["Subject Code", "Subject Name", "Type", "Status"]
    )
    
    # Summary Table
    parent.summary_table = QTableWidget()
    
    # Electives Table
    parent.electives_table = QTableWidget()
    parent.electives_table.setColumnCount(4)
    parent.electives_table.setHorizontalHeaderLabels(
        ["Subject Code", "Subject Name", "Type", "Status"]
    )
    
    # Add to layout with section headers
    layout.addWidget(create_section_header("📘 Subject Matching Results"))
    layout.addWidget(parent.results_table)
    
    layout.addWidget(create_section_header("📊 Progress Summary"))
    layout.addWidget(parent.summary_table)
    
    layout.addWidget(create_section_header("🧠 Suggested Electives"))
    layout.addWidget(parent.electives_table)
    
    # Add stretch to push everything to the top
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