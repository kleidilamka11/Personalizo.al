import uuid
from fastapi import status


def register_user(client, email=None, username=None, password="password", is_admin=False):
    """Register a user and return the response JSON."""
    email = email or f"{uuid.uuid4()}@example.com"
    username = username or f"user_{uuid.uuid4().hex[:8]}"
    response = client.post(
        "/auth/register",
        json={"email": email, "username": username, "password": password, "is_admin": is_admin},
    )
    assert response.status_code == status.HTTP_200_OK
    return response.json()


def login_user(client, email, password="password"):
    """Login a user and return the token response JSON."""
    response = client.post("/auth/login", json={"email": email, "password": password})
    assert response.status_code == status.HTTP_200_OK
    return response.json()


def create_package(client, tier="basic"):
    """Create a song package and return the response JSON."""
    payload = {
        "tier": tier,
        "name": f"{tier}_package",
        "description": "desc",
        "price_eur": 10,
        "duration_seconds": 30,
        "commercial_use": False,
    }
    res = client.post("/packages/", json=payload)
    assert res.status_code == status.HTTP_200_OK
    return res.json()


def auth_header(client):
    """Return an Authorization header for a newly registered user."""
    user = register_user(client)
    tokens = login_user(client, user["email"])
    return {"Authorization": f"Bearer {tokens['access_token']}"}


def create_order(client):
    """Create an order using a newly registered user and package."""
    package = create_package(client, "tier-order")
    header = auth_header(client)
    payload = {
        "song_package_id": package["id"],
        "recipient_name": "SongUser",
        "mood": "happy",
        "facts": "likes singing",
    }
    res = client.post("/orders/", json=payload, headers=header)
    assert res.status_code == status.HTTP_200_OK
    return res.json()

