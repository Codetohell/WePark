# WePark/testing/backend/app/repositories/user_repository.py
"""
User Repository - User Data Access
Handles database operations for users
"""

from typing import Optional
from .base_repository import BaseRepository
from ..models.user import User


class UserRepository(BaseRepository[User]):
    """Repository for user operations"""
    
    def __init__(self):
        super().__init__(User)
    
    def find_by_username(self, username: str) -> Optional[User]:
        """
        Find user by username
        
        Args:
            username: Username to search for
            
        Returns:
            User instance or None
        """
        return User.query.filter_by(username=username).first()
    
    def find_by_email(self, email: str) -> Optional[User]:
        """
        Find user by email
        
        Args:
            email: Email to search for
            
        Returns:
            User instance or None
        """
        return User.query.filter_by(email=email).first()

    def find_by_username_or_email(self, identifier: str) -> Optional[User]:
        """
        Find user by username or email
        
        Args:
            identifier: Username or email
            
        Returns:
            User instance or None
        """
        return User.query.filter((User.username == identifier) | (User.email == identifier)).first()
    
    def username_exists(self, username: str) -> bool:
        """
        Check if username already exists
        
        Args:
            username: Username to check
            
        Returns:
            True if exists, False otherwise
        """
        return self.exists({'username': username})
    
    def email_exists(self, email: str) -> bool:
        """
        Check if email already exists
        
        Args:
            email: Email to check
            
        Returns:
            True if exists, False otherwise
        """
        return self.exists({'email': email})
    
    def get_user_by_id(self, user_id: int) -> Optional[User]:
        """
        Get user by ID
        
        Args:
            user_id: User ID
            
        Returns:
            User instance or None
        """
        return User.query.filter_by(user_id=user_id).first()
