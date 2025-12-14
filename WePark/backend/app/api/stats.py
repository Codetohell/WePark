# Core imports
import calendar
import re
from collections import defaultdict

# Flask imports
from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt

# Local imports
from ..models import Spot, Reservation, User, Lot
from ..utils.decorators import role_required
from ..utils.business_helpers import lot_can_delete
from ..utils.datetime_helpers import get_ist_time, get_past_months
from .. import db, cache


class   StatsApi(Resource):
    
    @jwt_required()
    def get(self):
        try:
            decoded_token = get_jwt()
            role = decoded_token.get("role")
            if role == "admin":
                reservations_per_lot = {}
                reservations = Reservation.query.all()
                reservations_per_lot = {}
                for reservation in reservations:
                    prime_location = reservation.spot.lot.prime_location
                    if prime_location in reservations_per_lot:
                        reservations_per_lot[prime_location] += 1
                    else:
                        reservations_per_lot[prime_location] = 1
                return reservations_per_lot,200
            elif role == "user":
                username = get_jwt_identity()
                user = User.query.filter_by(username=username).first()
                user_id = user.user_id
                # Get all user reservations
                all_reservations = Reservation.query.filter_by(user_id=user_id).all()
                total_reservations = len(all_reservations)
                
                # Count completed bookings (those with leaving_timestamp)
                completed_reservations = [r for r in all_reservations if r.leaving_timestamp is not None]
                total_bookings = len(completed_reservations)
                
                # Calculate total amount spent (from completed reservations)
                total_amount = 0
                for reservation in completed_reservations:
                    if reservation.parking_cost:
                        # Smart detection: if cost > 1000, it's likely in paise (old data)
                        cost = reservation.parking_cost / 100 if reservation.parking_cost > 1000 else reservation.parking_cost
                        total_amount += cost
                lot_counts = {}
                reservation3 = Reservation.query.filter_by(user_id=user_id).all()
                for reserve in reservation3:
                    lot = reserve.spot.lot.prime_location
                    if lot in lot_counts:
                        lot_counts[lot] += 1
                    else:
                        lot_counts[lot] = 1
                most_visited_lot = max(lot_counts, key=lot_counts.get) if lot_counts else None
                #BAR CHART
                month_counts = defaultdict(int)
                months = get_past_months(k=4)

                for reservation in reservation3:
                    dt = reservation.parking_timestamp
                    if dt:
                        year_month = (dt.year, dt.month)
                        if year_month in months:
                            month_counts[year_month] += 1

                final_data = {
                    calendar.month_name[m]: month_counts[(y, m)]
                    for (y, m) in months
                }
                #PIE CHART
                reservations_per_lot = {}
                for reservation in reservation3:
                    prime_location = reservation.spot.lot.prime_location
                    if prime_location in reservations_per_lot:
                        reservations_per_lot[prime_location] += 1
                    else:
                        reservations_per_lot[prime_location] = 1
                return {
                    "total_reservations":total_reservations,
                    "total_amount": total_amount,
                    "total_bookings": total_bookings,
                    "most_visited_lot":most_visited_lot,
                    "barchart":final_data,
                    "piechart": reservations_per_lot
                }, 200
                
        except Exception as e:
            return {"message":f"Something went wrong!{e}"}, 500
                    
                
