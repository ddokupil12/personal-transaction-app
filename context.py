__all__ = ['app', 'DB_CONFIG', 'create_app']

from os import environ

from flask import Flask

from app_config import config, is_dotenv_loaded

# dotenv should be loaded in app_config
assert is_dotenv_loaded, 'Load dotenv before running app'

_config_name = environ.get('CONFIG_NAME')
app = Flask(__name__, template_folder='./templates')
app.config.from_object(config.get(_config_name, config['default']))
DB_CONFIG = app.config['DB_CONFIG']

def create_app():
    from routes.account_routes import acct_bp
    from routes.budget_routes import budget_bp
    from routes.cashflow_routes import cashflow_bp
    from routes.category_routes import category_bp
    from routes.transact_routes import transact_bp

    app.register_blueprint(acct_bp)
    app.register_blueprint(budget_bp)
    app.register_blueprint(cashflow_bp)
    app.register_blueprint(category_bp)
    app.register_blueprint(transact_bp)