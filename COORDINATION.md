# COORDINATION.md — Shared Task Board

This file is the shared task board for any agent session working on this repo.
Read it before starting. Claim a task by writing your session ID + file scope, then
commit and push the claim **immediately**. Never start a task another session owns.
Each session works on its own branch `session-<id>/<task>` and edits only files in
its claimed scope. Shared outputs (`index.html`, `data/rings.json`, nav) are changed
only by the final integration session.

Status values: `unclaimed` · `in progress` · `done` · `needs review`
(`needs review` = item is published on the Flagged for Review page; it does not block anything.)

---

## Session registry

| Session ID | Branch | Started (UTC) | Last commit (UTC) | Purpose |
|---|---|---|---|---|
| `session-982bfc88` | `arena/982bfc88-gold3` | 2026-10-22 23:10 | 2026-10-22 23:10 | Repo bootstrap + full build (single active session; acts as its own integration session) |

> **No-conflict rule in effect:** only one session (`session-982bfc88`) is active in this
> repository. It therefore owns every file listed below and no scope overlap is possible.
> If a second session appears, it must claim a scope below before editing anything.

---

## Task board

| # | Task | Status | Owner | File scope |
|---|---|---|---|---|
| T1 | Bootstrap repo: README, COORDINATION, .nojekyll, assets | in progress | session-982bfc88 | `README.md`, `COORDINATION.md`, `.nojekyll`, `assets/**` |
| T2 | Standards & law reference (16 CFR Part 23, 15 U.S.C. 291–300, karat math, XRF) | in progress | session-982bfc88 | `data/standards.json`, `standards.html` |
| T3 | Gold spot price record (official source, dated) | in progress | session-982bfc88 | `data/spot.json` |
| T4 | Seller register: contact info, return policy, payment methods (official pages only) | in progress | session-982bfc88 | `data/sellers.json`, `retailers.html` |
| T5 | Ring/product dataset: line-by-line verification with per-field evidence + source URL | in progress | session-982bfc88 | `data/rings.json`, `rings.html` |
| T6 | No-hallucination audit script + report (runs after every review) | unclaimed | — | `scripts/audit.py`, `reports/**` |
| T7 | Site build script (static HTML from JSON, no external deps) | unclaimed | — | `scripts/build.py` |
| T8 | Flagged for Review page (unverified values + irregularities) | unclaimed | — | `flagged.html` |
| T9 | Final integration: re-verify combined data, link check, PR to main, merge, confirm Pages deploy | unclaimed | — | `data/**`, `*.html`, `COORDINATION.md` |

---

## Log

### 2026-10-22 23:10 UTC — session-982bfc88
- Repo inspected: single commit `1c10511` ("Initial commit"), only a 7-byte `README.md`.
  No data, no site, no prior work. GitHub Pages is already enabled (`build_type: legacy`,
  source `main:/`), URL `https://karagemop466-tech.github.io/GOLD3/`.
- Claimed T1–T5 + T9 for `session-982bfc88`. Branch in use: `arena/982bfc88-gold3`
  (Arena-managed session branch; the `session-<id>/<task>` convention cannot be created
  because this session is pinned to its Arena branch — noted here for the record).
- Environment limits observed (logged, not a blocker): the agent's `bash` sandbox has no
  direct internet egress; all verification is done through the page-fetch tool, which
  returns the live HTML of retailer pages. `curl` fails with SSL_ERROR_SYSCALL.
- Merchant robots/dead-link observations: Costco product URLs return
  "Product Not Available" (item discontinued) — recorded as a dead listing, not a hallucination.
