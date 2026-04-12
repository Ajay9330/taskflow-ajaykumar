import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_register_and_login(client: AsyncClient):
    # Register
    register_data = {
        "name": "Integration Test User",
        "email": "test_integration@example.com",
        "password": "password123"
    }
    response = await client.post("/auth/register", json=register_data)
    assert response.status_code == 201
    data = response.json()
    assert "token" in data
    assert data["user"]["email"] == register_data["email"]

    # Login
    login_data = {
        "email": "test_integration@example.com",
        "password": "password123"
    }
    response = await client.post("/auth/login", json=login_data)
    assert response.status_code == 200
    data = response.json()
    assert "token" in data

@pytest.mark.asyncio
async def test_login_invalid_credentials(client: AsyncClient):
    login_data = {
        "email": "nonexistent@example.com",
        "password": "wrongpassword"
    }
    response = await client.post("/auth/login", json=login_data)
    assert response.status_code == 401
    assert response.json()["error"] == "unauthorized"
