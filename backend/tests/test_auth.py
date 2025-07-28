import uuid
from fastapi import status

from .utils import register_user, login_user
from app.routes.auth import limiter


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


def test_admin_access(client, db):
    from app.models.user import User
    from app.core.security import hash_password

    admin = User(
        email=f"{uuid.uuid4()}@example.com",
        username=f"admin_{uuid.uuid4().hex[:8]}",
        hashed_password=hash_password("password"),
        is_admin=True,
    )
    user = User(
        email=f"{uuid.uuid4()}@example.com",
        username=f"user_{uuid.uuid4().hex[:8]}",
        hashed_password=hash_password("password"),
    )
    db.add_all([admin, user])
    db.commit()

    admin_tokens = login_user(client, admin.email)
    user_tokens = login_user(client, user.email)

    admin_header = {"Authorization": f"Bearer {admin_tokens['access_token']}"}
    user_header = {"Authorization": f"Bearer {user_tokens['access_token']}"}

    res_admin = client.get("/admin/users", headers=admin_header)
    assert res_admin.status_code == status.HTTP_200_OK
    assert isinstance(res_admin.json(), list)

    res_user = client.get("/admin/users", headers=user_header)
    assert res_user.status_code == status.HTTP_403_FORBIDDEN


def test_register_duplicate(client):
    email = f"{uuid.uuid4()}@example.com"
    username = f"user_{uuid.uuid4().hex[:8]}"

    first = client.post(
        "/auth/register",
        json={"email": email, "username": username, "password": "pass"},
    )
    assert first.status_code == status.HTTP_200_OK

    duplicate = client.post(
        "/auth/register",
        json={"email": email, "username": username, "password": "pass"},
    )
    assert duplicate.status_code == status.HTTP_400_BAD_REQUEST


def test_login_invalid_credentials(client):
    user = register_user(client)

    res = client.post(
        "/auth/login", json={"email": user["email"], "password": "wrong"}
    )
    assert res.status_code == status.HTTP_401_UNAUTHORIZED


def test_refresh_invalid_token(client):
    res = client.post("/auth/refresh", json={"refresh_token": "bad"})
    assert res.status_code == status.HTTP_401_UNAUTHORIZED


def test_verification_flow(client):
    user = register_user(client)
    res = client.post("/auth/request-verify", json={"email": user["email"]})
    assert res.status_code == status.HTTP_200_OK
    token = res.json()["token"]

    res = client.post("/auth/verify", json={"token": token})
    assert res.status_code == status.HTTP_200_OK

    tokens = login_user(client, user["email"])
    auth_header = {"Authorization": f"Bearer {tokens['access_token']}"}
    me = client.get("/auth/me", headers=auth_header)
    assert me.json()["is_verified"] is True


def test_password_reset_flow(client):
    user = register_user(client)
    res = client.post("/auth/password-reset-request", json={"email": user["email"]})
    assert res.status_code == status.HTTP_200_OK
    token = res.json()["token"]

    res = client.post(
        "/auth/password-reset", json={"token": token, "new_password": "newpass"}
    )
    assert res.status_code == status.HTTP_200_OK

    tokens = login_user(client, user["email"], password="newpass")
    assert tokens["access_token"]


def test_rate_limit_login(client):
    user = register_user(client)
    for _ in range(5):
        client.post("/auth/login", json={"email": user["email"], "password": "wrong"})
    res = client.post("/auth/login", json={"email": user["email"], "password": "wrong"})
    assert res.status_code == status.HTTP_429_TOO_MANY_REQUESTS


def test_update_profile(client):
    user = register_user(client)
    tokens = login_user(client, user["email"])
    header = {"Authorization": f"Bearer {tokens['access_token']}"}

    new_email = f"{uuid.uuid4()}@example.com"
    new_username = f"user_{uuid.uuid4().hex[:8]}"
    res = client.put(
        "/auth/me",
        json={"email": new_email, "username": new_username},
        headers=header,
    )
    assert res.status_code == status.HTTP_200_OK
    data = res.json()
    assert data["email"] == new_email
    assert data["username"] == new_username


def test_update_profile_requires_auth(client):
    res = client.put("/auth/me", json={"email": "x@example.com"})
    assert res.status_code == status.HTTP_401_UNAUTHORIZED


def test_change_password(client):
    user = register_user(client)
    tokens = login_user(client, user["email"])
    header = {"Authorization": f"Bearer {tokens['access_token']}"}

    res = client.put(
        "/auth/password",
        json={"current_password": "password", "new_password": "newpass"},
        headers=header,
    )
    assert res.status_code == status.HTTP_200_OK

    login_res = client.post(
        "/auth/login", json={"email": user["email"], "password": "newpass"}
    )
    assert login_res.status_code == status.HTTP_200_OK


def test_change_password_requires_auth(client):
    res = client.put(
        "/auth/password",
        json={"current_password": "password", "new_password": "new"},
    )
    assert res.status_code == status.HTTP_401_UNAUTHORIZED


def test_delete_account(client):
    user = register_user(client)
    tokens = login_user(client, user["email"])
    header = {"Authorization": f"Bearer {tokens['access_token']}"}

    res = client.delete("/auth/me", headers=header)
    assert res.status_code == status.HTTP_204_NO_CONTENT

    login_res = client.post(
        "/auth/login", json={"email": user["email"], "password": "password"}
    )
    assert login_res.status_code == status.HTTP_401_UNAUTHORIZED


def test_delete_account_requires_auth(client):
    res = client.delete("/auth/me")
    assert res.status_code == status.HTTP_401_UNAUTHORIZED
