from PyQt5.QtWidgets import QTabWidget

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
        
    def initialize_tabs(self):
        """
        Initialize the tab widget and add tabs
        
        Returns:
            QTabWidget: The configured tab widget
        """
        from ui.tab_input import setup_input_tab
        from ui.tab_results import setup_results_tab
        from ui.tab_studentrecords import setup_studentrecords_tab
        
        # Create tab widget
        self.tabs = QTabWidget()
        
        # Create and add tabs
        self.input_tab = setup_input_tab(self.parent)
        self.results_tab = setup_results_tab(self.parent)
        self.studentrecords_tab = setup_studentrecords_tab(self.parent)
        
        # Add tabs to the tab widget
        self.tabs.addTab(self.input_tab, "Input")
        self.tabs.addTab(self.results_tab, "Results")
        self.tabs.addTab(self.studentrecords_tab, "Student Records")
        
        # Initially disable results tab
        self.disable_results_tab()
        
        return self.tabs
    
    def enable_results_tab(self):
        """Enable the results tab and switch to it"""
        if self.tabs:
            self.tabs.setTabEnabled(1, True)
            self.tabs.setCurrentIndex(1)
    
    def disable_results_tab(self):
        """Disable the results tab"""
        if self.tabs:
            self.tabs.setTabEnabled(1, False)
    
    def get_input_tab(self):
        """Get the input tab widget"""
        return self.input_tab
    
    def get_results_tab(self):
        """Get the results tab widget"""
        return self.results_tab
