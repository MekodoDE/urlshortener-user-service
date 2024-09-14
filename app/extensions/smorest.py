from flask_smorest import Api

api = Api()

def init_app(app, register_blueprints=None):
    """
    Initialize Flask-Smorest extension for the Flask application.

    Parameters:
    - app: Flask application instance
    - register_blueprints: Function to register blueprints (optional)
    """

    # Initialize Flask-Smorest extension
    api.init_app(app)

    # Register blueprints with the API
    if register_blueprints:
        register_blueprints(api)
