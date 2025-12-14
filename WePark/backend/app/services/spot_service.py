# WePark/testing/backend/app/services/spot_service.py
"""
Spot Service - Parking Spot Business Logic
Handles all business operations related to parking spots
"""

from typing import List, Optional, Dict, Any
from ..repositories.spot_repository import SpotRepository
from ..repositories.lot_repository import LotRepository


class SpotService:
    """Service for parking spot operations"""
    
    def __init__(self):
        self.spot_repo = SpotRepository()
        self.lot_repo = LotRepository()
    
    def get_spot_by_id(self, spot_id: int) -> Optional[Dict[str, Any]]:
        """
        Get spot details by ID
        
        Args:
            spot_id: Spot ID
            
        Returns:
            Spot details dictionary or None
        """
        spot = self.spot_repo.get_spot_by_id(spot_id)
        if not spot:
            return None
        
        return self._format_spot_details(spot)
    
    def get_spots_by_lot(self, lot_id: int) -> List[Dict[str, Any]]:
        """
        Get all spots for a lot
        
        Args:
            lot_id: Lot ID
            
        Returns:
            List of spot details
        """
        spots = self.spot_repo.find_by_lot(lot_id)
        return [self._format_spot_details(spot) for spot in spots]
    
    def get_available_spots(self, lot_id: int) -> List[Dict[str, Any]]:
        """
        Get available spots for a lot
        
        Args:
            lot_id: Lot ID
            
        Returns:
            List of available spot details
        """
        spots = self.spot_repo.find_available_spots(lot_id)
        return [self._format_spot_details(spot) for spot in spots]
    
    def check_spot_availability(self, spot_id: int) -> Dict[str, Any]:
        """
        Check if a spot is available for booking
        
        Args:
            spot_id: Spot ID
            
        Returns:
            Result dictionary with availability status
        """
        spot = self.spot_repo.get_spot_by_id(spot_id)
        if not spot:
            return {
                'available': False,
                'message': 'Spot not found'
            }
        
        is_available = self.spot_repo.is_spot_available(spot_id)
        return {
            'available': is_available,
            'spot': self._format_spot_details(spot) if is_available else None,
            'message': 'Spot is available' if is_available else 'Spot is occupied'
        }
    
    def mark_spot_occupied(self, spot_id: int) -> Dict[str, Any]:
        """
        Mark a spot as occupied
        
        Args:
            spot_id: Spot ID
            
        Returns:
            Result dictionary
        """
        try:
            spot = self.spot_repo.get_spot_by_id(spot_id)
            if not spot:
                return {
                    'success': False,
                    'message': 'Spot not found'
                }
            
            if spot.status == "occupied":
                return {
                    'success': False,
                    'message': 'Spot is already occupied'
                }
            
            self.spot_repo.mark_as_occupied(spot)
            self.spot_repo.commit()
            
            return {
                'success': True,
                'message': 'Spot marked as occupied'
            }
        except Exception as e:
            self.spot_repo.rollback()
            return {
                'success': False,
                'message': 'Something went wrong!',
                'error': str(e)
            }
    
    def mark_spot_available(self, spot_id: int) -> Dict[str, Any]:
        """
        Mark a spot as available
        
        Args:
            spot_id: Spot ID
            
        Returns:
            Result dictionary
        """
        try:
            spot = self.spot_repo.get_spot_by_id(spot_id)
            if not spot:
                return {
                    'success': False,
                    'message': 'Spot not found'
                }
            
            self.spot_repo.mark_as_available(spot)
            self.spot_repo.commit()
            
            return {
                'success': True,
                'message': 'Spot marked as available'
            }
        except Exception as e:
            self.spot_repo.rollback()
            return {
                'success': False,
                'message': 'Something went wrong!',
                'error': str(e)
            }
    
    def get_lot_spot_statistics(self, lot_id: int) -> Dict[str, Any]:
        """
        Get spot statistics for a lot
        
        Args:
            lot_id: Lot ID
            
        Returns:
            Statistics dictionary
        """
        lot = self.lot_repo.get_by_id(lot_id)
        if not lot:
            return {
                'success': False,
                'message': 'Lot not found'
            }
        
        total_spots = lot.no_of_spots
        available_count = self.spot_repo.count_available_spots(lot_id)
        occupied_count = self.spot_repo.count_occupied_spots(lot_id)
        
        return {
            'success': True,
            'lot_id': lot_id,
            'total_spots': total_spots,
            'available': available_count,
            'occupied': occupied_count,
            'occupancy_rate': round((occupied_count / total_spots * 100), 2) if total_spots > 0 else 0
        }
    
    def _format_spot_details(self, spot) -> Dict[str, Any]:
        """
        Format spot object to dictionary
        
        Args:
            spot: Spot model instance
            
        Returns:
            Formatted spot dictionary
        """
        return {
            'spot_id': spot.spot_id,
            'lot_id': spot.lot_id,
            'status': spot.status
        }
