from PyQt5.QtWidgets import QMessageBox, QLabel, QProgressBar
from resolvers.engine import match_transcript_with_curriculum, generate_progress_summary, suggest_electives
import uuid
import pandas as pd

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

            # # Database Integration
            # self._save_to_database(summary_df, electives_df, progress)
            
            return True
            
        except Exception as e:
            QMessageBox.critical(
                self.parent, 
                "Error", 
                f"Failed to process data: {str(e)}\n\nPlease ensure your files are in the correct format."
            )
            raise
    
    # def _save_to_database(self, summary_df, electives_df, progress):
    #     """
    #     Save processed session data to database
        
    #     Args:
    #         summary_df: Summary dataframe with progress data
    #         electives_df: Electives suggestions dataframe  
    #         progress: Progress percentage as integer
    #     """
    #     try:
    #         user_id = f"{self.student_name}_{uuid.uuid4().hex[:8]}"
    #         db_manager = self.parent.database_manager

    #         if db_manager and db_manager.supabase:
    #             # Save transcript data
    #             transcript_result = db_manager.save_transcript(user_id, self.transcript_df)
    #             if transcript_result:
    #                 print(f"✅ Transcript saved with ID: {transcript_result.get('id')}")
                
    #             # Save curriculum data  
    #             curriculum_result = db_manager.save_curriculum(user_id, self.curriculum_df)
    #             if curriculum_result:
    #                 print(f"✅ Curriculum saved with ID: {curriculum_result.get('id')}")
                
    #             # Save processed session data
    #             session_result = db_manager.save_processed_data(
    #                 user_id, 
    #                 self.results_df, 
    #                 summary_df, 
    #                 electives_df, 
    #                 progress
    #             )
    #             if session_result:
    #                 session_id = session_result.get('id')
    #                 print(f"✅ Session saved with ID: {session_id}")
                    
    #                 # Store session_id for potential UI display
    #                 self.last_session_id = session_id
                    
    #                 # Optional: Show success message to user
    #                 QMessageBox.information(
    #                     self.parent,
    #                     "Data Saved",
    #                     f"Success! Data saved successfully!"
    #                 )
    #             else:
    #                 print("⚠️ Failed to save session data")
    #         else:
    #             print("⚠️ Database not available - data not saved")
                
    #     except Exception as e:
    #         print(f"❌ Database save error: {e}")
    #         # Don't show error to user - processing was successful, just save failed

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
            user_id = f"{self.student_name}_{uuid.uuid4().hex[:8]}"
            
            # Access database manager from parent
            db_manager = self.parent.database_manager
            
            if not (db_manager and db_manager.supabase):
                return False
            
            # Calculate progress from current data
            from resolvers.engine import generate_progress_summary
            summary_df = generate_progress_summary(self.results_df)
            electives_df = pd.DataFrame({'status': ['electives_placeholder']})  # Placeholder
            
            total_done = summary_df["✅ Done"].sum() if "✅ Done" in summary_df.columns else 0
            total_subjects = summary_df["Total"].sum() if "Total" in summary_df.columns else 1
            progress = int(total_done / total_subjects * 100) if total_subjects > 0 else 0
            
            # Save all data
            transcript_result = db_manager.save_transcript(user_id, self.transcript_df)
            curriculum_result = db_manager.save_curriculum(user_id, self.curriculum_df)
            session_result = db_manager.save_processed_data(
                user_id, self.results_df, summary_df, electives_df, progress
            )
            
            if transcript_result and curriculum_result and session_result:
                session_id = session_result.get('id')
                print(f"✅ Session saved with ID: {session_id}")
                self.last_session_id = session_id
                return True
            
            return False
            
        except Exception as e:
            print(f"❌ Database save error: {e}")
            return False