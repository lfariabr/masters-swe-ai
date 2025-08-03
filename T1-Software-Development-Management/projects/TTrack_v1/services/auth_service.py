import os
import re
from typing import Optional, Dict, Any, Tuple
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()

class AuthService:
    def __init__(self):
        try:
            self.supabase = create_client(
                os.getenv("SUPABASE_URL"),
                os.getenv("SUPABASE_KEY")
            )
            self.current_user = None
            print("AuthService initialized.")
        except Exception as e:
            print(f"Failed to initialize Supabase client: {e}")
            self.supabase = None
            self.current_user = None

    def _validate_email(self, email: str) -> bool:
        """Validate email format"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None

    def _validate_password(self, password: str) -> Tuple[bool, str]:
        """Validate password strength"""
        if len(password) < 8:
            return False, "Password must be at least 8 characters long"
        if not re.search(r'[A-Z]', password):
            return False, "Password must contain at least one uppercase letter"
        if not re.search(r'[a-z]', password):
            return False, "Password must contain at least one lowercase letter"
        if not re.search(r'\d', password):
            return False, "Password must contain at least one number"
        return True, "Password is valid"

    def register_user(self, email: str, password: str) -> Tuple[bool, str, Optional[Dict[str, Any]]]:
        """
        Register a new user
        
        Returns:
            Tuple[bool, str, Optional[Dict]]: (success, message, user_data)
        """
        if not self.supabase:
            return False, "Authentication service not available", None

        # Validate inputs
        if not self._validate_email(email):
            return False, "Invalid email format", None
        
        password_valid, password_msg = self._validate_password(password)
        if not password_valid:
            return False, password_msg, None

        try:
            result = self.supabase.auth.sign_up({
                "email": email,
                "password": password
            })
            
            if result.user:
                return True, "Registration successful. Please check your email for verification.", result.user
            else:
                return False, "Registration failed. Please try again.", None
                
        except Exception as e:
            error_msg = str(e)
            if "already registered" in error_msg.lower():
                return False, "Email already registered. Please use a different email or try logging in.", None
            elif "invalid email" in error_msg.lower():
                return False, "Invalid email address", None
            else:
                print(f"Registration error: {e}")
                return False, "Registration failed. Please try again later.", None

    def login_user(self, email: str, password: str) -> Tuple[bool, str, Optional[Dict[str, Any]]]:
        """
        Login user with email and password
        
        Returns:
            Tuple[bool, str, Optional[Dict]]: (success, message, user_data)
        """
        if not self.supabase:
            return False, "Authentication service not available", None

        if not self._validate_email(email):
            return False, "Invalid email format", None

        try:
            result = self.supabase.auth.sign_in_with_password({
                "email": email,
                "password": password
            })
            
            if result.user:
                self.current_user = result.user
                return True, "Login successful", result.user
            else:
                return False, "Login failed. Please check your credentials.", None
                
        except Exception as e:
            error_msg = str(e)
            if "invalid login credentials" in error_msg.lower():
                return False, "Invalid email or password", None
            elif "email not confirmed" in error_msg.lower():
                return False, "Please verify your email before logging in", None
            else:
                print(f"Login error: {e}")
                return False, "Login failed. Please try again later.", None

    def logout_user(self) -> Tuple[bool, str]:
        """
        Logout current user
        
        Returns:
            Tuple[bool, str]: (success, message)
        """
        if not self.supabase:
            return False, "Authentication service not available"

        try:
            self.supabase.auth.sign_out()
            self.current_user = None
            return True, "Logout successful"
        except Exception as e:
            print(f"Logout error: {e}")
            return False, "Logout failed. Please try again."

    def get_current_user(self) -> Optional[Dict[str, Any]]:
        """
        Get current authenticated user
        
        Returns:
            Optional[Dict]: User data if authenticated, None otherwise
        """
        if not self.supabase:
            return None

        try:
            user = self.supabase.auth.get_user()
            if user and user.user:
                self.current_user = user.user
                return user.user
            else:
                self.current_user = None
                return None
        except Exception as e:
            print(f"Error getting current user: {e}")
            self.current_user = None
            return None

    def is_authenticated(self) -> bool:
        """Check if user is currently authenticated"""
        return self.get_current_user() is not None

    def get_user_id(self) -> Optional[str]:
        """Get current user ID"""
        user = self.get_current_user()
        return user.id if user else None

    def get_user_email(self) -> Optional[str]:
        """Get current user email"""
        user = self.get_current_user()
        return user.email if user else None