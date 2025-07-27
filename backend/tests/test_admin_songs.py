import os
import io
from fastapi import status

from .utils import register_user, login_user, create_order


def admin_header(client):
    admin = register_user(client, is_admin=True)
    tokens = login_user(client, admin["email"])
    return {"Authorization": f"Bearer {tokens['access_token']}"}


def ensure_media_dir():
    os.makedirs(os.path.join("media", "songs"), exist_ok=True)


def test_upload_song_success(client):
    ensure_media_dir()
    header = admin_header(client)
    order = create_order(client)

    data = {
        "order_id": order["id"],
        "title": "Admin Song",
        "genre": "rock",
        "duration_seconds": 42,
    }
    file_bytes = b"hello" * 1000
    files = {"file": ("song.mp3", io.BytesIO(file_bytes), "audio/mp3")}

    res = client.post("/admin/songs/", data=data, files=files, headers=header)
    assert res.status_code == status.HTTP_200_OK
    payload = res.json()
    assert payload["order_id"] == order["id"]
    assert payload["file_url"].startswith("/media/songs/")

    song_res = client.get(f"/songs/{order['id']}")
    assert song_res.status_code == status.HTTP_200_OK
    assert song_res.json()["title"] == "Admin Song"

    orders = client.get("/admin/orders/", headers=header)
    assert orders.status_code == status.HTTP_200_OK
    assert orders.json()[0]["status"] == "delivered"


def test_upload_song_invalid_file_type(client):
    ensure_media_dir()
    header = admin_header(client)
    order = create_order(client)

    data = {
        "order_id": order["id"],
        "title": "Bad File",
        "genre": "pop",
        "duration_seconds": 10,
    }
    files = {"file": ("bad.txt", io.BytesIO(b"text"), "text/plain")}

    res = client.post("/admin/songs/", data=data, files=files, headers=header)
    assert res.status_code == status.HTTP_400_BAD_REQUEST


def test_upload_song_too_large(client):
    ensure_media_dir()
    header = admin_header(client)
    order = create_order(client)

    data = {
        "order_id": order["id"],
        "title": "Big File",
        "genre": "pop",
        "duration_seconds": 10,
    }
    big_content = b"0" * (11 * 1024 * 1024)
    files = {"file": ("big.mp3", io.BytesIO(big_content), "audio/mp3")}

    res = client.post("/admin/songs/", data=data, files=files, headers=header)
    assert res.status_code == status.HTTP_400_BAD_REQUEST


def test_upload_song_requires_admin(client):
    ensure_media_dir()
    user = register_user(client)
    tokens = login_user(client, user["email"])
    header = {"Authorization": f"Bearer {tokens['access_token']}"}
    order = create_order(client)

    data = {
        "order_id": order["id"],
        "title": "No Admin",
        "genre": "rock",
        "duration_seconds": 5,
    }
    files = {"file": ("song.mp3", io.BytesIO(b"123"), "audio/mp3")}

    res = client.post("/admin/songs/", data=data, files=files, headers=header)
    assert res.status_code == status.HTTP_403_FORBIDDEN
