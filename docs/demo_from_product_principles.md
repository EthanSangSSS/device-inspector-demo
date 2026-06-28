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

## Public release checklist

- `docs/origin_bridge.md` exists.
- README links to origin bridge.
- No private repo path or local machine path appears.
- No production endpoint appears.
- Public-safety scan passes.
