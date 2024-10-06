import pytest
import os
from flask_jwt_extended import create_access_token
from app import create_app
from app.models.user import UserModel
from app.views.utils import hash_password
from app.extensions.database import db

db_path = "./instance/test.db"

class UserData:
    id = None
    username = "testuser"
    password = "testpassword"
    email = "testuser@example.com"
    role = "member"
    access_token = None

class AdminUserData:
    id = "18159319-08e4-478b-9ff6-eecf4bb44ed8"
    username = "testadmin"
    password = "testpassword"
    email = "testadmin@example.com"
    role = "admin"
    access_token = None

@pytest.fixture(scope="session")
def app():
    _app = create_app()

    with _app.app_context():
        user = UserModel(id=AdminUserData.id, username=AdminUserData.username, email=AdminUserData.email, password=hash_password(AdminUserData.password), role=AdminUserData.role)
        db.session.add(user)
        yield _app
        db.session.remove()
        db.engine.dispose()
        if os.path.exists(db_path):
            os.remove(db_path)

@pytest.fixture(scope="session")
def client(app):
    return app.test_client()

@pytest.fixture(scope="session")
def headers():
    return {
        'Authorization': f'Bearer {UserData.access_token}'
    }

@pytest.fixture(scope="session")
def admin_headers():
    return {
        "Authorization": f"Bearer {AdminUserData.access_token}"
    }