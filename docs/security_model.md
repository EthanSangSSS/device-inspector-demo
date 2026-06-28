# Security Model

## Scope

This repository is a public-safe demo. It is not a production incident-response, warranty, manufacturing, or customer-device system.

## Data classification

| Class | Allowed in this repo | Examples |
|---|---|---|
| Synthetic public demo data | Yes | `SYNTH-DEVICE-001`, mock thermal logs |
| Real user/device identifiers | No | IMEI, serial number, UDID, MAC address |
| Proprietary hardware logs | No | internal fixture logs, factory logs, unreleased design records |
| Secrets and credentials | No | API keys, JWT signing secrets, RSA private keys, cloud credentials |

## Identifier guard

The backend rejects non-synthetic identifiers for device, log, and report IDs. This is not a complete privacy system, but it reduces the chance of accidentally committing realistic identifiers into the demo flow.

## Authentication

The demo uses JWT bearer tokens to protect state-changing diagnostic endpoints. Production would require centralized identity, role-based access control, token revocation, audit events, and least-privilege service accounts.

## Report integrity

Reports are signed with RSA-PSS/SHA-256 over canonical JSON. Verification is expected to fail if any report field is changed after signing.

Covered by tests:

- valid report verifies successfully;
- modified report payload fails verification;
- protected endpoints require bearer token;
- non-synthetic identifiers are rejected.

## AI safety boundary

The triage agent is deterministic and local. It does not call external model APIs and does not transmit diagnostic evidence.

Future CV/VLM integration must add:

- approved dataset governance;
- model card and known-failure documentation;
- confidence calibration;
- false-positive and false-negative analysis;
- human review before any corrective action is accepted.

## Public release checklist

Before changing repository visibility to public:

1. Run `pytest -q`.
2. Run public-safety scans.
3. Confirm there are no real identifiers or credentials.
4. Confirm docs clearly state synthetic-data scope.
5. Confirm README does not claim production deployment.
