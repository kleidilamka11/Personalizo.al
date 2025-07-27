import uuid
from fastapi import status


def register_user(client, email=None, username=None, password="password", is_admin=False):
    email = email or f"{uuid.uuid4()}@example.com"
    username = username or f"user_{uuid.uuid4().hex[:8]}"
    response = client.post(
        "/auth/register",
        json={"email": email, "username": username, "password": password, "is_admin": is_admin},
    )
    assert response.status_code == status.HTTP_200_OK
    return response.json()


def login_user(client, email, password="password"):
    response = client.post("/auth/login", json={"email": email, "password": password})
    assert response.status_code == status.HTTP_200_OK
    return response.json()


def create_package(client, tier="basic"):
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
    user = register_user(client)
    tokens = login_user(client, user["email"])
    return {"Authorization": f"Bearer {tokens['access_token']}"}


def test_create_and_list_orders(client):
    package = create_package(client, "tier1")
    header = auth_header(client)
    payload = {
        "song_package_id": package["id"],
        "recipient_name": "Alice",
        "mood": "happy",
        "facts": "likes music",
    }
    res = client.post("/orders/", json=payload, headers=header)
    assert res.status_code == status.HTTP_200_OK
    order = res.json()
    assert order["recipient_name"] == "Alice"
    assert order["status"] == "pending"

    res = client.get("/orders/me", headers=header)
    assert res.status_code == status.HTTP_200_OK
    orders = res.json()
    assert len(orders) == 1
    assert orders[0]["id"] == order["id"]


def test_order_requires_auth(client):
    package = create_package(client, "tier2")
    payload = {
        "song_package_id": package["id"],
        "recipient_name": "Bob",
        "mood": "sad",
        "facts": None,
    }
    res = client.post("/orders/", json=payload)
    assert res.status_code == status.HTTP_401_UNAUTHORIZED


def test_create_order_invalid_package(client):
    header = auth_header(client)
    payload = {
        "song_package_id": 999,
        "recipient_name": "Charlie",
        "mood": "chill",
        "facts": "fact",
    }
    res = client.post("/orders/", json=payload, headers=header)
    assert res.status_code == status.HTTP_404_NOT_FOUND
