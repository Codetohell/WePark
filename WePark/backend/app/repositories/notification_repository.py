# WePark/testing/backend/app/repositories/notification_repository.py
"""
Notification Repository - Notification Data Access
Handles database operations for notifications
"""

from typing import List, Optional
from .base_repository import BaseRepository
from ..models.notification import Notification


class NotificationRepository(BaseRepository[Notification]):
    """Repository for notification operations"""
    
    def __init__(self):
        super().__init__(Notification)
    
    def find_by_user(self, user_id: int) -> List[Notification]:
        """
        Get all notifications for a user
        
        Args:
            user_id: User ID
            
        Returns:
            List of user's notifications
        """
        return Notification.query.filter_by(user_id=user_id).order_by(Notification.notification_id.desc()).all()
    
    def find_unread_by_user(self, user_id: int) -> List[Notification]:
        """
        Get unread notifications for a user (returns all since no is_read field)
        
        Args:
            user_id: User ID
            
        Returns:
            List of notifications
        """
        return Notification.query.filter_by(user_id=user_id).order_by(Notification.notification_id.desc()).all()
    
    def mark_as_read(self, notification: Notification) -> Notification:
        """
        Mark notification as read (no-op since no is_read field)
        
        Args:
            notification: Notification instance
            
        Returns:
            Notification unchanged
        """
        return notification
    
    def mark_all_as_read(self, user_id: int) -> None:
        """
        Mark all notifications as read (no-op since no is_read field)
        
        Args:
            user_id: User ID
        """
        pass
    
    def count_unread(self, user_id: int) -> int:
        """
        Count unread notifications (returns total count since no is_read field)
        
        Args:
            user_id: User ID
            
        Returns:
            Number of notifications
        """
        return Notification.query.filter_by(user_id=user_id).count()
    
    def get_notification_by_id(self, notification_id: int) -> Optional[Notification]:
        """
        Get notification by ID
        
        Args:
            notification_id: Notification ID
            
        Returns:
            Notification instance or None
        """
        return Notification.query.filter_by(notification_id=notification_id).first()
