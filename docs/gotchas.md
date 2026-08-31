# Gotchas

## Requested history and returned history are different

Issue: a connector can accept a multi-year request while returning a shorter provider window.

Verified fix: record both the requested window and the actual oldest and newest records returned.

## Connection time is not data freshness

Issue: a newly opened connector session can expose stale balances or transactions.

Verified fix: attach an observation time and freshness note to each snapshot and avoid real-time claims without provider evidence.

## Overlapping sources double-count spending

Issue: statements, exports, and connector feeds can contain the same transaction.

Verified fix: normalize and deduplicate by account reference, date, signed amount, and merchant descriptor while retaining provenance.

## Payments and transfers inflate spending or income

Issue: a card payment may appear as an outflow in one account and an inflow in another.

Verified fix: exclude owned-account transfers and card payments from purchase-spending totals but retain them for reconciliation.

## Proposed or submitted is not completed

Issue: a cancellation, refresh, payment, or connection flow may stop before direct confirmation.

Verified fix: keep the state pending until merchant or provider confirmation exists, then schedule later evidence checks when needed.

## Expected money can be counted twice

Issue: a receivable may remain listed after the deposit appears in cash.

Verified fix: close the receivable and add the cash once after verified receipt.

## The bundled skill checker may lack its YAML dependency

Issue: the local `quick_validate.py` entrypoint could not start because PyYAML was not installed in its Python environment, and the installed Ruby YAML version did not expose `safe_load_file` for the first fallback attempt.

Verified fix: the repository's dependency-free validator passed, the YAML frontmatter and `agents/openai.yaml` were parsed with `safe_load` over explicit file contents, and no scaffold placeholders remained.

## Packaging checks depend on the current directory

Issue: one final metadata command was launched from the `outputs` directory while still prefixing repository paths with `outputs/`, so the files were not found.

Verified fix: rerun the checks with repository paths relative to the actual current directory, then rebuild and test the archive.

## GitHub publishing may require approved network access

Issue: the first GitHub identity check produced no output inside the restricted network environment.

Verified fix: rerun the narrow GitHub command with approved network access, verify the active account, create the repository as private, push `main`, and read back the private visibility setting.
