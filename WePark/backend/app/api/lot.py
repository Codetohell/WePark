# WePark/testing/backend/app/api/lot.py

from flask_restful import Resource
from flask import request
from flask_jwt_extended import jwt_required
from ..services.lot_service import LotService
from ..utils.decorators import role_required
from .. import cache


class LotApi(Resource):
    """API endpoint for parking lot management"""
    
    def __init__(self):
        self.lot_service = LotService()
    
    @jwt_required()
    @role_required("admin")
    def post(self):
        """
        Create a new parking lot
        
        Request Body:
            prime_location: Location name
            price_per_hour: Hourly rate
            address: Full address
            pincode: Area pincode
            no_of_spots: Number of parking spots
            
        Returns:
            201: Lot created successfully
            400: Validation error
            500: Server error
        """
        cache.clear()
        data = request.get_json()
        
        # Extract and validate fields
        prime_location = data.get("prime_location")
        price_per_hour = data.get("price_per_hour")
        address = data.get("address")
        pincode = data.get("pincode")
        no_of_spots = data.get("no_of_spots")

        # Validate required fields
        if not prime_location:
            return {"message": "prime_location is required!"}, 400
        if not price_per_hour:
            return {"message": "price_per_hour is required!"}, 400
        if not address:
            return {"message": "address is required!"}, 400
        if not pincode:
            return {"message": "pincode is required!"}, 400
        if not no_of_spots:
            return {"message": "no_of_spots is required!"}, 400
        
        # Create lot using service
        result = self.lot_service.create_lot(
            prime_location=prime_location,
            price_per_hour=price_per_hour,
            address=address,
            pincode=pincode,
            no_of_spots=no_of_spots
        )
        
        if result['success']:
            return {"message": result['message']}, 201
        else:
            return {"message": result['message']}, 500
    
    @jwt_required()
    @cache.cached(timeout=60, query_string=True)
    def get(self, lot_id=None):
        """
        Get parking lot(s)
        
        Args:
            lot_id: Optional lot ID for specific lot
            
        Query Parameters:
            name: Filter by location name
            pincode: Filter by pincode
            address: Filter by address
            
        Returns:
            200: Lot details
            400: Lot not found
            500: Server error
        """
        try:
            if lot_id is None:
                # Get all lots with optional filters
                parameters = request.args
                name = parameters.get("name")
                pincode = parameters.get("pincode")
                address = parameters.get("address")
                
                lots = self.lot_service.get_all_lots(
                    name=name,
                    pincode=pincode,
                    address=address
                )
                return lots, 200
            else:
                # Get specific lot
                lot = self.lot_service.get_lot_by_id(lot_id)
                if lot:
                    return lot, 200
                else:
                    return {"message": "Parking Lot not found"}, 400
        except Exception as e:
            return {"message": "Something went wrong!"}, 500

    @jwt_required()
    @role_required("admin")
    def put(self, lot_id):
        """
        Update parking lot details
        
        Args:
            lot_id: Lot ID
            
        Request Body:
            prime_location: Optional location name
            price_per_hour: Optional hourly rate
            address: Optional address
            pincode: Optional pincode
            
        Returns:
            200: Lot updated successfully
            404: Lot not found
            500: Server error
        """
        cache.clear()
        data = request.get_json()
        
        # Update lot using service
        filtered_data = {k: v for k, v in data.items() if k != 'lot_id'}
        result = self.lot_service.update_lot(lot_id, **filtered_data)
        #result = self.lot_service.update_lot(lot_id, **data)
        
        if result['success']:
            return {"message": result['message']}, 200
        else:
            status_code = 404 if 'not found' in result['message'].lower() else 500
            return {"message": result['message']}, status_code

    @jwt_required()
    @role_required("admin")
    def delete(self, lot_id):
        """
        Delete a parking lot
        
        Args:
            lot_id: Lot ID
            
        Returns:
            200: Lot deleted successfully
            400: Cannot delete (spots occupied) or lot not found
            500: Server error
        """
        cache.clear()
        
        # Delete lot using service
        result = self.lot_service.delete_lot(lot_id)
        
        if result['success']:
            return {"message": result['message']}, 200
        else:
            return {"message": result['message']}, 400