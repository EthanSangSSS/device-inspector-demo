# Case/Device Report Binding Hardening Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Close F15 on exact `device-inspector-demo@679a2a79891327127e8a76af54c914f058014c1e` so a signed report can never combine one case's evidence with a different caller-selected device.

**Architecture:** Treat `case.device_id` as authoritative whenever `case_id` is supplied. A redundant request `device_id` may be omitted or may exactly match the case; a conflicting value is rejected before device lookup, triage, signing, or persistence. Case-less reports retain their existing explicit `device_id` behavior.

**Tech Stack:** Flask, pytest, existing in-memory `DiagnosticRepository` and `ReportSigner`.

**Spec:** GitHub Portfolio Engineering Review 2026-09-05 finding F15 as independently re-audited against `device-inspector-demo@679a2a79891327127e8a76af54c914f058014c1e`.

## Constraints

- Preserve existing API shape and successful case-bound report behavior.
- Do not silently substitute a caller-provided device when a case is present.
- Reject a case/device mismatch with HTTP 400 before report signing.
- Do not alter auth, signing, persistence schema, synthetic-data policy, CI, dependencies, or GitHub state.

### Task 1: Add RED mismatch regression

**Files:**
- Modify: `backend/flask_api/tests/test_case_report.py`

- [ ] Create two synthetic devices and a case bound to device A.
- [ ] Request a report with that case plus explicit device B.
- [ ] Require HTTP 400 and a stable mismatch error.
- [ ] Run the focused test and verify current code returns 201 (RED).

### Task 2: Bind report device to case

**Files:**
- Modify: `backend/flask_api/app.py`
- Test: `backend/flask_api/tests/test_case_report.py`

- [ ] When a case exists, compare any requested `device_id` with `case["device_id"]`.
- [ ] Reject a mismatch before lookup/triage/signing.
- [ ] Use the case's device ID as the report device ID.
- [ ] Leave case-less report behavior unchanged.

### Task 3: Verify

- [ ] Run focused case-report tests.
- [ ] Run all `backend/flask_api/tests`.
- [ ] Run `python -m compileall -q backend/flask_api`.
- [ ] Run `git diff --check`.
- [ ] Re-fetch `origin/main` and require exact `679a2a79891327127e8a76af54c914f058014c1e`.
- [ ] Do not commit, push, create/update PRs, or change CI.
