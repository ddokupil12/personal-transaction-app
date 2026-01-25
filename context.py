import traceback

from flask import Flask, flash

from config import config

config_name = 'development'
app = Flask(__name__)

app.config.from_object(config.get(config_name, config['default']))
app.secret_key = app.config['SECRET_KEY']
DB_CONFIG = app.config['DB_CONFIG']

def logError(message, e):
    flash(message, 'error')
    print('err:', e)
    traceback.print_exc()