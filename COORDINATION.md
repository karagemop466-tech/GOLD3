# COORDINATION — GOLD3 (Gold Engagement Ring Verification Project)

**Shared task board for all agent sessions.** Read this before starting work.

- Repo: `karagemop466-tech/GOLD3`
- Primary session (this session): **`arena/8aaa18bf-gold3`** — Arena-assigned branch, cannot be renamed or switched.
- Rule: **No hallucinations.** Every value in this project must trace to an official/primary source URL
  that a human can open. If a value cannot be confirmed at an official source, it is left **blank** and
  marked `unverified` — never inferred, never estimated, never "typical".

---

## How to claim a task

1. Find a task below with status `unclaimed`.
2. Replace `unclaimed` with `in progress`, write your session ID, your branch/worktree name, and the
   **exact file scope** you will edit.
3. Commit and push that claim **immediately** (small commits only).
4. Never start a task another session has claimed (`in progress`) unless the claim is > 60 minutes old
   with zero commits — then take over and log the handoff.
5. If you need a file owned by another session, **log a request here**; do not edit it.
6. Run `git pull --rebase` before every push. Never discard another session's work on conflict; stop,
   resolve additively, and log what happened.
7. Shared outputs (`data/*.json`, `index.html`, navigation) are written **only** by the final
   integration session, after other tasks are `done`.

Branch naming: `session-<id>/<task>`. (This primary session is pinned by the platform to
`arena/8aaa18bf-gold3`, so it works there; its file scopes are still disjoint per task below.)

---

## Task board

| ID | Task | Status | Owner | File scope |
|----|------|--------|-------|-----------|
| T1 | Verified gold benchmark price (spot) with date + source | **done** | `arena/8aaa18bf-gold3` | `data/gold-price.json` |
| T2 | Verified ring listings (price, karat, metal, solid-gold claim, weight) | **done** | `arena/8aaa18bf-gold3` | `data/rings.json` |
| T3 | Seller verification (return policy, payment, hallmark/maker-mark, contact) | **done** | `arena/8aaa18bf-gold3` | `data/sellers.json`, `data/flags.json` |
| T4 | Regulatory standards (FTC 16 CFR 23; National Stamping Act) | **done** | `arena/8aaa18bf-gold3` | `data/standards.json`, `standards.html` |
| T5 | Anti-hallucination audit tooling + audit report | **done** | `arena/8aaa18bf-gold3` | `scripts/`, `reports/` |
| T6 | Site build (landing, category pages, table, calculator, flagged page) | **done** | `arena/8aaa18bf-gold3` | `*.html`, `assets/` |
| T7 | Integration: re-verify combined data, link check, publish Pages, PR + merge | **done** | `arena/8aaa18bf-gold3` | `.github/workflows/`, repo root |

Status values: `unclaimed` · `in progress` · `done` · `needs review`.
`needs review` = the item is published on the **Flagged for Review** page; it does **not** block merge.

---

## Log

### 2026-10-22 — Session `arena/8aaa18bf-gold3` — repo bootstrap
- Repo found with only a 7-byte `README.md` and one commit (`1c10511`). No prior data, no prior claims,
  no competing session work in `main`. Nothing to duplicate or conflict with.
- Created this board. Claiming T1 (in progress).
- Constraint recorded: sandbox shell egress is limited, but the research tools have open web access, so
  sourcing is done by fetching the official pages directly (not by scraping via `curl`).
- **Baseline finding for the whole project:** mainstream retailers publish karat + metal but almost
  never publish **ring metal weight in grams**, and almost never publish a per-item XRF assay. Those
  cells stay blank + flagged `unverified` by design. The melt-value calculator therefore takes weight
  as a **user input**, not a fabricated default.

### 2026-10-22 — Session `arena/8aaa18bf-gold3` — T1-T6 done, T7 in progress

**Note superseded — see the merge entry below.** When this board was first written the repo was empty and
no other session had claimed anything. A second session (`session-982bfc88`) had in fact started at the same
time and merged its work to `main` as PR #1. The conflict and its resolution are logged at the end of this
file. Nothing was discarded.

