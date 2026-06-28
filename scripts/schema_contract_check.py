"""Lightweight contract checks for demo API and docs."""

from __future__ import annotations

import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]

REQUIRED_PATHS = [
    "openapi/device-inspector-demo.openapi.yaml",
    "docs/hardware_evidence_schema.md",
    "docs/apple_role_alignment.md",
    "docs/threat_model.md",
    "backend/flask_api/schemas.py",
]

REQUIRED_OPENAPI_TERMS = [
    "/cases",
    "/cases/{case_id}/evidence",
    "/cases/{case_id}/triage",
    "/cases/{case_id}/audit-events",
    "DiagnosticEvidence",
    "CaseStatus",
]


def main() -> int:
    missing = [path for path in REQUIRED_PATHS if not (ROOT / path).exists()]
    if missing:
        print("Missing required files:")
        for path in missing:
            print(f"- {path}")
        return 1

    openapi = (ROOT / "openapi/device-inspector-demo.openapi.yaml").read_text(encoding="utf-8")
    missing_terms = [term for term in REQUIRED_OPENAPI_TERMS if term not in openapi]
    if missing_terms:
        print("OpenAPI contract missing terms:")
        for term in missing_terms:
            print(f"- {term}")
        return 1

    print("Schema contract check passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
