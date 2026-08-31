# Privacy and security reference

## Data minimization

Import only the fields and date range needed for the requested analysis.
Use opaque local account references instead of real account numbers.
Keep raw statements and exports outside the public repository.

## Authentication

The user should complete passwords, multi-factor authentication, passkeys, and one-time codes directly in the provider interface.
The agent should not view, store, repeat, or log them.

## Connector scope

Prefer read-only balances, transactions, and holdings scopes.
Explain the requested scope before the user grants it.
Record the scope and revocation path without storing a token.

A connected data source authorizes only the granted reads.
It does not authorize payments, transfers, applications, trades, cancellations, or account changes.

## Sensitive output

Keep reports at the lowest useful level of detail.
Avoid repeating account identifiers or transaction descriptions when category-level summaries answer the question.
Use ranges or rounded values only when the loss of precision does not undermine the requested analysis.

## External actions

Require action-time confirmation for each external mutation.
After an action, record direct confirmation, effective date, reversibility, and any later verification needed.

For a subscription cancellation, merchant confirmation proves the request or account state.
A later statement check proves whether billing actually stopped.

## Financial guidance

State important assumptions, uncertainty, and time-sensitive terms.
Encourage qualified professional review for material tax, legal, insurance, credit, or investment decisions.

