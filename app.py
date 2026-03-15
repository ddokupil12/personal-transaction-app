__all__ = ['app', 'DB_CONFIG', 'create_app']

from os import environ

from flask import Flask
from logging import basicConfig, INFO

from config import config, is_dotenv_loaded

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

def create_app():
    from routes import acct_bp, budget_bp, cashflow_bp, category_bp, transact_bp

    app.register_blueprint(acct_bp)
    app.register_blueprint(budget_bp)
    app.register_blueprint(cashflow_bp)
    app.register_blueprint(category_bp)
    app.register_blueprint(transact_bp)