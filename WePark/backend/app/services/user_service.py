# WePark/testing/backend/app/services/user_service.py
"""
User Service - User Management Business Logic
Handles user profile and user-related operations
"""

from typing import List, Dict, Any, Optional
from ..repositories.user_repository import UserRepository
from ..repositories.admin_repository import AdminRepository


class UserService:
    """Service for user management operations"""
    
    def __init__(self):
        self.user_repo = UserRepository()
        self.admin_repo = AdminRepository()
    
    def get_user_by_id(self, user_id: int) -> Optional[Dict[str, Any]]:
        """
        Get user details by ID
        
        Args:
            user_id: User ID
            
        Returns:
            User details or None
        """
        user = self.user_repo.get_user_by_id(user_id)
        if not user:
            return None
        
        return self._format_user_details(user)
    
    def get_all_users(self) -> List[Dict[str, Any]]:
        """
        Get all users (admin operation)
        
        Returns:
            List of user details
        """
        users = self.user_repo.get_all()
        return [self._format_user_details(user) for user in users]
    
    def update_user(self, user_id: int, **kwargs) -> Dict[str, Any]:
        """
        Update user profile
        
        Args:
            user_id: User ID
            **kwargs: Fields to update
            
        Returns:
            Result dictionary
        """
        try:
            user = self.user_repo.get_user_by_id(user_id)
            if not user:
                return {
                    'success': False,
                    'message': 'User not found'
                }
            
            # Update allowed fields
            allowed_fields = ['email', 'address', 'pincode']
            update_data = {k: v for k, v in kwargs.items() if k in allowed_fields}
            
            # Check email uniqueness if updating email
            if 'email' in update_data and update_data['email'] != user.email:
                if self.user_repo.email_exists(update_data['email']):
                    return {
                        'success': False,
                        'message': 'Email already exists'
                    }
            
            self.user_repo.update(user, **update_data)
            self.user_repo.commit()
            
            return {
                'success': True,
                'message': 'User updated successfully'
            }
        except Exception as e:
            self.user_repo.rollback()
            return {
                'success': False,
                'message': 'Something went wrong!',
                'error': str(e)
            }
    
    def delete_user(self, user_id: int) -> Dict[str, Any]:
        """
        Delete a user (admin operation)
        
        Args:
            user_id: User ID
            
        Returns:
            Result dictionary
        """
        try:
            user = self.user_repo.get_user_by_id(user_id)
            if not user:
                return {
                    'success': False,
                    'message': 'User not found'
                }
            
            self.user_repo.delete(user)
            self.user_repo.commit()
            
            return {
                'success': True,
                'message': 'User deleted successfully'
            }
        except Exception as e:
            self.user_repo.rollback()
            return {
                'success': False,
                'message': 'Something went wrong!',
                'error': str(e)
            }
    
    def get_user_count(self) -> int:
        """
        Get total number of users
        
        Returns:
            User count
        """
        return self.user_repo.count()
    
    def change_password(self, user_id: int, current_password: str, new_password: str) -> Dict[str, Any]:
        """
        Change user password
        
        Args:
            user_id: User ID
            current_password: Current password
            new_password: New password
            
        Returns:
            Result dictionary
        """
        try:
            user = self.user_repo.get_user_by_id(user_id)
            if not user:
                return {
                    'success': False,
                    'message': 'User not found'
                }
            
            if not user.check_password(current_password):
                return {
                    'success': False,
                    'message': 'Current password is incorrect'
                }
            
            user.hash_password(new_password)
            self.user_repo.commit()
            
            return {
                'success': True,
                'message': 'Password changed successfully'
            }
        except Exception as e:
            self.user_repo.rollback()
            return {
                'success': False,
                'message': 'Something went wrong!',
                'error': str(e)
            }
    
    def _format_user_details(self, user) -> Dict[str, Any]:
        """
        Format user object to dictionary
        
        Args:
            user: User model instance
            
        Returns:
            Formatted user dictionary
        """
        return {
            'user_id': user.user_id,
            'username': user.username,
            'email': user.email,
            'address': user.address,
            'pincode': user.pincode
        }
