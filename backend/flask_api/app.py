"""Flask API for the Device Inspector public-safe demo."""

from __future__ import annotations

import os
import uuid
from typing import Any

from flask import Flask, jsonify, request

from auth import issue_token, require_auth
from database import DiagnosticRepository
from rsa_signing import ReportSigner
from sample_data import SYNTHETIC_DEVICE, SYNTHETIC_LOGS
from triage_agent import triage_failure_case


def create_app(
    repository: DiagnosticRepository | None = None,
    signer: ReportSigner | None = None,
) -> Flask:
    app = Flask(__name__)
    repo = repository or DiagnosticRepository(os.getenv("DEVICE_INSPECTOR_DB_PATH", ":memory:"))
    report_signer = signer or ReportSigner()

    @app.get("/health")
    def health() -> Any:
        return jsonify({"status": "ok", "mode": "public-safe-demo"})

    @app.post("/auth/token")
    def token() -> Any:
        payload = request.get_json(silent=True) or {}
        subject = payload.get("subject", "demo.engineer")
        role = payload.get("role", "engineer")
        return jsonify({"access_token": issue_token(subject=subject, role=role), "token_type": "bearer"})

    @app.post("/demo/seed")
    def seed_demo() -> Any:
        repo.save_device(dict(SYNTHETIC_DEVICE))
        for log in SYNTHETIC_LOGS:
            repo.save_log(dict(log))
        return jsonify({"device": SYNTHETIC_DEVICE, "logs": SYNTHETIC_LOGS})

    @app.post("/devices")
    @require_auth
    def create_device() -> Any:
        payload = request.get_json(force=True)
        try:
            device = repo.save_device(payload)
        except ValueError as exc:
            return jsonify({"error": str(exc)}), 400
        return jsonify({"device": device}), 201

    @app.post("/cases")
    @require_auth
    def create_case() -> Any:
        payload = request.get_json(force=True)
        try:
            case = repo.save_case(payload, actor="demo.engineer")
        except ValueError as exc:
            return jsonify({"error": str(exc)}), 400
        return jsonify({"case": case}), 201

    @app.get("/cases/<case_id>")
    @require_auth
    def get_case(case_id: str) -> Any:
        case = repo.get_case(case_id)
        if not case:
            return jsonify({"error": "unknown case_id"}), 404
        evidence = repo.list_case_logs(case_id)
        return jsonify({"case": case, "evidence": evidence})

    @app.post("/cases/<case_id>/status")
    @require_auth
    def update_case_status(case_id: str) -> Any:
        payload = request.get_json(force=True)
        try:
            case = repo.update_case_status(case_id, payload.get("status"), actor="demo.engineer")
        except ValueError as exc:
            return jsonify({"error": str(exc)}), 400
        return jsonify({"case": case})

    @app.post("/cases/<case_id>/evidence")
    @require_auth
    def create_case_evidence(case_id: str) -> Any:
        payload = request.get_json(force=True)
        payload["case_id"] = case_id
        try:
            evidence = repo.save_log(payload, actor="demo.engineer")
            repo.update_case_status(case_id, "evidence_collected", actor="system")
        except ValueError as exc:
            return jsonify({"error": str(exc)}), 400
        return jsonify({"evidence": evidence}), 201

    @app.post("/cases/<case_id>/triage")
    @require_auth
    def triage_case(case_id: str) -> Any:
        case = repo.get_case(case_id)
        if not case:
            return jsonify({"error": "unknown case_id"}), 404
        device = repo.get_device(case["device_id"])
        if not device:
            return jsonify({"error": "unknown device_id"}), 404
        logs = repo.list_case_logs(case_id)
        result = triage_failure_case(device, logs, case=case)
        repo.update_case_status(case_id, "triaged", actor="system")
        return jsonify({"triage": result})

    @app.get("/cases/<case_id>/audit-events")
    @require_auth
    def get_case_audit_events(case_id: str) -> Any:
        if not repo.get_case(case_id):
            return jsonify({"error": "unknown case_id"}), 404
        return jsonify({"audit_events": repo.list_audit_events(case_id)})

    @app.post("/diagnostic-logs")
    @require_auth
    def create_log() -> Any:
        payload = request.get_json(force=True)
        try:
            log = repo.save_log(payload)
        except ValueError as exc:
            return jsonify({"error": str(exc)}), 400
        return jsonify({"log": log}), 201

    @app.post("/triage")
    @require_auth
    def triage() -> Any:
        payload = request.get_json(force=True)
        device_id = payload.get("device_id")
        device = repo.get_device(device_id)
        if not device:
            return jsonify({"error": "unknown device_id"}), 404
        logs = repo.list_logs(device_id)
        result = triage_failure_case(device, logs)
        return jsonify({"triage": result})

    @app.post("/reports")
    @require_auth
    def create_report() -> Any:
        payload = request.get_json(force=True)
        case_id = payload.get("case_id")
        case = repo.get_case(case_id) if case_id else None
        if case_id and not case:
            return jsonify({"error": "unknown case_id"}), 404
        device_id = payload.get("device_id") or (case or {}).get("device_id")
        device = repo.get_device(device_id)
        if not device:
            return jsonify({"error": "unknown device_id"}), 404
        logs = repo.list_case_logs(case_id) if case_id else repo.list_logs(device_id)
        triage = triage_failure_case(device, logs, case=case)
        report = {
            "report_id": payload.get("report_id") or f"SYNTH-REPORT-{uuid.uuid4().hex[:8].upper()}",
            "case_id": case_id,
            "device_id": device_id,
            "privacy_class": "synthetic",
            "case": case,
            "device": device,
            "evidence": logs,
            "triage": triage,
            "review_state": "engineering-hypothesis-not-production-finding",
        }
        signature = report_signer.sign(report)
        repo.save_report(report, signature)
        return jsonify({"report": report, "signature": signature, "public_key_pem": report_signer.public_key_pem()}), 201

    @app.post("/reports/verify")
    def verify_report() -> Any:
        payload = request.get_json(force=True)
        report = payload.get("report")
        signature = payload.get("signature")
        if not isinstance(report, dict) or not isinstance(signature, str):
            return jsonify({"valid": False, "error": "report and signature required"}), 400
        return jsonify({"valid": report_signer.verify(report, signature)})

    return app


if __name__ == "__main__":
    create_app().run(host="127.0.0.1", port=5001, debug=True)
