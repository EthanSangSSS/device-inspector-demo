# Validation Log

This ledger records what has actually been verified, what remains synthetic, and what must be retested before any claim becomes product-grade.

## Validation status legend

| Status | Meaning |
|---|---|
| `verified` | Reproduced with a deterministic command, test, fixture, or documented manual run. |
| `partially_verified` | Workflow is implemented, but validation coverage is incomplete or synthetic-only. |
| `synthetic_only` | Demonstrated with generated examples only. No real device evidence is present. |
| `not_verified` | Planned but not yet exercised. |
| `blocked` | Cannot be validated without platform access, private data, hardware fixture, or local build. |

## Current public-demo validation baseline

| Area | Status | Evidence | Limitation | Next validation step |
|---|---|---|---|---|
| Backend API boot and test suite | partially_verified | Repository README documents `pytest -q` and black-box API test commands. | Connector-side edit cannot run local commands. | Local agent must run backend tests from a clean checkout. |
| Case lifecycle model | synthetic_only | Public demo describes case lifecycle, audit trail, and synthetic evidence examples. | No production case data is included or expected. | Confirm fixtures cover create, status update, evidence attach, triage, report generation, and verify. |
| Report signing and verification | synthetic_only | README states RSA report signing and tamper detection tests. | Integrity proves report immutability, not truth of upstream evidence. | Local agent should inspect tests and verify tamper-negative and tamper-positive cases. |
| AI triage agent | synthetic_only | Deterministic triage stub is documented as a safe boundary. | Not a real CV/VLM model and must not be marketed as autonomous diagnosis. | Confirm triage output contains fact, confidence, invalidators, and next tests. |
| Mobile client skeletons | partially_verified | README lists SwiftUI/Combine/CoreData and Kotlin MVVM skeletons. | Skeletons do not prove App Store / Play production readiness. | Local agent should run mobile skeleton checks and identify missing simulator/device validation. |
| Screen inspection model | not_verified | Added `DEVICE_INSPECTION_MATRIX.md`. | Matrix is a product-grade target model, not implementation proof. | Add guided test-pattern flow or synthetic fixture for at least one display check. |
| Report schema | not_verified | Added `REPORT_SCHEMA.md`. | Schema must be reconciled with existing API/report implementation. | Local agent should compare schema fields with current backend models and OpenAPI. |
| Public-safety posture | partially_verified | README states no real identifiers, logs, credentials, or production data. | Must be enforced by automated scan, not only policy text. | Run existing public-safety scan and secret scan locally. |

## Required local verification commands

Run from repository root unless a script says otherwise.

Terminal A - backend tests and local API server:

```bash
python3 -m compileall backend || true
cd backend/flask_api
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
PYTHONPATH=. pytest -q
python app.py
```

Terminal B - black-box and repository checks:

```bash
bash scripts/blackbox_api_test.sh
python3 scripts/public_safety_scan.py
python3 scripts/mobile_skeleton_check.py
git diff --check origin/main...HEAD
```

If a script name has changed or does not exist, the local agent must report the exact missing path and list the available scripts rather than inventing a replacement result.

## Validation entry template

Append one entry per meaningful validation run.

```markdown
### YYYY-MM-DD - <short run name>

- Branch:
- HEAD:
- Runner:
- Scope:
- Commands:
- Result: pass / fail / partial / blocked
- Evidence artifacts:
- Product claim affected:
- Risk changed:
- Follow-up:
```

## Claim upgrade rules

A capability may be called `implemented` only when all conditions are met:

1. The code path exists.
2. A deterministic local or CI command exercises it.
3. The output is captured in test logs or generated artifacts.
4. Limitations and invalidators are documented.
5. The report schema can represent both pass and fail outcomes.

A capability may be called `validated` only when it has been exercised on the intended platform or fixture, not merely simulated in a backend test.

## Known validation gaps

- No real device identifiers or real defect data should be added to this public repository.
- Display uniformity, HDR, refresh-rate behavior, and camera/audio defects require guided user tests or lab fixtures.
- Battery health, repair history, water damage, and board-level defects are not reliably available to third-party apps through public mobile APIs.
- AI triage must remain evidence-grounded and must never override raw telemetry or missing-data states.
