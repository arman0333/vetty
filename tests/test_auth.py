"""Tests for authentication."""

import pytest
from fastapi import status
from app.auth import (
    verify_password,
    get_password_hash,
    create_access_token,
    verify_token,
)
from jose import jwt
from app.config import settings


def test_password_hashing():
    """Test password hashing and verification."""
    password = "testpassword"
    hashed = get_password_hash(password)
    assert hashed != password
    assert verify_password(password, hashed)
    assert not verify_password("wrongpassword", hashed)


def test_create_access_token():
    """Test JWT token creation."""
    data = {"sub": "testuser"}
    token = create_access_token(data)
    assert token is not None
    assert isinstance(token, str)

    # Decode and verify token
    decoded = jwt.decode(
        token, settings.secret_key, algorithms=[settings.algorithm]
    )
    assert decoded["sub"] == "testuser"
    assert "exp" in decoded


def test_login_success(client):
    """Test successful login."""
    response = client.post(
        "/auth/login",
        json={"username": "testuser", "password": "testpass"},
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_invalid_username(client):
    """Test login with invalid username."""
    response = client.post(
        "/auth/login",
        json={"username": "invaliduser", "password": "testpass"},
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_login_invalid_password(client):
    """Test login with invalid password."""
    response = client.post(
        "/auth/login",
        json={"username": "testuser", "password": "wrongpass"},
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_protected_endpoint_without_token(client):
    """Test accessing protected endpoint without token."""
    response = client.get("/coins")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_protected_endpoint_with_invalid_token(client):
    """Test accessing protected endpoint with invalid token."""
    client.headers.update({"Authorization": "Bearer invalid_token"})
    response = client.get("/coins")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_protected_endpoint_with_valid_token(authenticated_client, mock_coingecko_response):
    """Test accessing protected endpoint with valid token."""
    from unittest.mock import AsyncMock, patch
    mock_get = AsyncMock(return_value=mock_coingecko_response["coins_list"])
    with patch("app.services.coingecko.coingecko_service.get_all_coins", side_effect=mock_get):
        response = authenticated_client.get("/coins?page_num=1&per_page=10")
        assert response.status_code == status.HTTP_200_OK

