# Reproducible sample evaluation

The evaluation uses only the repository's fictional accounts and transaction history.

It imports a normalized CSV, deduplicates evidence, excludes transfers and other non-purchase categories, totals clean spending, detects recurring candidates, measures source coverage, and takes no external action.

Run it with:

```bash
python3 scripts/evaluate_sample.py --check
```

## Committed result

| Metric | Result |
| --- | ---: |
| Raw fictional transactions | 16 |
| Transactions after deterministic deduplication | 16 |
| Clean purchase-spending records | 9 |
| Clean purchase spending | $4,510.72 |
| Recurring candidates | 3 |
| Requested source coverage | 92 days |
| Actual source coverage | 76 days, or 82.61% |
| Payments, transfers, cancellations, trades, or applications submitted | 0 |

The goal is reproducibility, not financial advice or a claim about a real person.

Change the fictional fixture, run the evaluation, and update the committed expected result only when the behavior change is intentional and reviewed.
