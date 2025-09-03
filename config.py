"""
Configuration file for the Medical Laboratory Management System
"""
import os

class Config:
    # Database configuration
    DATABASE_URL = os.environ.get('DATABASE_URL', 'sqlite:///medical_lab.db')
    
    # Security configuration
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key')
    PASSWORD_SALT = os.environ.get('PASSWORD_SALT', 'dev-password-salt')
    
    # Language configuration
    LANGUAGES = {
        'en': 'English',
        'ar': 'Arabic'
    }
    BABEL_DEFAULT_LOCALE = 'en'
    BABEL_DEFAULT_TIMEZONE = 'UTC'
    
    # Email configuration
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', '587'))
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'true').lower() in ['true', 'on', '1']
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    
    # Barcode configuration
    BARCODE_FORMAT = 'CODE128'
    
    # Pagination
    PATIENTS_PER_PAGE = 20
    TESTS_PER_PAGE = 20