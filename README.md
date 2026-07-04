# Device Inspector Demo

A privacy-preserving hardware diagnostic and failure-analysis workbench demo for engineering teams.

This repository is a **public-safe demo baseline** derived from the same product idea as the private Device Inspector project: trustworthy device inspection, evidence collection, and verifiable reports. It shows how a hardware diagnostics tool can structure synthetic device evidence, manage a case lifecycle, run AI-assisted triage, and generate tamper-evident reports without exposing real device identifiers or proprietary data.

## Target use case

Internal engineering teams often need a lightweight workbench to:

- track hardware defect cases across lifecycle states;
- collect structured engineering evidence from synthetic client tools;
- connect client-side inspection flows with a Python backend;
- triage likely failure modes with an AI-assisted workflow;
- generate signed reports that can be verified later;
- keep sensitive identifiers, logs, and user data out of public artifacts.

This demo maps that workflow into a Flask application with SQLite persistence, signed reports, synthetic evidence examples, mobile-client skeletons, and CI checks.

Recent product-facing ideas carried into the public demo are intentionally kept
at the abstraction level: signed evidence as the trust layer, fail-closed
entitlement boundaries, platform-safe evidence collection, and public
model-identifier fields with provenance instead of real serial records.

## What this demo proves

| Capability | Demo evidence |
|---|---|
| Product-origin traceability | [`docs/origin_bridge.md`](docs/origin_bridge.md) maps the original device-inspection idea to this public-safe engineering demo |
| Hardware diagnostics workflow | Case lifecycle, structured evidence schema, FA examples |
| Inspection capability discipline | [`docs/DEVICE_INSPECTION_MATRIX.md`](docs/DEVICE_INSPECTION_MATRIX.md) defines data source, automation level, confidence, invalidators, and report output for each diagnostic domain |
| Validation discipline | [`docs/VALIDATION_LOG.md`](docs/VALIDATION_LOG.md) separates verified, partially verified, synthetic-only, blocked, and not-yet-verified claims |
| Known limitations | [`docs/KNOWN_LIMITATIONS.md`](docs/KNOWN_LIMITATIONS.md) prevents overclaiming on battery health, repair history, water damage, display quality, sensors, and AI triage |
| Report contract | [`docs/REPORT_SCHEMA.md`](docs/REPORT_SCHEMA.md) defines the minimum evidence/finding/disposition/signature schema for trustworthy reports |
| Python backend | Flask API, SQLite-backed repository layer, pytest coverage |
| Security model | Protected write endpoints, RSA report signing, report tamper detection tests, no real secrets |
| AI-assisted triage | Deterministic triage agent with evidence, confidence, invalidators, next tests |
| Failure-analysis process | Evidence intake, triage, verification, audit trail, corrective-action handoff docs |
| Mobile integration architecture | SwiftUI/Combine/CoreData iOS skeleton and Kotlin MVVM Android skeleton |
| Evaluation discipline | Synthetic visual triage manifest, baseline classifier, deterministic evaluation script |
| Engineering quality | GitHub Actions CI, schema checks, mobile skeleton checks, public-safety scan |

## Inspection-system boundary

A device-inspection product must not claim more than its evidence can support. This demo therefore classifies each diagnostic signal by:

- data source: public API, guided user check, manual checklist, synthetic fixture, external fixture, or derived signal;
- automation level: automatic, guided, manual, or external fixture;
- evidence strength: high, medium, low, or not supported;
- invalidators: conditions that could make a finding wrong;
- next test: the smallest retest that would increase confidence.

The public demo can demonstrate the workflow, schema, synthetic examples, and signed reports. It must not include real serials, real defect photos, owner data, production logs, private model weights, vendor diagnostics, or proprietary hardware procedures.

## Non-goals

This repository intentionally does **not** include:

- real device identifiers or device-owner data;
- calls to third-party device-check APIs;
- proprietary hardware logs or internal company process material;
- production Apple, Android, object-storage, or cloud credentials;
- real defect images or production model weights.

