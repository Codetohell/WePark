# WePark/testing/backend/app/utils/decorators.py
"""
Custom Decorators for Authorization and Access Control
Provides decorators for JWT-based role checking
"""

from functools import wraps
from flask_jwt_extended import get_jwt
from typing import Callable, Any


def role_required(required_role: str) -> Callable:
    """
    Decorator to enforce role-based access control
    
    Args:
        required_role: Required role ('user' or 'admin')
        
    Returns:
        Decorator function
        
    Usage:
        @jwt_required()
        @role_required("admin")
        def admin_only_endpoint():
            pass
    """
    def decorator(fn: Callable) -> Callable:
        @wraps(fn)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            decoded_data = get_jwt()
            
            print(f"[DEBUG] role_required: checking for role '{required_role}'")
            print(f"[DEBUG] JWT data: {decoded_data}")
            
            user_role = decoded_data.get('role')
            
            if user_role != required_role:
                print(f"[DEBUG] Role mismatch! Expected '{required_role}', got '{user_role}'")
                return {'message': 'Forbidden, access denied!'}, 403
            
            print(f"[DEBUG] Role check passed!")
            return fn(*args, **kwargs)
        
        return wrapper
    return decorator


def roles_required(*allowed_roles: str) -> Callable:
    """
    Decorator to enforce multi-role access control
    
    Args:
        *allowed_roles: Multiple allowed roles
        
    Returns:
        Decorator function
        
    Usage:
        @jwt_required()
        @roles_required("admin", "moderator")
        def multi_role_endpoint():
            pass
    """
    def decorator(fn: Callable) -> Callable:
        @wraps(fn)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            decoded_data = get_jwt()
            user_role = decoded_data.get('role')
            
            if user_role not in allowed_roles:
                return {'message': 'Forbidden, access denied!'}, 403
            
            return fn(*args, **kwargs)
        
        return wrapper
    return decorator


def admin_required(fn: Callable) -> Callable:
    """
    Shorthand decorator for admin-only access
    
    Usage:
        @jwt_required()
        @admin_required
        def admin_endpoint():
            pass
    """
    return role_required("admin")(fn)


def user_required(fn: Callable) -> Callable:
    """
    Shorthand decorator for user-only access
    
    Usage:
        @jwt_required()
        @user_required
        def user_endpoint():
            pass
    """
    return role_required("user")(fn)
