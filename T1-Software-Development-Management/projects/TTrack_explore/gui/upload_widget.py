from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QFileDialog,
    QLabel, QHBoxLayout, QFrame
)
from PyQt5.QtCore import pyqtSignal, Qt

class UploadWidget(QWidget):
    transcript_uploaded = pyqtSignal(str)
    curriculum_uploaded = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.transcript_path = None
        self.curriculum_path = None
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(25)
        layout.setContentsMargins(30, 30, 30, 30)

        # Add upload sections styled as cards
        layout.addWidget(self.create_upload_card(
            title="📄 Upload Student Transcript",
            description="Select the transcript (.xlsx) file exported from your student system.",
            button_text="Choose Transcript File",
            callback=self.load_transcript,
            is_transcript=True
        ))

        layout.addWidget(self.create_upload_card(
            title="📚 Upload Program Curriculum",
            description="Select the official program curriculum (.xlsx) file to validate progress.",
            button_text="Choose Curriculum File",
            callback=self.load_curriculum,
            is_transcript=False
        ))

        layout.addStretch()
        self.setLayout(layout)

    def create_upload_card(self, title, description, button_text, callback, is_transcript=True):
        card = QFrame()
        card.setStyleSheet("""
            QFrame {
                background-color: #f8f9fa;
                border-radius: 12px;
                padding: 20px;
                border: 1px solid #ddd;
            }
        """)

        vbox = QVBoxLayout(card)
        vbox.setSpacing(12)

        # Title
        title_label = QLabel(title)
        title_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #333;")
        vbox.addWidget(title_label)

        # Description
        desc_label = QLabel(description)
        desc_label.setWordWrap(True)
        desc_label.setStyleSheet("color: #555; font-size: 13px;")
        vbox.addWidget(desc_label)

        # Button
        button = QPushButton(button_text)
        button.setStyleSheet("""
            QPushButton {
                background-color: #1976d2;
                color: white;
                padding: 8px 16px;
                font-weight: bold;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #1565c0;
            }
        """)
        button.clicked.connect(callback)
        vbox.addWidget(button)

        # File path display
        file_label = QLabel("No file selected.")
        file_label.setStyleSheet("font-style: italic; color: #888;")
        vbox.addWidget(file_label)

        # Save label reference
        if is_transcript:
            self.transcript_label = file_label
        else:
            self.curriculum_label = file_label

        return card

    def load_transcript(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select Transcript File", "", "Excel Files (*.xlsx);;All Files (*)"
        )
        if file_path:
            self.transcript_path = file_path
            self.transcript_label.setText(f"✅ {file_path}")
            self.transcript_label.setStyleSheet("color: #2e7d32; font-weight: bold;")
            self.transcript_uploaded.emit(file_path)

    def load_curriculum(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select Curriculum File", "", "Excel Files (*.xlsx);;All Files (*)"
        )
        if file_path:
            self.curriculum_path = file_path
            self.curriculum_label.setText(f"✅ {file_path}")
            self.curriculum_label.setStyleSheet("color: #2e7d32; font-weight: bold;")
            self.curriculum_uploaded.emit(file_path)

    def reset(self):
        self.transcript_path = None
        self.curriculum_path = None
        self.transcript_label.setText("No file selected.")
        self.curriculum_label.setText("No file selected.")
        self.transcript_label.setStyleSheet("font-style: italic; color: #888;")
        self.curriculum_label.setStyleSheet("font-style: italic; color: #888;")