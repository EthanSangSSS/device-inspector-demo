def test_case_lifecycle_and_audit_trail(client, auth_header):
    device = {
        "device_id": "SYNTH-DEVICE-CASE-001",
        "product_family": "mobile-device",
        "privacy_class": "synthetic",
    }
    case = {
        "case_id": "SYNTH-CASE-001",
        "device_id": "SYNTH-DEVICE-CASE-001",
        "build_phase": "DVT",
        "component": "thermal_system",
        "symptom": "Thermal drift during camera stress loop",
        "facts": ["Synthetic thermal delta exceeded demo limit."],
        "hypotheses": ["Heat-spreader contact variance."],
    }

    assert client.post("/devices", json=device, headers=auth_header).status_code == 201
    created = client.post("/cases", json=case, headers=auth_header)
    assert created.status_code == 201
    assert created.get_json()["case"]["status"] == "new"

    updated = client.post(
        "/cases/SYNTH-CASE-001/status",
        json={"status": "needs_reproduction"},
        headers=auth_header,
    )
    assert updated.status_code == 200
    assert updated.get_json()["case"]["status"] == "needs_reproduction"

    audit = client.get("/cases/SYNTH-CASE-001/audit-events", headers=auth_header)
    assert audit.status_code == 200
    actions = [event["action"] for event in audit.get_json()["audit_events"]]
    assert "case.upsert" in actions
    assert "case.status.update" in actions


def test_case_rejects_unknown_status(client, auth_header):
    device = {
        "device_id": "SYNTH-DEVICE-CASE-002",
        "product_family": "mobile-device",
        "privacy_class": "synthetic",
    }
    assert client.post("/devices", json=device, headers=auth_header).status_code == 201
    response = client.post(
        "/cases",
        json={
            "case_id": "SYNTH-CASE-002",
            "device_id": "SYNTH-DEVICE-CASE-002",
            "build_phase": "DVT",
            "component": "thermal_system",
            "symptom": "Thermal drift",
            "status": "definitely_not_a_valid_status",
        },
        headers=auth_header,
    )
    assert response.status_code == 400
    assert "status" in response.get_json()["error"]
