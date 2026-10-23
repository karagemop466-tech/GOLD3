# Pass P13 — Mejuri heading contradiction, Dataset B/C karat coverage and stale-prose repair

**Session:** `arena/fb7e5e3c-gold3` · **Date:** 2026-10-23 · **Machine-readable log:** `data/reverification-fb7e5e3c.json`
**Ledger entries:** `P13-01` … `P13-07` in `data/verification.json` (199 checks across passes `P1`–`P13`)
**Integrated on top of** `main` @ `7406ee9` (PR #51), preserving 100% of the concurrent `arena/57724486-gold3` pass `P12`
(spot live-check snapshot, Menē reprice corrections, `SRC3`, `SD14`/`SD15`).

> **No hallucinations.** No stored price, weight, karat or policy value was overwritten in this pass. Every change either
> (a) adds a flag for something the seller's own page contradicts, (b) corrects a flag that described the wrong defect,
> (c) fixes a figure the site's own build script typed in and let drift from `data/*.json`, or
> (d) adds rows that were already verified in another dataset but were missing from a category page.

---

## 1. What was opened live

| # | Official page | Rows | Outcome |
|---|---|---|---|
| P13-01 | `mejuri.com/products/bold-diamond-eternity-ring` | R01 | **corrected** (flag) |
| P13-02 | `mejuri.com/products/bold-diamond-half-eternity-ring` | R02 | confirmed |
| P13-03 | `mejuri.com/products/slim-diamond-eternity-band` | R03 | **corrected** (flag) |
| P13-04 | `ross-simons.com/products/985230` + `/932728` | R15, R16 | confirmed |
| P13-05 | `sarraf.com/products/14k-white-gold-solitaire-ring-0-94-ctw.html` | R20 | confirmed |
| P13-06 | `sarraf.com/products/10k-gold-6mm-high-polished-comfort-fit-wedding-band.html` | R21 | confirmed |
| P13-07 | `localeclectic.com/products/solid-gold-simple-knot-ring` | R31 | confirmed |

**Totals:** 5 confirmed · 1 corrected at the data level · 1 flagged, plus three site defects found by auditing the repo
against its own data (`SD18`–`SD20`, findings `F41`–`F43`).

The spot re-read taken in this session — GoldPrice.org **$3,997.22/oz** (`Oct 23rd, 2026 at 04:17 NY Time`) and
World Gold Council **$3,996.31/oz**, each **0.62% below** the stored primary of $4,022.22 — is already recorded as a
labelled `live-check` snapshot and as pass `P12-01` by the concurrent session, so this pass does not duplicate it.

---

## 2. Mejuri prints a yellow-gold heading above a white-gold selection

On **R01** (Bold Diamond Eternity Ring) and **R03** (Slim Diamond Eternity Band) the swatch line reads
`Solid White Gold (14k), Natural Diamond` and the copy says *"handcrafted in 14k solid gold"* — but the
**Materials & Specifications subheading prints `Solid Yellow Gold (14k)`**. The karat (14k) is consistent, so purity is
unaffected; the colour label contradicts the material actually selected.

R03 had been carrying flag **`SPEC2`**, whose stored definition is *the Local Eclectic 9k-vs-10k badge contradiction* —
it did not describe this defect. So:

* new flag **`SPEC8`** — "material heading contradicts the selected material" — attached to **R01** and **R03**;
* `SPEC2` **removed from R03** and left on the Local Eclectic row it actually describes (re-confirmed live in `P13-07`);
* a verbatim `materials_heading_note` stored on both rows.

---

## 3. Site defects found by auditing the repo against its own data

| ID | Page | Defect | Fix |
|---|---|---|---|
| `SD18` | `14k.html`, `18k.html` | The karat pages rendered **Dataset A only** (14 and 2 rows) although the navigation presents them as the site's karat views — and `18k.html` asserted *"No 18K listing here is a complete, verified ring at a verified price"*, contradicted by **R15** ($249, 0.7 g, re-read live this pass), **R17**, **R26**, **R29** and the Dataset C 18K settings. | Both pages now add a **Dataset B + C table for that karat** (31 rows on 14K, 13 on 18K), each row carrying its own official source link, plus counts computed from the data. |
| `SD19` | `rings.html`, `combined.html`, `flagged.html` | The `SPEC2` misuse above. | `SPEC8` created; `SPEC2` removed from R03. |
| `SD20` | `combined.html`, `methodology.html`, `calculator.html` | Typed-in prose had drifted: `$4,026.79/oz … $4,024.36/oz … 0.06% apart` (data: **$4,022.22 / $4,024.45 / 0.055%**); `"15 of 22 rows do not publish a weight"` (data: **17 of 31**); `"115 checks, 0 errors"` (audit: **176**). The labelled live-check snapshot was not surfaced on the calculator at all. | All figures now derive from `data/prices.json`, `data/rings.json` and `reports/audit-report.md` at build time; the calculator prints the live-check reading and its delta under the pre-filled spot field. |

---

## 4. How to reproduce

```bash
python3 scripts/verify.py             # PASS — no unsourced or impossible values
python3 scripts/verify_dataset_c.py   # PASS — 21 rings, 5 sellers, 0 dead links
python3 scripts/build_ext_pages.py
python3 scripts/build_site.py         # 18 pages, internal links OK
python3 scripts/audit.py              # rows=31 errors=0 warnings=0 passed=176
python3 scripts/run_security_audit.py # SEC-01..SEC-07 PASS
node scripts/render-test.js           # 145/145
python3 scripts/report_verify.py      # 199 checks
```

Every gate above was run on this branch before the pull request was opened, and runs again in CI on the push.
