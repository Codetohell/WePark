# WePark/testing/backend/app/api/reservation.py

from flask_restful import Resource
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..services.reservation_service import ReservationService
from ..services.payment_service import PaymentService
from .. import cache
from .. import db


class ReservationApi(Resource):
    """API endpoint for reservation management"""
    
    def __init__(self):
        self.reservation_service = ReservationService()
        self.payment_service = PaymentService()
    
    @jwt_required()
    def get(self):
        """
        Get user's reservations
        
        Query Parameters:
            active: If true, return only active reservations
            
        Returns:
            200: List of reservations
        """
        # Get user from JWT
        identity = get_jwt_identity()
        from ..models import User
        from flask_jwt_extended import get_jwt
        
        claims = get_jwt()
        role = claims.get('role')
        
        if role == 'admin':
            # Admin can see all reservations
            # If payment_status filter is present
            payment_status = request.args.get('payment_status')
            if payment_status:
                is_paid = payment_status.lower() == 'true'
                reservations = self.reservation_service.reservation_repo.find_by_payment_status(is_paid)
            else:
                reservations = self.reservation_service.reservation_repo.get_all()
            
            # Serialize reservations with user details for admin
            serialized = []
            for res in reservations:
                user = self.reservation_service.user_repo.get_by_id(res.user_id)
                serialized.append({
                    'reservation_id': res.reservation_id,
                    'user_id': res.user_id,
                    'username': user.username if user else 'Unknown',
                    'email': user.email if user else 'Unknown',
                    'spot_id': res.spot_id,
                    'parking_timestamp': res.parking_timestamp.isoformat() if res.parking_timestamp else None,
                    'leaving_timestamp': res.leaving_timestamp.isoformat() if res.leaving_timestamp else None,
                    'parking_cost': res.parking_cost,
                    'vehicle_number': res.vehicle_number,
                    'payment_status': res.payment_status
                })
            return serialized, 200
            
        user = User.query.filter_by(username=identity).first()
        
        if not user:
            return {"message": "User not found"}, 404
        
        # Check if only active reservations requested
        active_only = request.args.get('active', 'false').lower() == 'true'
        
        reservations = self.reservation_service.get_user_reservations(
            user_id=user.user_id,
            active_only=active_only
        )
        
        return reservations, 200
    
    @jwt_required()
    def post(self, spot_id=None):
        """
        Book a parking spot OR Release a parking spot
        
        Args:
            spot_id: Optional spot ID for booking
            
        Returns:
            200: Success
            400: Error
        """
        cache.clear()
        
        # Get request data
        data = request.get_json() or {}
        
        # Get user identity
        identity = get_jwt_identity()
        from ..models import User
        user = User.query.filter_by(username=identity).first()
        
        if not user:
            return {"message": "User not found"}, 404
        
        # If spot_id is provided in URL, it's a booking request for specific spot
        if spot_id:
            vehicle_number = data.get("vehicle_number", "Unknown")
                
            # Create reservation
            result = self.reservation_service.create_reservation(
                user_id=user.user_id,
                spot_id=spot_id,
                vehicle_number=vehicle_number
            )
            
            if result['success']:
                return result, 200
            else:
                return {"message": result['message']}, 400
        
        # Check if lot_id is provided for auto-allocation
        lot_id = data.get("lot_id")
        if lot_id:
            vehicle_number = data.get("vehicle_number", "Unknown")
            
            # Find first available spot in the lot
            from ..models import Spot
            available_spot = Spot.query.filter_by(
                lot_id=lot_id,
                status=True
            ).first()
            
            if not available_spot:
                return {"message": "No available spots in this parking lot"}, 400
            
            # Create reservation with auto-allocated spot
            result = self.reservation_service.create_reservation(
                user_id=user.user_id,
                spot_id=available_spot.spot_id,
                vehicle_number=vehicle_number
            )
            
            if result['success']:
                return result, 200
            else:
                return {"message": result['message']}, 400
        
        # If no spot_id or lot_id, it's a release request
        reservation_id = data.get("reservation_id")
        payment_id = data.get("payment_id")
        
        if not reservation_id:
            return {"message": "reservation_id or lot_id is required!"}, 400
        
        # Complete reservation
        result = self.reservation_service.complete_reservation(reservation_id)
        
        if result['success']:
            # Process payment if payment_id provided
            if payment_id:
                payment_result = self.payment_service.process_mock_payment(
                    payment_id=payment_id,
                    amount=result['total_amount'],
                    reservation_id=reservation_id
                )
                
                if not payment_result['success']:
                    return {"message": payment_result['message']}, 400
                
                # CRITICAL FIX: Update payment_status to True
                from ..models import Reservation
                reservation = Reservation.query.get(reservation_id)
                reservation.payment_status = True
                db.session.commit()
            
            return {
                "message": result['message'],
                "total_amount": result['total_amount']
            }, 200
        else:
            return {"message": result['message']}, 400

    @jwt_required()
    def put(self, reservation_id=None):
        """
        Update reservation (e.g. mark as parked)
        """
        if not reservation_id:
            return {"message": "reservation_id is required"}, 400
            
        # Handle "Occupy" action - set parking_timestamp
        from datetime import datetime
        from ..models import Reservation
        
        reservation = Reservation.query.get(reservation_id)
        if not reservation:
            return {"message": "Reservation not found"}, 404
            
        if reservation.parking_timestamp:
            return {"message": "Spot already occupied"}, 400
            
        reservation.parking_timestamp = datetime.now()
        db.session.commit()
        
        return {"message": "Spot occupied successfully", "parking_time": reservation.parking_timestamp.isoformat()}, 200