# WePark/testing/backend/app/services/reservation_service.py
"""
Reservation Service - Booking Business Logic
Handles all business operations related to parking reservations
"""

from typing import List, Optional, Dict, Any
from datetime import datetime
from ..repositories.reservation_repository import ReservationRepository
from ..repositories.spot_repository import SpotRepository
from ..repositories.lot_repository import LotRepository
from ..repositories.notification_repository import NotificationRepository
from ..repositories.user_repository import UserRepository
from .. import db


class ReservationService:
    """Service for reservation operations"""
    
    def __init__(self):
        self.reservation_repo = ReservationRepository()
        self.spot_repo = SpotRepository()
        self.lot_repo = LotRepository()
        self.notification_repo = NotificationRepository()
        self.user_repo = UserRepository()
    
    def create_reservation(self, user_id: int, spot_id: int, vehicle_number: str = "Unknown") -> Dict[str, Any]:
        """
        Create a new parking reservation
        
        Args:
            user_id: User ID
            spot_id: Spot ID
            vehicle_number: Vehicle registration number
            
        Returns:
            Result dictionary
        """
        try:
            # Check if spot exists and is available
            spot = self.spot_repo.get_spot_by_id(spot_id)
            if not spot:
                return {
                    'success': False,
                    'message': 'Spot not found'
                }
            
            if spot.status is False:
                return {
                    'success': False,
                    'message': 'Spot is already occupied'
                }
            
            # Create reservation
            reservation = self.reservation_repo.create(
                user_id=user_id,
                spot_id=spot_id,
                vehicle_number=vehicle_number
            )
            
            # Mark spot as occupied
            self.spot_repo.mark_as_occupied(spot)
            
            # Get lot details for notification
            lot = self.lot_repo.get_by_id(spot.lot_id)
            
            # Create notification
            if lot:
                self.notification_repo.create(
                    user_id=user_id,
                    title="Spot Booked",
                    body=f"You have successfully booked a spot at {lot.prime_location}"
                )
            
            self.reservation_repo.commit()
            
            return {
                'success': True,
                'message': 'Spot booked successfully!',
                'reservation_id': reservation.reservation_id
            }
        except Exception as e:
            self.reservation_repo.rollback()
            return {
                'success': False,
                'message': f'Something went wrong: {str(e)}',
                'error': str(e)
            }
    
    def complete_reservation(self, reservation_id: int) -> Dict[str, Any]:
        """
        Complete a reservation (release spot)
        
        Args:
            reservation_id: Reservation ID
            
        Returns:
            Result dictionary with total amount
        """
        try:
            reservation = self.reservation_repo.get_reservation_by_id(reservation_id)
            if not reservation:
                return {
                    'success': False,
                    'message': 'Reservation not found'
                }
            
            if reservation.leaving_timestamp is not None:
                return {
                    'success': False,
                    'message': 'Reservation already completed'
                }
            
            # Get spot and lot details
            spot = self.spot_repo.get_spot_by_id(reservation.spot_id)
            lot = self.lot_repo.get_by_id(spot.lot_id)
            
            # Calculate total amount
            total_amount = self.reservation_repo.calculate_total_amount(
                reservation, 
                lot.price_per_hour
            )
            # Set parking_cost on reservation
            reservation.parking_cost = total_amount

            # Mark reservation as completed
            self.reservation_repo.mark_as_completed(reservation)

            # Mark spot as available
            self.spot_repo.mark_as_available(spot)

            self.reservation_repo.commit()

            return {
                'success': True,
                'message': 'Reservation completed successfully',
                'total_amount': total_amount,
                'reservation_id': reservation_id
            }
        except Exception as e:
            self.reservation_repo.rollback()
            return {
                'success': False,
                'message': 'Something went wrong!',
                'error': str(e)
            }
    
    def get_user_reservations(self, user_id: int, active_only: bool = False) -> List[Dict[str, Any]]:
        """
        Get reservations for a user
        
        Args:
            user_id: User ID
            active_only: If True, return only active reservations
            
        Returns:
            List of reservation details
        """
        if active_only:
            reservations = self.reservation_repo.find_active_by_user(user_id)
        else:
            reservations = self.reservation_repo.find_by_user(user_id)
        
        return [self._format_reservation_details(r) for r in reservations]
    
    def get_reservation_by_id(self, reservation_id: int) -> Optional[Dict[str, Any]]:
        """
        Get reservation details by ID
        
        Args:
            reservation_id: Reservation ID
            
        Returns:
            Reservation details or None
        """
        reservation = self.reservation_repo.get_reservation_by_id(reservation_id)
        if not reservation:
            return None
        
        return self._format_reservation_details(reservation)
    
    def get_user_parking_history(self, user_id: int) -> List[Dict[str, Any]]:
        """
        Get parking history for a user
        
        Args:
            user_id: User ID
            
        Returns:
            List of completed reservations with details
        """
        reservations = self.reservation_repo.get_user_history(user_id)
        history = []
        
        for reservation in reservations:
            spot = self.spot_repo.get_spot_by_id(reservation.spot_id)
            lot = self.lot_repo.get_by_id(spot.lot_id)
            
            total_amount = self.reservation_repo.calculate_total_amount(
                reservation,
                lot.price_per_hour
            )
            
            history.append({
                **self._format_reservation_details(reservation),
                'lot_name': lot.prime_location,
                'lot_address': lot.address,
                'price_per_hour': lot.price_per_hour,
                'total_amount': total_amount
            })
        
        return history
    
    def _format_reservation_details(self, reservation) -> Dict[str, Any]:
        """
        Format reservation object to dictionary
        
        Args:
            reservation: Reservation model instance
            
        Returns:
            Formatted reservation dictionary
        """
        status = "active" if reservation.leaving_timestamp is None else "completed"
        return {
            'reservation_id': reservation.reservation_id,
            'user_id': reservation.user_id,
            'spot_id': reservation.spot_id,
            'status': status,
            'start_time': reservation.parking_timestamp.isoformat() if reservation.parking_timestamp else None,
            'parking_time': reservation.parking_timestamp.isoformat() if reservation.parking_timestamp else None, # Alias for frontend
            'end_time': reservation.leaving_timestamp.isoformat() if reservation.leaving_timestamp else None,
            'parking_cost': reservation.parking_cost,
            'vehicle_number': reservation.vehicle_number,
            'prime_location': reservation.spot.lot.prime_location if reservation.spot and reservation.spot.lot else "Unknown",
            'address': reservation.spot.lot.address if reservation.spot and reservation.spot.lot else "Unknown"
        }
