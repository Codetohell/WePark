# WePark/testing/backend/app/api/spot.py

from flask_restful import Resource
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..services.spot_service import SpotService
from ..services.reservation_service import ReservationService
from ..utils.decorators import role_required
from .. import cache


class SpotApi(Resource):
    """API endpoint for parking spot operations"""
    
    def __init__(self):
        self.spot_service = SpotService()
        self.reservation_service = ReservationService()
    
    @jwt_required()
    def post(self):
        """
        Book a parking spot
        
        Request Body:
            spot_id: Spot ID to book
            
        Returns:
            200: Spot booked successfully
            400: Validation error or spot unavailable
            500: Server error
        """
        cache.clear()
        data = request.get_json()
        spot_id = data.get("spot_id")
        
        if not spot_id:
            return {"message": "spot_id is required!"}, 400
        
        # Get user ID from JWT
        identity = get_jwt_identity()
        from ..models import User
        user = User.query.filter_by(username=identity).first()
        
        if not user:
            return {"message": "User not found"}, 404
        
        # Create reservation using service
        result = self.reservation_service.create_reservation(
            user_id=user.user_id,
            spot_id=spot_id
        )
        
        if result['success']:
            return {"message": result['message']}, 200
        else:
            return {"message": result['message']}, 400
    
    @jwt_required()
    @cache.cached(timeout=120, query_string=True)  # Cache for 2 minutes
    def get(self, spot_id=None):
        """
        Get spot details or availability
        
        Args:
            spot_id: Optional spot ID
            
        Returns:
            200: Spot details
            404: Spot not found
        """
        if spot_id:
            spot = self.spot_service.get_spot_by_id(spot_id)
            if spot:
                return spot, 200
            else:
                return {"message": "Spot not found"}, 404
        else:
            return {"message": "spot_id is required"}, 400
