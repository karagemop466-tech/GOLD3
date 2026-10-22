# Archive — session `session-982bfc88` (PR #1)

This folder is a **verbatim copy** of the parallel implementation that was merged to `main` as PR #1
while this session was working. It is kept so no work is lost and so the reconciliation is auditable.

- `pages/` — their static site (index, rings, sellers, calculator, standards, flagged, method).
- `data/` — their `rings.json` (9 listings), `sellers.json` (7 sellers), `standards.json`, `spot.json`.
- `scripts/` — their `build.py` generator and their 13-check `audit.py`.
- `reports/` — their audit and link-check output.
- `README.md`, `COORDINATION.md` — their original documents.

**What happened to it.** The live site is now the superset maintained in the repo root: their seven
verified listings were re-opened and re-verified, then folded into `data/rings.json`; their seller
register facts were folded into `data/sellers.json`; their two dead listings moved to
`excluded_listings`. Their page generator was retired because the root site is now hand-authored
against a stricter audit, so keeping a second generator that rewrites the same filenames would be a
loaded gun.

Their independent capture of the gold spot price (`spot.json`) matched this session's figure exactly —
USD 4,024.36 per troy ounce, market date 2026-10-21, World Gold Council — which is a genuine
two-session cross-check of the benchmark.

Nothing here is served by the live site and nothing here is part of the audited dataset. It is history.
