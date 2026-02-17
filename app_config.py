__all__ = ['config', 'is_dotenv_loaded']

from os import environ

from dotenv import load_dotenv

is_dotenv_loaded = load_dotenv()

class _Config:
    SECRET_KEY = environ.get('SECRET_KEY')
    DEBUG = True
    PORT = environ.get('PORT') # The server's port
    DB_CONFIG = {
        'host': environ.get('DB_HOST'),
        'database': environ.get('DB_NAME'),
        'user': environ.get('DB_USER'),
        'password': environ.get('DB_PASSWORD'),
        'port': int(environ.get('DB_PORT', 3306)) # The database's port
    }

class _ProductionConfig(_Config):
    DEBUG = False

# _Configuration dictionary to allow selection of a configuration
config = {
    'development': _Config,
    'production': _ProductionConfig,
    'default': _ProductionConfig,
}
