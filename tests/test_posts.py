import pytest
from httpx import AsyncClient


async def _auth_headers(client: AsyncClient, email: str, password: str) -> dict[str, str]:
    await client.post("/auth/register", json={"email": email, "password": password})
    login_response = await client.post(
        "/auth/jwt/login",
        data={"username": email, "password": password},
    )
    token = login_response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


@pytest.mark.asyncio
async def test_feed_empty(client: AsyncClient) -> None:
    headers = await _auth_headers(client, "feed@example.com", "securepass123")
    response = await client.get("/feed", headers=headers)
    assert response.status_code == 200
    body = response.json()
    assert body["posts"] == []
    assert body["total"] == 0
    assert body["limit"] == 20
    assert body["offset"] == 0


@pytest.mark.asyncio
async def test_feed_pagination_params(client: AsyncClient) -> None:
    headers = await _auth_headers(client, "paginate@example.com", "securepass123")
    response = await client.get("/feed?limit=5&offset=0", headers=headers)
    assert response.status_code == 200
    body = response.json()
    assert body["limit"] == 5
    assert body["offset"] == 0


@pytest.mark.asyncio
async def test_delete_invalid_post_id(client: AsyncClient) -> None:
    headers = await _auth_headers(client, "delete@example.com", "securepass123")
    response = await client.delete("/posts/not-a-uuid", headers=headers)
    assert response.status_code == 422
