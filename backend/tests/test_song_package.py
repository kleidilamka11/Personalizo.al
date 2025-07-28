import uuid
from fastapi import status


def create_package(client, tier="basic"):
    payload = {
        "tier": tier,
        "name": f"{tier}_package",
        "description": "desc",
        "price_eur": 10,
        "duration_seconds": 30,
        "commercial_use": False,
    }
    response = client.post("/packages/", json=payload)
    return response


def test_song_package_flow(client):
    # initially empty
    res = client.get("/packages/")
    assert res.status_code == status.HTTP_200_OK
    assert res.json() == []

    res = create_package(client, "short")
    assert res.status_code == status.HTTP_200_OK
    data = res.json()
    assert data["tier"] == "short"
    assert data["id"]

    # list packages should include the new one
    res = client.get("/packages/")
    assert res.status_code == status.HTTP_200_OK
    packages = res.json()
    assert len(packages) == 1
    assert packages[0]["tier"] == "short"

    # duplicate tier should fail
    dup = create_package(client, "short")
    assert dup.status_code == status.HTTP_400_BAD_REQUEST


def test_update_and_delete_package(client):
    res = create_package(client, "upd")
    assert res.status_code == status.HTTP_200_OK
    pkg = res.json()

    update_payload = {
        "tier": "upd2",
        "name": "updated",
        "description": "new",
        "price_eur": 20,
        "duration_seconds": 60,
        "commercial_use": True,
    }
    res = client.put(f"/packages/{pkg['id']}", json=update_payload)
    assert res.status_code == status.HTTP_200_OK
    updated = res.json()
    assert updated["tier"] == "upd2"

    res = client.delete(f"/packages/{pkg['id']}")
    assert res.status_code == status.HTTP_204_NO_CONTENT

    res = client.get("/packages/")
    ids = [p["id"] for p in res.json()]
    assert pkg["id"] not in ids
