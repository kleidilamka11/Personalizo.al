from fastapi import status
from .utils import create_package, auth_header


def test_create_checkout(monkeypatch, client):
    package = create_package(client, "tier-pay", variant_id=123)
    header = auth_header(client)
    order_payload = {
        "song_package_id": package["id"],
        "recipient_name": "PayUser",
        "mood": "happy",
        "facts": "test",
    }
    res = client.post("/orders/", json=order_payload, headers=header)
    assert res.status_code == status.HTTP_200_OK, res.text
    order = res.json()

    def mock_post(url, json=None, headers=None):
        class Resp:
            status_code = 201
            def json(self):
                return {"data": {"attributes": {"url": "http://example.com/pay"}}}
        return Resp()

    monkeypatch.setattr("httpx.post", mock_post)

    resp = client.post(f"/payments/checkout/{order['id']}", headers=header)
    assert resp.status_code == status.HTTP_200_OK
    assert resp.json()["url"] == "http://example.com/pay"
