from os import environ

from dotenv import load_dotenv

__all__ = ['config']

load_dotenv()

class _Config:
    """
    The default configuration for the app

    Attributes:
    SECRET_KEY: str (the server secret key)
    DEBUG: bool (determines if debug mode is on)
    PORT: int (the server's port)
    DB_CONFIG: dict (the database settings, from environment variables)
    """
    SECRET_KEY = environ.get('SECRET_KEY')
    DEBUG = True
    PORT = environ.get('PORT')
    DB_CONFIG = {
        'host': environ.get('DB_HOST'),
        'database': environ.get('DB_NAME'),
        'user': environ.get('DB_USER'),
        'password': environ.get('DB_PASSWORD'),
        'port': int(environ.get('DB_PORT'))
    }

class _ProductionConfig(_Config):
    """Production configuration"""
    DEBUG = False

# _Configuration dictionary to allow selection of a configuration
config = {
    'production': _ProductionConfig,
    'development': _Config,
    'default': _Config,
}
