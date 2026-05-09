import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_feed_requires_auth(client: AsyncClient) -> None:
    response = await client.get("/feed")
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_register_and_login(client: AsyncClient) -> None:
    register_response = await client.post(
        "/auth/register",
        json={"email": "user@example.com", "password": "securepass123"},
    )
    assert register_response.status_code == 201

    login_response = await client.post(
        "/auth/jwt/login",
        data={"username": "user@example.com", "password": "securepass123"},
    )
    assert login_response.status_code == 200
    assert "access_token" in login_response.json()


@pytest.mark.asyncio
async def test_users_me_requires_auth(client: AsyncClient) -> None:
    response = await client.get("/users/me")
    assert response.status_code == 401
