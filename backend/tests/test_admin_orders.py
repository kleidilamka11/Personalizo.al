from fastapi import status

from .utils import register_user, login_user, create_package


def auth_header_for(client, email):
    tokens = login_user(client, email)
    return {"Authorization": f"Bearer {tokens['access_token']}"}


def test_admin_orders_list_and_filter(client):
    admin = register_user(client, is_admin=True)
    user1 = register_user(client)
    user2 = register_user(client)

    package = create_package(client, "admintier")

    payload = {
        "song_package_id": package["id"],
        "recipient_name": "Rec",
        "mood": "happy",
        "facts": None,
    }
    res1 = client.post("/orders/", json=payload, headers=auth_header_for(client, user1["email"]))
    assert res1.status_code == status.HTTP_200_OK
    order1 = res1.json()
    res2 = client.post("/orders/", json=payload, headers=auth_header_for(client, user2["email"]))
    assert res2.status_code == status.HTTP_200_OK
    order2 = res2.json()

    admin_header = auth_header_for(client, admin["email"])
    res = client.get("/admin/orders/", headers=admin_header)
    assert res.status_code == status.HTTP_200_OK
    orders = res.json()
    assert {order1["id"], order2["id"]} == {o["id"] for o in orders}

    res = client.get(f"/admin/orders/?user_id={user1['id']}", headers=admin_header)
    assert res.status_code == status.HTTP_200_OK
    filtered = res.json()
    assert len(filtered) == 1
    assert filtered[0]["user"]["id"] == user1["id"]


def test_admin_orders_requires_admin(client):
    user = register_user(client)
    header = auth_header_for(client, user["email"])
    res = client.get("/admin/orders/", headers=header)
    assert res.status_code == status.HTTP_403_FORBIDDEN

