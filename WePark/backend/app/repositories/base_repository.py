# WePark/testing/backend/app/repositories/base_repository.py
"""
Base Repository - Common CRUD Operations
Provides reusable database operations for all repositories
"""

from typing import TypeVar, Generic, List, Optional, Type, Dict, Any
from sqlalchemy.orm import Session
from .. import db

ModelType = TypeVar('ModelType')


class BaseRepository(Generic[ModelType]):
    """Base repository with common CRUD operations"""
    
    def __init__(self, model: Type[ModelType]):
        """
        Initialize repository with model class
        
        Args:
            model: SQLAlchemy model class
        """
        self.model = model
        self.session: Session = db.session
    
    def create(self, **kwargs) -> ModelType:
        """
        Create a new record
        
        Args:
            **kwargs: Field values for the new record
            
        Returns:
            Created model instance
        """
        instance = self.model(**kwargs)
        self.session.add(instance)
        return instance
    
    def get_by_id(self, id_value: Any) -> Optional[ModelType]:
        """
        Get record by primary key
        
        Args:
            id_value: Primary key value
            
        Returns:
            Model instance or None
        """
        return self.model.query.get(id_value)
    
    def get_by_field(self, field_name: str, value: Any) -> Optional[ModelType]:
        """
        Get first record matching field value
        
        Args:
            field_name: Name of the field to filter by
            value: Value to match
            
        Returns:
            Model instance or None
        """
        return self.model.query.filter_by(**{field_name: value}).first()
    
    def get_all(self, filters: Optional[Dict[str, Any]] = None) -> List[ModelType]:
        """
        Get all records, optionally filtered
        
        Args:
            filters: Optional dictionary of field:value filters
            
        Returns:
            List of model instances
        """
        query = self.model.query
        if filters:
            query = query.filter_by(**filters)
        return query.all()
    
    def update(self, instance: ModelType, **kwargs) -> ModelType:
        """
        Update a record
        
        Args:
            instance: Model instance to update
            **kwargs: Fields to update
            
        Returns:
            Updated model instance
        """
        for key, value in kwargs.items():
            if hasattr(instance, key):
                setattr(instance, key, value)
        return instance
    
    def delete(self, instance: ModelType) -> None:
        """
        Delete a record
        
        Args:
            instance: Model instance to delete
        """
        self.session.delete(instance)
    
    def commit(self) -> None:
        """Commit the current transaction"""
        self.session.commit()
    
    def rollback(self) -> None:
        """Rollback the current transaction"""
        self.session.rollback()
    
    def flush(self) -> None:
        """Flush pending changes"""
        self.session.flush()
    
    def count(self, filters: Optional[Dict[str, Any]] = None) -> int:
        """
        Count records
        
        Args:
            filters: Optional dictionary of field:value filters
            
        Returns:
            Number of records
        """
        query = self.model.query
        if filters:
            query = query.filter_by(**filters)
        return query.count()
    
    def exists(self, filters: Dict[str, Any]) -> bool:
        """
        Check if record exists
        
        Args:
            filters: Dictionary of field:value filters
            
        Returns:
            True if record exists, False otherwise
        """
        return self.count(filters) > 0
