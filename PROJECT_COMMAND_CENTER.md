# Project Command Center

Repo: `EthanSangSSS/device-inspector-demo`

Role: public-safe hardware diagnostics and failure-analysis demo.

## Hard rules

- Do not add real IMEI, serial number, UDID, MAC address, user identity, location, or proprietary hardware log data.
- Do not call third-party device-check services from default demo paths.
- Do not add production credentials, signing material, cloud buckets, access keys, certificates, provisioning profiles, or private endpoints.
- Prefer synthetic data, deterministic stubs, and explicit interfaces over opaque model calls.
- Every public-facing feature must explain data source, trust level, privacy boundary, and verification path.

## Review checklist

### P0

- Real device identifier or credential appears in source, docs, tests, fixtures, CI, or commit text.
- Public demo performs network transmission of device/user data without explicit mock mode.
- Report signature verification can be bypassed by payload mutation.
- CI cannot run backend tests.

### P1

- AI triage output lacks evidence, confidence, invalidators, or next-test recommendation.
- Diagnostic data model is ambiguous about whether evidence is synthetic.
- Docs imply production readiness without security, privacy, or model-risk review.

### P2

- README lacks role-fit narrative.
- Error states are unclear.
- Tests cover only happy paths.

## Release gate before making public

- `pytest -q` passes in CI.
- Public-safety scan passes.
- README and docs state synthetic-data boundary.
- No real identifiers or credentials are present.
- Repo remains demo-scoped and does not claim production deployment.
