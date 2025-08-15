from typing import Tuple, Optional, Dict, Any
from services.auth_service import AuthService

class LoginController:
    def __init__(self):
        self.auth = AuthService()
        self.current_user = None

    def login(self, email: str, password: str) -> Tuple[bool, str, Optional[Dict[str, Any]]]:
        """
        Handle user login
        
        Args:
            email: User email address
            password: User password
            
        Returns:
            Tuple[bool, str, Optional[Dict]]: (success, message, user_data)
        """
        # Input validation
        if not email or not password:
            return False, "Email and password are required", None
        
        email = email.strip().lower()
        
        # Attempt login
        success, message, user_data = self.auth.login_user(email, password)
        
        if success:
            self.current_user = user_data
            print(f"✅ Login successful: {user_data.email if user_data else 'Unknown'}")
        else:
            self.current_user = None
            print(f"❌ Login failed: {message}")
        
        return success, message, user_data

    def register(self, email: str, password: str, confirm_password: str) -> Tuple[bool, str, Optional[Dict[str, Any]]]:
        """
        Handle user registration
        
        Args:
            email: User email address
            password: User password
            confirm_password: Password confirmation
            
        Returns:
            Tuple[bool, str, Optional[Dict]]: (success, message, user_data)
        """
        # Input validation
        if not email or not password or not confirm_password:
            return False, "All fields are required", None
        
        if password != confirm_password:
            return False, "Passwords do not match", None
        
        email = email.strip().lower()
        
        # Attempt registration
        success, message, user_data = self.auth.register_user(email, password)
        
        if success:
            print(f"✅ Registration successful: {email}")
        else:
            print(f"❌ Registration failed: {message}")
        
        return success, message, user_data

    def logout(self) -> Tuple[bool, str]:
        """
        Handle user logout
        
        Returns:
            Tuple[bool, str]: (success, message)
        """
        success, message = self.auth.logout_user()
        
        if success:
            self.current_user = None
            print("✅ Logout successful")
        else:
            print(f"❌ Logout failed: {message}")
        
        return success, message

    def is_authenticated(self) -> bool:
        """Check if user is currently authenticated"""
        return self.auth.is_authenticated()

    def get_current_user(self) -> Optional[Dict[str, Any]]:
        """Get current authenticated user"""
        if not self.current_user:
            self.current_user = self.auth.get_current_user()
        return self.current_user

    def get_user_id(self) -> Optional[str]:
        """Get current user ID"""
        return self.auth.get_user_id()

    def get_user_email(self) -> Optional[str]:
        """Get current user email"""
        return self.auth.get_user_email()

    def refresh_user_session(self) -> bool:
        """Refresh current user session"""
        try:
            self.current_user = self.auth.get_current_user()
            return self.current_user is not None
        except Exception as e:
            print(f"Session refresh failed: {e}")
            self.current_user = None
            return False

    def validate_session(self) -> bool:
        """Validate current session is still active"""
        return self.refresh_user_session()