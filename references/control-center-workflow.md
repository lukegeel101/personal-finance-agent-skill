# Control Center workflow

## Recommended sections

A canonical Control Center should contain:

1. Read-first and write-back rules.
2. Document or state version.
3. Active workstreams.
4. Source coverage and connector status.
5. Balances and freshness.
6. Income and payroll evidence.
7. Budget and cash flow.
8. Debt and payoff plans.
9. Savings goals and reserves.
10. Recurring transactions and subscriptions.
11. Assets, liabilities, receivables, and net worth.
12. Investment and retirement accounts.
13. Insurance, benefits, and fixed obligations.
14. Open questions and verification needs.
15. Evidence conventions.
16. Dated change log.

Not every installation needs every section.
Preserve the evidence and coordination rules even when the domain is narrower.

## Start a workstream

Read the Control Center and newest change-log entries.
Check whether another active workstream already covers the requested scope.

Register:

```text
IN_PROGRESS | scope | agent or task | start time | intended write-back
```

Choose the smallest scope that can produce a useful result.
Do not remove another task's active entry.

## Ingest source evidence

For every source, record:

- Source type and stable non-secret reference.
- Requested date window.
- Oldest and newest records actually returned.
- Provider-reported completeness when available.
- Observation and refresh-request times.
- Read-only scope.
- Gaps, pagination limits, and unresolved errors.

The phrase `full history` must mean the full history actually available from the source, not the full requested calendar window.
A refresh request is an action record, not proof of new data.

## Reconcile transactions

Normalize account reference, posted date, signed amount, currency, and merchant descriptor.
Build a deduplication key from account reference, posted date, signed amount, and normalized descriptor.

Keep the highest-quality source record as the canonical analysis record while retaining the source links for reconciliation.
Do not merge distinct transactions only because date and amount happen to match.

Identify replacement-card continuity before treating several card identifiers as separate liabilities.

Exclude these from purchase-spending totals while retaining them for reconciliation:

- Transfers between owned accounts.
- Credit-card payments.
- Refunds and reversals.
- Cashback or reward redemptions.
- Cash withdrawals unless the requested report explicitly treats them as spending.

## Run analyses

### Budget and cash flow

State whether debt principal, transfers, taxes, savings contributions, and investment contributions are inside or outside the budget.
Compare actual categorized spending with configured caps.
Separate unusual periods from the forward baseline when the evidence supports that distinction.

### Recurring charges and subscriptions

Use descriptor grouping, cadence, amount stability, and source coverage to identify candidates.
Distinguish active, recurring-like, irregular, inactive, and pending-verification states.
Do not infer a specific subscription product from an ambiguous payment descriptor.

### Debt

Record balance date, rate evidence, minimum payment, due date, fees, payoff target, and liquidity guardrails.
Treat promotional terms and balance-transfer fees as time-sensitive evidence.
Do not optimize rewards while ignoring interest cost.

### Goals and receivables

Keep expected inflows separate from available cash.
When a receivable is observed as cash, close the receivable and add the cash once so the asset is not double-counted.

### Investments

Keep taxable, retirement, and cash accounts distinct.
Review allocation, concentration, fees, expense ratios, cash drag, tax treatment, and contribution settings only from verified source data.
Do not recommend liquidating retirement assets for a short-term need without a separate suitability and tax analysis.

## Propose actions

Recommendations may include canceling a subscription, paying debt, moving cash, changing a contribution, connecting an account, applying for credit, or selling an asset.
Each external mutation belongs in an approval queue.

The approval item should state:

- Exact provider and action.
- Amount or scope.
- Reason and expected effect.
- Reversibility.
- Key risks and alternatives.
- Evidence cutoff.
- Confirmation required.

## Write back and close

Update the relevant current-state section first.
Then append a change-log record with date, source, task, old state, new state, and remaining uncertainty.

Read back the state and confirm that no confirmed fact was silently replaced.
Remove only the current workstream entry.
Report every material action explicitly not taken.

