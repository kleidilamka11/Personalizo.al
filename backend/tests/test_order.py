from fastapi import status

import os
import io
from .utils import register_user, login_user, create_package, auth_header, create_order


def admin_header(client):
    admin = register_user(client, is_admin=True)
    tokens = login_user(client, admin["email"])
    return {"Authorization": f"Bearer {tokens['access_token']}"}


def ensure_media_dir():
    os.makedirs(os.path.join("media", "songs"), exist_ok=True)


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


def test_update_order(client):
    user = register_user(client)
    tokens = login_user(client, user["email"])
    header = {"Authorization": f"Bearer {tokens['access_token']}"}

    package = create_package(client, "tier-order")
    payload = {
        "song_package_id": package["id"],
        "recipient_name": "SongUser",
        "mood": "happy",
        "facts": "likes singing",
    }
    res = client.post("/orders/", json=payload, headers=header)
    assert res.status_code == status.HTTP_200_OK
    order = res.json()

    update_payload = {"mood": "excited", "facts": "new facts"}
    res = client.patch(f"/orders/{order['id']}", json=update_payload, headers=header)
    assert res.status_code == status.HTTP_200_OK
    updated = res.json()
    assert updated["mood"] == "excited"
    assert updated["facts"] == "new facts"


def test_update_order_not_owner(client):
    order = create_order(client)
    user = register_user(client)
    tokens = login_user(client, user["email"])
    other_header = {"Authorization": f"Bearer {tokens['access_token']}"}
    res = client.patch(f"/orders/{order['id']}", json={"mood": "angry"}, headers=other_header)
    assert res.status_code == status.HTTP_403_FORBIDDEN


def test_cancel_order(client):
    user = register_user(client)
    tokens = login_user(client, user["email"])
    header = {"Authorization": f"Bearer {tokens['access_token']}"}

    package = create_package(client, "tier-order")
    payload = {
        "song_package_id": package["id"],
        "recipient_name": "SongUser",
        "mood": "happy",
        "facts": "likes singing",
    }
    res = client.post("/orders/", json=payload, headers=header)
    assert res.status_code == status.HTTP_200_OK
    order = res.json()

    res = client.post(f"/orders/{order['id']}/cancel", headers=header)
    assert res.status_code == status.HTTP_200_OK
    assert res.json()["status"] == "cancelled"


def test_cancel_order_delivered(client):
    ensure_media_dir()

    user = register_user(client)
    tokens = login_user(client, user["email"])
    user_header = {"Authorization": f"Bearer {tokens['access_token']}"}

    package = create_package(client, "tier-order")
    payload = {
        "song_package_id": package["id"],
        "recipient_name": "SongUser",
        "mood": "happy",
        "facts": "likes singing",
    }
    res = client.post("/orders/", json=payload, headers=user_header)
    assert res.status_code == status.HTTP_200_OK
    order = res.json()

    header_admin = admin_header(client)
    data = {
        "order_id": order["id"],
        "title": "delivered",
        "genre": "pop",
        "duration_seconds": 1,
    }
    files = {"file": ("song.mp3", io.BytesIO(b"abc"), "audio/mp3")}
    client.post("/admin/songs/", data=data, files=files, headers=header_admin)

    res = client.post(f"/orders/{order['id']}/cancel", headers=user_header)
    assert res.status_code == status.HTTP_400_BAD_REQUEST
