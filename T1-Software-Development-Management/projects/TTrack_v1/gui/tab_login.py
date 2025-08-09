from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QHBoxLayout, QMessageBox
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from controllers.login_controller import LoginController


def setup_login_tab(parent):
    parent.login_tab = QWidget()
    parent.login_tab_layout = QVBoxLayout()
    layout = parent.login_tab_layout
    layout.setSpacing(20)
    layout.setContentsMargins(30, 30, 30, 30)

    # Initialize login controller
    parent.login_controller = LoginController()

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

    # Confirm password input (initially hidden, shown for registration)
    parent.login_confirm_password_input = QLineEdit()
    parent.login_confirm_password_input.setPlaceholderText("Confirm Password")
    parent.login_confirm_password_input.setEchoMode(QLineEdit.Password)
    parent.login_confirm_password_input.setFixedHeight(40)
    parent.login_confirm_password_input.hide()  # Hidden by default
    layout.addWidget(parent.login_confirm_password_input)

    # Login and Register buttons
    btn_layout = QHBoxLayout()
    parent.login_btn = QPushButton("Login")
    parent.register_btn = QPushButton("Register")
    
    # Connect button events
    parent.login_btn.clicked.connect(lambda: handle_login(parent))
    parent.register_btn.clicked.connect(lambda: handle_register(parent))
    
    # Enable Enter key for login
    parent.login_password_input.returnPressed.connect(lambda: handle_login(parent))
    parent.login_confirm_password_input.returnPressed.connect(lambda: handle_register(parent))
    
    for btn in (parent.login_btn, parent.register_btn):
        btn.setFixedWidth(200)
        btn.setFixedHeight(40)
        btn_layout.addWidget(btn)
    btn_layout.addStretch()
    layout.addLayout(btn_layout)

    # Toggle between login/register mode
    parent.mode_toggle_btn = QPushButton("Need an account? Register here")
    parent.mode_toggle_btn.clicked.connect(lambda: toggle_login_mode(parent))
    parent.mode_toggle_btn.setStyleSheet("border: none; color: #0078D4; text-decoration: underline;")
    layout.addWidget(parent.mode_toggle_btn, alignment=Qt.AlignCenter)

    # Azure button (placeholder for future Microsoft integration)
    # parent.azure_btn = QPushButton("Login with Microsoft 🔗")
    # parent.azure_btn.setFixedWidth(200)
    # parent.azure_btn.setFixedHeight(40)
    # parent.azure_btn.clicked.connect(lambda: show_coming_soon(parent))
    # layout.addWidget(parent.azure_btn, alignment=Qt.AlignCenter)

    # Track current mode (login/register)
    parent.is_register_mode = False

    parent.login_tab.setLayout(layout)

    refresh_login_tab_styles(parent)
    return parent.login_tab


def handle_login(parent):
    """Handle login button click"""
    email = parent.login_email_input.text().strip()
    password = parent.login_password_input.text()
    
    if not email or not password:
        QMessageBox.warning(parent, "Input Error", "Please enter both email and password.")
        return
    
    # Disable button during login attempt
    parent.login_btn.setEnabled(False)
    parent.login_btn.setText("Logging in...")
    
    try:
        success, message, user_data = parent.login_controller.login(email, password)
        
        if success:
            QMessageBox.information(parent, "Login Successful", f"Welcome back!\n{message}")
            # Clear inputs
            parent.login_email_input.clear()
            parent.login_password_input.clear()
            # Navigate to main app (you'll implement this)
            navigate_to_main_app(parent)
        else:
            QMessageBox.warning(parent, "Login Failed", message)
    
    finally:
        # Re-enable button
        parent.login_btn.setEnabled(True)
        parent.login_btn.setText("Login")


def handle_register(parent):
    """Handle register button click"""
    email = parent.login_email_input.text().strip()
    password = parent.login_password_input.text()
    confirm_password = parent.login_confirm_password_input.text()
    
    if not email or not password or not confirm_password:
        QMessageBox.warning(parent, "Input Error", "Please fill in all fields.")
        return
    
    # Disable button during registration attempt
    parent.register_btn.setEnabled(False)
    parent.register_btn.setText("Registering...")
    
    try:
        success, message, user_data = parent.login_controller.register(email, password, confirm_password)
        
        if success:
            QMessageBox.information(parent, "Registration Successful", message)
            # Switch back to login mode
            toggle_login_mode(parent)
            # Clear inputs
            parent.login_email_input.clear()
            parent.login_password_input.clear()
            parent.login_confirm_password_input.clear()
        else:
            QMessageBox.warning(parent, "Registration Failed", message)
    
    finally:
        # Re-enable button
        parent.register_btn.setEnabled(True)
        parent.register_btn.setText("Register")


def toggle_login_mode(parent):
    """Toggle between login and register modes"""
    parent.is_register_mode = not parent.is_register_mode
    
    if parent.is_register_mode:
        # Switch to register mode
        parent.login_subtitle.setText("🔐 Create your TTrack account\nJoin thousands of students tracking their progress")
        parent.login_confirm_password_input.show()
        parent.mode_toggle_btn.setText("Already have an account? Login here")
        parent.register_btn.show()
        parent.login_btn.hide()
    else:
        # Switch to login mode
        parent.login_subtitle.setText("🔐 Welcome to your Degree Tracker\nPlease log in or register to continue")
        parent.login_confirm_password_input.hide()
        parent.mode_toggle_btn.setText("Need an account? Register here")
        parent.login_btn.show()
        parent.register_btn.hide()


def navigate_to_main_app(parent):
    """Navigate to main application after successful login"""
    # Enable other tabs
    if hasattr(parent, 'tab_controller'):
        parent.tab_controller.enable_all_tabs()
        parent.tab_controller.hide_login_tab()  # Hide login tab when logged in
    
    # Switch to input tab
    if hasattr(parent, 'tabs'):
        parent.tabs.setCurrentIndex(0)  # Now index 0 since login tab is removed
    
    print(f"✅ User logged in: {parent.login_controller.get_user_email()}")


# def show_coming_soon(parent):
#     """Show coming soon message for Microsoft login"""
#     QMessageBox.information(
#         parent, 
#         "Coming Soon", 
#         "Microsoft Azure integration is coming soon!\nFor now, please use email registration."
#     )


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
    """)

    # Inputs
    for input_field in (parent.login_email_input, parent.login_password_input, parent.login_confirm_password_input):
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

    # Make login button orange
    parent.login_btn.setStyleSheet(
        """
        background-color: #F57B07;
        color: white;
        border: none;
        border-radius: 5px;
        font-weight: 500;
        """
    )

    # Azure button
    # parent.azure_btn.setStyleSheet(
    #     """
    #     background-color: #0078D4;
    #     color: white;
    #     border-radius: 5px;
    #     font-weight: bold;
    #     """
    # )


def toggle_and_refresh_theme(parent):
    parent.theme_manager.toggle_theme()
    refresh_login_tab_styles(parent)