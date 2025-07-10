from PyQt5.QtWidgets import QMessageBox, QLabel, QProgressBar
from resolvers.engine import match_transcript_with_curriculum, generate_progress_summary, suggest_electives


class DataProcessor:
    """
    Handles the processing of transcript and curriculum data, including:
    - Data matching and analysis
    - Results generation
    - UI updates for results
    """
    
    def __init__(self, parent):
        """
        Initialize the data processor
        
        Args:
            parent: The main window instance this processor is attached to
        """
        self.parent = parent
        self.transcript_df = None
        self.curriculum_df = None
        self.results_df = None
        self.student_name = "Student"
        self.university = "Torrens University"
    
    def set_transcript_data(self, dataframe):
        """Set the transcript dataframe"""
        self.transcript_df = dataframe
        self._extract_student_info()
        
    def set_curriculum_data(self, dataframe):
        """Set the curriculum dataframe"""
        self.curriculum_df = dataframe
    
    def _extract_student_info(self):
        """Extract student information from the transcript dataframe"""
        if self.transcript_df is None:
            return
            
        try:
            # Check if metadata columns exist - common formats for transcript data
            if 'Student Name' in self.transcript_df.columns:
                self.student_name = self.transcript_df['Student Name'].iloc[0]
            elif 'Name' in self.transcript_df.columns:
                self.student_name = self.transcript_df['Name'].iloc[0]
            else:
                self.student_name = "Student"
                
            if 'University' in self.transcript_df.columns:
                self.university = self.transcript_df['University'].iloc[0]
            elif 'Institution' in self.transcript_df.columns:
                self.university = self.transcript_df['Institution'].iloc[0]
            else:
                self.university = "Torrens University"
        except (AttributeError, IndexError, KeyError):
            # Fallback to defaults if extraction fails
            self.student_name = "Student"
            self.university = "Torrens University"
    
    def process_data(self):
        """
        Process the loaded data and display results
        
        Returns:
            bool: True if processing succeeded, False otherwise
        """
        if self.transcript_df is None or self.curriculum_df is None:
            return False
        
        try:
            # Process the data using engine functions
            self.results_df = match_transcript_with_curriculum(
                self.transcript_df, self.curriculum_df)
            summary_df = generate_progress_summary(self.results_df)
            electives_df = suggest_electives(self.results_df)
            
            # Populate tables using helpers
            self.parent.helpers.populate_table(self.parent.results_table, self.results_df)
            self.parent.helpers.populate_table(self.parent.summary_table, summary_df)
            self.parent.helpers.populate_table(self.parent.electives_table, electives_df)
            
            # Update header labels with student info
            header_label = self.parent.results_tab.findChild(QLabel, "header_label")
            sub_header = self.parent.results_tab.findChild(QLabel, "sub_header")
            
            if header_label:
                header_label.setText(f"Student: {self.student_name}")
            
            if sub_header:
                sub_header.setText(f"University: {self.university}")

            # Degree progress bar % based on DONE vs Total subjects
            total_done = summary_df["✅ Done"].sum()
            total_subjects = summary_df["Total"].sum()
            progress = int(total_done / total_subjects * 100) if total_subjects > 0 else 0
            
            # Update progress bar if present
            for progress_bar in self.parent.results_tab.findChildren(QProgressBar):
                progress_bar.setValue(progress)
                print(f"Updated progress bar: {progress}%")
                break
            
            return True
            
        except Exception as e:
            QMessageBox.critical(
                self.parent, 
                "Error", 
                f"Failed to process data: {str(e)}\n\nPlease ensure your files are in the correct format."
            )
            raise
