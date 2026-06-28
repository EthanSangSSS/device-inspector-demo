"""Deterministic AI-assisted triage stub.

This module imitates the contract of a CV/VLM/multi-agent triage layer without
sending data to a model provider. It is suitable for public demo and CI tests.
"""

from __future__ import annotations

from typing import Any


def triage_failure_case(device: dict[str, Any], logs: list[dict[str, Any]]) -> dict[str, Any]:
    """Return a structured failure-analysis hypothesis.

    The logic is intentionally deterministic so that tests can verify evidence,
    confidence, invalidators, and next-test recommendations.
    """

    messages = " ".join(str(log.get("message", "")).lower() for log in logs)
    severities = {str(log.get("severity", "")).lower() for log in logs}

    if "thermal" in messages:
        failure_mode = "thermal-envelope-instability"
        confidence = "medium"
        next_tests = [
            "Repeat camera stress loop under controlled ambient temperature.",
            "Compare thermal sensor trace with current draw and enclosure-pressure events.",
            "Inspect recent assembly process changes around heat-spreader contact.",
        ]
        invalidators = [
            "No temperature delta appears under repeated stress loops.",
            "Control device on same firmware shows identical telemetry.",
        ]
    elif "microphone" in messages or "audio" in messages:
        failure_mode = "intermittent-audio-path-noise"
        confidence = "low"
        next_tests = [
            "Run sealed/unsealed acoustic path A/B test.",
            "Capture synchronized audio waveform and enclosure-pressure trace.",
            "Check microphone mesh and flex seating under microscope.",
        ]
        invalidators = [
            "Noise cannot be reproduced across stress cycles.",
            "Known-good fixture produces the same waveform artifact.",
        ]
    else:
        failure_mode = "unknown-requires-more-evidence"
        confidence = "low"
        next_tests = [
            "Collect additional structured logs.", "Reproduce failure under controlled fixture conditions."]
        invalidators = ["New evidence points to a software-only issue."]

    evidence = [
        {
            "log_id": log.get("log_id"),
            "source": log.get("source"),
            "severity": log.get("severity"),
            "evidence_strength": log.get("evidence_strength", "unknown"),
        }
        for log in logs
    ]

    return {
        "device_id": device.get("device_id"),
        "failure_mode": failure_mode,
        "confidence": confidence,
        "evidence": evidence,
        "invalidators": invalidators,
        "next_tests": next_tests,
        "action": "Keep as engineering hypothesis until reproduced and reviewed by the owning hardware team.",
        "risk_flags": sorted(flag for flag in severities if flag in {"warning", "critical"}),
    }
