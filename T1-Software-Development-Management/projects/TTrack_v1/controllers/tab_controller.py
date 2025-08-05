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
            self.tabs.setTabEnabled(2, True) # index 2, appears only after data processed
            self.tabs.setCurrentIndex(2) # index 2, appears only after data processed
    
    def disable_results_tab(self):
        """Disable the results tab"""
        if self.tabs:
            self.tabs.setTabEnabled(2, False) # index 2, appears only after data processed
    
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
