from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QComboBox, QLabel
)

def setup_studentrecords_tab(parent):
    tab = QWidget()
    layout = QVBoxLayout()
    layout.setSpacing(20)
    layout.setContentsMargins(30, 30, 30, 30)

    # Mock data
    mock_students = [
        ("1001", "Hussain", "Masters SWE AI", "2025-02-10", "30%"),
        ("1002", "Luis", "Masters SWE AI", "2025-02-15", "60%"),
        ("1003", "Nomayer", "Masters IT", "2025-03-01", "90%"),
        ("1004", "Rosa", "Masters IT", "2025-02-15", "60%"),
        ("1005", "Victor", "Masters Cybersec", "2025-02-15", "60%"),
    ]
    parent.all_students_data = mock_students

    # Student selector label
    selector_label = QLabel("Select Student ID:")

    # Create student dropdown
    student_selector = QComboBox()
    is_dark = parent.theme_manager.is_dark_mode

    # Style for both dark and light mode
    student_selector.setStyleSheet(f"""
        QComboBox {{
            padding: 5px 10px;
            font-size: 14px;
            border: 1px solid {'#888888' if not is_dark else '#555555'};
            border-radius: 6px;
            background-color: {'#f2f2f2' if not is_dark else '#2d2d2d'};
            color: {'#000000' if not is_dark else '#ffffff'};
        }}
        QComboBox:hover {{
            border: 1px solid {'#555555' if not is_dark else '#aaaaaa'};
        }}
        QComboBox::drop-down {{
            subcontrol-origin: padding;
            subcontrol-position: top right;
            width: 25px;
            border-left: 1px solid {'#888888' if not is_dark else '#555555'};
        }}
        QComboBox QAbstractItemView {{
            background-color: {'#ffffff' if not is_dark else '#121212'};
            color: {'#000000' if not is_dark else '#ffffff'};
            selection-background-color: {'#d0d0d0' if not is_dark else '#3d3d3d'};
            selection-color: {'#000000' if not is_dark else '#ffffff'};
        }}
    """)

    # Add "All Students" option first
    student_selector.addItem("All Students", userData=None)

    # Fill dropdown with name + ID
    for sid, name, *_ in mock_students:
        student_selector.addItem(f"{name} ({sid})", userData=sid)

    # Table widget
    parent.database_table = QTableWidget()
    parent.database_table.setColumnCount(5)
    parent.database_table.setHorizontalHeaderLabels(
        ["Student ID", "Student Name", "Course Name", "Date Added", "Degree Progress"]
    )
    parent.database_table.setSortingEnabled(True)

    # Filtering logic
    def filter_table():
        selected_id = student_selector.currentData()
        if selected_id is None:
            data_to_show = mock_students  # Show all
        else:
            data_to_show = [s for s in mock_students if s[0] == selected_id]

        parent.database_table.setRowCount(len(data_to_show))
        for row, (sid, name, course, date, progress) in enumerate(data_to_show):
            parent.database_table.setItem(row, 0, QTableWidgetItem(sid))
            parent.database_table.setItem(row, 1, QTableWidgetItem(name))
            parent.database_table.setItem(row, 2, QTableWidgetItem(course))
            parent.database_table.setItem(row, 3, QTableWidgetItem(date))
            parent.database_table.setItem(row, 4, QTableWidgetItem(progress))

    student_selector.currentIndexChanged.connect(filter_table)

    # Add to layout
    layout.addWidget(selector_label)
    layout.addWidget(student_selector)
    layout.addWidget(parent.database_table)
    tab.setLayout(layout)

    # Default to first student
    student_selector.setCurrentIndex(0)
    filter_table()

    return tab