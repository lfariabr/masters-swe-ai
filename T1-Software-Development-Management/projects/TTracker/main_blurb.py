# TTrack Desktop Application - Main Entry Point
# File: main.py

import sys
import sqlite3
import pandas as pd
from pathlib import Path
from PyQt6.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, 
                             QWidget, QPushButton, QLabel, QFileDialog, QTableWidget, 
                             QTableWidgetItem, QTabWidget, QProgressBar, QTextEdit,
                             QMessageBox, QGroupBox, QGridLayout, QComboBox)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QFont, QIcon

class DatabaseManager:
    """Handles all database operations for TTrack"""
    
    def __init__(self, db_path="ttrack.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize the SQLite database with required tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Programs table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS programs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                total_credits INTEGER NOT NULL,
                core_credits INTEGER NOT NULL,
                elective_credits INTEGER NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Courses table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS courses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                code TEXT NOT NULL,
                name TEXT NOT NULL,
                credits INTEGER NOT NULL,
                type TEXT CHECK(type IN ('core', 'elective')) NOT NULL,
                program_id INTEGER NOT NULL,
                prerequisites TEXT,
                category TEXT,
                FOREIGN KEY (program_id) REFERENCES programs (id),
                UNIQUE(code, program_id)
            )
        ''')
        
        # Students table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                student_id TEXT UNIQUE NOT NULL,
                program_id INTEGER NOT NULL,
                enrollment_year INTEGER,
                FOREIGN KEY (program_id) REFERENCES programs (id)
            )
        ''')
        
        # Completed courses table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS completed_courses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id INTEGER NOT NULL,
                course_code TEXT NOT NULL,
                grade TEXT NOT NULL,
                credits INTEGER NOT NULL,
                semester TEXT,
                year INTEGER,
                FOREIGN KEY (student_id) REFERENCES students (id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def add_program(self, name, total_credits, core_credits, elective_credits):
        """Add a new degree program"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO programs (name, total_credits, core_credits, elective_credits)
                VALUES (?, ?, ?, ?)
            ''', (name, total_credits, core_credits, elective_credits))
            conn.commit()
            return cursor.lastrowid
        except sqlite3.IntegrityError:
            return None
        finally:
            conn.close()
    
    def get_programs(self):
        """Get all degree programs"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM programs ORDER BY name')
        programs = cursor.fetchall()
        conn.close()
        return programs

class ExcelProcessor:
    """Handles Excel file processing for course requirements and transcripts"""
    
    @staticmethod
    def process_course_requirements(file_path):
        """Process course requirements Excel file"""
        try:
            df = pd.read_excel(file_path)
            
            # Expected columns: Course Code, Course Name, Credits, Type, Prerequisites, Category
            required_columns = ['Course Code', 'Course Name', 'Credits', 'Type']
            
            if not all(col in df.columns for col in required_columns):
                raise ValueError(f"Excel file must contain columns: {required_columns}")
            
            # Clean and validate data
            df['Course Code'] = df['Course Code'].astype(str).str.strip()
            df['Course Name'] = df['Course Name'].astype(str).str.strip()
            df['Credits'] = pd.to_numeric(df['Credits'], errors='coerce')
            df['Type'] = df['Type'].astype(str).str.lower().str.strip()
            
            # Validate course types
            valid_types = ['core', 'elective']
            df = df[df['Type'].isin(valid_types)]
            
            return df.to_dict('records')
            
        except Exception as e:
            raise Exception(f"Error processing course requirements file: {str(e)}")
    
    @staticmethod
    def process_transcript(file_path):
        """Process student transcript Excel file"""
        try:
            df = pd.read_excel(file_path)
            
            # Expected columns: Course Code, Grade, Credits, Semester, Year
            required_columns = ['Course Code', 'Grade', 'Credits']
            
            if not all(col in df.columns for col in required_columns):
                raise ValueError(f"Transcript file must contain columns: {required_columns}")
            
            # Clean and validate data
            df['Course Code'] = df['Course Code'].astype(str).str.strip()
            df['Grade'] = df['Grade'].astype(str).str.strip()
            df['Credits'] = pd.to_numeric(df['Credits'], errors='coerce')
            
            # Filter out failed courses (assuming F or Fail grades)
            passing_grades = ['A+', 'A', 'A-', 'B+', 'B', 'B-', 'C+', 'C', 'C-', 'D+', 'D', 'P', 'PASS']
            df = df[df['Grade'].str.upper().isin(passing_grades)]
            
            return df.to_dict('records')
            
        except Exception as e:
            raise Exception(f"Error processing transcript file: {str(e)}")

class ProgressCalculator:
    """Calculates degree progress and requirement fulfillment"""
    
    def __init__(self, db_manager):
        self.db = db_manager
    
    def calculate_progress(self, student_id):
        """Calculate comprehensive progress for a student"""
        conn = sqlite3.connect(self.db.db_path)
        
        # Get student and program info
        student_query = '''
            SELECT s.*, p.name as program_name, p.total_credits, p.core_credits, p.elective_credits
            FROM students s
            JOIN programs p ON s.program_id = p.id
            WHERE s.id = ?
        '''
        student_info = conn.execute(student_query, (student_id,)).fetchone()
        
        if not student_info:
            conn.close()
            return None
        
        # Get completed courses
        completed_query = '''
            SELECT course_code, credits, grade
            FROM completed_courses
            WHERE student_id = ?
        '''
        completed_courses = conn.execute(completed_query, (student_id,)).fetchall()
        
        # Get program requirements
        requirements_query = '''
            SELECT code, name, credits, type, category
            FROM courses
            WHERE program_id = ?
        '''
        requirements = conn.execute(requirements_query, (student_info[3],)).fetchall()
        
        conn.close()
        
        # Calculate progress
        completed_codes = {course[0] for course in completed_courses}
        total_completed_credits = sum(course[1] for course in completed_courses)
        
        # Separate core and elective requirements
        core_requirements = [req for req in requirements if req[3] == 'core']
        elective_requirements = [req for req in requirements if req[3] == 'elective']
        
        # Calculate core progress
        completed_core = [req for req in core_requirements if req[0] in completed_codes]
        core_credits_completed = sum(req[2] for req in completed_core)
        core_progress = (core_credits_completed / student_info[7]) * 100 if student_info[7] > 0 else 0
        
        # Calculate elective progress
        completed_electives = [req for req in elective_requirements if req[0] in completed_codes]
        elective_credits_completed = sum(req[2] for req in completed_electives)
        elective_progress = (elective_credits_completed / student_info[8]) * 100 if student_info[8] > 0 else 0
        
        # Overall progress
        overall_progress = (total_completed_credits / student_info[6]) * 100 if student_info[6] > 0 else 0
        
        return {
            'student_info': student_info,
            'total_completed_credits': total_completed_credits,
            'core_progress': min(core_progress, 100),
            'elective_progress': min(elective_progress, 100),
            'overall_progress': min(overall_progress, 100),
            'completed_core': completed_core,
            'remaining_core': [req for req in core_requirements if req[0] not in completed_codes],
            'completed_electives': completed_electives,
            'remaining_electives': [req for req in elective_requirements if req[0] not in completed_codes]
        }

class FileProcessingThread(QThread):
    """Background thread for processing Excel files"""
    finished = pyqtSignal(dict)
    error = pyqtSignal(str)
    
    def __init__(self, file_path, file_type):
        super().__init__()
        self.file_path = file_path
        self.file_type = file_type
    
    def run(self):
        try:
            if self.file_type == 'requirements':
                data = ExcelProcessor.process_course_requirements(self.file_path)
            else:  # transcript
                data = ExcelProcessor.process_transcript(self.file_path)
            
            self.finished.emit({'data': data, 'type': self.file_type})
        except Exception as e:
            self.error.emit(str(e))

class TTrackMainWindow(QMainWindow):
    """Main application window"""
    
    def __init__(self):
        super().__init__()
        self.db = DatabaseManager()
        self.calculator = ProgressCalculator(self.db)
        self.init_ui()
    
    def init_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle("TTrack - Torrens Degree Track")
        self.setGeometry(100, 100, 1200, 800)
        
        # Create central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Create tab widget
        self.tab_widget = QTabWidget()
        
        # Create tabs
        self.create_dashboard_tab()
        self.create_upload_tab()
        self.create_progress_tab()
        self.create_reports_tab()
        
        # Main layout
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.tab_widget)
        central_widget.setLayout(main_layout)
        
        # Style the application
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f0f0f0;
            }
            QTabWidget::pane {
                border: 1px solid #c0c0c0;
                background-color: white;
            }
            QTabBar::tab {
                background-color: #e0e0e0;
                padding: 8px 20px;
                margin: 2px;
            }
            QTabBar::tab:selected {
                background-color: #4CAF50;
                color: white;
            }
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QGroupBox {
                font-weight: bold;
                border: 2px solid #c0c0c0;
                border-radius: 5px;
                margin: 10px 0;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 20px;
                padding: 0 10px 0 10px;
            }
        """)
    
    def create_dashboard_tab(self):
        """Create the main dashboard tab"""
        dashboard_widget = QWidget()
        layout = QVBoxLayout()
        
        # Welcome section
        welcome_label = QLabel("Welcome to TTrack - Torrens Degree Track")
        welcome_label.setFont(QFont("Arial", 20, QFont.Weight.Bold))
        welcome_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(welcome_label)
        
        # Quick stats section
        stats_group = QGroupBox("Quick Statistics")
        stats_layout = QGridLayout()
        
        self.total_students_label = QLabel("Total Students: 0")
        self.total_programs_label = QLabel("Total Programs: 0")
        self.avg_progress_label = QLabel("Average Progress: 0%")
        
        stats_layout.addWidget(self.total_students_label, 0, 0)
        stats_layout.addWidget(self.total_programs_label, 0, 1)
        stats_layout.addWidget(self.avg_progress_label, 0, 2)
        stats_group.setLayout(stats_layout)
        layout.addWidget(stats_group)
        
        # Recent activity section
        activity_group = QGroupBox("Recent Activity")
        activity_layout = QVBoxLayout()
        
        self.activity_text = QTextEdit()
        self.activity_text.setMaximumHeight(200)
        self.activity_text.setPlainText("No recent activity to display.")
        activity_layout.addWidget(self.activity_text)
        activity_group.setLayout(activity_layout)
        layout.addWidget(activity_group)
        
        layout.addStretch()
        dashboard_widget.setLayout(layout)
        self.tab_widget.addTab(dashboard_widget, "Dashboard")
    
    def create_upload_tab(self):
        """Create the file upload tab"""
        upload_widget = QWidget()
        layout = QVBoxLayout()
        
        # Course requirements upload
        requirements_group = QGroupBox("Upload Course Requirements")
        requirements_layout = QVBoxLayout()
        
        requirements_info = QLabel("Upload an Excel file containing course requirements (Course Code, Course Name, Credits, Type)")
        requirements_info.setWordWrap(True)
        requirements_layout.addWidget(requirements_info)
        
        requirements_button = QPushButton("Select Course Requirements File")
        requirements_button.clicked.connect(lambda: self.select_file('requirements'))
        requirements_layout.addWidget(requirements_button)
        
        self.requirements_status = QLabel("No file selected")
        requirements_layout.addWidget(self.requirements_status)
        
        requirements_group.setLayout(requirements_layout)
        layout.addWidget(requirements_group)
        
        # Transcript upload
        transcript_group = QGroupBox("Upload Student Transcript")
        transcript_layout = QVBoxLayout()
        
        transcript_info = QLabel("Upload an Excel file containing student transcript (Course Code, Grade, Credits)")
        transcript_info.setWordWrap(True)
        transcript_layout.addWidget(transcript_info)
        
        transcript_button = QPushButton("Select Transcript File")
        transcript_button.clicked.connect(lambda: self.select_file('transcript'))
        transcript_layout.addWidget(transcript_button)
        
        self.transcript_status = QLabel("No file selected")
        transcript_layout.addWidget(self.transcript_status)
        
        transcript_group.setLayout(transcript_layout)
        layout.addWidget(transcript_group)
        
        layout.addStretch()
        upload_widget.setLayout(layout)
        self.tab_widget.addTab(upload_widget, "Upload Files")
    
    def create_progress_tab(self):
        """Create the progress tracking tab"""
        progress_widget = QWidget()
        layout = QVBoxLayout()
        
        # Student selection
        selection_group = QGroupBox("Select Student")
        selection_layout = QHBoxLayout()
        
        self.student_combo = QComboBox()
        self.student_combo.currentTextChanged.connect(self.update_progress_display)
        selection_layout.addWidget(QLabel("Student:"))
        selection_layout.addWidget(self.student_combo)
        
        refresh_button = QPushButton("Refresh")
        refresh_button.clicked.connect(self.refresh_student_list)
        selection_layout.addWidget(refresh_button)
        
        selection_group.setLayout(selection_layout)
        layout.addWidget(selection_group)
        
        # Progress display
        progress_group = QGroupBox("Progress Overview")
        progress_layout = QGridLayout()
        
        # Progress bars
        progress_layout.addWidget(QLabel("Overall Progress:"), 0, 0)
        self.overall_progress_bar = QProgressBar()
        progress_layout.addWidget(self.overall_progress_bar, 0, 1)
        self.overall_progress_label = QLabel("0%")
        progress_layout.addWidget(self.overall_progress_label, 0, 2)
        
        progress_layout.addWidget(QLabel("Core Courses:"), 1, 0)
        self.core_progress_bar = QProgressBar()
        progress_layout.addWidget(self.core_progress_bar, 1, 1)
        self.core_progress_label = QLabel("0%")
        progress_layout.addWidget(self.core_progress_label, 1, 2)
        
        progress_layout.addWidget(QLabel("Elective Courses:"), 2, 0)
        self.elective_progress_bar = QProgressBar()
        progress_layout.addWidget(self.elective_progress_bar, 2, 1)
        self.elective_progress_label = QLabel("0%")
        progress_layout.addWidget(self.elective_progress_label, 2, 2)
        
        progress_group.setLayout(progress_layout)
        layout.addWidget(progress_group)
        
        # Course details table
        details_group = QGroupBox("Course Details")
        details_layout = QVBoxLayout()
        
        self.course_table = QTableWidget()
        self.course_table.setColumnCount(5)
        self.course_table.setHorizontalHeaderLabels(["Course Code", "Course Name", "Credits", "Type", "Status"])
        details_layout.addWidget(self.course_table)
        
        details_group.setLayout(details_layout)
        layout.addWidget(details_group)
        
        progress_widget.setLayout(layout)
        self.tab_widget.addTab(progress_widget, "Progress Tracking")
    
    def create_reports_tab(self):
        """Create the reports tab"""
        reports_widget = QWidget()
        layout = QVBoxLayout()
        
        # Report generation
        report_group = QGroupBox("Generate Reports")
        report_layout = QVBoxLayout()
        
        export_button = QPushButton("Export Progress Report")
        export_button.clicked.connect(self.export_report)
        report_layout.addWidget(export_button)
        
        print_button = QPushButton("Print Summary")
        print_button.clicked.connect(self.print_summary)
        report_layout.addWidget(print_button)
        
        report_group.setLayout(report_layout)
        layout.addWidget(report_group)
        
        # Report preview
        preview_group = QGroupBox("Report Preview")
        preview_layout = QVBoxLayout()
        
        self.report_preview = QTextEdit()
        self.report_preview.setPlainText("Select a student from the Progress Tracking tab to generate a report preview.")
        preview_layout.addWidget(self.report_preview)
        
        preview_group.setLayout(preview_layout)
        layout.addWidget(preview_group)
        
        reports_widget.setLayout(layout)
        self.tab_widget.addTab(reports_widget, "Reports")
    
    def select_file(self, file_type):
        """Handle file selection for upload"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, 
            f"Select {file_type.title()} File", 
            "", 
            "Excel Files (*.xlsx *.xls)"
        )
        
        if file_path:
            # Update status
            if file_type == 'requirements':
                self.requirements_status.setText(f"Selected: {Path(file_path).name}")
            else:
                self.transcript_status.setText(f"Selected: {Path(file_path).name}")
            
            # Process file in background thread
            self.processing_thread = FileProcessingThread(file_path, file_type)
            self.processing_thread.finished.connect(self.handle_file_processed)
            self.processing_thread.error.connect(self.handle_file_error)
            self.processing_thread.start()
    
    def handle_file_processed(self, result):
        """Handle successful file processing"""
        data = result['data']
        file_type = result['type']
        
        if file_type == 'requirements':
            # Store course requirements in database
            QMessageBox.information(self, "Success", f"Processed {len(data)} course requirements successfully!")
        else:
            # Store transcript data in database
            QMessageBox.information(self, "Success", f"Processed {len(data)} transcript entries successfully!")
        
        # Refresh displays
        self.refresh_student_list()
    
    def handle_file_error(self, error_message):
        """Handle file processing errors"""
        QMessageBox.critical(self, "Error", f"Failed to process file:\n{error_message}")
    
    def refresh_student_list(self):
        """Refresh the student dropdown list"""
        # This would be implemented to fetch students from database
        pass
    
    def update_progress_display(self):
        """Update the progress display for selected student"""
        # This would be implemented to calculate and display progress
        pass
    
    def export_report(self):
        """Export progress report to file"""
        QMessageBox.information(self, "Export", "Report export functionality coming soon!")
    
    def print_summary(self):
        """Print progress summary"""
        QMessageBox.information(self, "Print", "Print functionality coming soon!")

def main():
    """Main application entry point"""
    app = QApplication(sys.argv)
    
    # Set application properties
    app.setApplicationName("TTrack")
    app.setApplicationVersion("1.0.0")
    app.setOrganizationName("Torrens University")
    
    # Create and show main window
    window = TTrackMainWindow()
    window.show()
    
    # Run application
    sys.exit(app.exec())

if __name__ == "__main__":
    main()