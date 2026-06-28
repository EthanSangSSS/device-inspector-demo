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
        device_id = payload.get("device_id")
        device = repo.get_device(device_id)
        if not device:
            return jsonify({"error": "unknown device_id"}), 404
        logs = repo.list_logs(device_id)
        triage = triage_failure_case(device, logs)
        report = {
            "report_id": payload.get("report_id") or f"SYNTH-REPORT-{uuid.uuid4().hex[:8].upper()}",
            "device_id": device_id,
            "privacy_class": "synthetic",
            "device": device,
            "logs": logs,
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
