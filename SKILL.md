---
name: personal-finance-agent-skill
description: Coordinate privacy-first personal finance audits across generic bank, credit, investment, and file sources while preserving evidence, uncertainty, approvals, and a canonical change log.
---

# Personal Finance Control Center

Use this skill for budgeting, spending analysis, recurring-charge audits, subscription review, debt planning, savings goals, financial-account summaries, and multi-agent finance coordination.

## Default authority

The default mode is read-only analysis.

Do not connect an account, grant a data scope, submit a payment, move money, cancel a subscription, apply for credit, buy or sell an asset, change a contribution, or contact a provider without a separate user request and action-time confirmation for that exact action.

Never request that credentials, one-time codes, security answers, full account numbers, or recovery codes be pasted into the agent context.

## Canonical state rule

Use one Control Center as the source of truth.
Read it and the newest change-log entries before finance work.
Register a bounded active workstream and avoid overlapping another active workstream.

When finished, update both the relevant current-state section and the dated change log.
A change-log-only update is incomplete.

## Evidence statuses

Use these statuses consistently:

- `CONFIRMED`: supported by direct evidence or an uncontradicted explicit user statement.
- `CONNECTED_SNAPSHOT`: observed through a connector at a stated time and subject to change.
- `USER_REPORTED`: supplied by the user but not independently verified.
- `ESTIMATE`: calculated or approximate, with assumptions stated.
- `PLAN`: a target or chosen strategy, not a completed action.
- `PENDING_VERIFICATION`: incomplete, conflicting, stale, or unsupported.

Evidence priority is official contract, statement, merchant confirmation, or account record; explicit user statement; connected classification; then agent calculation or inference.
Preserve conflicting claims and move them to verification instead of deleting one silently.

## Core workflow

1. Read the Control Center, active workstreams, source coverage, and newest changes.
2. Register the smallest non-overlapping workstream.
3. Import data through a read-only generic connector or local export adapter.
4. Record the source window, provider-reported coverage, observation time, requested refreshes, and known gaps.
5. Normalize account references, posted dates, signed amounts, currencies, and merchant descriptors.
6. Deduplicate overlap by account reference, posted date, signed amount, and normalized descriptor.
7. Reconcile statements, exports, and connected data without assuming the connector contains the full requested history.
8. Exclude internal transfers, card payments, refunds, cashback, and cash withdrawals from purchase-spending totals while retaining them for reconciliation.
9. Produce the requested budget, cash-flow, recurring-charge, subscription, fee, debt, goal, asset, liability, investment, or net-worth analysis.
10. Separate observations, estimates, plans, and action proposals.
11. Put external mutations in an approval queue and stop.
12. Update current state and the change log with source, date, old state, new state, and remaining uncertainty.
13. Read back the result, close the workstream, and report actions explicitly not taken.

## Analysis invariants

- A connector timestamp does not prove real-time balances or complete transaction history.
- A requested refresh does not prove that older data became available.
- Expected income, gifts, reimbursements, or receivables are not cash until observed as received.
- A credit-card payment is not purchase spending.
- Transfers between owned accounts do not create income or expense.
- Refunds and cashback should remain reconcilable but must not inflate purchase totals.
- Retirement and taxable assets must remain distinct.
- A proposed cancellation is not complete until merchant confirmation and later billing-stop evidence are available.
- A budget excludes debt principal or savings contributions only when the configuration says so and the report states that convention.

## Output contract

Return:

1. Source coverage and freshness.
2. Confirmed findings.
3. Connected snapshots.
4. User-reported facts and estimates.
5. Budget, recurring-charge, debt, goal, or portfolio findings requested.
6. Conflicts and missing evidence.
7. Recommended next steps.
8. Approval queue for any external action.
9. Actions explicitly not taken.
10. Proposed Control Center and change-log updates.

## Supporting references

- Read [references/control-center-workflow.md](references/control-center-workflow.md) for coordination and write-back details.
- Read [references/data-contract.md](references/data-contract.md) before writing an adapter or changing normalized data.
- Read [references/privacy-security.md](references/privacy-security.md) before handling real financial data or connector scopes.
- Use [examples/prompts.md](examples/prompts.md) for common invocations.
