# WePark/testing/backend/app/api/payment.py

from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from ..services.payment_service import PaymentService
from datetime import datetime


class PaymentApi(Resource):
    """API endpoint for payment processing"""
    
    def __init__(self):
        self.payment_service = PaymentService()
    
    @jwt_required()
    def post(self):
        """
        Process a payment
        
        Request Body:
            payment_id: Payment ID (mock or Razorpay)
            amount: Payment amount
            reservation_id: Associated reservation ID
            payment_type: 'mock' or 'razorpay'
            
        Returns:
            200: Payment processed
            400: Validation error
        """
        data = request.get_json()
        payment_id = data.get("payment_id")
        amount = data.get("amount")
        reservation_id = data.get("reservation_id")
        payment_type = data.get("payment_type", "mock")
        
        if not payment_id:
            return {"message": "payment_id is required!"}, 400
        if not amount:
            return {"message": "amount is required!"}, 400
        if not reservation_id:
            return {"message": "reservation_id is required!"}, 400
        
        # Process payment based on type
        if payment_type == "mock":
            result = self.payment_service.process_mock_payment(
                payment_id=payment_id,
                amount=amount,
                reservation_id=reservation_id
            )
        elif payment_type == "razorpay":
            razorpay_order_id = data.get("razorpay_order_id")
            razorpay_signature = data.get("razorpay_signature")
            
            result = self.payment_service.process_razorpay_payment(
                razorpay_payment_id=payment_id,
                razorpay_order_id=razorpay_order_id,
                razorpay_signature=razorpay_signature,
                amount=amount,
                reservation_id=reservation_id
            )
        else:
            return {"message": "Invalid payment_type"}, 400
        
        if result['success']:
            return result, 200
        else:
            return {"message": result['message']}, 400
    
    @jwt_required()
    def get(self):
        """
        Verify a payment OR Get payment details for reservation
        
        Query Parameters:
            payment_id: Payment ID to verify
            reservation_id: Reservation ID to initiate payment
            
        Returns:
            200: Payment verification result or Order details
        """
        payment_id = request.args.get("payment_id")
        reservation_id = request.args.get("reservation_id")
        
        if reservation_id:
            # Initiate payment / Get order details
            from ..services.reservation_service import ReservationService
            reservation_service = ReservationService()
            
            reservation = reservation_service.reservation_repo.get_reservation_by_id(reservation_id)
            if not reservation:
                return {"message": "Reservation not found"}, 404
                
            # Calculate amount
            spot = reservation_service.spot_repo.get_spot_by_id(reservation.spot_id)
            lot = reservation_service.lot_repo.get_by_id(spot.lot_id)
            
            total_amount = reservation_service.reservation_repo.calculate_total_amount(
                reservation,
                lot.price_per_hour
            )
            
            # Create mock order
            import uuid
            order_id = f"order_{uuid.uuid4().hex[:10]}"
            
            return {
                "id": order_id,
                "entity": "order",
                "amount": int(total_amount * 100), # Amount in paise
                "amount_paid": 0,
                "amount_due": int(total_amount * 100),
                "currency": "INR",
                "receipt": f"rcpt_{reservation_id}",
                "status": "created",
                "attempts": 0,
                "created_at": 1234567890,
                "reservation_data": {
                    "reservation_id": reservation.reservation_id,
                    "spot_id": reservation.spot_id,
                    "vehicle_number": reservation.vehicle_number,
                    "parking_time": reservation.parking_timestamp.isoformat() if reservation.parking_timestamp else None,
                    "leaving_time": datetime.now().isoformat(),
                    "total_cost": int(total_amount * 100)  # Amount in paise for consistency
                }
            }, 200
        
        if not payment_id:
            return {"message": "payment_id or reservation_id is required!"}, 400
        
        result = self.payment_service.verify_mock_payment(payment_id)
        
        return result, 200