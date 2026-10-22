# COORDINATION.md — Shared Task Board

This file is the shared task board for any agent session working on this repo.
Read it before starting. Claim a task by writing your session ID + file scope, then
commit and push the claim **immediately**. Never start a task another session owns.
Each session works on its own branch `session-<id>/<task>` and edits only files in
its claimed scope. Shared outputs (`*.html`, `data/rings.json`, navigation) are changed
only by the final integration session.

Status values: `unclaimed` · `in progress` · `done` · `needs review`
(`needs review` = item is published on the Flagged for Review page; it does not block anything.)

---

## Session registry

| Session ID | Branch | Started (UTC) | Last commit (UTC) | Purpose |
|---|---|---|---|---|
| `session-982bfc88` | `arena/982bfc88-gold3` | 2026-10-22 23:10 | 2026-10-22 23:35 | Repo bootstrap, dataset, site, audit, final integration |

> **No-conflict rule in effect:** only `session-982bfc88` has been active in this repository.
> It therefore owns every file listed below and no scope overlap is possible. A second session
> must claim a scope below before editing anything. Note: this session is pinned by Arena to the
> branch `arena/982bfc88-gold3`, so the `session-<id>/<task>` naming convention could not be used.

---

## Task board

| # | Task | Status | Owner | File scope |
|---|---|---|---|---|
| T1 | Bootstrap repo: README, COORDINATION, `.nojekyll`, assets | `done` | session-982bfc88 | `README.md`, `COORDINATION.md`, `.nojekyll`, `assets/**` |
| T2 | Standards & law reference (16 CFR Part 23, 15 U.S.C. §§ 294–297, karat maths) | `done` | session-982bfc88 | `data/standards.json`, `standards.html` |
| T3 | Gold spot price record (official source, dated) | `done` | session-982bfc88 | `data/spot.json` |
| T4 | Seller register: contact info, return policy (official pages only) | `done` | session-982bfc88 | `data/sellers.json`, `sellers.html` |
| T5 | Ring dataset with per-field evidence + source URL | `done` (7 live, 2 dead) | session-982bfc88 | `data/rings.json`, `rings.html` |
| T6 | No-hallucination audit script + report | `done` | session-982bfc88 | `scripts/audit.py`, `reports/**` |
| T7 | Site build script (static HTML from JSON, no external deps) | `done` | session-982bfc88 | `scripts/build.py` |
| T8 | Flagged for Review page | `done` | session-982bfc88 | `flagged.html` |
| T9 | Final integration: re-verify, link check, PR to main, merge, confirm Pages deploy | `in progress` | session-982bfc88 | `data/**`, `*.html`, `COORDINATION.md` |
| T10 | Seller reputation research (independent reviews, complaints, registered address) | `needs review` | unclaimed | `data/sellers.json` |
| T11 | Gram weights for every live listing (ask each seller in writing) | `needs review` | unclaimed | `data/rings.json` |
| T12 | Quote full return policies for Ross-Simons, Catbird | `needs review` | unclaimed | `data/sellers.json` |
| T13 | Second spot-price source for cross-checking melt values | `needs review` | unclaimed | `data/spot.json` |

---

## Log

### 2026-10-22 23:10 UTC — session-982bfc88 — claim
- Repo inspected: single commit `1c10511` ("Initial commit"), only a 7-byte `README.md`. No data, no site,
  no prior session work. GitHub Pages already enabled (`build_type: legacy`, source `main:/`),
  URL `https://karagemop466-tech.github.io/GOLD3/`.
- Claimed T1–T9 for `session-982bfc88`.
- Environment limit logged (not a blocker): the sandbox `bash` has no internet egress (`curl` →
  SSL_ERROR_SYSCALL). All verification was done through the page-fetch tool against the live pages.

### 2026-10-22 23:20 UTC — session-982bfc88 — T1–T3, T6–T8 done
- `scripts/audit.py`: 13 checks (A1–A13). Fails the run if any value lacks a quoted source, if a karat is
  not present in its own evidence quote, if a solid/plated verdict contradicts its quote, if a weight is
  not positive, if derived maths cannot be recomputed, or if a spot price is undated. It also runs a
  **price-drift detector** across every recorded observation of the same item.
- `scripts/build.py`: dependency-free generator for 7 pages + internal link/anchor checker.
- `data/standards.json`: 10 requirements, each quoted from eCFR or the U.S. Code, read 2026-10-22
  (16 CFR §§ 23.0, 23.3, 23.4, 23.7, 23.8; 15 U.S.C. §§ 294, 295, 297).
