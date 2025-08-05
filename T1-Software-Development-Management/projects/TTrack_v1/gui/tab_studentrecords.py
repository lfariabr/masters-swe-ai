from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QComboBox, QLabel, QPushButton
)
from PyQt5.QtCore import Qt
from services.database import DatabaseManager

def setup_studentrecords_tab(parent):
    tab = QWidget()
    layout = QVBoxLayout()
    layout.setSpacing(20)
    layout.setContentsMargins(30, 30, 30, 30)

    # Mock data
    mock_students = []
    # ("1001", "Hussain", "Masters SWE AI", "2025-02-10", "30%"),
    # ("1002", "Luis", "Masters SWE AI", "2025-02-15", "60%"),
    # ("1003", "Nomayer", "Masters IT", "2025-03-01", "90%"),
    # ("1004", "Rosa", "Masters IT", "2025-02-15", "60%"),
    # ("1005", "Victor", "Masters Cybersec", "2025-02-15", "60%"),
    # ]
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
    
    def view_all_records():
        """
        Get ALL STUDENT records from database
        """
        parent.database_table.clearContents()
        parent.database_table.setRowCount(0)
        
        try:
            # Use existing database manager from parent
            db = parent.database_manager # lfariaus@gmail.com
            
            # Get current user id from login controller
            if hasattr(parent, 'login_controller') and parent.login_controller.is_authenticated():
                user_id = parent.login_controller.get_user_id()
                print(f"Current user id: {user_id}")
            else:
                print("❌ User not authenticated")
                return
            
            # Fetch user's session history
            records = db.fetch_user_history(user_id)
            print(f"Found {len(records) if records else 0} records")
            
            if records and len(records) > 0:
                # Update table headers to match database structure
                parent.database_table.setColumnCount(8)
                parent.database_table.setHorizontalHeaderLabels([
                    "Session ID", "results_data", "summary_data", "electives_data",
                    "User ID", "Progress", "Created Date", "Actions"
                ])
                
                parent.database_table.setRowCount(len(records))
                
                for row, record in enumerate(records):
                    # Extract data safely
                    session_id = record.get('id', 'N/A')[:8] + "..."  # Truncate ID
                    user_id_display = record.get('user_id', 'N/A')
                    progress = f"{record.get('progress_data', 0)}%"
                    created_at = record.get('created_at', 'N/A')
                    results_data = record.get('results_data', 'N/A')
                    summary_data = record.get('summary_data', 'N/A')
                    electives_data = record.get('electives_data', 'N/A')
                    
                    # Populate table
                    parent.database_table.setItem(row, 0, QTableWidgetItem(session_id))
                    parent.database_table.setItem(row, 1, QTableWidgetItem(results_data))
                    parent.database_table.setItem(row, 2, QTableWidgetItem(summary_data))
                    parent.database_table.setItem(row, 3, QTableWidgetItem(electives_data))
                    parent.database_table.setItem(row, 4, QTableWidgetItem(user_id_display))
                    parent.database_table.setItem(row, 5, QTableWidgetItem(progress))
                    parent.database_table.setItem(row, 6, QTableWidgetItem(created_at))
                    parent.database_table.setItem(row, 7, QTableWidgetItem("View Details"))
                
                print(f"✅ Loaded {len(records)} records successfully")
            else:
                print("⚠️ No records found for this user")
                # Show message in table
                parent.database_table.setRowCount(1)
                parent.database_table.setItem(0, 0, QTableWidgetItem("No records found"))
                parent.database_table.setItem(0, 1, QTableWidgetItem("Process some data first"))
                parent.database_table.setItem(0, 2, QTableWidgetItem(""))
                parent.database_table.setItem(0, 3, QTableWidgetItem(""))
                parent.database_table.setItem(0, 4, QTableWidgetItem(""))
                parent.database_table.setItem(0, 5, QTableWidgetItem(""))
                parent.database_table.setItem(0, 6, QTableWidgetItem(""))
                parent.database_table.setItem(0, 7, QTableWidgetItem(""))
                
        except Exception as e:
            print(f"❌ Error loading records: {e}")
            # Show error in table
            parent.database_table.setRowCount(1)
            parent.database_table.setItem(0, 0, QTableWidgetItem("Error"))
            parent.database_table.setItem(0, 1, QTableWidgetItem(str(e)))
            parent.database_table.setItem(0, 2, QTableWidgetItem(""))
            parent.database_table.setItem(0, 3, QTableWidgetItem(""))
            parent.database_table.setItem(0, 4, QTableWidgetItem(""))
            parent.database_table.setItem(0, 5, QTableWidgetItem(""))
            parent.database_table.setItem(0, 6, QTableWidgetItem(""))
            parent.database_table.setItem(0, 7, QTableWidgetItem(""))
    
    # view_button = QPushButton("View Student Record")
    # view_button.clicked.connect(lambda: view_student_record(student_selector.currentData()))
    # layout.addWidget(view_button)

    view_all_button = QPushButton("View All Records")
    view_all_button.clicked.connect(lambda: view_all_records())
    layout.addWidget(view_all_button)

    return tab