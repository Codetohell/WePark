# WePark/testing/backend/app/services/notification_service.py
"""
Notification Service - Notification Business Logic
Handles notification creation and management
"""

from typing import List, Dict, Any, Optional
from ..repositories.notification_repository import NotificationRepository


class NotificationService:
    """Service for notification operations"""
    
    def __init__(self):
        self.notification_repo = NotificationRepository()
    
    def create_notification(self, user_id: int, title: str, body: str) -> Dict[str, Any]:
        """
        Create a new notification for a user
        
        Args:
            user_id: User ID
            title: Notification title
            body: Notification body/message
            
        Returns:
            Result dictionary
        """
        try:
            notification = self.notification_repo.create(
                user_id=user_id,
                title=title,
                body=body
            )
            self.notification_repo.commit()
            
            return {
                'success': True,
                'message': 'Notification created',
                'notification_id': notification.notification_id
            }
        except Exception as e:
            self.notification_repo.rollback()
            return {
                'success': False,
                'message': 'Failed to create notification',
                'error': str(e)
            }
    
    def get_user_notifications(self, user_id: int, unread_only: bool = False) -> List[Dict[str, Any]]:
        """
        Get notifications for a user
        
        Args:
            user_id: User ID
            unread_only: If True, return only unread notifications
            
        Returns:
            List of notification details
        """
        if unread_only:
            notifications = self.notification_repo.find_unread_by_user(user_id)
        else:
            notifications = self.notification_repo.find_by_user(user_id)
        
        return [self._format_notification_details(n) for n in notifications]
    
    def mark_notification_read(self, notification_id: int) -> Dict[str, Any]:
        """
        Mark a notification as read
        
        Args:
            notification_id: Notification ID
            
        Returns:
            Result dictionary
        """
        try:
            notification = self.notification_repo.get_notification_by_id(notification_id)
            if not notification:
                return {
                    'success': False,
                    'message': 'Notification not found'
                }
            
            self.notification_repo.mark_as_read(notification)
            self.notification_repo.commit()
            
            return {
                'success': True,
                'message': 'Notification marked as read'
            }
        except Exception as e:
            self.notification_repo.rollback()
            return {
                'success': False,
                'message': 'Failed to update notification',
                'error': str(e)
            }
    
    def mark_all_read(self, user_id: int) -> Dict[str, Any]:
        """
        Mark all notifications as read for a user
        
        Args:
            user_id: User ID
            
        Returns:
            Result dictionary
        """
        try:
            self.notification_repo.mark_all_as_read(user_id)
            self.notification_repo.commit()
            
            return {
                'success': True,
                'message': 'All notifications marked as read'
            }
        except Exception as e:
            self.notification_repo.rollback()
            return {
                'success': False,
                'message': 'Failed to update notifications',
                'error': str(e)
            }
    
    def get_unread_count(self, user_id: int) -> int:
        """
        Get count of unread notifications for a user
        
        Args:
            user_id: User ID
            
        Returns:
            Unread notification count
        """
        return self.notification_repo.count_unread(user_id)
    
    def delete_notification(self, notification_id: int) -> Dict[str, Any]:
        """
        Delete a notification
        
        Args:
            notification_id: Notification ID
            
        Returns:
            Result dictionary
        """
        try:
            notification = self.notification_repo.get_notification_by_id(notification_id)
            if not notification:
                return {
                    'success': False,
                    'message': 'Notification not found'
                }
            
            self.notification_repo.delete(notification)
            self.notification_repo.commit()
            
            return {
                'success': True,
                'message': 'Notification deleted'
            }
        except Exception as e:
            self.notification_repo.rollback()
            return {
                'success': False,
                'message': 'Failed to delete notification',
                'error': str(e)
            }
    
    def _format_notification_details(self, notification) -> Dict[str, Any]:
        """
        Format notification object to dictionary
        
        Args:
            notification: Notification model instance
            
        Returns:
            Formatted notification dictionary
        """
        return {
            'notification_id': notification.notification_id,
            'user_id': notification.user_id,
            'title': notification.title,
            'body': notification.body
        }