- `data/spot.json`: USD 4,024.36/ozt as of 2026-10-21 (World Gold Council / ICE Data Services).
  LBMA and ICE licence the historical tables, so WGC's displayed spot is the quotable official figure.

### 2026-10-22 23:32 UTC — session-982bfc88 — T4, T5 done
Live-verified listings (each field re-read on the seller's page on 2026-10-22):
Blue Nile 195730 ($1,145 setting, 14K white, rhodium) · Ross-Simons 985230 ($249, 18K, **0.7 g**) ·
Ross-Simons 932728 ($299, 14K, **0.8 g**) · Mejuri Bold Diamond Eternity ($2,900 from, solid 14k white) ·
Mejuri Duet Mixed Ring ($178, 18k **vermeil** — counter-example, not solid) ·
Tiffany Setting 40318275 ($1,600 from, 18k yellow + platinum head) · Catbird Woodland ($276, 14K, sale).
Dead/redirected, kept for the record and excluded from the buy list: James Allen 41515 (now redirects to
Blue Nile, "sold out"), Costco 100423493 ("Page Not Found").

Return policies read on the sellers' own pages and quoted in `data/sellers.json`:
Blue Nile (30 days; **items resized after purchase are not eligible**; two complimentary returns per year),
Tiffany (30 days; personalised/altered/engraved excluded; ≥ $75,000 exchange-only), Mejuri (30 days;
engraving excluded). Ross-Simons, Catbird, James Allen, Costco: **not verified** → T12.

### 2026-10-22 23:35 UTC — session-982bfc88 — final integration pass
- Audit: **10 checks pass, 2 warn, 0 fail**. Warnings are published on the Flagged page: 4 items have more than
  one recorded price observation, and 4 sellers have no verified return-policy URL.
- Build: 7 pages, **95 internal links / 0 broken**, 10 anchors / 0 missing.
- Second read of the dataset this pass: every dead listing re-checked (both still dead), every live URL still
  resolving to its product page. The spec blocks were **not** re-read for every row in this pass — each row
  carries its own `checked` date and A11 will warn once an entry is older than 30 days.
- Re-verification method for future passes: re-fetch each `url` in `data/rings.json`, compare the quoted
  evidence strings against the page text, update `checked`, then run `scripts/audit.py` **and look
  specifically for hallucinations** (a price that no longer appears on the page = failed re-verification).

### Irregularities to review (all published on `flagged.html`)
1. Ross-Simons 932728: cached copy $270 vs live page $299 — live value used.
2. Tiffany's own pages quote four different "starting from" prices ($1,540 / $1,560 / $1,600 / $1,650);
   only the live product-page figure is stored.
3. Tiffany product page showed both "non returnable" and "exchange only" notices plus "currently unavailable",
   which does not reconcile with its 30-day return policy page. Left unresolved and flagged.
4. James Allen product URLs now redirect to Blue Nile; the item is sold out. The $660 seen in a search copy
   was discarded rather than recorded.
5. Two Costco URLs are dead; the gram weights visible in search copies were **not** copied into the dataset.
6. 5 of 7 live listings never use the word "solid" — recorded as `null`, not upgraded to "solid gold".
7. Only 2 of 7 live listings publish a gram weight (both Ross-Simons) — the checklist's biggest open gap.

### 2026-10-22 23:5x UTC — session-982bfc88 — release record

| Item | Result |
|---|---|
| PR #1 → `main` | https://github.com/karagemop466-tech/GOLD3/pull/1 — **merged** (merge commit `38ff035`) |
| PR #3 → `main` (polish + hallucination watchlist) | https://github.com/karagemop466-tech/GOLD3/pull/3 — **merged** (merge commit `6bf9615`) |
| GitHub Pages | **built** — https://karagemop466-tech.github.io/GOLD3/ (source `main:/`, HTTPS enforced) |
| Live verification | `index.html`, `rings.html`, `method.html`, `calculator.html` fetched from the Pages URL and read back; all content present, all internal links resolving |

**One defect found and fixed during live verification:** the calculator's "gold value per gram of the ring" line
printed the fine-gold price ($129.39/g) instead of the alloy price ($75.48/g for 14K). Caught by reading the
deployed page, not by the audit — the audit only checks stored data, not JavaScript. Fixed in the next commit and
re-deployed. This is recorded because it is exactly the class of error this project is built to avoid.

T9 (final integration) is `done`. T10–T13 remain `needs review` and are published on `flagged.html`; they do not
block the merge, per the project rules.
