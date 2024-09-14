from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
ma = Marshmallow()

def init_app(app):
    """
    Initialize SQLAlchemy and Marshmallow extensions for the Flask application.

    Parameters:
    - app: Flask application instance
    """

    # Initialize SQLAlchemy extension
    db.init_app(app)

    # Create database tables within the application context
    with app.app_context():
        db.create_all()
