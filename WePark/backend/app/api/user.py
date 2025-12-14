# WePark/testing/backend/app/api/user.py

from flask_restful import Resource
from flask import request
from flask_jwt_extended import jwt_required
from ..services.user_service import UserService
from ..utils.decorators import role_required


class UserApi(Resource):
    """API endpoint for user management"""
    
    def __init__(self):
        self.user_service = UserService()
    
    @jwt_required()
    def get(self, user_id=None):
        """
        Get user(s) information
        
        Args:
            user_id: Optional user ID for specific user
            
        Returns:
            200: User details
            403: Forbidden (user trying to access another user's profile)
            404: User not found
        """
        from flask_jwt_extended import get_jwt, get_jwt_identity
        
        claims = get_jwt()
        role = claims.get('role')
        current_user_id = claims.get('id')
        
        # Admin can view all users or any specific user
        if role == 'admin':
            if user_id:
                user = self.user_service.get_user_by_id(user_id)
                if user:
                    return user, 200
                else:
                    return {"message": "User not found"}, 404
            else:
                # Get all users
                users = self.user_service.get_all_users()
                return users, 200
        
        # Regular user can only view their own profile
        if user_id:
            # Check if user is trying to access their own profile
            if user_id != current_user_id:
                return {"message": "Forbidden, access denied!"}, 403
            
            user = self.user_service.get_user_by_id(user_id)
            if user:
                return user, 200
            else:
                return {"message": "User not found"}, 404
        else:
            # If no user_id provided, return current user's profile
            user = self.user_service.get_user_by_id(current_user_id)
            if user:
                return user, 200
            else:
                return {"message": "User not found"}, 404
    
    @jwt_required()
    @role_required("admin")
    def delete(self, user_id):
        """
        Delete a user
        
        Args:
            user_id: User ID
            
        Returns:
            200: User deleted
            404: User not found
            500: Server error
        """
        result = self.user_service.delete_user(user_id)
        
        if result['success']:
            return {"message": result['message']}, 200
        else:
            status_code = 404 if 'not found' in result['message'].lower() else 500
            return {"message": result['message']}, status_code
    
    @jwt_required()
    def put(self, user_id):
        """
        Update user profile
        
        Args:
            user_id: User ID
            
        Request Body:
            email: Optional new email
            address: Optional new address
            pincode: Optional new pincode
            
        Returns:
            200: User updated
            400: Validation error
            404: User not found
        """
        data = request.get_json()
        
        result = self.user_service.update_user(user_id, **data)
        
        if result['success']:
            return {"message": result['message']}, 200
        else:
            status_code = 404 if 'not found' in result['message'].lower() else 400
            return {"message": result['message']}, status_code
