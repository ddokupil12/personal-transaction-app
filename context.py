from os import environ

from flask import Flask

from app_config import config, is_dotenv_loaded

__all__ = ['app', 'DB_CONFIG']

assert is_dotenv_loaded # Should be loaded in app_config
_config_name = environ.get('CONFIG_NAME')

app = Flask(__name__)

app.config.from_object(config.get(_config_name, config['default']))
DB_CONFIG = app.config['DB_CONFIG']