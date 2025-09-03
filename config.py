import os

class Config:
    """Base configuration class"""
    SECRET_KEY = os.environ.get('SECRET_KEY') # or 'your-secret-key-change-this-in-production'
    
    # Database configuration
    DB_CONFIG = {
        'host': os.environ.get('DB_HOST'), # or 'localhost',
        'database': os.environ.get('DB_NAME'), # or 'budget_db',
        'user': os.environ.get('DB_USER'), # or 'your_username',
        'password': os.environ.get('DB_PASSWORD'), # or 'your_password',
        'port': int(os.environ.get('DB_PORT', 3306))
    }

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    # In production, these should come from environment variables
    DB_CONFIG = {
        'host': os.environ.get('DB_HOST'),
        'database': os.environ.get('DB_NAME'),
        'user': os.environ.get('DB_USER'),
        'password': os.environ.get('DB_PASSWORD'),
        'port': int(os.environ.get('DB_PORT', 3306))
    }

# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
