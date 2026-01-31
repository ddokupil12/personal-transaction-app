from flask import Flask

from config import config

config_name = 'development'
app = Flask(__name__)

app.config.from_object(config.get(config_name, config['default']))
DB_CONFIG = app.config['DB_CONFIG']