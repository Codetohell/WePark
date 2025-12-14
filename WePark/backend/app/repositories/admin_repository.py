# WePark/testing/backend/app/repositories/admin_repository.py
"""
Admin Repository - Admin Data Access
Handles database operations for admins
"""

from typing import Optional
from .base_repository import BaseRepository
from ..models.admin import Admin


class AdminRepository(BaseRepository[Admin]):
    """Repository for admin operations"""
    
    def __init__(self):
        super().__init__(Admin)
    
    def find_by_username(self, username: str) -> Optional[Admin]:
        """
        Find admin by username
        
        Args:
            username: Username to search for
            
        Returns:
            Admin instance or None
        """
        return Admin.query.filter_by(username=username).first()
    
    def find_by_email(self, email: str) -> Optional[Admin]:
        """
        Find admin by email
        
        Args:
            email: Email to search for
            
        Returns:
            Admin instance or None
        """
        return Admin.query.filter_by(email=email).first()

    def find_by_username_or_email(self, identifier: str) -> Optional[Admin]:
        """
        Find admin by username or email
        
        Args:
            identifier: Username or email
            
        Returns:
            Admin instance or None
        """
        return Admin.query.filter((Admin.username == identifier) | (Admin.email == identifier)).first()
    
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
    
    def get_admin_by_id(self, admin_id: int) -> Optional[Admin]:
        """
        Get admin by ID
        
        Args:
            admin_id: Admin ID
            
        Returns:
            Admin instance or None
        """
        return Admin.query.filter_by(admin_id=admin_id).first()
