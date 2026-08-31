# Contributing

Thanks for helping make personal-finance agents safer, more transparent, and easier to audit.

## Good contributions

- Improve connector-neutral normalization and reconciliation.
- Add fictional cases for duplicates, transfers, refunds, recurring charges, and incomplete coverage.
- Clarify evidence status, uncertainty, privacy boundaries, and approval gates.
- Improve compatibility with ChatGPT-style and Claude-style skill environments.

Never include real balances, transactions, account identifiers, statements, tax information, credentials, or access tokens.

## Development workflow

1. Create a focused branch from `main`.
2. Make the smallest coherent change.
3. Add or update tests using fictional data.
4. Run the complete local verification suite.

```bash
python3 scripts/validate_workspace.py
python3 scripts/evaluate_sample.py --check
python3 scripts/demo_audit.py
python3 -m unittest discover -s tests -v
```

5. Open a pull request using the repository template.

## Pull-request expectations

- Explain the user outcome, evidence implications, safety implications, and verification performed.
- Keep all public examples fictional.
- Preserve the rule that payments, transfers, cancellations, applications, trades, and account changes require explicit authorization.
- Update `docs/gotchas.md` when a verified issue and fix would help future contributors.

By participating, you agree to follow [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).
