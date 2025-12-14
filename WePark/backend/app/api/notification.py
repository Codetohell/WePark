# WePark/testing/backend/app/api/notification.py

from flask_restful import Resource
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..services.notification_service import NotificationService


class NotificationApi(Resource):
    """API endpoint for notification management"""
    
    def __init__(self):
        self.notification_service = NotificationService()
    
    @jwt_required()
    def get(self):
        """
        Get user's notifications
        
        Query Parameters:
            unread: If true, return only unread notifications
            
        Returns:
            200: List of notifications
        """
        # Get user from JWT
        identity = get_jwt_identity()
        from ..models import User
        user = User.query.filter_by(username=identity).first()
        
        if not user:
            return {"message": "User not found"}, 404
        
        # Check if only unread notifications requested
        unread_only = request.args.get('unread', 'false').lower() == 'true'
        
        notifications = self.notification_service.get_user_notifications(
            user_id=user.user_id,
            unread_only=unread_only
        )
        
        return notifications, 200
    
    @jwt_required()
    def post(self):
        """
        Mark notification(s) as read
        
        Request Body:
            notification_id: Optional specific notification ID
            mark_all: If true, mark all as read
            
        Returns:
            200: Notification(s) marked as read
            400: Validation error
        """
        data = request.get_json()
        notification_id = data.get("notification_id")
        mark_all = data.get("mark_all", False)
        
        # Get user from JWT
        identity = get_jwt_identity()
        from ..models import User
        user = User.query.filter_by(username=identity).first()
        
        if not user:
            return {"message": "User not found"}, 404
        
        if mark_all:
            result = self.notification_service.mark_all_read(user.user_id)
        elif notification_id:
            result = self.notification_service.mark_notification_read(notification_id)
        else:
            return {"message": "notification_id or mark_all is required"}, 400
        
        if result['success']:
            return {"message": result['message']}, 200
        else:
            return {"message": result['message']}, 400
    
    @jwt_required()
    def delete(self, notification_id):
        """
        Delete a notification
        
        Args:
            notification_id: Notification ID
            
        Returns:
            200: Notification deleted
            404: Notification not found
        """
        result = self.notification_service.delete_notification(notification_id)
        
        if result['success']:
            return {"message": result['message']}, 200
        else:
            return {"message": result['message']}, 404