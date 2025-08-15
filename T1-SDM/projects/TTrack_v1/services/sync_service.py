"""
TTrack Sync Service - v3.4.0 Cloud Sync with Fallback
Provides cloud database sync with local CSV fallback when offline
"""

import os
import json
import pandas as pd
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any, Tuple, List
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

class SyncService:
    """
    Cloud sync service with local fallback capabilities
    Handles both online (Supabase) and offline (CSV) data persistence
    """
    
    def __init__(self, database_manager=None, fallback_dir="data/local"):
        """
        Initialize sync service
        
        Args:
            database_manager: DatabaseManager instance for cloud sync
            fallback_dir: Directory for local CSV fallback files
        """
        self.database_manager = database_manager
        self.fallback_dir = Path(fallback_dir)
        self.fallback_dir.mkdir(parents=True, exist_ok=True)
        
        # Connection status
        self.is_cloud_available = False
        self.last_sync_attempt = None
        
        # Setup logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
        # Test cloud connection on initialization
        self._test_cloud_connection()
    
    def _test_cloud_connection(self) -> bool:
        """
        Test if cloud database is available
        
        Returns:
            bool: True if cloud is available, False otherwise
        """
        try:
            if self.database_manager and hasattr(self.database_manager, 'supabase'):
                # Simple ping to test connection
                response = self.database_manager.supabase.table('transcripts').select('id').limit(1).execute()
                self.is_cloud_available = True
                self.logger.info("✅ Cloud database connection successful")
                return True
        except Exception as e:
            self.is_cloud_available = False
            self.logger.warning(f"⚠️ Cloud database unavailable: {e}")
            return False
        
        self.is_cloud_available = False
        return False
    
    def _get_fallback_filename(self, data_type: str, user_id: str) -> Path:
        """
        Generate fallback CSV filename
        
        Args:
            data_type: Type of data (transcript, curriculum, session)
            user_id: User identifier
            
        Returns:
            Path: Full path to fallback CSV file
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{data_type}_{user_id[:8]}_{timestamp}.csv"
        return self.fallback_dir / filename
    
    def save_transcript(self, user_id: str, transcript_df: pd.DataFrame) -> Tuple[bool, str, Optional[Dict]]:
        """
        Save transcript with cloud sync and local fallback
        
        Args:
            user_id: User identifier
            transcript_df: Transcript DataFrame
            
        Returns:
            Tuple[bool, str, Optional[Dict]]: (success, message, data)
        """
        # Try cloud first
        if self.is_cloud_available and self.database_manager:
            try:
                result = self.database_manager.save_transcript(user_id, transcript_df)
                if result:
                    self.logger.info(f"✅ Transcript saved to cloud for user {user_id[:8]}...")
                    return True, "Saved to cloud database", result
            except Exception as e:
                self.logger.error(f"❌ Cloud save failed: {e}")
                self.is_cloud_available = False
        
        # Fallback to local CSV
        try:
            fallback_file = self._get_fallback_filename("transcript", user_id)
            
            # Add metadata
            transcript_with_meta = transcript_df.copy()
            transcript_with_meta['user_id'] = user_id
            transcript_with_meta['saved_at'] = datetime.now().isoformat()
            transcript_with_meta['sync_status'] = 'pending_cloud_sync'
            
            # Save to CSV
            transcript_with_meta.to_csv(fallback_file, index=False)
            
            self.logger.info(f"💾 Transcript saved locally: {fallback_file.name}")
            return True, f"Saved locally (offline mode): {fallback_file.name}", {"local_file": str(fallback_file)}
            
        except Exception as e:
            self.logger.error(f"❌ Local save failed: {e}")
            return False, f"Save failed: {e}", None
    
    def save_curriculum(self, user_id: str, curriculum_df: pd.DataFrame) -> Tuple[bool, str, Optional[Dict]]:
        """
        Save curriculum with cloud sync and local fallback
        
        Args:
            user_id: User identifier
            curriculum_df: Curriculum DataFrame
            
        Returns:
            Tuple[bool, str, Optional[Dict]]: (success, message, data)
        """
        # Try cloud first
        if self.is_cloud_available and self.database_manager:
            try:
                result = self.database_manager.save_curriculum(user_id, curriculum_df)
                if result:
                    self.logger.info(f"✅ Curriculum saved to cloud for user {user_id[:8]}...")
                    return True, "Saved to cloud database", result
            except Exception as e:
                self.logger.error(f"❌ Cloud save failed: {e}")
                self.is_cloud_available = False
        
        # Fallback to local CSV
        try:
            fallback_file = self._get_fallback_filename("curriculum", user_id)
            
            # Add metadata
            curriculum_with_meta = curriculum_df.copy()
            curriculum_with_meta['user_id'] = user_id
            curriculum_with_meta['saved_at'] = datetime.now().isoformat()
            curriculum_with_meta['sync_status'] = 'pending_cloud_sync'
            
            # Save to CSV
            curriculum_with_meta.to_csv(fallback_file, index=False)
            
            self.logger.info(f"💾 Curriculum saved locally: {fallback_file.name}")
            return True, f"Saved locally (offline mode): {fallback_file.name}", {"local_file": str(fallback_file)}
            
        except Exception as e:
            self.logger.error(f"❌ Local save failed: {e}")
            return False, f"Save failed: {e}", None
    
    def save_processed_data(self, user_id: str, results_df: pd.DataFrame, 
                          summary_df: pd.DataFrame, electives_df: pd.DataFrame, 
                          progress: int) -> Tuple[bool, str, Optional[Dict]]:
        """
        Save processed session data with cloud sync and local fallback
        
        Args:
            user_id: User identifier
            results_df: Results DataFrame
            summary_df: Summary DataFrame
            electives_df: Electives DataFrame
            progress: Progress percentage
            
        Returns:
            Tuple[bool, str, Optional[Dict]]: (success, message, data)
        """
        # Try cloud first
        if self.is_cloud_available and self.database_manager:
            try:
                result = self.database_manager.save_processed_data(
                    user_id, results_df, summary_df, electives_df, progress
                )
                if result:
                    self.logger.info(f"✅ Session saved to cloud for user {user_id[:8]}...")
                    return True, "Saved to cloud database", result
            except Exception as e:
                self.logger.error(f"❌ Cloud save failed: {e}")
                self.is_cloud_available = False
        
        # Fallback to local CSV
        try:
            # Create session directory
            session_timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            session_dir = self.fallback_dir / f"session_{user_id[:8]}_{session_timestamp}"
            session_dir.mkdir(exist_ok=True)
            
            # Save each DataFrame separately
            results_df.to_csv(session_dir / "results.csv", index=False)
            summary_df.to_csv(session_dir / "summary.csv", index=False)
            electives_df.to_csv(session_dir / "electives.csv", index=False)
            
            # Save session metadata
            metadata = {
                "user_id": user_id,
                "progress": progress,
                "saved_at": datetime.now().isoformat(),
                "sync_status": "pending_cloud_sync",
                "session_id": session_timestamp
            }
            
            with open(session_dir / "metadata.json", 'w') as f:
                json.dump(metadata, f, indent=2)
            
            self.logger.info(f"💾 Session saved locally: {session_dir.name}")
            return True, f"Saved locally (offline mode): {session_dir.name}", {"local_dir": str(session_dir)}
            
        except Exception as e:
            self.logger.error(f"❌ Local save failed: {e}")
            return False, f"Save failed: {e}", None
    
    def get_sync_status(self) -> Dict[str, Any]:
        """
        Get current sync status and statistics
        
        Returns:
            Dict: Sync status information
        """
        # Count local files pending sync
        pending_files = list(self.fallback_dir.glob("**/*"))
        pending_count = len([f for f in pending_files if f.is_file() and f.suffix == '.csv'])
        
        return {
            "cloud_available": self.is_cloud_available,
            "last_sync_attempt": self.last_sync_attempt,
            "pending_local_files": pending_count,
            "fallback_directory": str(self.fallback_dir),
            "total_local_size_mb": sum(f.stat().st_size for f in pending_files if f.is_file()) / (1024*1024)
        }
    
    def retry_cloud_connection(self) -> bool:
        """
        Retry cloud connection and return status
        
        Returns:
            bool: True if connection successful
        """
        self.last_sync_attempt = datetime.now()
        return self._test_cloud_connection()
    
    def list_local_files(self) -> List[Dict[str, Any]]:
        """
        List all local fallback files
        
        Returns:
            List[Dict]: List of local files with metadata
        """
        files = []
        for file_path in self.fallback_dir.rglob("*"):
            if file_path.is_file():
                files.append({
                    "name": file_path.name,
                    "path": str(file_path),
                    "size_kb": file_path.stat().st_size / 1024,
                    "modified": datetime.fromtimestamp(file_path.stat().st_mtime).isoformat(),
                    "type": file_path.suffix
                })
        
        return sorted(files, key=lambda x: x['modified'], reverse=True)
