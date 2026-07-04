# Demo-from-Product Principles

## Why this exists

The public demo should not feel like an unrelated toy project. It should visibly grow out of the original Device Inspector product idea while staying safe enough to publish.

## Principles

1. **Product origin, engineering abstraction**
   - Preserve the original product problem: trustworthy device inspection and report verification.
   - Express it as a hardware diagnostic workbench for engineering review.

2. **Synthetic by default**
   - Every example starts with `SYNTH-`.
   - No public artifact should require a real device, user, endpoint, or credential.

3. **Trust through verification**
   - Reports are not just generated; they are signed and verified.
   - Audit events explain how a case changed over time.

4. **AI as triage, not authority**
   - AI output proposes hypotheses, invalidators, and next tests.
   - Human review remains required before root-cause acceptance.

5. **Mobile architecture without private app leakage**
   - iOS and Android folders demonstrate client architecture.
   - They do not copy private app implementation or assets.

6. **Interview-safe traceability**
   - The repo can explain how a personal product idea evolved into an engineering demo.
   - It should never imply access to proprietary hardware programs or private datasets.

## Public ideas carried forward

These ideas are safe to expose because they describe product and architecture
principles, not private implementation details:

1. **Low-friction trust upgrade**
   - The product value is not just raw diagnostics; it is a trusted decision aid
     for second-hand device review.
   - Public demo equivalent: a clear free workflow plus a visible trust layer
     for signed reports and richer evidence review.

2. **Signed evidence is the differentiator**
   - Inspection results should be tamper-evident and verifiable after sharing.
   - Public demo equivalent: RSA-signed synthetic diagnostic reports with a
     verification endpoint and tamper-detection tests.

3. **Fail closed on monetization and trust**
   - Purchase or entitlement checks must never grant access from local-only
     claims or weak token-shape checks.
   - Public demo equivalent: protected write endpoints, explicit auth stubs,
     and docs that separate demo credentials from production identity.

4. **Platform-safe evidence collection**
   - Mobile clients should respect platform review boundaries and degrade to
     guided/manual or desktop-assisted flows when direct collection is risky.
   - Public demo equivalent: client skeletons collect synthetic evidence and
     document mobile architecture without private platform probes.

5. **Public model identifiers beat brittle serial guessing**
   - Device identification should prefer public model numbers and transparent
     confidence labels over opaque prefix heuristics.
   - Public demo equivalent: hardware evidence schemas can include public model
     identifiers, provenance, and confidence instead of real serial numbers.

## Public release checklist

- `docs/origin_bridge.md` exists.
- README links to origin bridge.
- No private repo path or local machine path appears.
- No production endpoint appears.
- Public-safety scan passes.
