import os
from flask import Flask
from flask_cors import CORS
from datetime import timedelta

from . import extensions, views, models


def create_app():
    """
    Create and configure the Flask application instance.
    """

    # Initialize Flask application
    app = Flask(__name__)

    # Load configuration from environment variable or use default
    CONFIG_TYPE = os.getenv('CONFIG_TYPE', default='config.DevelopmentConfig')
    app.config.from_object(CONFIG_TYPE)
    app.config.from_mapping(os.environ)
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes=int(app.config['JWT_ACCESS_TOKEN_EXPIRES_MINUTES']))
    app.config['CORS_ORIGINS'] = [origin.strip() for origin in app.config['CORS_ORIGINS'].split(',')]
    if all(key in app.config for key in ["DB_USER", "DB_PASSWORD", "DB_HOST", "DB_PORT", "DB_NAME"]):
        app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql://{app.config["DB_USER"]}:{app.config["DB_PASSWORD"]}@{app.config["DB_HOST"]}:{app.config["DB_PORT"]}/{app.config["DB_NAME"]}'

    # Enable Cross-Origin Resource Sharing (CORS) with origins specified in configuration
    CORS(app, origins=app.config['CORS_ORIGINS'])

    # Initialize extensions and register blueprints
    extensions.init_app(app, register_blueprints=views.register_blueprints)

    return app
