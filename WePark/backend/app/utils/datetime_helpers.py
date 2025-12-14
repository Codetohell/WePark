# WePark/testing/backend/app/utils/datetime_helpers.py
"""
DateTime Utility Functions
Provides timezone-aware datetime operations
"""

from datetime import datetime
from typing import List, Tuple
import pytz


def get_ist_time() -> datetime:
    """
    Get current time in IST (Indian Standard Time)
    
    Returns:
        Current datetime in IST timezone
    """
    ist = pytz.timezone('Asia/Kolkata')
    return datetime.now(ist)


def get_utc_time() -> datetime:
    """
    Get current time in UTC
    
    Returns:
        Current datetime in UTC timezone
    """
    return datetime.now(pytz.UTC)


def convert_to_ist(dt: datetime) -> datetime:
    """
    Convert datetime to IST timezone
    
    Args:
        dt: Datetime to convert
        
    Returns:
        Datetime in IST timezone
    """
    ist = pytz.timezone('Asia/Kolkata')
    if dt.tzinfo is None:
        # Assume UTC if no timezone
        dt = pytz.UTC.localize(dt)
    return dt.astimezone(ist)


def get_past_months(k: int = 3) -> List[Tuple[int, int]]:
    """
    Get list of past k months as (year, month) tuples
    
    Args:
        k: Number of past months to retrieve (default: 3)
        
    Returns:
        List of (year, month) tuples in chronological order
        
    Example:
        >>> get_past_months(3)
        [(2024, 10), (2024, 11), (2024, 12)]
    """
    now = datetime.now()
    months = []
    
    for i in range(k):
        month = (now.month - i - 1) % 12 + 1
        year = now.year - ((now.month - i - 1) // 12)
        months.append((year, month))
    
    return months[::-1]  # Reverse to chronological order


def get_month_name(month: int) -> str:
    """
    Get month name from month number
    
    Args:
        month: Month number (1-12)
        
    Returns:
        Month name (e.g., "January")
    """
    import calendar
    return calendar.month_name[month]


def format_datetime_ist(dt: datetime, format_string: str = "%Y-%m-%d %H:%M:%S") -> str:
    """
    Format datetime in IST timezone
    
    Args:
        dt: Datetime to format
        format_string: strftime format string
        
    Returns:
        Formatted datetime string
    """
    ist_dt = convert_to_ist(dt)
    return ist_dt.strftime(format_string)


def calculate_duration_hours(start_time: datetime, end_time: datetime) -> float:
    """
    Calculate duration between two datetimes in hours
    
    Args:
        start_time: Start datetime
        end_time: End datetime
        
    Returns:
        Duration in hours (rounded to 2 decimal places)
    """
    duration_seconds = (end_time - start_time).total_seconds()
    duration_hours = duration_seconds / 3600
    return round(duration_hours, 2)
