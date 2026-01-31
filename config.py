from os import environ

from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = environ.get('SECRET_KEY')
    DEBUG = True
    PORT = environ.get('PORT')
    
    # Database configuration
    DB_CONFIG = {
        'host': environ.get('DB_HOST'),
        'database': environ.get('DB_NAME'),
        'user': environ.get('DB_USER'),
        'password': environ.get('DB_PASSWORD'),
        'port': int(environ.get('DB_PORT', 3306))
    }

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False

# Configuration dictionary
config = {
    'production': ProductionConfig,
    'development': Config,
    'default': Config,
}
