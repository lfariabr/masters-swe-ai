from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QTableWidget,
    QProgressBar, QHBoxLayout, QFrame
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont


def setup_results_tab(parent):
    """
    Set up the results tab to visualize subject match and elective credits.
    """
    tab = QWidget()
    layout = QVBoxLayout()
    layout.setSpacing(25)
    layout.setContentsMargins(40, 30, 40, 30)

    # --- Core Subjects Progress Section ---
    layout.addWidget(create_section_header("🎓 Core Subjects"))

    parent.core_progress_widgets = []  # List of (label, progressbar) tuples

    for i in range(6):  # Dummy placeholders; you can update later with real data
        subject_label = QLabel(f"core {i+1}")
        subject_label.setFont(QFont("Courier", 14))
        progress = QProgressBar()
        progress.setValue(0)
        progress.setTextVisible(True)
        progress.setFormat("%p%")
        progress.setFixedHeight(18)
        progress.setStyleSheet("""
            QProgressBar {
                border: 1px solid #555;
                border-radius: 5px;
                text-align: center;
                background-color: #222;
                color: #eee;
            }
            QProgressBar::chunk {
                background-color: #4CAF50;
            }
        """)

        row = QHBoxLayout()
        row.addWidget(subject_label)
        row.addWidget(progress, stretch=1)
        layout.addLayout(row)

        parent.core_progress_widgets.append((subject_label, progress))

    layout.addSpacing(20)
    layout.addWidget(horizontal_divider())

    # --- Elective Credit Progress Section ---
    layout.addWidget(create_section_header("✨ Elective Credits"))

    credit_info = QLabel("elective credits")
    credit_info.setFont(QFont("Courier", 16))
    layout.addWidget(credit_info)

    parent.credit_stars = QLabel("★ ★ ★ ☆ ☆  30/50")
    parent.credit_stars.setFont(QFont("Courier", 16))
    parent.credit_stars.setStyleSheet("color: #4CAF50;")
    layout.addWidget(parent.credit_stars)

    layout.addSpacing(10)
    layout.addWidget(QLabel("suggestions:"))

    # Suggested Electives Table
    parent.electives_table = QTableWidget()
    parent.electives_table.setColumnCount(3)
    parent.electives_table.setHorizontalHeaderLabels(["subj code", "sub name", "credits"])
    parent.electives_table.horizontalHeader().setStretchLastSection(True)
    layout.addWidget(parent.electives_table)
    parent.results_table = QTableWidget()  # for full match results
    parent.summary_table = QTableWidget()  # for summary
    parent.electives_table = QTableWidget()  # already there, used in UI
    layout.addStretch()
    tab.setLayout(layout)
    return tab


def create_section_header(text):
    label = QLabel(text)
    label.setStyleSheet("""
        QLabel {
            font-weight: bold;
            font-size: 18px;
            color: #fff;
        }
    """)
    return label


def horizontal_divider():
    line = QFrame()
    line.setFrameShape(QFrame.HLine)
    line.setFrameShadow(QFrame.Sunken)
    line.setStyleSheet("color: #666;")
    return line