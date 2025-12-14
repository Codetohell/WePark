# WePark/testing/backend/app/api/login.py

from flask_restful import Resource
from flask import request, jsonify, make_response
from flask_jwt_extended import set_access_cookies
from ..services.auth_service import AuthService
from ..utils.validators import check_email_format


class LoginApi(Resource):
    """API endpoint for user and admin authentication"""
    
    def __init__(self):
        self.auth_service = AuthService()
    
    def post(self):
        """
        Authenticate user or admin
        
        Request Body:
            user_or_mail: Username or email
            password: Password
            
        Returns:
            200: Login successful with JWT cookie
            401: Invalid credentials
            400: Missing required fields
        """
        data = request.get_json()
        user_or_mail = data.get("user_or_mail")
        password = data.get("password")

        # Validate required fields
        if not user_or_mail:
            return {'message': "Username or Email Address is required!"}, 400
        if not password:
            return {"message": "Password is required!"}, 400
        
        user_or_mail = user_or_mail.lower()
        
        # Determine if input is email or username
        is_email = check_email_format(user_or_mail)
        
        # Try admin login first, then user login
        if is_email:
            # For email, we need to get username first for token identity
            # Try admin by email
            admin_details = self.auth_service.get_admin_by_username(user_or_mail) if not is_email else None
            if not admin_details and is_email:
                # Get admin by email - need to check both
                result = self.auth_service.login_admin(user_or_mail, password)
                if result['success']:
                    return self._create_response(result)
            
            # Try user by email
            result = self.auth_service.login_user(user_or_mail, password)
            if result['success']:
                return self._create_response(result)
        else:
            # Try admin login by username
            result = self.auth_service.login_admin(user_or_mail, password)
            if result['success']:
                return self._create_response(result)
            
            # Try user login by username
            result = self.auth_service.login_user(user_or_mail, password)
            if result['success']:
                return self._create_response(result)
        
        # If we get here, login failed
        return {'message': 'Invalid username or password'}, 401
    
    def _create_response(self, auth_result: dict):
        """Create HTTP response with JWT cookie"""
        response = make_response(jsonify({
            "message": auth_result['message'],
            "role": auth_result['role'],
            "username": auth_result['username']
        }), 200)
        set_access_cookies(response, auth_result['access_token'])
        return response
