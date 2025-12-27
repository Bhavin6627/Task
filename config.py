import os

class Config:
    # JWT Configuration
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'super-secret-jwt-key-change-in-production')
    JWT_ACCESS_TOKEN_EXPIRES = 3600  # 1 hour
    
    # Database
    SQLALCHEMY_DATABASE_URI = 'sqlite:///booking.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # CRM Configuration
    CRM_URL = os.environ.get('CRM_URL', 'http://localhost:5001')
    CRM_BEARER_TOKEN = os.environ.get('CRM_BEARER_TOKEN', 'crm-secret-token-12345')


class CRMConfig:
    # CRM Database
    SQLALCHEMY_DATABASE_URI = 'sqlite:///crm.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Static Bearer Token for authentication
    BEARER_TOKEN = os.environ.get('CRM_BEARER_TOKEN', 'crm-secret-token-12345')
