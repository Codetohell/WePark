# WePark/testing/backend/app/repositories/reservation_repository.py
"""
Reservation Repository - Booking Data Access
Handles database operations for parking reservations
"""

from typing import List, Optional
from datetime import datetime
from .base_repository import BaseRepository
from ..models.reservation import Reservation


class ReservationRepository(BaseRepository[Reservation]):
    """Repository for reservation operations"""
    
    def __init__(self):
        super().__init__(Reservation)
    
    def find_by_user(self, user_id: int) -> List[Reservation]:
        """
        Get all reservations for a user
        
        Args:
            user_id: User ID
            
        Returns:
            List of user's reservations
        """
        return Reservation.query.filter_by(user_id=user_id).all()
    
    def find_active_by_user(self, user_id: int) -> List[Reservation]:
        """
        Get active reservations for a user
        
        Args:
            user_id: User ID
            
        Returns:
            List of active reservations
        """
        return Reservation.query.filter_by(user_id=user_id, leaving_timestamp=None).all()
    
    def find_by_spot(self, spot_id: int) -> List[Reservation]:
        """
        Get all reservations for a spot
        
        Args:
            spot_id: Spot ID
            
        Returns:
            List of spot's reservations
        """
        return Reservation.query.filter_by(spot_id=spot_id).all()
    
    def find_active_by_spot(self, spot_id: int) -> Optional[Reservation]:
        """
        Get active reservation for a spot
        
        Args:
            spot_id: Spot ID
            
        Returns:
            Active reservation or None
        """
        return Reservation.query.filter_by(spot_id=spot_id, leaving_timestamp=None).first()
    
    def get_reservation_by_id(self, reservation_id: int) -> Optional[Reservation]:
        """
        Get reservation by ID
        
        Args:
            reservation_id: Reservation ID
            
        Returns:
            Reservation instance or None
        """
        return Reservation.query.filter_by(reservation_id=reservation_id).first()
    
    def mark_as_completed(self, reservation: Reservation) -> Reservation:
        """
        Mark reservation as completed
        
        Args:
            reservation: Reservation instance
            
        Returns:
            Updated reservation
        """
        reservation.leaving_timestamp = datetime.now()
        return reservation
    
    def calculate_total_amount(self, reservation: Reservation, price_per_hour: float) -> float:
        """
        Calculate total amount for a reservation
        
        Args:
            reservation: Reservation instance
            price_per_hour: Hourly rate
            
        Returns:
            Total amount
        """
        if reservation.leaving_timestamp is None:
            end_time = datetime.now()
        else:
            end_time = reservation.leaving_timestamp
        
        start_time = reservation.parking_timestamp
        if not start_time:
             # Fallback if parking_timestamp is missing (shouldn't happen)
             return 0.0
             
        duration_hours = (end_time - start_time).total_seconds() / 3600
        return round(duration_hours * price_per_hour, 2)
    
    def get_user_history(self, user_id: int) -> List[Reservation]:
        """
        Get reservation history for a user (completed reservations)
        
        Args:
            user_id: User ID
            
        Returns:
            List of completed reservations
        """
        return Reservation.query.filter(Reservation.user_id == user_id, Reservation.leaving_timestamp != None).all()
    
    def count_active_reservations(self, user_id: int) -> int:
        """
        Count active reservations for a user
        
        Args:
            user_id: User ID
            
        Returns:
            Number of active reservations
        """
        return Reservation.query.filter_by(user_id=user_id, leaving_timestamp=None).count()

    def find_by_payment_status(self, is_paid: bool) -> List[Reservation]:
        """
        Find reservations by payment status
        
        Args:
            is_paid: Payment status
            
        Returns:
            List of reservations
        """
        return Reservation.query.filter_by(payment_status=is_paid).all()
