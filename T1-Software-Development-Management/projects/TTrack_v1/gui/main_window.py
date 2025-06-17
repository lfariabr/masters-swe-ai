from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QPushButton,
    QFileDialog, QLabel, QTableView, QHBoxLayout, QFrame
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from .utils import load_excel_as_model, is_dark_mode


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        dark_mode = is_dark_mode()

        main_color = "#ffffff" if dark_mode else "#2c3e50"
        sub_color = "#bbbbbb" if dark_mode else "#555555"
        credit_color = "#999999" if dark_mode else "#777777"

        self.setWindowTitle("TTrack – Degree Tracker")
        self.setGeometry(100, 100, 1100, 700)

        self.transcript_table = QTableView()
        self.curriculum_table = QTableView()

        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)

        # 🏫 Title Section
        title = QLabel("🎓 TTrack – Torrens Degree Tracker")
        title.setFont(QFont("Arial", 20, QFont.Bold))
        title.setStyleSheet("color: " + main_color + ";")
        title.setAlignment(Qt.AlignCenter)

        subtitle = QLabel("Built by students for academic advisors at Torrens University Australia.")
        subtitle.setStyleSheet("color: " + sub_color + "; font-size: 13px;")
        subtitle.setAlignment(Qt.AlignCenter)

        credit = QLabel("Guided by Dr. Atif Qureshi – Software Development Management, 2025")
        credit.setStyleSheet("color: " + credit_color + "; font-size: 11px; font-style: italic;")
        credit.setAlignment(Qt.AlignCenter)

        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addWidget(credit)
        layout.addSpacing(20)

        # 📂 Upload Section
        button_layout = QHBoxLayout()
        self.transcript_btn = QPushButton("📄 Upload Transcript")
        self.curriculum_btn = QPushButton("📚 Upload Curriculum")

        self.transcript_btn.clicked.connect(self.load_transcript)
        self.curriculum_btn.clicked.connect(self.load_curriculum)

        self.set_button_style(self.transcript_btn)
        self.set_button_style(self.curriculum_btn)

        button_layout.addWidget(self.transcript_btn)
        button_layout.addWidget(self.curriculum_btn)

        layout.addLayout(button_layout)

        # 🧾 Display Section
        layout.addSpacing(15)
        layout.addWidget(QLabel("Transcript Table"))
        layout.addWidget(self.transcript_table)
        layout.addSpacing(10)
        layout.addWidget(QLabel("Curriculum Table"))
        layout.addWidget(self.curriculum_table)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def set_button_style(self, button):
        button.setStyleSheet("""
            QPushButton {
                background-color: " + main_color + ";
                color: white;
                padding: 10px 20px;
                font-size: 14px;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: " + main_color + ";
            }
        """)

    def load_transcript(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open Transcript", "", "Excel Files (*.xlsx)")
        if file_path:
            model = load_excel_as_model(file_path)
            self.transcript_table.setModel(model)

    def load_curriculum(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open Curriculum", "", "Excel Files (*.xlsx)")
        if file_path:
            model = load_excel_as_model(file_path)
            self.curriculum_table.setModel(model)
    