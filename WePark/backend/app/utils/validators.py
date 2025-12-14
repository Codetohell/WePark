# WePark/testing/backend/app/utils/validators.py
"""
Input Validation Utilities
Provides validation functions for user inputs
"""

import re
from typing import Optional


def validate_email_format(email: str) -> bool:
    """
    Validate email address format
    
    Args:
        email: Email address to validate
        
    Returns:
        True if valid email format, False otherwise
    """
    if not email:
        return False
    
    regex_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(regex_pattern, email) is not None


def validate_username_format(username: str) -> bool:
    """
    Validate username format
    
    Rules:
    - 3-20 characters
    - Alphanumeric and underscores only
    
    Args:
        username: Username to validate
        
    Returns:
        True if valid username format, False otherwise
    """
    if not username:
        return False
    
    regex_pattern = r'^[a-zA-Z0-9_]{3,20}$'
    return re.match(regex_pattern, username) is not None


def validate_password_strength(password: str, min_length: int = 8) -> tuple[bool, Optional[str]]:
    """
    Validate password strength
    
    Args:
        password: Password to validate
        min_length: Minimum password length (default: 8)
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not password:
        return False, "Password is required"
    
    if len(password) < min_length:
        return False, f"Password must be at least {min_length} characters"
    
    return True, None


def validate_pincode(pincode: str) -> bool:
    """
    Validate pincode format
    
    Args:
        pincode: Pincode to validate
        
    Returns:
        True if valid pincode, False otherwise
    """
    if not pincode:
        return False
    
    # Accept 5-6 digit pincodes
    return pincode.isdigit() and 5 <= len(pincode) <= 6


def validate_phone_number(phone: str) -> bool:
    """
    Validate phone number format
    
    Args:
        phone: Phone number to validate
        
    Returns:
        True if valid phone number, False otherwise
    """
    if not phone:
        return False
    
    # Remove common separators
    cleaned = phone.replace('-', '').replace(' ', '').replace('(', '').replace(')', '')
    
    # Check if 10 digits
    return cleaned.isdigit() and len(cleaned) == 10


# Backward compatibility aliases
check_email_format = validate_email_format
check_username_format = validate_username_format
