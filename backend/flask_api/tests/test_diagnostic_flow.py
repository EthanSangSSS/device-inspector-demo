def test_rejects_non_synthetic_identifier(client, auth_header):
    response = client.post(
        "/devices",
        json={
            "device_id": "REAL-LOOKING-DEVICE-001",
            "product_family": "mobile-device",
            "privacy_class": "synthetic",
        },
        headers=auth_header,
    )
    assert response.status_code == 400
    assert "SYNTH-" in response.get_json()["error"]


def test_full_diagnostic_triage_flow(client, auth_header):
    device = {
        "device_id": "SYNTH-DEVICE-002",
        "product_family": "mobile-device",
        "privacy_class": "synthetic",
    }
    log = {
        "log_id": "SYNTH-LOG-002",
        "device_id": "SYNTH-DEVICE-002",
        "source": "thermal_sensor_mock",
        "severity": "warning",
        "message": "Thermal instability after repeated load cycle.",
        "evidence_strength": "medium",
    }

    assert client.post("/devices", json=device, headers=auth_header).status_code == 201
    assert client.post("/diagnostic-logs", json=log, headers=auth_header).status_code == 201

    triage = client.post("/triage", json={"device_id": "SYNTH-DEVICE-002"}, headers=auth_header)
    assert triage.status_code == 200
    result = triage.get_json()["triage"]
    assert result["failure_mode"] == "thermal-envelope-instability"
    assert result["confidence"] == "medium"
    assert result["evidence"][0]["log_id"] == "SYNTH-LOG-002"
    assert result["invalidators"]
    assert result["next_tests"]
