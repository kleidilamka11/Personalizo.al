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
