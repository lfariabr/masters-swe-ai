"""
TTrack Sync Status Widget - v3.4.0
Shows cloud sync status and provides manual sync controls
"""

from PyQt5.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout, QLabel, QPushButton, 
    QProgressBar, QFrame, QMessageBox
)
from PyQt5.QtCore import Qt, QTimer, pyqtSignal
from PyQt5.QtGui import QFont
from datetime import datetime
import os

class SyncStatusWidget(QWidget):
    """
    Widget to display sync status and provide manual sync controls
    """
    
    # Signals
    sync_requested = pyqtSignal()
    
    def __init__(self, sync_service, theme_manager):
        super().__init__()
        self.sync_service = sync_service
        self.theme_manager = theme_manager
        
        # Auto-refresh timer
        self.refresh_timer = QTimer()
        self.refresh_timer.timeout.connect(self.update_status)
        self.refresh_timer.start(30000)  # Update every 30 seconds
        
        self.setup_ui()
        self.update_status()
    
    def setup_ui(self):
        """Setup the sync status UI"""
        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 5, 10, 5)
        layout.setSpacing(15)
        
        # Connection status indicator
        self.status_frame = QFrame()
        self.status_frame.setFrameStyle(QFrame.StyledPanel)
        status_layout = QHBoxLayout(self.status_frame)
        status_layout.setContentsMargins(8, 4, 8, 4)
        
        self.status_icon = QLabel("🔄")
        self.status_text = QLabel("Checking...")
        self.status_text.setFont(QFont("Arial", 9))
        
        status_layout.addWidget(self.status_icon)
        status_layout.addWidget(self.status_text)
        
        # Local files counter
        self.local_files_label = QLabel("📁 Local: 0")
        self.local_files_label.setFont(QFont("Arial", 9))
        
        # Sync button
        self.sync_button = QPushButton("🔄 Retry Sync")
        self.sync_button.setMaximumWidth(100)
        self.sync_button.clicked.connect(self.manual_sync)
        
        # Add widgets to layout
        layout.addWidget(self.status_frame)
        layout.addWidget(self.local_files_label)
        layout.addStretch()
        layout.addWidget(self.sync_button)
        
        # Apply theme
        self.apply_theme()
    
    def apply_theme(self):
        """Apply current theme to the widget"""
        is_dark = self.theme_manager.is_dark_mode
        
        # Main widget background
        bg_color = "#2d2d2d" if is_dark else "#f5f5f5"
        text_color = "#ffffff" if is_dark else "#000000"
        border_color = "#555555" if is_dark else "#cccccc"
        
        self.setStyleSheet(f"""
            QWidget {{
                background-color: {bg_color};
                color: {text_color};
                border: 1px solid {border_color};
                border-radius: 4px;
            }}
            QFrame {{
                background-color: {'#3d3d3d' if is_dark else '#ffffff'};
                border: 1px solid {border_color};
                border-radius: 4px;
            }}
            QPushButton {{
                background-color: #2980b9;
                color: white;
                border: none;
                padding: 4px 8px;
                border-radius: 4px;
                font-size: 10px;
            }}
            QPushButton:hover {{
                background-color: #3498db;
            }}
            QPushButton:disabled {{
                background-color: #7f8c8d;
            }}
        """)
    
    def update_status(self):
        """Update the sync status display"""
        try:
            status = self.sync_service.get_sync_status()
            
            # Update connection status
            if status['cloud_available']:
                self.status_icon.setText("☁️")
                self.status_text.setText("Online")
                self.status_frame.setStyleSheet("QFrame { background-color: #d5f4e6; }")
                self.sync_button.setEnabled(False)
                self.sync_button.setText("✅ Synced")
            else:
                self.status_icon.setText("📱")
                self.status_text.setText("Offline")
                self.status_frame.setStyleSheet("QFrame { background-color: #ffeaa7; }")
                self.sync_button.setEnabled(True)
                self.sync_button.setText("🔄 Retry")
            
            # Update local files count
            pending_count = status['pending_local_files']
            if pending_count > 0:
                self.local_files_label.setText(f"📁 Local: {pending_count}")
                self.local_files_label.setStyleSheet("color: #e17055; font-weight: bold;")
            else:
                self.local_files_label.setText("📁 Local: 0")
                self.local_files_label.setStyleSheet("color: #00b894; font-weight: normal;")
            
            # Update tooltip with detailed info
            tooltip = f"""
            Cloud Status: {'Online' if status['cloud_available'] else 'Offline'}
            Local Files: {pending_count}
            Storage Used: {status['total_local_size_mb']:.1f} MB
            Fallback Dir: {status['fallback_directory']}
            """
            self.setToolTip(tooltip.strip())
            
        except Exception as e:
            self.status_icon.setText("❌")
            self.status_text.setText("Error")
            self.status_frame.setStyleSheet("QFrame { background-color: #fab1a0; }")
            print(f"Sync status update error: {e}")
    
    def manual_sync(self):
        """Handle manual sync button click"""
        try:
            self.sync_button.setEnabled(False)
            self.sync_button.setText("🔄 Connecting...")
            
            # Attempt to reconnect
            success = self.sync_service.retry_cloud_connection()
            
            if success:
                QMessageBox.information(
                    self, 
                    "Sync Status", 
                    "✅ Successfully reconnected to cloud database!\n\nNew data will be saved to the cloud."
                )
            else:
                # Show local files info
                local_files = self.sync_service.list_local_files()
                file_count = len(local_files)
                
                msg = f"⚠️ Cloud connection still unavailable.\n\n"
                msg += f"📁 {file_count} files saved locally\n"
                msg += f"💾 Data will sync automatically when connection is restored"
                
                QMessageBox.warning(self, "Sync Status", msg)
            
            # Update status immediately
            self.update_status()
            
        except Exception as e:
            QMessageBox.critical(
                self, 
                "Sync Error", 
                f"❌ Sync retry failed:\n\n{str(e)}"
            )
            self.sync_button.setEnabled(True)
            self.sync_button.setText("🔄 Retry")
    
    def show_local_files(self):
        """Show dialog with local files information"""
        try:
            local_files = self.sync_service.list_local_files()
            
            if not local_files:
                QMessageBox.information(
                    self, 
                    "Local Files", 
                    "📁 No local files found.\n\nAll data is synced to the cloud."
                )
                return
            
            # Create file list message
            msg = f"📁 Local Files ({len(local_files)}):\n\n"
            for file_info in local_files[:10]:  # Show first 10 files
                size_kb = file_info['size_kb']
                msg += f"• {file_info['name']} ({size_kb:.1f} KB)\n"
            
            if len(local_files) > 10:
                msg += f"\n... and {len(local_files) - 10} more files"
            
            msg += f"\n\n💡 These files will sync automatically when cloud connection is restored."
            
            QMessageBox.information(self, "Local Files", msg)
            
        except Exception as e:
            QMessageBox.critical(
                self, 
                "Error", 
                f"❌ Could not load local files:\n\n{str(e)}"
            )
    
    def closeEvent(self, event):
        """Clean up when widget is closed"""
        if self.refresh_timer:
            self.refresh_timer.stop()
        event.accept()