**Sources used (all opened and quoted this session, 2026-10-22)**
- 16 CFR Part 23 — FTC jewellery guides, via eCFR (gold content, vermeil, quality marks, tolerances).
- 15 U.S.C. 294-297 — National Stamping Act (maker's mark duty), cited through 16 CFR 23.10.
- World Gold Council Goldhub — spot price, USD 4,024.36/oz, market date 2026-10-21.
- LBMA — verified only that its historical tables are licence-gated (so the LBMA fix is not used).
- Blue Nile: engagement-ring listing, one product page, return-policy page.
- Mejuri: engagement-rings collection, two product pages, standard-return-policy FAQ.
- Costco: yellow-gold engagement-ring listing, one product page, official return-policy answer.
- Wilson's Estate Jewelry: engagement-rings collection, three product pages.

**Verification performed**
- 13 listings across 4 sellers; each price copied from the seller's own page and stored with its
  verbatim basis ("Setting Price", "Sale price", "From").
- `scripts/audit.py` — 55 checks, 0 errors, 0 warnings. It caught three self-overreaches: estate rows
  marked "solid" on the strength of a stamp stating the karat, where the seller never used the word
  "solid". Those were downgraded to `UNVERIFIED` and flagged `S2`. Report: `reports/audit-report.md`.
- `scripts/render-test.js` — 20/20 render checks; the R11 melt figure reproduces the arithmetic
  exactly, and the calculator refuses to produce a number without a user-supplied weight.

**Irregularities flagged (published on flagged.html, non-blocking)**
- `RET1` Costco's official policy: "Precious metals are non-refundable" — fails the return requirement.
- `S1` A mainstream listing named "18k" is 18k gold **vermeil** over sterling silver.
- `P1` Blue Nile prices shown are **setting only**; the centre stone is extra.
- `RET2` Wilson's estate return window is 7 days to request and 3 days to ship back.
- `W1` Weight in grams is unpublished on 10 of 13 rows; never estimated.
- `X1` No seller publishes a per-item XRF scan or assay.
- `M1` Independent review scores deliberately not asserted (not verified against a primary source).
- Excluded listings are recorded, including a James Allen URL that redirected to an unrelated pendant.

**Standing recommendation** (also on the site): re-run the audit after every review, then spend one
pass doing nothing but looking for hallucinations — take any number and try to find it on the linked
page. If it is not there, delete it and mark the field unverified.

### 2026-10-22 — Session `arena/8aaa18bf-gold3` — MERGE CONFLICT with `session-982bfc88`, resolved

**What happened.** PR #2 was opened from `arena/8aaa18bf-gold3`. The merge to `main` was rejected: while this
session was researching, `session-982bfc88` had built its own implementation and merged it as **PR #1**
(`38ff035`). Both sides had written `COORDINATION.md`, `data/rings.json`, `data/sellers.json`,
`data/standards.json`, the seller/standards pages and an audit script, so the trees conflicted.

**How it was resolved (no work discarded).**
1. `git merge -X ours origin/main` merged the histories without dropping any *file*; the other session's
   unique files came in cleanly.
2. Their **seven verified listings** were inspected individually. Five were re-opened by this session and
   re-verified on the live official page on 2026-10-22 — Blue Nile item 195730, Ross-Simons 985230,
   Ross-Simons 932728, The Tiffany Setting, Catbird Woodland — and folded into `data/rings.json` as R14-R18.
   Pricing and gram weights matched their records exactly in every case. Their Mejuri Duet vermeil row was
   imported as R19 and carries flag `L3` because this session did not re-fetch it.
3. Their **two dead listings** (James Allen 41515, Costco 100423493) were moved to `excluded_listings`, with
   their reasons preserved.
4. Their **four sellers** (Ross-Simons, Tiffany & Co., Catbird, James Allen) were merged into the register,
   keeping their evidence quotes and marking which fields this session re-verified.
5. Their **original site, data, generator, audit script and reports** are preserved verbatim under
   `archive/session-982bfc88/`, with a README explaining what superseded what and why. Their page generator
   was retired because it rewrites the same filenames as the new site — running it would silently revert the
   front end — not because its output was wrong.
6. Their **standards.json** was diffed against ours: our citation set is a strict superset (23.3, 23.4, 23.7,
   23.8 plus 23.10, 23.18, 15 U.S.C. 295/297), so no legal content was lost.

**Cross-check that came out of the merge.** Their independent capture of the gold spot price was
USD 4,024.36/oz, market date 2026-10-21, from the World Gold Council — identical to this session's figure,
taken separately. Two sessions, two fetches, same number.

**New findings this merge added (all verified live, published on flagged.html):**
- `RET6` — Tiffany & Co.'s product page states The Tiffany Setting is **non returnable** and
  **can only be exchanged**, while its general policy advertises 30 days. Directly fails the return rule.
- `FP1` — "Starting from" pricing that depends on the centre stone.
- `MM1` — 18k gold band plus a platinum head (multi-metal disclosure, 16 CFR 23.8).
- `WT2` / `LT1` — Ross-Simons publishes grams, qualified as approximate; 0.7 g and 0.8 g bands.
- `RH1` — rhodium-plated white gold surface (16 CFR 23.7).
- `DL1`, `PD1`, `POL1`, `AV1`, `L3` — dead listings, cached-vs-live price drift, unread policy pages,
  availability, and imported-not-re-fetched provenance.

**State at this entry.** 19 listings, 8 sellers, 5 excluded listings, 28 flag definitions.
`scripts/audit.py`: 74 checks, 0 errors, 0 warnings. `scripts/render-test.js`: 20/20.
