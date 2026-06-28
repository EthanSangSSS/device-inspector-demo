def _seed_case(client, auth_header):
    device = {
        "device_id": "SYNTH-DEVICE-EVIDENCE-001",
        "product_family": "mobile-device",
        "privacy_class": "synthetic",
    }
    case = {
        "case_id": "SYNTH-CASE-EVIDENCE-001",
        "device_id": "SYNTH-DEVICE-EVIDENCE-001",
        "build_phase": "EVT",
        "component": "connector",
        "symptom": "Intermittent connector continuity loss under fixture vibration",
        "facts": ["Synthetic continuity failure reproduced in 3 of 10 runs."],
        "hypotheses": ["Connector seating or fixture tolerance issue."],
    }
    assert client.post("/devices", json=device, headers=auth_header).status_code == 201
    assert client.post("/cases", json=case, headers=auth_header).status_code == 201


def test_hardware_evidence_schema_and_triage(client, auth_header):
    _seed_case(client, auth_header)
    evidence = {
        "log_id": "SYNTH-LOG-EVIDENCE-001",
        "device_id": "SYNTH-DEVICE-EVIDENCE-001",
        "source": "fixture_continuity_mock",
        "severity": "warning",
        "component": "connector",
        "test_name": "vibration_continuity_loop",
        "fixture_id": "SYNTH-FIXTURE-CONN-001",
        "station": "SYNTH-STATION-EVT-01",
        "message": "Connector continuity loss observed during synthetic vibration loop.",
        "measurement": {
            "metric": "continuity_drop_count",
            "value": 3,
            "unit": "count",
            "limit": 0,
        },
        "reproduction_rate": "3/10",
        "evidence_strength": "medium",
    }
    created = client.post(
        "/cases/SYNTH-CASE-EVIDENCE-001/evidence",
        json=evidence,
        headers=auth_header,
    )
    assert created.status_code == 201
    payload = created.get_json()["evidence"]
    assert payload["measurement"]["metric"] == "continuity_drop_count"
    assert payload["fixture_id"] == "SYNTH-FIXTURE-CONN-001"

    triage = client.post("/cases/SYNTH-CASE-EVIDENCE-001/triage", json={}, headers=auth_header)
    assert triage.status_code == 200
    result = triage.get_json()["triage"]
    assert result["failure_mode"] == "connector-contact-instability"
    assert result["owner_domain"] == "EE/ME"
    assert result["evidence"][0]["measurement"]["value"] == 3


def test_rejects_malformed_measurement(client, auth_header):
    _seed_case(client, auth_header)
    bad = {
        "log_id": "SYNTH-LOG-EVIDENCE-002",
        "device_id": "SYNTH-DEVICE-EVIDENCE-001",
        "source": "fixture_continuity_mock",
        "severity": "warning",
        "component": "connector",
        "test_name": "vibration_continuity_loop",
        "message": "Connector continuity loss observed.",
        "measurement": {"metric": "continuity_drop_count", "value": "three", "unit": "count"},
        "evidence_strength": "medium",
    }
    response = client.post(
        "/cases/SYNTH-CASE-EVIDENCE-001/evidence",
        json=bad,
        headers=auth_header,
    )
    assert response.status_code == 400
    assert "measurement.value" in response.get_json()["error"]
