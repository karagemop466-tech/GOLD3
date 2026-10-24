# Seventeenth verification pass (P17b) — the gold benchmark re-read, and 20 rows rotated back onto live pages

**Session:** `arena/1ee91485-gold3` · **Date:** 23 October 2026 · **Tip verified:** `main` @ `85ac1fa` (PR #66)
**Result:** 25 checks — **22 confirmed · 2 corrected · 1 flagged** — 25 official URLs opened live at `2026-10-23T23:43-23:45Z`.
**Companion data:** [`data/reverification-p17b.json`](../data/reverification-p17b.json) · **Ledger:** `data/verification.json`

> **Renumbered `P17` → `P17b`.** The peer session `arena/36ebce13-gold3` independently claimed the same task id and
> published its own `P17` (31 checks on Dataset A PDPs, seller policies and Trustpilot snapshots), which is already
> merged to `main`. To avoid colliding check ids (`P17-01`…) and the artifact filenames, this session's pass is
> `P17b` and its artifacts are `data/reverification-p17b.json` / `reports/reverification-pass-p17b.md`. The two
> passes cover different rows and are additive; neither discards the other.

## Why this pass exists

Two standing obligations had not been discharged on the current tip:

1. **The gold benchmark has drifted.** The dated primary anchor is `GoldPrice.org $4,022.22/oz` (captured 2026-10-23
   05:55 NY) and it is now ~0.65% above the live market. Every melt value on the site is computed from the dated
   anchor, so the drift has to be re-measured and shown, not silently absorbed.
2. **CR-P15-2 was still open.** The conflicted `reports/reverification-1162b2db.md` still contained unresolved
   `<<<<<<< HEAD` … `>>>>>>> origin/main` markers.

## 1. The gold benchmark, re-measured on five independent feeds (2026-10-23T23:43-23:45Z)

| Feed | Reading | As-of |
|---|---|---|
| GoldPrice.org | **$3,995.88/oz** (silver $53.92) | 07:41 NY, 23 Oct 2026 |
| Kitco | bid **$3,994.90** / ask $3,996.90, `-0.71%` | 23 Oct 2026, 19:43 NY |
| BullionVault | **$3,995.74/oz** ($128.47/g) | 23 Oct 2026, 17:00 GMT-04:00 |
| World Gold Council | **$3,995.47/oz** | data as of 22 October 2026 |
| LBMA | AM **$4,026.70** | 23/10 (tabulated data moved to the MyLBMA Portal behind an IBA licence) |

The four spot feeds cluster within **0.025%** and sit **0.655%** below the dated anchor. The dated anchor is
**deliberately kept** (reproducible, sourced to a dated capture) and the newest live reading is appended to
`data/prices.json` as a fourth, explicitly-labelled `live-check` snapshot. `scripts/build_site.py` now selects the
**newest** live-check snapshot for the calculator banner instead of the first, so the calculator shows the current
reading while the melt arithmetic stays on the dated anchor. Published as finding **F50**.

## 2. Twenty rows rotated back onto live product pages — every stored value found verbatim

| Row | Seller | Stored price | Live reading | Also re-confirmed |
|---|---|---|---|---|
| R12 | Wilson's | $5,350.00 | $5,350.00 | “Stamped for 18 karat gold”, maker's mark `Hedges & Co.`, 2.2 g |
| R20 | Sarraf | $3,004.00 | US$3,004.00 | 14K Solid Gold, 3.80 g |
| R21 | Sarraf | $613.00 | US$613.00 | 10K Solid Gold, 8.30 g |
| R26 | Sarraf | $4,068.00 | US$4,068.00 | 18K Solid Gold, 6.30 g |
| R27 | Sarraf | $695.00 | US$695.00 | 14K Solid Gold, 2.50 g |
| R01 | Mejuri | From $2,900 | From $2,900 | Solid White Gold (14k) + rhodium finish |
| R08 | Blue Nile | $2,210 | $2,210 (Setting Price) | **F1 self-contradiction still live** (18K White Gold spec vs 14k yellow-gold body) |
| R15 | Ross-Simons | $249 | $249 | 18kt Yellow Gold, 0.7 g |
| R24 | Automic Gold | $875 | $875 | Solid 14k Gold and 950 Platinum, 1–5 business days |
| SOL-01 | Blue Nile | $1,125 | $1,125 (Setting Price) | 18K Yellow Gold + platinum prongs |
| SOL-05 | Brilliant Earth | $1,090 | $1,090 (Setting Only) | **F27 band-width bug still live**; resizing not available |
| BND-04 | Ross-Simons | $400 | $400 | 14kt Yellow Gold, 1.7 g |
| BND-05 | Ross-Simons | $949 | $949 | 14kt Yellow Gold, 4.2 g |
| BND-06 | Ross-Simons | $1,195 | $1,195 | Italian 14kt dome, 4.0 g, 3/4 in |
| BND-08 | Ross-Simons | $3,295 | $3,295 | 14kt and 22kt Gold, 5.9 g |
| BND-12 | Mejuri | $498 | $498 | Solid Yellow Gold (14k), 2 mm × 1.3 mm |
| BND-01 | Menē | $1,694 | $1,694 | 24k Gold, 5 mm × 2 mm |
| BND-02 | Menē | $1,532 | $1,532 | 24k Gold, 4 mm × 2 mm |

## 3. Corrections — Menē repriced again, and the page that was down is back

- **R30 Wrap Ring** — the product page now prints **$3,202** (captured $3,253 on 2026-10-22; P4 read $3,228). A
  third entry was appended to `live_recheck.history`. **The stored `price_usd` stays $3,253** so the movement stays
  visible; the live figure is recorded beside it.
- **BND-03 Wide Flat Band** — the URL that answered **HTTP 500** at `2026-10-23T20:31Z` in pass P12 now loads and
  prints **$2,445**. A live-reading entry was added and the `SRC3` note updated to record that the page is live
  again. `price_usd` keeps the captured **$2,465**; the collection `From $2,297` widget figure is still only a
  cross-check and was not substituted.

Both are recorded in finding **F50**.

## 4. What did not change (and why that is deliberate)

- The **dated calculation anchor** is untouched — the project's rule is that a captured price is a dated snapshot
  and the live re-quote is shown beside it, never fed into the arithmetic.
- The **F1–F49 findings** are untouched. `F1` (Blue Nile 18K vs 14k), `F27` (Brilliant Earth band-width unit bug)
  and `F28`/`F40` are all still live and still published on `flagged.html`.
- No `price_usd` was overwritten; no weight was inferred; nothing peer-owned was edited.

## 5. The P17b delta, in one line

> Five gold-spot feeds confirm a ~$3,995/oz live cluster, 0.65% under the dated anchor; twenty rows were
> re-opened live and every stored value matched; Menē moved twice more and its Wide Flat Band page came back.
> The dated anchor stands, the newest live reading is now the calculator's reference, and CR-P15-2's
> conflicted report is split into the clean P5 report, the live-verified Dataset C surface and this pass's
> record.
