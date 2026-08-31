# Security policy

## Never commit real financial data

The public repository must not contain:

- Real account names, institution names tied to a person, account numbers, routing numbers, or card numbers.
- Real balances, transactions, holdings, statements, tax documents, pay records, or credit reports.
- Usernames, passwords, API keys, cookies, connector tokens, refresh tokens, security answers, or one-time codes.
- Real addresses, phone numbers, email addresses, employer records, or identity-verification artifacts.

## Connector rules

Prefer read-only scopes.
Store tokens in a platform secret store, never in configuration or agent memory.
Record the scope granted, connection time, provider coverage, and revocation path without recording the token.
Treat a successful connection as permission to read only the granted scope, not permission to mutate an account.

## Retention

Keep raw exports and statements private and retain them only as long as required.
Store derived reports separately from raw source material when that reduces exposure.
Delete temporary decrypted files through the platform's approved recoverable process when the user authorizes cleanup.

## Reporting a problem

Use a private security channel to contact the maintainer.
Do not paste real financial data or credentials into a public issue.

