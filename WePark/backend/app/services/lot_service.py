# WePark/testing/backend/app/services/lot_service.py
"""
Lot Service - Parking Lot Business Logic
Handles all business operations related to parking lots
"""

from typing import List, Optional, Dict, Any
from ..repositories.lot_repository import LotRepository
from ..repositories.spot_repository import SpotRepository
from .. import db


class LotService:
    """Service for parking lot operations"""
    
    def __init__(self):
        self.lot_repo = LotRepository()
        self.spot_repo = SpotRepository()
    
    def create_lot(self, prime_location: str, price_per_hour: int, 
                   address: str, pincode: int, no_of_spots: int) -> Dict[str, Any]:
        """Creates parking lot and initializes all spots"""
        try:
            # Step 1: Initialize the lot record
            lot = self.lot_repo.create(
                prime_location=prime_location,
                price_per_hour=price_per_hour,
                address=address,
                pincode=pincode,
                no_of_spots=no_of_spots
            )
            self.lot_repo.flush()
            
            # Step 2: Generate individual spots for this lot
            for _ in range(no_of_spots):
                self.spot_repo.create(lot_id=lot.lot_id)
            
            self.lot_repo.commit()
            
            return {
                'success': True,
                'message': 'Parking Lot added successfully!',
                'lot_id': lot.lot_id
            }
        except Exception as e:
            self.lot_repo.rollback()
            return {
                'success': False,
                'message': 'Something went wrong!',
                'error': str(e)
            }
    
    def get_lot_by_id(self, lot_id: int) -> Optional[Dict[str, Any]]:
        """
        Get lot details by ID
        
        Args:
            lot_id: Lot ID
            
        Returns:
            Lot details dictionary or None
        """
        lot = self.lot_repo.get_by_id(lot_id)
        if not lot:
            return None
        
        return self._format_lot_details(lot)
    
    def get_all_lots(self, name: Optional[str] = None, 
                     pincode: Optional[str] = None, 
                     address: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Get all lots with optional filters
        
        Args:
            name: Optional location name filter
            pincode: Optional pincode filter
            address: Optional address filter
            
        Returns:
            List of lot details
        """
        lots = self.lot_repo.search_lots(name=name, pincode=pincode, address=address)
        return [self._format_lot_details(lot) for lot in lots]
    
    def update_lot(self, lot_id: int, **kwargs) -> Dict[str, Any]:
        """
        Update lot details
        
        Args:
            lot_id: Lot ID
            **kwargs: Fields to update
            
        Returns:
            Result dictionary
        """
        try:
            kwargs.pop('lot_id', None)
            lot = self.lot_repo.get_by_id(lot_id)
            if not lot:
                return {
                    'success': False,
                    'message': 'Parking Lot not found!'
                }
            
            # Update allowed fields
            allowed_fields = ['prime_location', 'price_per_hour', 'address', 'pincode']
            update_data = {k: v for k, v in kwargs.items() if k in allowed_fields}
            
            self.lot_repo.update(lot, **update_data)
            self.lot_repo.commit()
            
            return {
                'success': True,
                'message': 'Parking Lot updated successfully!'
            }
        except Exception as e:
            self.lot_repo.rollback()
            return {
                'success': False,
                'message': 'Something went wrong!',
                'error': str(e)
            }
    
    def delete_lot(self, lot_id: int) -> Dict[str, Any]:
        """
        Delete a parking lot
        
        Args:
            lot_id: Lot ID
            
        Returns:
            Result dictionary
        """
        try:
            lot = self.lot_repo.get_by_id(lot_id)
            if not lot:
                return {
                    'success': False,
                    'message': 'Parking lot not found!'
                }
            
            if not self.lot_repo.can_delete_lot(lot):
                return {
                    'success': False,
                    'message': 'This Parking Lot cannot be deleted. One or more spots are occupied!'
                }
            
            self.lot_repo.delete(lot)
            self.lot_repo.commit()
            
            return {
                'success': True,
                'message': 'Parking lot deleted successfully!'
            }
        except Exception as e:
            self.lot_repo.rollback()
            return {
                'success': False,
                'message': 'Something went wrong!',
                'error': str(e)
            }
    
    def _format_lot_details(self, lot) -> Dict[str, Any]:
        """
        Format lot object to dictionary
        
        Args:
            lot: Lot model instance
            
        Returns:
            Formatted lot dictionary
        """
        return {
            'lot_id': lot.lot_id,
            'prime_location': lot.prime_location,
            'price_per_hour': lot.price_per_hour,
            'address': lot.address,
            'pincode': lot.pincode,
            'no_of_spots': lot.no_of_spots,
            'spots': [{
                'spot_id': spot.spot_id,
                'status': spot.status
            } for spot in lot.spots]
        }
