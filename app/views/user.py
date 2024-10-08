import uuid
from flask import jsonify
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from flask_jwt_extended import create_access_token, get_jwt, jwt_required
from flask_jwt_extended.exceptions import JWTExtendedException

from .utils import hash_password
from app.extensions.database import db
from app.models import UserModel
from app.models.schemas import UserSchema, BasicUserSchema, UserQueryArgsSchema

# Create a Blueprint for User management
blp = Blueprint('User', 'user', description='User management', url_prefix="/users/")


@blp.route('/')
class Users(MethodView):
    """
    Endpoint for managing multiple users.
    """

    @jwt_required()
    @blp.arguments(UserQueryArgsSchema, location='query')
    @blp.response(200, UserSchema(many=True))
    def get(self, args):
        """
        Get a list of Users based on query parameters.
        """
        try:
            jwt_claims = get_jwt()
            user_id = uuid.UUID(jwt_claims.get("sub"))
            role = jwt_claims.get("role", "viewer")  # Default to 'viewer' if no role is present
        except JWTExtendedException as e:
            abort(401, message="Invalid or expired token")  # Handle token issues specifically

        UserModel.query.get_or_404(user_id, description="User not found")

        if role != "admin":
            abort(403, message="You are not authorized to perform this action")

        # Ensure to execute query with .all()
        return UserModel.query.filter_by(**args).all()

    @blp.arguments(UserSchema)
    @blp.response(201, BasicUserSchema)
    def post(self, new_data):
        """
        Create a new User.
        """
        # Hash password before storing
        new_data['password'] = hash_password(new_data['password'])
        user = UserModel(**new_data)

        try:
            db.session.add(user)
            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()
            abort(400, message="Integrity error: " + str(e.orig))
        except SQLAlchemyError as e:
            db.session.rollback()
            abort(400, message="Database error: " + str(e))
        
        return user
    
@blp.route('/<uuid:id>')
class UserById(MethodView):
    """
    Endpoint for managing a single user by its id.
    """

    @jwt_required()
    @blp.response(200, BasicUserSchema)
    def get(self, id):
        """
        Get details of a User by its id.
        """
        try:
            jwt_claims = get_jwt()
            user_id = uuid.UUID(jwt_claims.get("sub"))
            role = jwt_claims.get("role", "viewer")  # Default to 'viewer' if no role is present
        except JWTExtendedException as e:
            abort(401, message="Invalid or expired token")  # Handle token issues specifically

        if user_id != id and role != "admin":
            abort(403, message="You are not authorized to perform this action")

        user = UserModel.query.get_or_404(id, description="User not found")

        return user
    
    @jwt_required()
    @blp.arguments(UserSchema(partial=True))  # Allow partial updates
    @blp.response(200, BasicUserSchema)
    def put(self, data, id):
        """
        Update details of a user by its id.
        """
        try:
            jwt_claims = get_jwt()
            user_id = uuid.UUID(jwt_claims.get("sub"))
            role = jwt_claims.get("role", "viewer")  # Default to 'viewer' if no role is present
        except JWTExtendedException as e:
            abort(401, message="Invalid or expired token")  # Handle token issues specifically

        if user_id != id and role != "admin":
            abort(403, message="You are not authorized to perform this action")

        user = UserModel.query.get_or_404(id, description="User not found")

        # If the password is being changed, hash it
        if 'password' in data:
            data['password'] = hash_password(data['password'])

        for key, value in data.items():
            setattr(user, key, value)

        try:
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            abort(500, message="Database error: " + str(e))

        return user
    
    @jwt_required()
    @blp.response(204)
    def delete(self, id):
        """
        Delete a user by its id.
        """
        try:
            jwt_claims = get_jwt()
            user_id = uuid.UUID(jwt_claims.get("sub"))
            role = jwt_claims.get("role", "viewer")  # Default to 'viewer' if no role is present
        except JWTExtendedException as e:
            abort(401, message="Invalid or expired token")  # Handle token issues specifically

        if user_id != id and role != "admin":
            abort(403, message="You are not authorized to perform this action")
        
        user = UserModel.query.get_or_404(id, description="User not found")

        try:
            db.session.delete(user)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            abort(500, message="Database error: " + str(e))

        # Explicitly return empty dictionary and status code
        return {}

@blp.route('/login')
class Login(MethodView):
    """
    Endpoint for login.
    """

    @blp.arguments(UserSchema(only=('username', 'password')))
    @blp.response(200)
    def post(self, args):
        username = args['username']
        password = args['password']

        user = UserModel.query.filter_by(username=username).first()

        if user and hash_password(password) == user.password:
            # Generate access token (JWT) using user's ID and role
            additional_claims = {'role': user.role}
            access_token = create_access_token(identity=user.id, additional_claims=additional_claims)
            return jsonify(access_token=access_token)
        else:
            abort(401, message='Invalid username or password')