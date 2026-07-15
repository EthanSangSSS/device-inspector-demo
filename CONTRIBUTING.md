# Contributing

Thank you for improving `device-inspector-demo`.

This repository is a public-safe demo for hardware diagnostics workflow design. Contributions should preserve the synthetic-data boundary and improve reviewability, reproducibility, validation, or documentation.

## Contribution priorities

High-value contributions include:

1. clearer synthetic evidence examples;
2. stronger validation for report signing, schema checks, API behavior, and public-safety boundaries;
3. documentation that separates verified behavior from synthetic-only demonstration;
4. safer demo setup and local run instructions;
5. architecture, privacy, or security boundary clarifications.

## Required boundaries

Do not include:

- real device identifiers, owner data, serials, production logs, defect photos, or vendor diagnostics;
- credentials, private keys, certificates, API tokens, cloud keys, or provisioning profiles;
- proprietary repair procedures, employer/customer data, or private model weights;
- claims that the demo can certify device condition, repair history, water damage, or authenticity without evidence.

## Pull request process

1. Keep the scope narrow.
2. Identify changed surfaces: backend, clients, docs, examples, schemas, scripts, or CI.
3. State whether data is synthetic.
4. Run available validation and paste exact outputs.
5. Report limitations instead of overclaiming.

## Suggested validation

```bash
cd backend/flask_api
pytest -q
cd ../..
bash scripts/blackbox_api_test.sh
python3 scripts/check_public_safety.py
```

If a command is unavailable in the current environment, state that instead of claiming success.
