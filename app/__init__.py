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

    # Enable Cross-Origin Resource Sharing (CORS) with origins specified in configuration
    CORS(app, origins=app.config['CORS_ORIGINS'])

    # Initialize extensions and register blueprints
    extensions.init_app(app, register_blueprints=views.register_blueprints)

    return app
