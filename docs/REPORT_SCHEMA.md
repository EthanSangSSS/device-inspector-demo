# Diagnostic Report Schema

This schema defines the minimum report contract for a trustworthy device-inspection workflow. It is intentionally implementation-neutral so the Flask backend, OpenAPI contract, mobile clients, and future CV/VLM triage pipelines can converge on the same evidence model.

## Design principles

1. Reports must distinguish raw evidence, user-confirmed observations, AI-assisted findings, and final disposition.
2. Every finding must include confidence and invalidators.
3. Missing data is a first-class state, not a silent omission.
4. A report signature verifies integrity of the payload, not truth of evidence collection.
5. Public demo reports must use synthetic identifiers only.

## Top-level report object

| Field | Type | Required | Notes |
|---|---|---:|---|
| `report_id` | string | yes | Opaque UUID or deterministic demo ID. |
| `schema_version` | string | yes | Start with `device-inspector.report.v1`. |
| `generated_at` | ISO-8601 string | yes | UTC timestamp. |
| `inspection_session` | object | yes | Session metadata and provenance. |
| `device_profile` | object | yes | Public-safe device metadata. |
| `evidence` | array | yes | Raw or guided observations. |
| `findings` | array | yes | Classified diagnostic findings. |
| `triage` | object | no | AI-assisted triage summary. |
| `limitations` | array | yes | Platform and workflow limitations that affect interpretation. |
| `disposition` | object | yes | Final summary for engineering handoff. |
| `signature` | object | no | Present after signing. Omitted before signing. |

## `inspection_session`

| Field | Type | Required | Notes |
|---|---|---:|---|
| `session_id` | string | yes | Public-safe generated ID. |
| `case_id` | string | yes | Backend case reference. |
| `client_type` | enum | yes | `backend`, `ios`, `android`, `web`, `fixture`, `synthetic`. |
| `client_version` | string | yes | App/backend build version. |
| `operator_role` | enum | no | `engineer`, `tester`, `user`, `agent`, `synthetic`. Do not store names in public demo. |
| `environment` | object | no | Brightness, ambient condition, network condition, fixture info where applicable. |

## `device_profile`

| Field | Type | Required | Notes |
|---|---|---:|---|
| `public_model_id` | string | yes | Public model or synthetic model identifier. |
| `platform` | enum | yes | `ios`, `android`, `windows`, `macos`, `synthetic`, `unknown`. |
| `os_version` | string | no | Public OS version where allowed. |
| `hardware_class` | enum | no | `phone`, `tablet`, `laptop`, `desktop`, `accessory`, `unknown`. |
| `identifier_policy` | string | yes | Must state that private serial/IMEI/owner identifiers are excluded in public demo. |

## `evidence[]`

| Field | Type | Required | Notes |
|---|---|---:|---|
| `evidence_id` | string | yes | Stable ID referenced by findings. |
| `domain` | enum | yes | `identity`, `display`, `touch`, `camera`, `audio`, `sensor`, `battery`, `thermal`, `connectivity`, `enclosure`, `report_integrity`, `triage`, `other`. |
| `capability` | string | yes | Must map to `DEVICE_INSPECTION_MATRIX.md`. |
| `source_type` | enum | yes | `api`, `guided_user_check`, `manual_checklist`, `synthetic_fixture`, `external_fixture`, `derived`. |
| `automation_level` | enum | yes | `automatic`, `guided`, `manual`, `external_fixture`. |
| `collected_at` | ISO-8601 string | yes | UTC timestamp. |
| `raw_value` | object/string/number/null | no | Raw reading or synthetic payload. Avoid private data. |
| `normalized_value` | object/string/number/null | no | Parsed value used by rules. |
| `result` | enum | yes | `pass`, `fail`, `suspect`, `not_supported`, `missing`, `not_applicable`. |
| `confidence` | enum | yes | `high`, `medium`, `low`, `not_supported`. |
| `limitations` | array | yes | Explicit limitations affecting this evidence item. |
| `provenance` | object | yes | Client, script, fixture, synthetic seed, or API path. |

## `findings[]`

