from fastapi import status

from .utils import register_user, login_user, create_package, auth_header


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
