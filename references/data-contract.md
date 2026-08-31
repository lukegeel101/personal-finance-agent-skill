# Data contract

## Account

| Field | Type | Meaning |
| --- | --- | --- |
| `account_ref` | string | Stable opaque reference that is not a real account number |
| `kind` | string | `checking`, `savings`, `credit`, `investment`, `loan`, or `other` |
| `currency` | string | ISO 4217 currency code |
| `display_name` | string | Non-sensitive label |
| `source_ref` | string | Connector or import source reference |

## Transaction

| Field | Type | Meaning |
| --- | --- | --- |
| `transaction_ref` | string | Stable source or derived identifier |
| `account_ref` | string | Opaque account reference |
| `posted_at` | string | ISO 8601 date or timestamp |
| `amount` | number | Signed amount, with inflows positive and outflows negative |
| `currency` | string | ISO 4217 currency code |
| `description` | string | Source descriptor |
| `category` | string | Normalized category |
| `source_ref` | string | Provenance reference |
| `evidence_status` | string | Control Center evidence status |

The public CSV adapter expects these columns in this order:

```text
transaction_ref,account_ref,posted_at,amount,currency,description,category,source_ref,evidence_status
```

## Balance

A balance record contains account reference, current or available amount, currency, observed time, source reference, and freshness note.
Do not infer real-time freshness from the connector session alone.

## Holding

A holding record contains account reference, asset reference, description, quantity, market value, currency, observed time, and tax treatment when verified.
Do not include full brokerage account numbers or credentials.

## Sync batch

A sync batch should record:

- Source reference.
- Requested start and end.
- Actual oldest and newest records returned.
- Observation time.
- Accounts, transactions, balances, and holdings returned.
- Coverage notes and warnings.

## Control Center fact

Every material fact should contain:

| Field | Meaning |
| --- | --- |
| `id` | Stable fact identifier |
| `domain` | Budget, debt, subscription, goal, asset, or another domain |
| `statement` | Human-readable current state |
| `status` | Evidence status |
| `observed_at` | Evidence or statement time |
| `source_ref` | Non-secret provenance reference |
| `assumptions` | Assumptions for an estimate or plan |
| `remaining_uncertainty` | What still needs proof |

## Change log

Every change should identify date, task, source, old state, new state, and remaining uncertainty.
The log is append-only.