| Field | Type | Required | Notes |
|---|---|---:|---|
| `finding_id` | string | yes | Stable ID. |
| `severity` | enum | yes | `critical`, `major`, `minor`, `info`. |
| `title` | string | yes | Human-readable finding. |
| `fact` | string | yes | What was directly observed. |
| `why_it_matters` | string | yes | Engineering or acceptance impact. |
| `evidence_ids` | array | yes | References one or more evidence objects. |
| `evidence_strength` | enum | yes | `high`, `medium`, `low`, `not_supported`. |
| `invalidators` | array | yes | Conditions that could make the finding wrong. |
| `next_test` | string | yes | Smallest useful retest. |
| `owner` | enum | no | `client`, `backend`, `lab`, `service_center`, `human_reviewer`, `unknown`. |

## `triage`

| Field | Type | Required | Notes |
|---|---|---:|---|
| `agent_version` | string | yes | Deterministic demo agent or future model version. |
| `summary` | string | yes | Must not overclaim. |
| `candidate_failure_modes` | array | yes | Each item requires confidence and invalidators. |
| `recommended_next_tests` | array | yes | Ordered by evidence value and cost. |
| `model_risk_note` | string | yes | Explains deterministic/synthetic boundary or model limitations. |

## `disposition`

| Field | Type | Required | Notes |
|---|---|---:|---|
| `status` | enum | yes | `pass`, `conditional_pass`, `retest_required`, `fail`, `inconclusive`. |
| `summary` | string | yes | User/engineer-facing summary. |
| `blocking_findings` | array | yes | Finding IDs that block acceptance. |
| `non_blocking_findings` | array | yes | Finding IDs to monitor. |
| `handoff_actions` | array | yes | Engineering, lab, service, or product actions. |

## `signature`

| Field | Type | Required | Notes |
|---|---|---:|---|
| `algorithm` | string | yes | Example: `RS256` or demo-specific value. |
| `payload_hash` | string | yes | Hash of canonical report payload before signature. |
| `signature_value` | string | yes | Base64 signature. |
| `public_key_id` | string | yes | Demo key ID only; never commit production private keys. |
| `verified` | boolean | no | Present in verification responses, not necessarily in signed payload. |

## Minimal JSON example

```json
{
  "report_id": "demo-report-001",
  "schema_version": "device-inspector.report.v1",
  "generated_at": "2026-07-05T00:00:00Z",
  "inspection_session": {
    "session_id": "demo-session-001",
    "case_id": "case-001",
    "client_type": "synthetic",
    "client_version": "demo"
  },
  "device_profile": {
    "public_model_id": "synthetic-phone-a",
    "platform": "synthetic",
    "hardware_class": "phone",
    "identifier_policy": "Public demo excludes serial, IMEI, owner, and production asset identifiers."
  },
  "evidence": [
    {
      "evidence_id": "ev-display-001",
      "domain": "display",
      "capability": "display_uniformity_guided_check",
      "source_type": "guided_user_check",
      "automation_level": "guided",
      "collected_at": "2026-07-05T00:00:00Z",
      "result": "suspect",
      "confidence": "low",
      "limitations": ["Ambient light and user perception may affect result."],
      "provenance": {"client": "synthetic"}
    }
  ],
  "findings": [
    {
      "finding_id": "finding-display-001",
      "severity": "minor",
      "title": "Guided display uniformity check requires retest",
      "fact": "The guided display check was marked suspect by the operator.",
      "why_it_matters": "Uniformity issues can affect perceived display quality and acceptance decisions.",
      "evidence_ids": ["ev-display-001"],
      "evidence_strength": "low",
      "invalidators": ["Ambient light", "screen protector", "brightness setting", "user perception"],
      "next_test": "Repeat under fixed brightness and low ambient light; use a fixture if available."
    }
  ],
  "limitations": ["Public demo uses synthetic and guided evidence only."],
  "disposition": {
    "status": "retest_required",
    "summary": "A guided display observation requires controlled retest before acceptance.",
    "blocking_findings": [],
    "non_blocking_findings": ["finding-display-001"],
    "handoff_actions": ["Run controlled display pattern retest."]
  }
}
```

## Implementation reconciliation checklist

Before release, local agent must compare this schema against:

- backend report generation model;
- OpenAPI request/response schemas;
- synthetic FA examples;
- report verification endpoint;
- existing pytest assertions;
- mobile client evidence DTOs, if present.

Any mismatch must be reported as either intentional boundary, missing implementation, or stale documentation.
