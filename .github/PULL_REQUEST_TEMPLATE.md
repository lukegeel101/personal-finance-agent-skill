## What changed

Describe the user-visible outcome.

## Evidence, safety, and privacy

- [ ] No real financial record, account identifier, credential, or secret was added.
- [ ] External financial actions remain approval-gated.
- [ ] New examples use fictional data and preserve evidence statuses.

## Verification

- [ ] `python3 scripts/validate_workspace.py`
- [ ] `python3 scripts/evaluate_sample.py --check`
- [ ] `python3 scripts/demo_audit.py`
- [ ] `python3 -m unittest discover -s tests -v`

List any additional checks and their results.
