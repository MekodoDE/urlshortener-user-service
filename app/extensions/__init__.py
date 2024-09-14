from . import smorest, database, jwt

def init_app(app, register_blueprints=None):
    """
    Initialize extensions for the Flask application.

    Parameters:
    - app: Flask application instance
    - register_blueprints: Function to register blueprints (optional)
    """

    # Initialize Flask-Smorest extension
    smorest.init_app(app, register_blueprints)

    # Initialize database extension
    database.init_app(app)

    # Initialize jwt extension
    jwt.init_app(app)
