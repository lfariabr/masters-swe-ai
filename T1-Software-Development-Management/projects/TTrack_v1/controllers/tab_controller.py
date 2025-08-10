from PyQt5.QtWidgets import QTabWidget
from gui.tab_input import setup_input_tab
from gui.tab_results import setup_results_tab
from gui.tab_studentrecords import setup_studentrecords_tab
from gui.tab_login import setup_login_tab

class TabController:
    """
    Manages application tab interactions, including:
    - Tab initialization
    - Tab switching
    - Tab state management (enabled/disabled)
    """
    
    def __init__(self, parent):
        """
        Initialize the tab controller
        
        Args:
            parent: The main window instance this controller is attached to
        """
        self.parent = parent
        self.tabs = None
        self.input_tab = None
        self.results_tab = None
        self.login_tab = None
        
    def initialize_tabs(self):
        """
        Initialize the tab widget and add tabs
        
        Returns:
            QTabWidget: The configured tab widget
        """
        
        # Create tab widget
        self.tabs = QTabWidget()
        
        # Create and add tabs
        self.login_tab = setup_login_tab(self.parent)
        self.input_tab = setup_input_tab(self.parent)
        self.results_tab = setup_results_tab(self.parent)
        self.studentrecords_tab = setup_studentrecords_tab(self.parent)
            
        # Add tabs to the tab widget
        # Tab indices:
        # 0 - Login, 1 - Input, 2 - Results, 3 - Student Records
        self.tabs.addTab(self.login_tab, "Login") 
        self.tabs.addTab(self.input_tab, "Input") 
        self.tabs.addTab(self.results_tab, "Results") 
        self.tabs.addTab(self.studentrecords_tab, "Student Records") 
        
        # Initially disable results tab
        self.disable_results_tab()
        
        return self.tabs
    
    def enable_results_tab(self):
        """Enable the results tab and switch to it"""
        if self.tabs:
            # Find the Results tab index dynamically (handles login tab removal)
            results_index = -1
            for i in range(self.tabs.count()):
                if self.tabs.tabText(i) == "Results":
                    results_index = i
                    break
            
            if results_index >= 0:
                self.tabs.setTabEnabled(results_index, True)
                self.tabs.setCurrentIndex(results_index)
                print(f"✅ Switched to Results tab at index {results_index}")
            else:
                print("❌ Results tab not found!")
    
    def switch_to_student_records(self):
        """Switch to the Student Records tab"""
        if self.tabs:
            # Find the Student Records tab index dynamically
            student_records_index = -1
            for i in range(self.tabs.count()):
                if self.tabs.tabText(i) == "Student Records":
                    student_records_index = i
                    break
            
            if student_records_index >= 0:
                self.tabs.setCurrentIndex(student_records_index)
                print(f"✅ Switched to Student Records tab at index {student_records_index}")
            else:
                print("❌ Student Records tab not found!")
    
    def disable_results_tab(self):
        """Disable the results tab"""
        if self.tabs:
            # Find the Results tab index dynamically
            for i in range(self.tabs.count()):
                if self.tabs.tabText(i) == "Results":
                    self.tabs.setTabEnabled(i, False)
                    break
    
    def hide_tabs(self):
        if self.tabs:
            self.tabs.hide()
    
    def get_input_tab(self):
        """Get the input tab widget"""
        return self.input_tab
    
    def get_results_tab(self):
        """Get the results tab widget"""
        return self.results_tab
    
    def get_login_tab(self):
        """Get the login tab widget"""
        return self.login_tab
    
    def enable_all_tabs(self):
        """Enable all tabs"""
        if self.tabs:
            for i in range(self.tabs.count()):
                self.tabs.setTabEnabled(i, True)

    def hide_login_tab(self):
        """Hide the login tab after successful login"""
        if self.tabs:
            # Find and remove the login tab
            for i in range(self.tabs.count()):
                if self.tabs.tabText(i) == "Login":
                    self.tabs.removeTab(i)
                    break
