# Claude project instructions

Read and follow `SKILL.md` for every finance task in this repository.

Treat `data/sample/` as fictional test data only.
Real exports, statements, credentials, tokens, balances, and account identifiers must remain outside the public repository.

Use the connector-neutral interfaces in `src/finance_control/adapters.py`.
Do not hard-code a financial institution in the public core.

Run `python3 scripts/validate_workspace.py` and `python3 -m unittest discover -s tests -v` after changing schemas, adapters, public samples, or audit logic.

Default to read-only analysis.
Require a separate action-time confirmation before every external financial mutation.

