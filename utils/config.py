__all__ = ['config', 'is_dotenv_loaded']

from os import environ

from dotenv import load_dotenv

is_dotenv_loaded = load_dotenv()

class _Config: # Default app configuration
    SECRET_KEY = environ['SECRET_KEY']
    DEBUG = True
    PORT = environ.get('PORT') # The server's port
    DB_CONFIG = {
        'host': environ.get('DB_HOST'),
        'database': environ.get('DB_NAME'),
        'user': environ.get('DB_USER'),
        'password': environ.get('DB_PASSWORD'),
        'port': int(environ.get('DB_PORT', 3306)) # The database's port
    }
    ALLOWED_HOSTS = environ.get('ALLOWED_HOSTS').split(',')

class _ProductionConfig(_Config): # Production app configuration
    DEBUG = False

# _Configuration dictionary to allow selection of a configuration
config = {
    'development': _Config,
    'production': _ProductionConfig,
    'default': _ProductionConfig,
}
