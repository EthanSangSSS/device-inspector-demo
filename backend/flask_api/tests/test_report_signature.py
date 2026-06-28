def _seed_case(client, auth_header):
    device = {
        "device_id": "SYNTH-DEVICE-001",
        "product_family": "mobile-device",
        "privacy_class": "synthetic",
    }
    log = {
        "log_id": "SYNTH-LOG-001",
        "device_id": "SYNTH-DEVICE-001",
        "source": "thermal_sensor_mock",
        "severity": "warning",
        "message": "Thermal envelope exceeded expected range during camera stress loop.",
        "evidence_strength": "medium",
    }
    assert client.post("/devices", json=device, headers=auth_header).status_code == 201
    assert client.post("/diagnostic-logs", json=log, headers=auth_header).status_code == 201


def test_report_signature_verifies(client, auth_header):
    _seed_case(client, auth_header)
    created = client.post(
        "/reports",
        json={"device_id": "SYNTH-DEVICE-001", "report_id": "SYNTH-REPORT-001"},
        headers=auth_header,
    )
    assert created.status_code == 201
    payload = created.get_json()

    verified = client.post(
        "/reports/verify",
        json={"report": payload["report"], "signature": payload["signature"]},
    )
    assert verified.status_code == 200
    assert verified.get_json()["valid"] is True


def test_report_tamper_detection(client, auth_header):
    _seed_case(client, auth_header)
    created = client.post(
        "/reports",
        json={"device_id": "SYNTH-DEVICE-001", "report_id": "SYNTH-REPORT-001"},
        headers=auth_header,
    )
    payload = created.get_json()
    tampered_report = dict(payload["report"])
    tampered_report["review_state"] = "production-finding"

    verified = client.post(
        "/reports/verify",
        json={"report": tampered_report, "signature": payload["signature"]},
    )
    assert verified.status_code == 200
    assert verified.get_json()["valid"] is False
