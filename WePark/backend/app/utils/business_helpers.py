# WePark/testing/backend/app/utils/business_helpers.py
"""
Business Logic Helper Functions
Provides domain-specific helper functions
"""

from typing import Any


def can_delete_lot(lot: Any) -> bool:
    """
    Check if a parking lot can be deleted
    
    A lot can only be deleted if all spots are available (not occupied)
    
    Args:
        lot: Lot model instance
        
    Returns:
        True if lot can be deleted, False otherwise
    """
    for spot in lot.spots:
        # spot.status is False when occupied (legacy logic)
        if spot.status == "occupied" or spot.status is False:
            return False
    return True


def calculate_parking_cost(duration_hours: float, hourly_rate: float) -> float:
    """
    Calculate parking cost based on duration and hourly rate
    
    Args:
        duration_hours: Duration in hours
        hourly_rate: Cost per hour
        
    Returns:
        Total cost (rounded to 2 decimal places)
    """
    import math
    # Round up to nearest hour for billing
    billing_hours = math.ceil(duration_hours)
    total_cost = billing_hours * hourly_rate
    return round(total_cost, 2)


def format_currency(amount: float, currency_symbol: str = "₹") -> str:
    """
    Format amount as currency string
    
    Args:
        amount: Amount to format
        currency_symbol: Currency symbol (default: ₹)
        
    Returns:
        Formatted currency string
    """
    return f"{currency_symbol}{amount:,.2f}"


def calculate_occupancy_rate(total_spots: int, occupied_spots: int) -> float:
    """
    Calculate occupancy rate percentage
    
    Args:
        total_spots: Total number of spots
        occupied_spots: Number of occupied spots
        
    Returns:
        Occupancy rate as percentage (0-100)
    """
    if total_spots == 0:
        return 0.0
    return round((occupied_spots / total_spots) * 100, 2)


# Backward compatibility alias
lot_can_delete = can_delete_lot
