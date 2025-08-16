from PyQt5.QtWidgets import QMessageBox, QLabel, QProgressBar
import uuid
import pandas as pd

from core.engine import (
    match_transcript_with_curriculum,
    generate_progress_summary,
    suggest_electives,
    suggest_electives_v2,
    generate_progress_summary_v2,
    match_transcript_with_curriculum_v2
)

# Import course data loader
from data.courses.msit_ad import load_curriculum_df, load_elective_bank_df
from data.courses.adit21 import load_curriculum_adit_df, load_elective_bank_adit_df


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
        Args: parent: The main window instance this processor is attached to
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
        """
        Extract student information from the transcript dataframe
        """
        if self.transcript_df is None:
            return
            
        try:
            # Check if metadata columns exist - common formats for transcript data
            if 'Student Name' in self.transcript_df.columns:
                self.student_name = self.transcript_df['Student Name'].iloc[0]
            else:
                self.student_name = "Student"
                
            if 'University' in self.transcript_df.columns:
                self.university = self.transcript_df['University'].iloc[0]
            else:
                self.university = "Torrens University"
                
        except (AttributeError, IndexError, KeyError):
            # Fallback to defaults if extraction fails
            self.student_name = "Student"
            self.university = "Torrens University"
    
    def process_data(self, use_enhanced=True):
        """
        Process the loaded data and display results
        Args: use_enhanced (bool): Use enhanced v2 engine with canonical course data
        Returns: bool: True if processing succeeded, False otherwise
        """
        if use_enhanced:
            return self.process_data_v2()
        else:
            return self.process_data_legacy()
    
    def process_data_legacy(self):
        """
        Legacy processing method (original implementation)
        Args: None
        Returns: bool: True if processing succeeded, False otherwise
        """
        if self.transcript_df is None or self.curriculum_df is None:
            return False
        
        try:
            # Process the data using original engine functions
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
    
    def process_data_v2(self):
        """
        Enhanced processing using canonical course data and v2 engine functions after meeting with Dr. Atif
        Args: None
        Returns: bool: True if processing succeeded, False otherwise
        """
        if self.transcript_df is None: # here we ignore curriculum_df as it is pulling from hardcoded data
            return False
        
        try:
            # Load canonical course structures that we took from ***"MSIT Course Structure TUA.pdf"***
            curriculum_df = load_curriculum_adit_df() # load_curriculum_df or load_curriculum_adit_df
            elective_bank_df = load_elective_bank_adit_df() # load_elective_bank_df or load_elective_bank_adit_df
            
            # Process using enhanced v2 engine
            self.results_df = match_transcript_with_curriculum_v2(
                self.transcript_df, curriculum_df, elective_bank_df)
            summary_df = generate_progress_summary_v2(self.results_df)
            electives_df = suggest_electives_v2(
                self.results_df, elective_bank_df, self.transcript_df, max_electives=3)
            
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

            # Calculate progress from v2 summary
            total_done = summary_df["✅ Done"].sum() if "✅ Done" in summary_df.columns else 0
            total_subjects = summary_df["Total"].sum() if "Total" in summary_df.columns else 1
            progress = int(total_done / total_subjects * 100) if total_subjects > 0 else 0
            
            # Update progress bar if present
            for progress_bar in self.parent.results_tab.findChildren(QProgressBar):
                progress_bar.setValue(progress)
                print(f"Updated progress bar: {progress}%")
                break

            print(f"✅ Enhanced processing complete - {len(self.results_df)} subjects analyzed")
            return True
            
        except Exception as e:
            QMessageBox.critical(
                self.parent, 
                "Error", 
                f"Failed to process data with enhanced engine: {str(e)}\n\nPlease ensure your transcript file is in the correct format."
            )
            print(f"❌ Enhanced processing error: {e}")
            return False
    
    def save_session_to_database(self):
        """
        Save current session data to database (called manually from UI)
        
        Returns:
            bool: True if save was successful, False otherwise
        """
        if self.results_df is None or self.transcript_df is None or self.curriculum_df is None:
            return False
            
        try:
            # Generate unique user_id for this session
            # user_id = f"{self.student_name}_{uuid.uuid4().hex[:8]}"

            # Generate user_id from login controller
            user_id = self.parent.login_controller.get_user_id()

            # Access database manager from parent
            db_manager = self.parent.database_manager
            
            if not (db_manager and db_manager.supabase):
                return False
            
            # Calculate progress from current data
            summary_df = generate_progress_summary(self.results_df)
            electives_df = suggest_electives(self.results_df)  # Generate actual electives data
            
            total_done = summary_df["✅ Done"].sum() if "✅ Done" in summary_df.columns else 0
            total_subjects = summary_df["Total"].sum() if "Total" in summary_df.columns else 1
            progress = int(total_done / total_subjects * 100) if total_subjects > 0 else 0
            
            # Extract credit points from transcript data
            total_credit_points = 0
            try:
                # Look for common credit point column names
                credit_columns = ['Credit Points']
                for col in credit_columns:
                    if col in self.transcript_df.columns:
                        # Sum all credit points, converting to numeric and handling NaN
                        credit_points = pd.to_numeric(self.transcript_df[col], errors='coerce').fillna(0).sum()
                        total_credit_points = int(credit_points)
                        break
            except Exception as e:
                print(f"Warning: Could not extract credit points: {e}")
                total_credit_points = 0
            
            # Save all data with additional fields
            transcript_result = db_manager.save_transcript(user_id, self.transcript_df)
            curriculum_result = db_manager.save_curriculum(user_id, self.curriculum_df)
            session_result = db_manager.save_processed_data(
                user_id, self.results_df, summary_df, electives_df, progress,
                student_name=self.student_name, credit_points=total_credit_points
            )
            
            if transcript_result and curriculum_result and session_result:
                session_id = session_result.get('id')
                print(f"✅ Session saved with ID: {session_id}")
                self.last_session_id = session_id
                return True
            else:
                print("❌ Failed to save session data")
                return False
            
        except Exception as e:
            print(f"❌ Database save error: {e}")
            return False
    
    def save_session_to_database_v2(self):
        """
        Save current session data to database (v2 processing pattern)
        Returns:
            bool: True if save was successful, False otherwise
        """
        if self.results_df is None or self.transcript_df is None:
            return False

        try:
            # Use login-based user_id (same as legacy)
            user_id = self.parent.login_controller.get_user_id()

            # Access database manager
            db_manager = self.parent.database_manager
            if not (db_manager and db_manager.supabase):
                return False

            # Load canonical curriculum + elective bank (same source as process_data_v2)
            curriculum_df = load_curriculum_df()
            elective_bank_df = load_elective_bank_df()

            # Calculate summary + electives using v2 functions
            summary_df = generate_progress_summary_v2(self.results_df)
            electives_df = suggest_electives_v2(
                self.results_df,
                elective_bank_df,
                self.transcript_df,
                max_electives=3
            )

            # Progress %
            total_done = summary_df["✅ Done"].sum() if "✅ Done" in summary_df.columns else 0
            total_subjects = summary_df["Total"].sum() if "Total" in summary_df.columns else 1
            progress = int(total_done / total_subjects * 100) if total_subjects > 0 else 0

            # Credit points
            total_credit_points = 0
            try:
                if "Credit Points" in self.transcript_df.columns:
                    credit_points = pd.to_numeric(
                        self.transcript_df["Credit Points"], errors='coerce'
                    ).fillna(0).sum()
                    total_credit_points = int(credit_points)
            except Exception as e:
                print(f"Warning: Could not extract credit points: {e}")

            # Save to DB
            transcript_result = db_manager.save_transcript(user_id, self.transcript_df)
            curriculum_result = db_manager.save_curriculum(user_id, curriculum_df)
            session_result = db_manager.save_processed_data(
                user_id,
                self.results_df,
                summary_df,
                electives_df,
                progress,
                student_name=self.student_name,
                credit_points=total_credit_points
            )

            if transcript_result and curriculum_result and session_result:
                session_id = session_result.get('id')
                print(f"✅ Session saved with ID: {session_id}")
                self.last_session_id = session_id
                return True
            else:
                print("❌ Failed to save session data")
                return False

        except Exception as e:
            print(f"❌ Database save error: {e}")
            return False