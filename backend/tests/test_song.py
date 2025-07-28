from fastapi import status



from .utils import register_user,login_user,create_package,auth_header,create_order





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


def test_get_song_not_found(client):
    res = client.get("/songs/9999")
    assert res.status_code == status.HTTP_404_NOT_FOUND


def test_get_my_songs(client):
    user = register_user(client)
    tokens = login_user(client, user["email"])
    header = {"Authorization": f"Bearer {tokens['access_token']}"}

    package = create_package(client, "mytier")
    order_payload = {
        "song_package_id": package["id"],
        "recipient_name": "Me",
        "mood": "joy",
        "facts": None,
    }
    order_res = client.post("/orders/", json=order_payload, headers=header)
    assert order_res.status_code == status.HTTP_200_OK
    order = order_res.json()

    song_payload = {
        "order_id": order["id"],
        "title": "Mine",
        "genre": "rock",
        "duration_seconds": 30,
        "file_path": "mine.mp3",
    }
    client.post("/songs/", json=song_payload)

    res = client.get("/songs/me", headers=header)
    assert res.status_code == status.HTTP_200_OK
    songs = res.json()
    assert len(songs) == 1
    assert songs[0]["title"] == "Mine"


def test_get_my_songs_requires_auth(client):
    res = client.get("/songs/me")
    assert res.status_code == status.HTTP_401_UNAUTHORIZED


def test_update_and_delete_song(client):
    order = create_order(client)
    song_payload = {
        "order_id": order["id"],
        "title": "Original",
        "genre": "pop",
        "duration_seconds": 45,
        "file_path": "orig.mp3",
    }
    res = client.post("/songs/", json=song_payload)
    assert res.status_code == status.HTTP_200_OK
    song = res.json()

    update_payload = {
        "title": "Updated",
        "genre": "rock",
        "duration_seconds": 60,
        "file_path": "upd.mp3",
    }
    res = client.put(f"/songs/{song['id']}", json=update_payload)
    assert res.status_code == status.HTTP_200_OK
    updated = res.json()
    assert updated["title"] == "Updated"

    res = client.delete(f"/songs/{song['id']}")
    assert res.status_code == status.HTTP_204_NO_CONTENT

    res = client.get(f"/songs/{order['id']}")
    assert res.status_code == status.HTTP_404_NOT_FOUND
