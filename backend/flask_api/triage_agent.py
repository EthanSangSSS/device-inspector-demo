"""Deterministic AI-assisted triage stub.

This module imitates the contract of a CV/VLM/multi-agent triage layer without
sending data to a model provider. It is suitable for public demo and CI tests.
"""

from __future__ import annotations

from typing import Any


def triage_failure_case(
    device: dict[str, Any], logs: list[dict[str, Any]], case: dict[str, Any] | None = None
) -> dict[str, Any]:
    """Return a structured failure-analysis hypothesis.

    The logic is intentionally deterministic so that tests can verify evidence,
    confidence, invalidators, and next-test recommendations.
    """

    messages = " ".join(str(log.get("message", "")).lower() for log in logs)
    components = {str(log.get("component", "")).lower() for log in logs}
    tests = {str(log.get("test_name", "")).lower() for log in logs if log.get("test_name")}
    severities = {str(log.get("severity", "")).lower() for log in logs}

    if "thermal" in messages or "thermal_system" in components:
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
        owner_domain = "ME/thermal"
    elif "microphone" in messages or "audio" in messages or "microphone" in components:
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
        owner_domain = "Acoustic/ME"
    elif "connector" in messages or "connector" in components:
        failure_mode = "connector-contact-instability"
        confidence = "medium"
        next_tests = [
            "Run insertion-force and continuity tests across synthetic fixture conditions.",
            "Inspect connector seating, contamination, and tolerance stack-up.",
            "Correlate failure rate with station and fixture metadata.",
        ]
        invalidators = [
            "Continuity remains stable under vibration and insertion cycles.",
            "Failures reproduce equally on known-good connectors and fixtures.",
        ]
        owner_domain = "EE/ME"
    else:
        failure_mode = "unknown-requires-more-evidence"
        confidence = "low"
        next_tests = [
            "Collect additional structured logs.",
            "Reproduce failure under controlled fixture conditions.",
        ]
        invalidators = ["New evidence points to a software-only issue."]
        owner_domain = "unassigned"

    evidence = [
        {
            "log_id": log.get("log_id"),
            "source": log.get("source"),
            "severity": log.get("severity"),
            "component": log.get("component"),
            "test_name": log.get("test_name"),
            "measurement": log.get("measurement", {}),
            "evidence_strength": log.get("evidence_strength", "unknown"),
        }
        for log in logs
    ]

    return {
        "case_id": (case or {}).get("case_id"),
        "device_id": device.get("device_id"),
        "failure_mode": failure_mode,
        "confidence": confidence,
        "owner_domain": owner_domain,
        "evidence": evidence,
        "invalidators": invalidators,
        "next_tests": next_tests,
        "action": "Keep as engineering hypothesis until reproduced and reviewed by the owning hardware team.",
        "risk_flags": sorted(flag for flag in severities if flag in {"warning", "critical"}),
        "observed_test_names": sorted(tests),
        "facts_hypotheses_boundary": {
            "facts": (case or {}).get("facts", []),
            "hypotheses": [(case or {}).get("symptom")] if case else [],
        },
    }
