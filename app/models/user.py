import uuid
import sqlalchemy_utils

from app.extensions.database import db

class UserModel(db.Model):
    """
    Model class for representing shortened URL entries in the database
    """

    __tablename__ = "users"

    # Define columns for the Url table
    id = db.Column(sqlalchemy_utils.types.uuid.UUIDType(binary=False), primary_key=True, default=uuid.uuid4)
    username = db.Column(db.String(255), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(50), default="member")
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
