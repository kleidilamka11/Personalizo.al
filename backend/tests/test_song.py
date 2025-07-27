import uuid
from fastapi import status

# Helpers duplicated from other tests

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


def create_order(client):
    package = create_package(client, "tier-song")
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


def test_create_and_get_song(client):
    order = create_order(client)
    song_payload = {
        "order_id": order["id"],
        "title": "My Song",
        "genre": "pop",
        "duration_seconds": 120,
        "file_path": "song.mp3",
    }
    res = client.post("/songs/", json=song_payload)
    assert res.status_code == status.HTTP_200_OK
    created = res.json()
    assert created["title"] == "My Song"
    assert created["order_id"] == order["id"]

    res = client.get(f"/songs/{order['id']}")
    assert res.status_code == status.HTTP_200_OK
    fetched = res.json()
    assert fetched["id"] == created["id"]

    res = client.get("/songs/")
    assert res.status_code == status.HTTP_200_OK
    songs = res.json()
    assert len(songs) == 1
    assert songs[0]["id"] == created["id"]


def test_create_song_invalid_order(client):
    song_payload = {
        "order_id": 999,
        "title": "Bad Song",
        "genre": "rock",
        "duration_seconds": 90,
        "file_path": "bad.mp3",
    }
    res = client.post("/songs/", json=song_payload)
    assert res.status_code == status.HTTP_404_NOT_FOUND


def test_duplicate_song_for_order(client):
    order = create_order(client)
    song_payload = {
        "order_id": order["id"],
        "title": "First",
        "genre": "pop",
        "duration_seconds": 60,
        "file_path": "first.mp3",
    }
    res1 = client.post("/songs/", json=song_payload)
    assert res1.status_code == status.HTTP_200_OK

    res2 = client.post("/songs/", json=song_payload)
    assert res2.status_code == status.HTTP_400_BAD_REQUEST
