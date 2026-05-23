__all__ = ['app', 'DB_CONFIG', 'create_app']

from os import environ

from flask import Flask, request, abort
from logging import basicConfig, INFO

from utils.config import config, is_dotenv_loaded

# dotenv should be loaded in config
assert is_dotenv_loaded, 'Load dotenv before running app'

_config_name = environ.get('CONFIG_NAME')
app = Flask(__name__)
app.config.from_object(config.get(_config_name, config['default']))
DB_CONFIG = app.config['DB_CONFIG']

basicConfig(
    filename='error.log',
    level=INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

@app.before_request
def check_allowed_hosts():
    if request.host not in app.config['ALLOWED_HOSTS']:
        abort(403)

def create_app():
    from account import acct_bp
    from budget import budget_bp
    from cashflow import cashflow_bp
    from category import category_bp
    from transact import transact_bp

    app.register_blueprint(acct_bp)
    app.register_blueprint(budget_bp)
    app.register_blueprint(cashflow_bp)
    app.register_blueprint(category_bp)
    app.register_blueprint(transact_bp)