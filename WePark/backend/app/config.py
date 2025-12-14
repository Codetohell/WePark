# WePark/testing/backend/app/config.py
"""
Application Configuration
Provides environment-specific configuration classes
"""

from dotenv import load_dotenv
import os
from datetime import timedelta
from typing import Optional

load_dotenv()


class BaseConfig:
    """Base configuration with common settings"""
    
    # Database
    SQLALCHEMY_DATABASE_URI: str = os.getenv("SQLALCHEMY_DATABASE_URI", "sqlite:///wepark.db")
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False
    SQLALCHEMY_ECHO: bool = False
    
    # JWT Configuration
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "default-secret-key-change-in-production")
    JWT_TOKEN_LOCATION: list = ["cookies"]
    JWT_ACCESS_TOKEN_EXPIRES: timedelta = timedelta(days=30)
    JWT_COOKIE_SECURE: bool = False  # Set to True in production with HTTPS
    JWT_COOKIE_CSRF_PROTECT: bool = False
    JWT_COOKIE_SAMESITE: str = "Lax"
    JWT_COOKIE_HTTPONLY: bool = False  # Allow JS to read cookie for persistence
    
    # Payment Gateway (Razorpay)
    RAZORPAY_ACCESS_KEY: Optional[str] = os.getenv("RAZORPAY_ACCESS_KEY")
    RAZORPAY_CLIENT_ID: Optional[str] = os.getenv("RAZORPAY_CLIENT_ID")
    
    # Email Configuration (MailHog for development)
    MAIL_SERVER: str = os.getenv("MAIL_SERVER", "localhost")
    MAIL_PORT: int = int(os.getenv("MAIL_PORT", "1025"))
    MAIL_NAME: Optional[str] = os.getenv("MAIL_NAME", "WePark")
    MAIL_USERNAME: Optional[str] = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD: Optional[str] = os.getenv("MAIL_PASSWORD")
    MAIL_USE_TLS: bool = os.getenv("MAIL_USE_TLS", "False").lower() == "true"
    MAIL_USE_SSL: bool = os.getenv("MAIL_USE_SSL", "False").lower() == "true"
    MAIL_DEFAULT_SENDER: str = os.getenv("MAIL_DEFAULT_SENDER", "noreply@wepark.com")
    
    # Celery Configuration (Redis broker)
    CELERY_BROKER_URL: str = os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/1")
    CELERY_RESULT_BACKEND: str = os.getenv("CELERY_RESULT_BACKEND", "redis://localhost:6379/1")
    CELERY_TASK_SERIALIZER: str = "json"
    CELERY_RESULT_SERIALIZER: str = "json"
    CELERY_ACCEPT_CONTENT: list = ["json"]
    CELERY_TIMEZONE: str = "Asia/Kolkata"
    CELERY_ENABLE_UTC: bool = True
    
    # Redis Cache Configuration
    CACHE_TYPE: str = "RedisCache"
    CACHE_REDIS_HOST: str = os.getenv("CACHE_REDIS_HOST", "localhost")
    CACHE_REDIS_PORT: int = int(os.getenv("CACHE_REDIS_PORT", "6379"))
    CACHE_REDIS_DB: int = int(os.getenv("CACHE_REDIS_DB", "0"))
    CACHE_REDIS_URL: str = os.getenv("CACHE_REDIS_URL", "redis://localhost:6379/0")
    CACHE_DEFAULT_TIMEOUT: int = 300  # 5 minutes
    
    # Frontend Configuration
    FRONTEND_URL: str = os.getenv("FRONTEND_URL", "http://localhost:5173")
    
    # Application Settings
    DEBUG: bool = False
    TESTING: bool = False
    SECRET_KEY: str = os.getenv("SECRET_KEY", "default-secret-key-change-in-production")


class DevelopmentConfig(BaseConfig):
    """Development environment configuration"""
    
    DEBUG: bool = True
    SQLALCHEMY_ECHO: bool = True  # Log SQL queries
    
    # Development-specific overrides
    JWT_COOKIE_SECURE: bool = False
    CACHE_DEFAULT_TIMEOUT: int = 60  # Shorter cache for development


class ProductionConfig(BaseConfig):
    """Production environment configuration"""
    
    DEBUG: bool = False
    TESTING: bool = False
    
    # Production-specific settings
    JWT_COOKIE_SECURE: bool = True  # Require HTTPS
    JWT_COOKIE_CSRF_PROTECT: bool = True  # Enable CSRF protection
    SQLALCHEMY_ECHO: bool = False  # Don't log SQL in production
    
    # Stricter cache timeout
    CACHE_DEFAULT_TIMEOUT: int = 600  # 10 minutes


class TestingConfig(BaseConfig):
    """Testing environment configuration"""
    
    TESTING: bool = True
    DEBUG: bool = True
    
    # Use in-memory database for tests
    SQLALCHEMY_DATABASE_URI: str = "sqlite:///:memory:"
    
    # Disable cache for testing
    CACHE_TYPE: str = "SimpleCache"
    
    # Shorter JWT expiry for tests
    JWT_ACCESS_TOKEN_EXPIRES: timedelta = timedelta(minutes=15)


# Configuration dictionary
config_by_name = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}


def get_config(env_name: Optional[str] = None) -> type[BaseConfig]:
    """
    Get configuration class based on environment name
    
    Args:
        env_name: Environment name ('development', 'production', 'testing')
                 If None, uses FLASK_ENV environment variable
    
    Returns:
        Configuration class
    """
    if env_name is None:
        env_name = os.getenv('FLASK_ENV', 'development')
    
    return config_by_name.get(env_name, DevelopmentConfig)


# Backward compatibility - default Configuration class
Configuration = DevelopmentConfig