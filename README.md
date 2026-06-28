# Device Inspector Demo

A privacy-preserving hardware diagnostic and failure-analysis demo for engineering teams.

This repository is a **public-safe demo baseline**. It is designed to show how a hardware diagnostics tool could collect synthetic device telemetry, structure diagnostic logs, run AI-assisted triage, and generate tamper-evident reports without exposing real device identifiers or proprietary data.

## Target use case

Internal engineering teams often need a lightweight tool to:

- track hardware defects and diagnostic evidence;
- collect structured logs from mobile or desktop clients;
- connect client-side inspection flows with a Python backend;
- triage likely failure modes with an AI-assisted workflow;
- generate signed reports that can be verified later;
- keep sensitive identifiers, logs, and user data out of public artifacts.

This demo maps that workflow into a small Flask application with synthetic data, test coverage, and security-first documentation.

## What this demo proves

| Capability | Demo evidence |
|---|---|
| Hardware diagnostics workflow | Synthetic device records, diagnostic logs, defect cases, report generation |
| Python backend | Flask API, SQLite-backed repository layer, pytest coverage |
| Security model | JWT auth, RSA report signing, report tamper detection tests, no real secrets |
| AI-assisted triage | Deterministic triage agent stub with evidence, confidence, invalidators, next tests |
| Failure-analysis process | Structured workflow docs for evidence intake, triage, verification, corrective-action handoff |
| Engineering quality | GitHub Actions CI, black-box API smoke script, test-first public-safe baseline |

## Non-goals

This repository intentionally does **not** include:

- real IMEI, serial number, UDID, MAC address, or device-owner data;
- calls to third-party device-check APIs;
- proprietary hardware logs or internal company process material;
- production Apple, Android, OSS, or cloud credentials;
- a trained CV/VLM model with real defect images.

The AI module is a safe, deterministic stub that demonstrates system boundaries and data contracts. It can later be replaced by a real CV/VLM pipeline after data-governance approval.

## Architecture

```text
Synthetic client / tester
  -> Flask API
  -> SQLite repository
  -> diagnostic log normalizer
  -> AI triage agent stub
  -> RSA-signed diagnostic report
  -> verification endpoint / black-box test
```

Key documents:

- [`docs/architecture.md`](docs/architecture.md)
- [`docs/security_model.md`](docs/security_model.md)
- [`docs/failure_analysis_workflow.md`](docs/failure_analysis_workflow.md)
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
| `POST` | `/auth/token` | Demo JWT issuance |
| `POST` | `/devices` | Create synthetic device case |
| `POST` | `/diagnostic-logs` | Attach structured diagnostic evidence |
| `POST` | `/triage` | Generate AI-assisted failure triage |
| `POST` | `/reports` | Generate RSA-signed diagnostic report |
| `POST` | `/reports/verify` | Verify report signature and tamper status |

## Repository layout

```text
backend/flask_api/      Flask backend, auth, signing, storage, triage, tests
ai/                     AI triage contract and CV/VLM stub
docs/                   Architecture, security model, failure-analysis workflow
scripts/                Local run and black-box verification helpers
.github/workflows/      CI for backend tests and public-safety checks
```

## Safety posture

Public repositories are evidence, not authority. This demo uses only synthetic records and deterministic logic. Any production use would require privacy review, data-retention policy, real authentication, access control, audit logging, approved storage, and model-risk validation.

## Role-fit summary

This project is intended to demonstrate a practical intersection of:

- consumer-electronics hardware context;
- diagnostic-data engineering;
- Python backend development;
- AI-assisted root-cause analysis;
- secure report verification;
- cross-functional engineering communication.
