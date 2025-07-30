import os
import json
import pandas as pd
from supabase import Client, create_client
from dotenv import load_dotenv
from typing import Optional, Dict, Any
from datetime import datetime

load_dotenv()

class DatabaseManager:
    def __init__(self, parent):
        self.parent = parent
        print("DatabaseManager initialized")
        try:
            self.supabase = create_client(
                os.getenv("SUPABASE_URL"),
                os.getenv("SUPABASE_KEY")
            )
            self.connect_to_db()
        except Exception as e:
            print(f"Failed to initialize Supabase client: {e}")
            self.supabase = None

    def connect_to_db(self) -> bool:
        """
        Test database connection
        """
        try:
            response = self.supabase.table('transcripts').select('*').limit(1).execute()
            print("DatabaseManager connected successfully")
            return True
        except Exception as e:
            print(f"Database connection failed: {e}")
            return False

    def create_db(self):
        """
        Database tables are created via Supabase dashboard
        """
        print("Database tables managed via Supabase dashboard")
    
    def close_db(self):
        """
        Cleanup connection resources
        """
        print("Database connection closed")
    
    def save_transcript(self, user_id: str, transcript_df: pd.DataFrame) -> Optional[Dict[str, Any]]:
        """
        Save transcript to database
        """
        try:
            transcript_data = {
                'user_id': user_id,
                'transcript_data': transcript_df.to_json(orient='records'),
                'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            }
            response = self.supabase.table('transcripts').insert(transcript_data).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Error saving transcript: {e}")
            return None
            
    def save_curriculum(self, user_id: str, curriculum_df: pd.DataFrame) -> Optional[Dict[str, Any]]:
        """
        Save curriculum to database
        """
        try:
            curriculum_data = {
                'user_id': user_id,
                'curriculum_data': curriculum_df.to_json(orient='records'),
                'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            }
            response = self.supabase.table('curriculums').insert(curriculum_data).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Error saving curriculum: {e}")
            return None

    def save_processed_data(self, user_id: str, results_table: pd.DataFrame,
                        summary_table: pd.DataFrame, electives_table: pd.DataFrame,
                        progress: float) -> Optional[Dict[str, Any]]:
        """
        Save processed data to database
        """
        try:
            session_data = {
                'user_id': user_id,
                'results_data': results_table.to_json(orient='records'),
                'summary_data': summary_table.to_json(orient='records'),
                'electives_data': electives_table.to_json(orient='records'),
                'progress': progress,
                'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            }
            response = self.supabase.table('student_records').insert(session_data).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Error saving processed data: {e}")
            return None

    def fetch_user_history(self, user_id):
        """
        Fetch all sessions for a user
        """
        try:
            response = self.supabase.table('student_records').select('*').eq('user_id', user_id).execute()
            return response.data if response.data else None
        except Exception as e:
            print(f"Error fetching user history: {e}")
            return None

    def get_entry_by_id(self, entry_id):
        """
        Get specific session by ID
        """
        try:
            response = self.supabase.table('student_records').select('*').eq('id', entry_id).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Error getting entry by ID: {e}")
            return None

    def delete_entry(self, entry_id):
        """
        Delete specific session by ID
        """
        try:
            response = self.supabase.table('student_records').delete().eq('id', entry_id).execute()
            return len(response.data) > 0
        except Exception as e:
            print(f"Error deleting entry: {e}")
            return False