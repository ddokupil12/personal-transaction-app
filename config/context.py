from flask import Flask

from .app_config import config

__all__ = ['app', 'DB_CONFIG']

_config_name = 'development'
app = Flask(__name__)

app.config.from_object(config.get(_config_name, config['default']))
DB_CONFIG = app.config['DB_CONFIG']