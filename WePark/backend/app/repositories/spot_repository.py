# WePark/testing/backend/app/repositories/spot_repository.py
"""
Spot Repository - Parking Spot Data Access
Handles database operations for parking spots
"""

from typing import List, Optional
from .base_repository import BaseRepository
from ..models.spot import Spot


class SpotRepository(BaseRepository[Spot]):
    """Repository for parking spot operations"""
    
    def __init__(self):
        super().__init__(Spot)
    
    def find_by_lot(self, lot_id: int) -> List[Spot]:
        """
        Get all spots for a specific lot
        
        Args:
            lot_id: Lot ID
            
        Returns:
            List of spots in the lot
        """
        return Spot.query.filter_by(lot_id=lot_id).all()
    
    def find_available_spots(self, lot_id: int) -> List[Spot]:
        """
        Get available spots for a lot
        
        Args:
            lot_id: Lot ID
            
        Returns:
            List of available spots
        """
        return Spot.query.filter_by(lot_id=lot_id, status=True).all()
    
    def find_occupied_spots(self, lot_id: int) -> List[Spot]:
        """
        Get occupied spots for a lot
        
        Args:
            lot_id: Lot ID
            
        Returns:
            List of occupied spots
        """
        return Spot.query.filter_by(lot_id=lot_id, status=False).all()
    
    def get_spot_by_id(self, spot_id: int) -> Optional[Spot]:
        """
        Get spot by ID
        
        Args:
            spot_id: Spot ID
            
        Returns:
            Spot instance or None
        """
        return Spot.query.filter_by(spot_id=spot_id).first()
    
    def is_spot_available(self, spot_id: int) -> bool:
        """
        Check if a spot is available
        
        Args:
            spot_id: Spot ID
            
        Returns:
            True if available, False otherwise
        """
        spot = self.get_spot_by_id(spot_id)
        return spot is not None and spot.status is True
    
    def mark_as_occupied(self, spot: Spot) -> Spot:
        """
        Mark a spot as occupied
        
        Args:
            spot: Spot instance
            
        Returns:
            Updated spot
        """
        spot.status = False
        return spot
    
    def mark_as_available(self, spot: Spot) -> Spot:
        """
        Mark a spot as available
        
        Args:
            spot: Spot instance
            
        Returns:
            Updated spot
        """
        spot.status = True
        return spot
    
    def count_available_spots(self, lot_id: int) -> int:
        """
        Count available spots in a lot
        
        Args:
            lot_id: Lot ID
            
        Returns:
            Number of available spots
        """
        return Spot.query.filter_by(lot_id=lot_id, status=True).count()
    
    def count_occupied_spots(self, lot_id: int) -> int:
        """
        Count occupied spots in a lot
        
        Args:
            lot_id: Lot ID
            
        Returns:
            Number of occupied spots
        """
        return Spot.query.filter_by(lot_id=lot_id, status=False).count()
