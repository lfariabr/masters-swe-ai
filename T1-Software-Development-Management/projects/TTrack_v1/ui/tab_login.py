from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QHBoxLayout
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt


def setup_login_tab(parent):
    parent.login_tab = QWidget()
    parent.login_tab_layout = QVBoxLayout()
    layout = parent.login_tab_layout
    layout.setSpacing(20)
    layout.setContentsMargins(30, 30, 30, 30)

    # Title
    parent.login_title = QLabel("🎓 TTrack")
    parent.login_title.setFont(QFont("Arial", 40, QFont.Bold))
    parent.login_title.setAlignment(Qt.AlignCenter)
    layout.addWidget(parent.login_title)

    # Subtitle
    parent.login_subtitle = QLabel("🔐 Welcome to your Degree Tracker\nPlease log in or register to continue")
    parent.login_subtitle.setFont(QFont("Arial", 16))
    parent.login_subtitle.setAlignment(Qt.AlignCenter)
    layout.addWidget(parent.login_subtitle)

    # Theme toggle button
    parent.theme_toggle_btn = QPushButton()
    parent.theme_toggle_btn.setFixedSize(50, 50)
    parent.theme_toggle_btn.clicked.connect(lambda: toggle_and_refresh_theme(parent))
    # layout.addWidget(parent.theme_toggle_btn, alignment=Qt.AlignCenter)

    # Email input
    parent.login_email_input = QLineEdit()
    parent.login_email_input.setPlaceholderText("Email")
    parent.login_email_input.setFixedHeight(40)
    layout.addWidget(parent.login_email_input)

    # Password input
    parent.login_password_input = QLineEdit()
    parent.login_password_input.setPlaceholderText("Password")
    parent.login_password_input.setEchoMode(QLineEdit.Password)
    parent.login_password_input.setFixedHeight(40)
    layout.addWidget(parent.login_password_input)

    # Login and Register buttons
    btn_layout = QHBoxLayout()
    parent.login_btn = QPushButton("Login")
    parent.register_btn = QPushButton("Register")
    for btn in (parent.login_btn, parent.register_btn):
        btn.setFixedWidth(200)
        btn.setFixedHeight(40)
        btn_layout.addWidget(btn)
    btn_layout.addStretch()
    layout.addLayout(btn_layout)

    # Azure button
    parent.azure_btn = QPushButton("Login with Microsoft 🔗")
    parent.azure_btn.setFixedWidth(200)
    parent.azure_btn.setFixedHeight(40)
    layout.addWidget(parent.azure_btn, alignment=Qt.AlignCenter)

    parent.login_tab.setLayout(layout)

    refresh_login_tab_styles(parent)
    return parent.login_tab


def refresh_login_tab_styles(parent):
    dark_mode = parent.theme_manager.is_dark_mode
    text_color = "#ffffff" if dark_mode else "#000000"
    subtext_color = "#cccccc" if dark_mode else "#333333"
    input_bg = "#2b2b2b" if dark_mode else "#ffffff"
    input_fg = "#ffffff" if dark_mode else "#000000"
    border_color = "#555555" if dark_mode else "#cccccc"

    # Labels
    parent.login_title.setStyleSheet("color: #000000; font-weight: bold; padding: 5px;" if not dark_mode else "color: #ffffff; font-weight: bold; padding: 5px;")
    parent.login_subtitle.setStyleSheet("color: #000000; font-weight: bold; padding: 5px;" if not dark_mode else "color: #ffffff; font-weight: bold; padding: 5px;")

    # Theme toggle button
    icon = "🌙" if not dark_mode else "☀️"
    parent.theme_toggle_btn.setText(icon)
    parent.theme_toggle_btn.setToolTip("Switch to Dark Mode" if not dark_mode else "Switch to Light Mode")
    parent.theme_toggle_btn.setStyleSheet(f"""
        QPushButton {{
            border: 2px solid {'#2c3e50' if not dark_mode else '#ffffff'};
            border-radius: 25px;
            font-size: 24px;
            background-color: {'#f0f0f0' if not dark_mode else '#2d2d2d'};
            color: {'#2c3e50' if not dark_mode else '#ffffff'};
            padding: 0;
        }}
        QPushButton:hover {{
            background-color: {'#e0e0e0' if not dark_mode else '#3d3d3d'};
        }}
    """)

    # Inputs
    for input_field in (parent.login_email_input, parent.login_password_input):
        input_field.setStyleSheet(
            f"""
            background-color: {input_bg};
            color: {input_fg};
            border: 1px solid {border_color};
            border-radius: 5px;
            padding: 5px;
            """
        )

    # Buttons
    for btn in (parent.login_btn, parent.register_btn):
        btn.setStyleSheet(
            f"""
            background-color: {'#3c3f41' if dark_mode else '#f0f0f0'};
            color: {text_color};
            border: 1px solid {border_color};
            border-radius: 5px;
            """
        )

    # Azure button
    parent.azure_btn.setStyleSheet(
        """
        background-color: #0078D4;
        color: white;
        border-radius: 5px;
        font-weight: bold;
        """
    )


def toggle_and_refresh_theme(parent):
    parent.theme_manager.toggle_theme()
    refresh_login_tab_styles(parent)