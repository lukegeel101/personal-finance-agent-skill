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

## Inspect ZIP archives one at a time

Issue: `zipinfo` treats a second archive argument as a filename pattern inside the first archive rather than as another archive to inspect.

Verified fix: inspect each archive in a separate command and confirm that neither contains `.git` metadata.

## A technical README can hide the useful discoveries

Issue: the original README led with adapters and repository layout before showing what the Control Center can uncover about recurring charges, duplicated records, budget drift, stale data, and approval-gated next actions.

Verified fix: lead with practical discoveries and visual examples, move implementation details lower, and keep every claim tied to the evidence and authority model.

## Preview SVG artwork through a rendered copy

Issue: the local image viewer does not open SVG files directly, so it could not provide the required visual inspection of the README hero artwork.

Verified fix: validate the source SVG as XML, render a temporary PNG with ImageMagick, visually inspect the PNG, and keep the resolution-independent SVG as the only repository asset.

## Use the supported Ruby YAML interface

Issue: the installed Ruby YAML library does not expose `safe_load_file`, so the first final metadata check failed before parsing the agent manifest.

Verified fix: read the file explicitly and pass its contents to `YAML.safe_load`; the manifest then parsed successfully with aliases disabled.

## Verify demo commands against the repository entry point

Issue: one final verification command used the outdated filename `scripts/run_demo_audit.py`, which does not exist in the release repository.

Verified fix: confirm the documented entry point in the repository, run `scripts/demo_audit.py`, and verify its fictional audit output before running the complete test suite.

## Use the supported repository view output

Issue: `gh-axi repo view` does not support the GitHub CLI `--json` flag, so the first remote visibility check was rejected.

Verified fix: inspect the command help, run the supported repository view command without that flag, and confirm that the repository reports `visibility: private` and `branch: main`.

## README heroes and social cards use different aspect ratios

Issue: the wide 1200 by 360 README hero crops poorly when reused directly as GitHub's approximately 2:1 social preview.

Verified fix: render a separate 1280 by 640 PNG from a converter-stable SVG copy, replace unsupported gradients with matching solid palette colors, preserve the full hero inside a matching background, and visually verify the result before upload.

## Fall back cleanly when the GitHub wrapper cache is unavailable

Issue: `npx -y gh-axi` could not start because the local npm cache contained root-owned temporary files.

Verified fix: use the already authenticated `gh` CLI for the same narrowly scoped GitHub operations, and verify each remote result through GitHub's API.

## Verify current action versions with network access

Issue: the first action-version lookup could not reach GitHub from the restricted environment.

Verified fix: grant network access for the GitHub task, query the official action repositories, and pin the workflow to the current `actions/checkout@v7` and `actions/setup-python@v7` major versions.

## Use explicit percentage coordinates for social-card gradients

Issue: ImageMagick interpreted unitless SVG gradient endpoints differently and rendered the first social-preview background nearly black.

Verified fix: replace conversion-sensitive gradient fills with calibrated solid brand colors, render the PNG again, and visually inspect the final 1280 by 640 asset.

## Preserve concurrent public-presentation improvements

Issue: the remote repository gained a presentation commit while the local CI and social-preview commit was being prepared, so the first push was correctly rejected and the rebase found overlapping social assets.

Verified fix: fetch and inspect the remote commit, retain its README copy and cross-repository links, keep the newer 1280 by 640 social card, combine both gotcha records, rerun validation, and only then push the integrated history.

## Use fields supported by the installed release client

Issue: the installed GitHub CLI does not expose an `isLatest` field through `gh release view --json`, so the first release-verification query was rejected.

Verified fix: query the supported tag, draft, prerelease, immutability, publication-time, target, and URL fields, then confirm that `v0.1.0` is a published non-draft release.
