# Security Policy

`device-inspector-demo` is a public-safe hardware diagnostics workflow demo. It must not contain real device identifiers, owner data, production logs, proprietary diagnostics, private model weights, or credentials.

## Supported scope

Security reports are in scope when they involve:

- real device identifiers, owner data, serial-like records, production logs, or proprietary hardware data appearing in the public repository;
- secrets, credentials, private keys, certificates, API tokens, or cloud keys;
- report-signing or verification logic that could misrepresent tamper status;
- demo authentication or authorization flaws that affect the public demo boundary;
- documentation that overclaims diagnostic certainty beyond synthetic evidence.

## Out of scope

- Requests for private Device Inspector source, private datasets, private model weights, or production credentials.
- Reports requiring access to real devices, third-party device-check services, vendor tools, or systems not owned by the maintainer.
- Findings that depend on private downstream deployments not present in this public demo.

## Reporting

Open a GitHub issue if no sensitive data is included. If sensitive material is involved, do not paste it into the issue. Open a minimal report with:

- affected path;
- risk category;
- safe reproduction outline;
- whether private data or credentials may be involved.

## Maintainer handling SOP

1. Confirm the affected path and risk category.
2. Reproduce with synthetic data only.
3. Remove or rewrite unsafe content.
4. Add or update validation checks where feasible.
5. Document the fix without exposing sensitive details.

## Boundary

This repository demonstrates workflow design and public-safe architecture only. It is not a production diagnostic service and must not be used to process real device-owner data without privacy, security, retention, and model-risk review.
