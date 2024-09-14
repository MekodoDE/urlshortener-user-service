import pytest
from .conftest import UserData

def test_create_user(client):
    """
    Test user creation.
    Verifies user is created and 'id' is returned.
    """
    response = client.post('/', json={
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
    response = client.post('/login', json=login_data)
    assert response.status_code == 200
    data = response.get_json()
    assert 'access_token' in data
    UserData.access_token = data['access_token']  # Save token for authenticated requests

def test_all_user_list(client, headers):
    """
    Test access to user list.
    Verifies that access is forbidden without proper credentials.
    """
    response = client.get('/', headers=headers)
    assert response.status_code == 403

def test_get_user(client, headers):
    """
    Test retrieving user details.
    Verifies that correct user details are returned.
    """
    response = client.get(f'/{UserData.id}', headers=headers)
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
    response = client.put(f'/{UserData.id}', json=update_data, headers=headers)
    assert response.status_code == 200
    data = response.get_json()
    assert data['email'] == update_data['email']

def test_delete_user(client, headers):
    """
    Test user deletion.
    Verifies that the user is deleted and cannot be retrieved.
    """
    response = client.delete(f'/{UserData.id}', headers=headers)
    assert response.status_code == 204

    response = client.get(f'/{UserData.id}', headers=headers)
    assert response.status_code == 404