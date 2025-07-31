import os
import io
from fastapi import status

from app.core.config import settings

from .utils import register_user, login_user, create_order, create_package


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
    admin_order = orders.json()[0]
    assert admin_order["status"] == "delivered"
    assert admin_order["delivered_url"].startswith("/media/songs/")


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


def test_upload_song_sends_email(client, monkeypatch):
    ensure_media_dir()
    admin_header_token = admin_header(client)

    # create a user and order manually so we know the email
    package = create_package(client, "emailtier")
    user = register_user(client)
    tokens = login_user(client, user["email"])
    user_header = {"Authorization": f"Bearer {tokens['access_token']}"}
    payload = {
        "song_package_id": package["id"],
        "recipient_name": "Rec",
        "mood": "happy",
        "facts": "",
    }
    res = client.post("/orders/", json=payload, headers=user_header)
    assert res.status_code == status.HTTP_200_OK
    order = res.json()

    captured = {}

    def fake_send(to: str, subject: str, body: str) -> None:
        captured["to"] = to
        captured["subject"] = subject
        captured["body"] = body

    monkeypatch.setattr("app.routes.admin_songs.send_email", fake_send)

    data = {
        "order_id": order["id"],
        "title": "Notify Song",
        "genre": "pop",
        "duration_seconds": 5,
    }
    files = {"file": ("song.mp3", io.BytesIO(b"abc"), "audio/mp3")}
    res = client.post("/admin/songs/", data=data, files=files, headers=admin_header_token)
    assert res.status_code == status.HTTP_200_OK

    assert captured["to"] == user["email"]

    orders = client.get("/admin/orders/", headers=admin_header_token)
    admin_order = [o for o in orders.json() if o["id"] == order["id"]][0]
    expected_url = f"{settings.BASE_URL}/download{admin_order['delivered_url']}"
    assert expected_url in captured["body"]
