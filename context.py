# context.py
from config import config
from flask import Flask

config_name = 'development'
app = Flask(__name__)

app.config.from_object(config.get(config_name, config['default']))
app.secret_key = app.config['SECRET_KEY']
DB_CONFIG = app.config['DB_CONFIG']