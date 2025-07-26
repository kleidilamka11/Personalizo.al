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


def test_auth_flow(client):
    user = register_user(client)
    tokens = login_user(client, user["email"])

    auth_header = {"Authorization": f"Bearer {tokens['access_token']}"}
    me = client.get("/auth/me", headers=auth_header)
    assert me.status_code == status.HTTP_200_OK
    assert me.json()["email"] == user["email"]

    refresh = client.post("/auth/refresh", json={"refresh_token": tokens["refresh_token"]})
    assert refresh.status_code == status.HTTP_200_OK
    assert refresh.json()["access_token"]


def test_admin_access(client):
    admin = register_user(client, is_admin=True)
    admin_tokens = login_user(client, admin["email"])
    user = register_user(client)
    user_tokens = login_user(client, user["email"])

    admin_header = {"Authorization": f"Bearer {admin_tokens['access_token']}"}
    user_header = {"Authorization": f"Bearer {user_tokens['access_token']}"}

    res_admin = client.get("/admin/users", headers=admin_header)
    assert res_admin.status_code == status.HTTP_200_OK
    assert isinstance(res_admin.json(), list)

    res_user = client.get("/admin/users", headers=user_header)
    assert res_user.status_code == status.HTTP_403_FORBIDDEN
