# Personal Finance Control Center Skill

A connector-neutral, privacy-first agent workflow for personal finance audits, budgeting, subscription review, debt planning, savings goals, and investment-account summaries.

The repository implements a canonical Control Center pattern so multiple agent sessions can share facts without silently overwriting one another.
It defaults to read-only analysis and requires separate action-time approval for every external financial action.

## What it does

- Imports normalized data through generic bank, credit, investment, or file adapters.
- Preserves source, observation time, evidence status, and uncertainty for material facts.
- Deduplicates overlapping statements, exports, and connector records.
- Separates spending from internal transfers, card payments, refunds, and cashback.
- Builds budget variance, cash-flow, recurring-charge, subscription, fee, debt, goal, and net-worth views.
- Maintains an active-workstream registry and dated change log for multi-agent coordination.
- Produces an approval queue for cancellations, transfers, payments, applications, account links, or sales.
- Never treats a connection timestamp as proof of real-time data freshness.

## Repository layout

```text
.
|-- SKILL.md                         Agent instructions
|-- CLAUDE.md                        Claude-style entrypoint
|-- agents/openai.yaml               ChatGPT/Codex UI metadata
|-- config/finance.example.json      Safe connector-neutral example
|-- data/sample/                     Fictional accounts and transactions
|-- schemas/control-center.schema.json
|-- src/finance_control/             Adapter contract and audit helpers
|-- scripts/validate_workspace.py    Validation and public-data safety checks
|-- scripts/demo_audit.py            Mock-data audit demonstration
|-- references/                      Evidence, workflow, and privacy guidance
|-- docs/architecture.md             Workflow diagram
|-- tests/                            Regression tests
`-- linkedin-post.md                 Launch-post draft
```

## Quick start

1. Keep the public examples unchanged and create private copies of the configuration and state files.
2. Map a supported export into the generic transaction columns described in [references/data-contract.md](references/data-contract.md).
3. Run the validation and mock audit.

```bash
python3 scripts/validate_workspace.py
python3 scripts/demo_audit.py
python3 -m unittest discover -s tests -v
```

4. In a ChatGPT-style skill environment, install or reference the repository and invoke `$personal-finance-agent-skill`.
5. In a Claude-style project, keep `CLAUDE.md` at the repository root and ask Claude to follow `SKILL.md`.

Example request:

```text
Use $personal-finance-agent-skill to audit my private normalized transaction export.
Identify recurring charges, budget variance, fees, and open verification questions.
Do not cancel anything, move money, or connect another account.
```

## Connector design

`src/finance_control/adapters.py` defines a provider-neutral `FinancialConnector` protocol.
Provider-specific authentication and API behavior belong in private adapters or separate integration packages.
The public repository does not name or hard-code a financial institution.

The included CSV adapter is read-only and operates on fictional mock data.

## Canonical Control Center

Every finance task should:

1. Read the current Control Center and newest change-log entries.
2. Register a bounded, non-overlapping workstream.
3. Preserve confirmed facts and label estimates or conflicts.
4. Update both the relevant current-state section and the change log.
5. Close its workstream after readback verification.

See [references/control-center-workflow.md](references/control-center-workflow.md) for the full procedure.

## Security model

Never commit real account data, transactions, balances, statements, credentials, access tokens, account identifiers, or tax documents.
Keep real financial data in an encrypted private location with the smallest practical retention period.
Use read-only connector scopes where available.

See [SECURITY.md](SECURITY.md) and [references/privacy-security.md](references/privacy-security.md).

## Important limitation

This project helps organize evidence and decisions.
It is not financial, tax, legal, or investment advice, and it does not guarantee that imported data is complete or current.

## License

MIT.
