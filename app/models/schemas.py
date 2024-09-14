import marshmallow as mar
from marshmallow_sqlalchemy import field_for

from app.extensions.database import ma
from app.models import UserModel

class UserSchema(ma.SQLAlchemySchema):
    """
    Schema for serializing and deserializing Url model objects.
    """
    class Meta:
        model = UserModel
        ordered = True
        unknown = mar.EXCLUDE

    id = field_for(UserModel, "id", dump_only=True)
    username = field_for(UserModel, "username", required=True)
    email = field_for(UserModel, "email", required=True)
    password = field_for(UserModel, "password", load_only=True)  # Load only for security
    role = field_for(UserModel, "role", dump_default=False)
    is_active = field_for(UserModel, "is_active", dump_default=True)
    created_at = field_for(UserModel, "created_at", dump_only=True)
    updated_at = field_for(UserModel, "updated_at", dump_only=True)

class BasicUserSchema(UserSchema):
    class Meta(UserSchema.Meta):
        exclude = ("password", "role")

class AdminUserSchema(UserSchema):
    class Meta(UserSchema.Meta):
        exclude = ("password",)


class UserQueryArgsSchema(ma.Schema):
    username = mar.fields.Str()
    email = mar.fields.Str()
    team_id = mar.fields.UUID()