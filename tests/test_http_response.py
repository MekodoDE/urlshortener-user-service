import pytest
from .conftest import UserData, AdminUserData

url_prefix = '/users'

def test_create_user(client):
    """
    Test user creation.
    Verifies user is created and 'id' is returned.
    """
    response = client.post(url_prefix+  '/', json={
        'username': UserData.username,
        'password': UserData.password,
        'email': UserData.email,
    })
    assert response.status_code == 201
    data = response.get_json()
    assert data['username'] == UserData.username
    assert 'id' in data
    UserData.id = data['id']  # Save ID for other tests

def test_login(client):
    """
    Test user login.
    Checks that login returns a JWT access token.
    """
    login_data = {
        'username': UserData.username,
        'password': UserData.password
    }
    response = client.post(url_prefix + '/login', json=login_data)
    assert response.status_code == 200
    data = response.get_json()
    assert 'access_token' in data
    UserData.access_token = data['access_token']  # Save token for authenticated requests

def test_admin_login(client):
    """
    Test admin login.
    Checks that login returns a JWT access token.
    """
    login_data = {
        'username': AdminUserData.username,
        'password': AdminUserData.password
    }
    response = client.post(url_prefix + '/login', json=login_data)
    assert response.status_code == 200
    data = response.get_json()
    assert 'access_token' in data
    AdminUserData.access_token = data['access_token']  # Save token for authenticated requests

def test_get_users(client, headers):
    """
    Test access to user list.
    Verifies that access is forbidden without proper credentials.
    """
    response = client.get(url_prefix + '/', headers=headers)
    assert response.status_code == 403

def test_admin_get_users(client, admin_headers):
    """
    Test access to user list.
    Verifies that access is allowed with admin credentials.
    """
    response = client.get(url_prefix + '/', headers=admin_headers)
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 2

def test_get_user(client, headers):
    """
    Test retrieving user details.
    Verifies that correct user details are returned.
    """
    response = client.get(url_prefix + f'/{UserData.id}', headers=headers)
    assert response.status_code == 200
    data = response.get_json()
    assert data['username'] == UserData.username

def test_get_other_user(client, headers):
    """
    Test retrieving other users details.
    Verifies that access is not allowed.
    """
    response = client.get(url_prefix + f'/{AdminUserData.id}', headers=headers)
    assert response.status_code == 403

def test_admin_get_user(client, admin_headers):
    """
    Test retrieving user details.
    Verifies that correct user details are returned.
    """
    response = client.get(url_prefix + f'/{UserData.id}', headers=admin_headers)
    assert response.status_code == 200
    data = response.get_json()
    assert data['username'] == UserData.username

def test_update_user(client, headers):
    """
    Test updating user information.
    Verifies that the user's email is updated.
    """
    update_data = {
        'email': 'newemail@example.com'
    }
    response = client.put(url_prefix + f'/{UserData.id}', json=update_data, headers=headers)
    assert response.status_code == 200
    data = response.get_json()
    assert data['email'] == update_data['email']

def test_admin_update_user(client, admin_headers):
    """
    Test updating user information.
    Verifies that the user's email is updated.
    """
    update_data = {
        'email': 'newemail2@example.com'
    }
    response = client.put(url_prefix + f'/{UserData.id}', json=update_data, headers=admin_headers)
    assert response.status_code == 200
    data = response.get_json()
    assert data['email'] == update_data['email']

def test_delete_user(client, headers):
    """
    Test user deletion.
    Verifies that the user is deleted and cannot be retrieved.
    """
    response = client.delete(url_prefix + f'/{UserData.id}', headers=headers)
    assert response.status_code == 204

    response = client.get(url_prefix + f'/{UserData.id}', headers=headers)
    assert response.status_code == 404