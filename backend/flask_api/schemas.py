"""Schema helpers for hardware diagnostic cases.

The demo intentionally uses explicit dictionaries instead of a heavier validation
framework so that the public baseline stays inspectable and dependency-light.
"""

from __future__ import annotations

from typing import Any

CASE_STATUSES = {
    "new",
    "evidence_collected",
    "triaged",
    "needs_reproduction",
    "assigned_to_domain_owner",
    "corrective_action_proposed",
    "verification_pending",
    "closed",
}

BUILD_PHASES = {"EVT", "DVT", "PVT", "MP", "UNKNOWN"}
COMPONENTS = {
    "battery",
    "camera_module",
    "connector",
    "display",
    "enclosure",
    "microphone",
    "speaker",
    "thermal_system",
    "unknown",
}
EVIDENCE_STRENGTHS = {"low", "medium", "high"}
SEVERITIES = {"info", "warning", "critical"}


def require_synthetic_identifier(value: Any, field: str) -> str:
    if not isinstance(value, str) or not value.startswith("SYNTH-"):
        raise ValueError(f"{field} must be a synthetic identifier prefixed with SYNTH-")
    return value


def normalize_case(payload: dict[str, Any]) -> dict[str, Any]:
    case_id = require_synthetic_identifier(payload.get("case_id"), "case_id")
    device_id = require_synthetic_identifier(payload.get("device_id"), "device_id")
    status = payload.get("status", "new")
    if status not in CASE_STATUSES:
        raise ValueError(f"status must be one of {sorted(CASE_STATUSES)}")

    build_phase = str(payload.get("build_phase", "UNKNOWN")).upper()
    if build_phase not in BUILD_PHASES:
        raise ValueError(f"build_phase must be one of {sorted(BUILD_PHASES)}")

    return {
        "case_id": case_id,
        "device_id": device_id,
        "status": status,
        "build_phase": build_phase,
        "component": normalize_choice(payload.get("component", "unknown"), COMPONENTS, "component"),
        "symptom": require_non_empty_text(payload.get("symptom"), "symptom"),
        "owner_domain": str(payload.get("owner_domain", "unassigned")),
        "privacy_class": "synthetic",
        "facts": list(payload.get("facts", [])),
        "hypotheses": list(payload.get("hypotheses", [])),
    }


def normalize_evidence(payload: dict[str, Any]) -> dict[str, Any]:
    log_id = require_synthetic_identifier(payload.get("log_id"), "log_id")
    case_id = require_synthetic_identifier(payload.get("case_id"), "case_id")
    device_id = require_synthetic_identifier(payload.get("device_id"), "device_id")
    measurement = payload.get("measurement", {})
    if measurement and not isinstance(measurement, dict):
        raise ValueError("measurement must be an object")

    return {
        "log_id": log_id,
        "case_id": case_id,
        "device_id": device_id,
        "source": require_non_empty_text(payload.get("source"), "source"),
        "severity": normalize_choice(payload.get("severity", "info"), SEVERITIES, "severity"),
        "component": normalize_choice(payload.get("component", "unknown"), COMPONENTS, "component"),
        "test_name": require_non_empty_text(payload.get("test_name"), "test_name"),
        "fixture_id": str(payload.get("fixture_id", "SYNTH-FIXTURE-UNKNOWN")),
        "station": str(payload.get("station", "SYNTH-STATION-UNKNOWN")),
        "message": require_non_empty_text(payload.get("message"), "message"),
        "measurement": normalize_measurement(measurement),
        "reproduction_rate": str(payload.get("reproduction_rate", "unknown")),
        "evidence_strength": normalize_choice(payload.get("evidence_strength", "low"), EVIDENCE_STRENGTHS, "evidence_strength"),
        "privacy_class": "synthetic",
    }


def normalize_status(value: Any) -> str:
    status = str(value)
    if status not in CASE_STATUSES:
        raise ValueError(f"status must be one of {sorted(CASE_STATUSES)}")
    return status


def normalize_measurement(measurement: dict[str, Any]) -> dict[str, Any]:
    if not measurement:
        return {}
    metric = require_non_empty_text(measurement.get("metric"), "measurement.metric")
    unit = require_non_empty_text(measurement.get("unit"), "measurement.unit")
    value = measurement.get("value")
    limit = measurement.get("limit")
    if not isinstance(value, (int, float)):
        raise ValueError("measurement.value must be numeric")
    if limit is not None and not isinstance(limit, (int, float)):
        raise ValueError("measurement.limit must be numeric when provided")
    return {"metric": metric, "value": value, "unit": unit, "limit": limit}


def require_non_empty_text(value: Any, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field} must be a non-empty string")
    return value.strip()


def normalize_choice(value: Any, allowed: set[str], field: str) -> str:
    text = str(value).lower()
    if text not in allowed:
        raise ValueError(f"{field} must be one of {sorted(allowed)}")
    return text
