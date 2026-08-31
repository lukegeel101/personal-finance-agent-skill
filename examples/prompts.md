# Example prompts

## Spending and budget audit

```text
Use $personal-finance-agent-skill to analyze my private normalized transactions for the last three complete months.
Deduplicate overlapping sources, exclude transfers and card payments from spending, and compare categories with my saved budget.
Show source coverage and uncertainty.
```

## Subscription audit

```text
Use $personal-finance-agent-skill to identify active, recurring-like, irregular, and inactive merchant charges.
Do not infer a product from an ambiguous descriptor.
Create an approval queue for possible cancellations, but do not cancel anything.
```

## Debt plan

```text
Use $personal-finance-agent-skill to compare payoff options using my verified balance, rate, minimum payment, cash floor, and monthly surplus.
Keep projected income separate from current cash.
Do not submit a payment or application.
```

## Investment-account review

```text
Use $personal-finance-agent-skill to summarize my private connector-normalized holdings.
Separate taxable and retirement accounts, then review allocation, concentration, fees, expense ratios, and cash drag.
Do not trade or change contributions.
```

## Control Center handoff

```text
Use $personal-finance-agent-skill to reconcile these new findings with the canonical state.
Preserve conflicting claims, update the relevant current section and change log, close only this task's workstream, and list actions not taken.
```
