def test_case_report_signature_includes_case_and_evidence(client, auth_header):
    device = {
        "device_id": "SYNTH-DEVICE-REPORT-001",
        "product_family": "mobile-device",
        "privacy_class": "synthetic",
    }
    case = {
        "case_id": "SYNTH-CASE-REPORT-001",
        "device_id": "SYNTH-DEVICE-REPORT-001",
        "build_phase": "PVT",
        "component": "thermal_system",
        "symptom": "Thermal warning during synthetic camera stress loop",
    }
    evidence = {
        "log_id": "SYNTH-LOG-REPORT-001",
        "device_id": "SYNTH-DEVICE-REPORT-001",
        "source": "thermal_sensor_mock",
        "severity": "warning",
        "component": "thermal_system",
        "test_name": "camera_stress_loop",
        "message": "Thermal envelope exceeded expected range.",
        "measurement": {"metric": "surface_temp_delta_c", "value": 8.4, "unit": "C", "limit": 5.0},
        "evidence_strength": "medium",
    }
    assert client.post("/devices", json=device, headers=auth_header).status_code == 201
    assert client.post("/cases", json=case, headers=auth_header).status_code == 201
    assert client.post("/cases/SYNTH-CASE-REPORT-001/evidence", json=evidence, headers=auth_header).status_code == 201

    created = client.post(
        "/reports",
        json={"case_id": "SYNTH-CASE-REPORT-001", "report_id": "SYNTH-REPORT-CASE-001"},
        headers=auth_header,
    )
    assert created.status_code == 201
    payload = created.get_json()
    report = payload["report"]
    assert report["case"]["case_id"] == "SYNTH-CASE-REPORT-001"
    assert report["evidence"][0]["measurement"]["metric"] == "surface_temp_delta_c"

    verified = client.post("/reports/verify", json={"report": report, "signature": payload["signature"]})
    assert verified.status_code == 200
    assert verified.get_json()["valid"] is True

    tampered = dict(report)
    tampered["review_state"] = "closed-root-cause-accepted"
    invalid = client.post("/reports/verify", json={"report": tampered, "signature": payload["signature"]})
    assert invalid.status_code == 200
    assert invalid.get_json()["valid"] is False
