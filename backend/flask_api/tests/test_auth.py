def test_health_does_not_require_auth(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.get_json()["status"] == "ok"


def test_protected_endpoint_requires_bearer_token(client):
    response = client.post("/devices", json={"device_id": "SYNTH-DEVICE-001"})
    assert response.status_code == 401
    assert response.get_json()["error"] == "missing bearer token"


def test_token_allows_device_creation(client, auth_header):
    response = client.post(
        "/devices",
        json={
            "device_id": "SYNTH-DEVICE-001",
            "product_family": "mobile-device",
            "privacy_class": "synthetic",
        },
        headers=auth_header,
    )
    assert response.status_code == 201
    assert response.get_json()["device"]["device_id"] == "SYNTH-DEVICE-001"
