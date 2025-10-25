import pytest
from app.auth import get_password_hash, verify_password, create_access_token, verify_token
from app.schemas.customer import CustomerCreate

def test_get_password_hash():
    """Test password hashing."""
    password = "testpassword"
    hashed = get_password_hash(password)
    assert hashed != password
    assert verify_password(password, hashed)

def test_verify_password():
    """Test password verification."""
    password = "testpassword"
    hashed = get_password_hash(password)
    assert verify_password(password, hashed)
    assert not verify_password("wrongpassword", hashed)

def test_create_access_token():
    """Test JWT token creation."""
    data = {"sub": "test@example.com", "is_admin": False}
    token = create_access_token(data)
    assert isinstance(token, str)
    assert len(token) > 0

def test_verify_token():
    """Test JWT token verification."""
    data = {"sub": "test@example.com", "is_admin": False}
    token = create_access_token(data)
    payload = verify_token(token, lambda: None)
    assert payload.email == "test@example.com"
    assert payload.is_admin == False

def test_verify_token_invalid():
    """Test JWT token verification with invalid token."""
    from fastapi import HTTPException
    credentials_exception = HTTPException(status_code=401, detail="Invalid token")
    with pytest.raises(HTTPException):
        verify_token("invalid_token", credentials_exception)

def test_get_current_admin_nonexistent_user(client, db_session):
    """Test get_current_admin with token for non-existent user."""
    # Create a token for a non-existent admin
    from app.auth import create_access_token
    data = {"sub": "nonexistent@example.com", "is_admin": True}
    token = create_access_token(data)
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/admins/loans", headers=headers)
    assert response.status_code == 401
    assert "Could not validate credentials" in response.json()["detail"]

def test_get_current_customer_nonexistent_user(client, db_session):
    """Test get_current_customer with token for non-existent user."""
    # Create a token for a non-existent customer
    from app.auth import create_access_token
    data = {"sub": "nonexistent@example.com", "is_admin": False}
    token = create_access_token(data)
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/customers/me", headers=headers)
    assert response.status_code == 401
    assert "Could not validate credentials" in response.json()["detail"]

def test_customer_registration(client, db_session):
    """Test customer registration endpoint."""
    customer_data = {
        "name": "John Doe",
        "email": "john@example.com",
        "password": "password123",
        "age": 30,
        "phone": "1234567890",
        "address": "123 Main St"
    }
    response = client.post("/auth/register", json=customer_data)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "John Doe"
    assert data["email"] == "john@example.com"
    assert "id" in data

def test_customer_registration_duplicate_email(client, test_customer):
    """Test registration with duplicate email."""
    customer_data = {
        "name": "Jane Doe",
        "email": "test@example.com",  # Same as test_customer
        "password": "password123",
        "age": 25
    }
    response = client.post("/auth/register", json=customer_data)
    assert response.status_code == 400
    assert "Email already registered" in response.json()["detail"]

def test_customer_registration_age_validation(client):
    """Test age validation in registration."""
    customer_data = {
        "name": "Young User",
        "email": "young@example.com",
        "password": "password123",
        "age": 17  # Under 18
    }
    response = client.post("/auth/register", json=customer_data)
    assert response.status_code == 422  # Validation error

def test_customer_login(client, test_customer):
    """Test customer login."""
    response = client.post("/auth/token", data={
        "username": test_customer.email,
        "password": "password123"
    })
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_customer_login_wrong_password(client, test_customer):
    """Test login with wrong password."""
    response = client.post("/auth/token", data={
        "username": test_customer.email,
        "password": "wrongpassword"
    })
    assert response.status_code == 401
    assert "Incorrect username or password" in response.json()["detail"]

def test_admin_login(client, test_admin):
    """Test admin login."""
    response = client.post("/auth/token", data={
        "username": test_admin.email,
        "password": "admin123"
    })
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data

def test_get_customer_profile(client, auth_headers):
    """Test getting customer profile."""
    response = client.get("/customers/me", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "test@example.com"

def test_get_customer_profile_unauthorized(client):
    """Test accessing profile without authentication."""
    response = client.get("/customers/me")
    assert response.status_code == 401

def test_root_endpoint(client):
    """Test root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Welcome to HCL Banking Backend API"

def test_admin_access_customer_endpoint(client, admin_auth_headers):
    """Test admin trying to access customer endpoint."""
    response = client.get("/customers/me", headers=admin_auth_headers)
    assert response.status_code == 403
    assert "Not authorized for customer access" in response.json()["detail"]

def test_customer_access_admin_endpoint(client, auth_headers):
    """Test customer trying to access admin endpoint."""
    response = client.get("/admins/loans", headers=auth_headers)
    assert response.status_code == 403
    assert "Not authorized for admin access" in response.json()["detail"]

def test_invalid_token_customer_endpoint(client):
    """Test invalid token for customer endpoint."""
    headers = {"Authorization": "Bearer invalid_token"}
    response = client.get("/customers/me", headers=headers)
    assert response.status_code == 401
    assert "Could not validate credentials" in response.json()["detail"]

def test_invalid_token_admin_endpoint(client):
    """Test invalid token for admin endpoint."""
    headers = {"Authorization": "Bearer invalid_token"}
    response = client.get("/admins/loans", headers=headers)
    assert response.status_code == 401
    assert "Could not validate credentials" in response.json()["detail"]