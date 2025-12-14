# WePark/testing/backend/app/services/auth_service.py
"""
Auth Service - Authentication & Authorization Business Logic
Handles user/admin authentication, registration, and authorization
"""

from typing import Optional, Dict, Any
from flask_jwt_extended import create_access_token
from ..repositories.user_repository import UserRepository
from ..repositories.admin_repository import AdminRepository
from ..models.user import User
from ..models.admin import Admin


class AuthService:
    """Service for authentication and authorization operations"""
    
    def __init__(self):
        self.user_repo = UserRepository()
        self.admin_repo = AdminRepository()
    
    
    def register_user(self, username: str, email: str, password: str, 
                     address: str, pincode: int) -> Dict[str, Any]:
        """Create new user account with validation"""
        try:
            # NOTE: Username must be unique across the system
            if self.user_repo.username_exists(username):
                return {
                    'success': False,
                    'message': 'Username already exists!'
                }
            
            # Email uniqueness check - prevents duplicate accounts
            if self.user_repo.email_exists(email):
                return {
                    'success': False,
                    'message': 'Email already exists!'
                }
            
            # Build user object with provided credentials
            user = User(
                username=username,
                email=email,
                address=address,
                pincode=pincode
            )
            # Hash password before storage for security
            user.hash_password(password)
            
            self.user_repo.session.add(user)
            self.user_repo.commit()
            
            return {
                'success': True,
                'message': 'User registered successfully!',
                'user_id': user.user_id
            }
        except Exception as e:
            # Rollback on any database error
            self.user_repo.rollback()
            return {
                'success': False,
                'message': 'Something went wrong!',
                'error': str(e)
            }
    
    def login_user(self, username: str, password: str) -> Dict[str, Any]:
        """
        Authenticate a user
        
        Args:
            username: Username or Email
            password: Plain text password
            
        Returns:
            Result dictionary with access token
        """
        user = self.user_repo.find_by_username_or_email(username)
        
        if not user:
            return {
                'success': False,
                'message': 'Invalid username or password'
            }
        
        if not user.check_password(password):
            return {
                'success': False,
                'message': 'Invalid username or password'
            }
        
        # Create access token
        access_token = create_access_token(
            identity=user.username,
            additional_claims={
                'role': 'user',
                'id': user.user_id
            }
        )
        
        return {
            'success': True,
            'message': 'Login successful',
            'access_token': access_token,
            'role': 'user',
            'user_id': user.user_id,
            'username': user.username
        }
    
    def login_admin(self, username: str, password: str) -> Dict[str, Any]:
        """
        Authenticate an admin
        
        Args:
            username: Admin username or Email
            password: Plain text password
            
        Returns:
            Result dictionary with access token
        """
        admin = self.admin_repo.find_by_username_or_email(username)
        
        if not admin:
            return {
                'success': False,
                'message': 'Invalid username or password'
            }
        
        if not admin.check_password(password):
            return {
                'success': False,
                'message': 'Invalid username or password'
            }
        
        # Create access token
        access_token = create_access_token(
            identity=admin.username,
            additional_claims={
                'role': 'admin',
                'id': admin.admin_id
            }
        )
        
        return {
            'success': True,
            'message': 'Login successful',
            'access_token': access_token,
            'role': 'admin',
            'admin_id': admin.admin_id,
            'username': admin.username
        }
    
    def verify_user_credentials(self, username: str, password: str) -> bool:
        """
        Verify user credentials without creating token
        
        Args:
            username: Username or Email
            password: Password
            
        Returns:
            True if valid, False otherwise
        """
        user = self.user_repo.find_by_username_or_email(username)
        if not user:
            return False
        return user.check_password(password)
    
    def verify_admin_credentials(self, username: str, password: str) -> bool:
        """
        Verify admin credentials without creating token
        
        Args:
            username: Admin username or Email
            password: Password
            
        Returns:
            True if valid, False otherwise
        """
        admin = self.admin_repo.find_by_username_or_email(username)
        if not admin:
            return False
        return admin.check_password(password)
    
    def get_user_by_username(self, username: str) -> Optional[Dict[str, Any]]:
        """
        Get user details by username
        
        Args:
            username: Username
            
        Returns:
            User details or None
        """
        user = self.user_repo.find_by_username(username)
        if not user:
            return None
        
        return {
            'user_id': user.user_id,
            'username': user.username,
            'email': user.email,
            'address': user.address,
            'pincode': user.pincode
        }
    
    def get_admin_by_username(self, username: str) -> Optional[Dict[str, Any]]:
        """
        Get admin details by username
        
        Args:
            username: Admin username
            
        Returns:
            Admin details or None
        """
        admin = self.admin_repo.find_by_username(username)
        if not admin:
            return None
        
        return {
            'admin_id': admin.admin_id,
            'username': admin.username,
            'email': admin.email
        }
