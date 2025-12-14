# WePark/testing/backend/app/api/signup.py

from flask_restful import Resource
from flask import request
from ..services.auth_service import AuthService
from ..utils.validators import check_email_format, check_username_format


class SignupApi(Resource):
    """API endpoint for user registration"""
    
    def __init__(self):
        self.auth_service = AuthService()
    
    def post(self):
        """
        Register a new user
        
        Request Body:
            email: Email address
            username: Username
            password: Password
            confirm_password: Password confirmation
            address: User address
            pincode: Area pincode
            
        Returns:
            200: Registration successful
            400: Validation error
            500: Server error
        """
        data = request.get_json()
        email = data.get("email")
        username = data.get("username")
        password = data.get("password")
        confirm_password = data.get("confirm_password")
        address = data.get("address")
        pincode = data.get("pincode")

        # Validate required fields
        if not email:
            return {'message': 'Email Address is required!'}, 400
        if not username:
            return {'message': 'Username is required!'}, 400
        if not password:
            return {'message': 'Password is required!'}, 400
        if not confirm_password:
            return {'message': 'Confirm password is required!'}, 400
        if not address:
            return {'message': 'Address is required!'}, 400
        if not pincode:
            return {'message': 'Pincode is required!'}, 400
        
        # Normalize inputs
        email = email.lower()
        username = username.lower()

        # Validate formats
        if not check_email_format(email):
            return {'message': 'Email Address is invalid!'}, 400
        if not check_username_format(username):
            return {'message': 'Username is invalid!'}, 400

        # Validate password
        if len(password) < 8 or len(confirm_password) < 8:
            return {'message': 'Password must be at least 8 characters!'}, 400
        if password != confirm_password:
            return {'message': 'Password and Confirm Password must be same!'}, 400

        # Register user using service
        result = self.auth_service.register_user(
            username=username,
            email=email,
            password=password,
            address=address,
            pincode=pincode
        )
        
        if result['success']:
            return {'message': result['message']}, 200
        else:
            return {'message': result['message']}, 400
