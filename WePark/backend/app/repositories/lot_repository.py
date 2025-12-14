# WePark/testing/backend/app/repositories/lot_repository.py
"""
Lot Repository - Parking Lot Data Access
Handles database operations for parking lots
"""

from typing import List, Optional
from .base_repository import BaseRepository
from ..models.lot import Lot


class LotRepository(BaseRepository[Lot]):
    """Repository for parking lot operations"""
    
    def __init__(self):
        super().__init__(Lot)
    
    def find_by_location(self, location: str) -> List[Lot]:
        """
        Find lots by prime location (case-insensitive partial match)
        
        Args:
            location: Location string to search for
            
        Returns:
            List of matching lots
        """
        return Lot.query.filter(Lot.prime_location.ilike(f"%{location}%")).all()
    
    def find_by_pincode(self, pincode: str) -> List[Lot]:
        """
        Find lots by pincode (case-insensitive partial match)
        
        Args:
            pincode: Pincode to search for
            
        Returns:
            List of matching lots
        """
        return Lot.query.filter(Lot.pincode.ilike(f"%{pincode}%")).all()
    
    def find_by_address(self, address: str) -> List[Lot]:
        """
        Find lots by address (case-insensitive partial match)
        
        Args:
            address: Address string to search for
            
        Returns:
            List of matching lots
        """
        return Lot.query.filter(Lot.address.ilike(f"%{address}%")).all()
    
    def search_lots(self, name: Optional[str] = None, 
                    pincode: Optional[str] = None, 
                    address: Optional[str] = None) -> List[Lot]:
        """
        Search lots with multiple optional filters
        
        Args:
            name: Optional location name filter
            pincode: Optional pincode filter
            address: Optional address filter
            
        Returns:
            List of matching lots
        """
        query = Lot.query
        
        if name:
            query = query.filter(Lot.prime_location.ilike(f"%{name}%"))
        if pincode:
            query = query.filter(Lot.pincode.ilike(f"%{pincode}%"))
        if address:
            query = query.filter(Lot.address.ilike(f"%{address}%"))
        
        return query.all()
    
    def get_lot_with_spots(self, lot_id: int) -> Optional[Lot]:
        """
        Get lot with all its spots loaded
        
        Args:
            lot_id: Lot ID
            
        Returns:
            Lot instance with spots or None
        """
        return Lot.query.filter_by(lot_id=lot_id).first()
    
    def can_delete_lot(self, lot: Lot) -> bool:
        """
        Check if a lot can be deleted (no occupied spots)
        
        Args:
            lot: Lot instance to check
            
        Returns:
            True if lot can be deleted, False otherwise
        """
        for spot in lot.spots:
            if spot.status is False:
                return False
        return True