The AI module is a safe, deterministic stub that demonstrates system boundaries and data contracts. It can later be replaced by a real CV/VLM pipeline after data-governance approval.

## Architecture

```text
Private device-inspection product idea
  -> public-safe engineering abstraction
  -> synthetic client / tester
  -> Flask API
  -> SQLite repository
  -> case lifecycle and audit trail
  -> diagnostic evidence schema
  -> inspection capability matrix
  -> validation evidence ledger
  -> AI triage agent stub
  -> RSA-signed diagnostic report
  -> verification endpoint / black-box test
```

Key documents:

- [`docs/origin_bridge.md`](docs/origin_bridge.md)
- [`docs/demo_from_product_principles.md`](docs/demo_from_product_principles.md)
- [`docs/architecture.md`](docs/architecture.md)
- [`docs/security_model.md`](docs/security_model.md)
- [`docs/threat_model.md`](docs/threat_model.md)
- [`docs/failure_analysis_workflow.md`](docs/failure_analysis_workflow.md)
- [`docs/hardware_evidence_schema.md`](docs/hardware_evidence_schema.md)
- [`docs/DEVICE_INSPECTION_MATRIX.md`](docs/DEVICE_INSPECTION_MATRIX.md)
- [`docs/VALIDATION_LOG.md`](docs/VALIDATION_LOG.md)
- [`docs/KNOWN_LIMITATIONS.md`](docs/KNOWN_LIMITATIONS.md)
- [`docs/REPORT_SCHEMA.md`](docs/REPORT_SCHEMA.md)
- [`docs/apple_role_alignment.md`](docs/apple_role_alignment.md)
- [`docs/demo_scope.md`](docs/demo_scope.md)

## Quick start

```bash
cd backend/flask_api
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pytest -q
python app.py
```

In another terminal:

```bash
bash ../../scripts/blackbox_api_test.sh
```

## API surface

| Method | Path | Purpose |
|---|---|---|
| `GET` | `/health` | Service health |
| `POST` | `/auth/token` | Demo access credential issuance |
| `POST` | `/devices` | Create synthetic device case |
| `POST` | `/cases` | Create synthetic hardware diagnostic case |
| `GET` | `/cases/{case_id}` | Fetch case and evidence |
| `POST` | `/cases/{case_id}/status` | Update lifecycle state |
| `POST` | `/cases/{case_id}/evidence` | Attach structured hardware evidence |
| `POST` | `/cases/{case_id}/triage` | Generate AI-assisted case triage |
| `GET` | `/cases/{case_id}/audit-events` | Review case audit trail |
| `POST` | `/diagnostic-logs` | Attach legacy synthetic diagnostic evidence |
| `POST` | `/triage` | Generate device-level triage |
| `POST` | `/reports` | Generate RSA-signed diagnostic report |
| `POST` | `/reports/verify` | Verify report signature and tamper status |

## Repository layout

```text
backend/flask_api/      Flask backend, auth, signing, storage, triage, tests
clients/                iOS SwiftUI and Android Kotlin diagnostic client skeletons
examples/fa_cases/      Synthetic failure-analysis case examples
ml/                     Synthetic visual triage evaluation lab
openapi/                API contract
docs/                   Origin bridge, architecture, security, FA workflow, inspection matrix, validation ledger, role alignment
scripts/                Local run, schema, mobile, and public-safety checks
.github/workflows/      CI for backend tests and public-safety checks
```

## Safety posture

Public repositories are evidence, not authority. This demo uses only synthetic records and deterministic logic. Any production use would require privacy review, data-retention policy, real authentication, access control, audit logging, approved storage, and model-risk validation.

## Role-fit summary

This project is intended to demonstrate a practical intersection of:

- consumer-electronics hardware context;
- diagnostic-data engineering;
- Python backend development;
- mobile-client architecture;
- AI-assisted root-cause analysis;
- secure report verification;
- cross-functional engineering communication.
