# Pass P14 — full weight-bearing re-read and four-feed spot corroboration

- **Session:** `arena/438a583e-gold3`
- **Date:** 2026-10-23, reads taken at 20:17Z / 16:17 NY Time
- **Method:** every value below was read off the page named beside it. Where a
  page returned a figure, the figure is quoted verbatim; where it returned
  nothing (a JavaScript-only price), the value stays null and is recorded as
  unverified rather than estimated.
- **Checks:** `P14-01` … `P14-12` in `data/verification.json`
  (211 checks across 15 passes after this one).
- **Renumbered twice:** drafted as `P12`, but `arena/57724486-gold3` merged its own `P12`
  (PR #51) mid-flight, and `arena/fb7e5e3c-gold3` then merged its own `P13` (PR #54). Every id
  here is `P14` and the new finding is `F44`. All of their merged work is preserved unchanged.

## 1. Why this pass exists

The whole melt table, the calculator and every "price ÷ melt" ratio on the site
divide by one number: the gold spot price. That anchor was captured at
**05:55 NY Time on 2026-10-23**. Re-read the same day at **16:17 NY Time**, four
independent publishers agreed on a figure **$25.00/oz lower**.

| Publisher | Read (2026-10-23, 16:17 NY) | Verbatim from the page |
|---|---|---|
| GoldPrice.org (primary) | **$3,997.22/oz** | `Spot Gold Price: USD 3,997.22 / Ounce \| Spot Silver Price: USD 53.92 / Ounce Oct 23rd, 2026 at 04:17 NY Time` |
| Kitco (Dataset C basis) | **$3,996.20 bid** / $3,998.20 ask | `GOLD Oct 23, 2026 16:17 3,996.20 3,998.20 -27.20 -0.68% 3,975.10 4,040.20` |
| BullionVault (Dataset C cross-check) | **$3,997.14/oz** ($128.51/g) | `Current Gold Price - $3,997.14 per Ounce … 23 October 2026, 16:17:24 (GMT-04:00)` |
| World Gold Council (cross-check) | **$3,996.31/oz** | `Gold Spot price USD/oz - 3,996.31 … Data as of 22 October, 2026` |

Spread across the four: **0.023%** between GoldPrice.org and the WGC tile,
**0.024%** between Kitco and BullionVault. Both are far inside the project's 2%
tolerance, so the new anchor is independently corroborated rather than copied.

The previous anchor ($4,022.22) was not invented — it was a correct reading of
the same page ten hours earlier. It was, however, out of date, and leaving it in
place would have overstated every melt figure by 0.62%. Finding **F39** (raised by session `arena/57724486-gold3`, which flagged the drift rather
than acting on it) records that move, and **F41** records this pass's decision to promote the
corroborated read to the calculation anchor. Both tell the reader to treat every melt number as dated.

## 2. What this pass did — and deliberately did not do

The live reading is **published, not promoted**. Two earlier sessions independently
caught the same 0.62% gap and both chose to keep the dated calculation anchor and
show the live figure as a reference row (finding `F39`). Rather than re-litigate a
decision that had already been taken twice, this pass **confirms** their reading,
adds three more independent feeds at the same minute, and leaves every stored
number untouched. The melt arithmetic therefore still reproduces exactly from
`$4,022.70/oz = $129.3328/g` (checked as `P14-12`).

What is added instead:

- **`scripts/refresh_spot_anchor.py`** (new): if the owner ever decides to promote a
  live reading, this performs the whole re-anchor from one dated capture — 2
  snapshots, 7 karat tiers, 4 melt rows, both Dataset C spot references — keeps the
  superseded snapshots as `history`, refuses to run when the capture date is not
  today, and supports `--check`. It is the reviewed alternative to hand-editing
  five JSON files, and it is **not** run as part of the build.
- **Four-feed corroboration** of the live reading so the reference row is not a
  single-publisher claim.

## 3. Every weight-bearing listing, re-read live

All 14 rows in `data/rings.json` that publish a gram figure were re-opened. This
is the only subset the calculator consumes, so a wrong weight here is a wrong
melt value.

| Row | Seller | Price on page | Weight on page | Result |
|---|---|---|---|---|
| R11 | Wilson's Estate Jewelry | `Sale price$3,725.00` | `Total Weight: 6.1 grams`, `Stamped for 14 karat gold` | confirmed |
| R12 | Wilson's Estate Jewelry | `Sale price$5,350.00` | `Total Weight: 2.2 grams`, `Stamped for 18 karat gold` | confirmed |
| R13 | Wilson's Estate Jewelry | `Sale price$2,850.00` | `Total Weight: 6.5 grams` | confirmed |
| R15 | Ross-Simons | `$249` | `Gold Weight 0.7 grams` | confirmed |
| R16 | Ross-Simons | `$299` | `Gold Weight 0.8 grams` | confirmed |
| R20 | Sarraf | `Now: US$3,004.00` | `Approximate Metal Weight: 3.80 grams` | confirmed |
| R21 | Sarraf | `Now: US$613.00` | `8.30 grams` | confirmed |
| R22 | Automic Gold | `$3,074` | `Approximately 5.4g for gold or 8.1g for platinum` | confirmed |
| R23 | Automic Gold | `$1,910` | `Approximately 6.1g (gold) or 9.2g (platinum)` | confirmed |
| R24 | Automic Gold | `$875` | `Approximately 2.3g (gold) or 3.5g (platinum)` | confirmed |
| R25 | Automic Gold | `$551` | `Approximately 1.4g (gold) or 2.1g (platinum)` | confirmed |
| R26 | Sarraf | `Now: US$4,068.00` | `6.30 grams` | confirmed |
| R27 | Sarraf | `Now: US$695.00` | `2.50 grams` | confirmed |
| R28 | VRAI | no price in static HTML | `Metal weight:2.3g` | confirmed |

**0 price changes, 0 weight changes, 0 dead links.** Two caveats stay attached to
the rows as before and are not defects:

- R21's page states `The weight listed is an approximate weight of a ring in size
  10 Made in the USA` — an approximate, size-specific figure.
- R22–R25 print a metal-dependent weight (gold **or** platinum). The stored value
  is the gold figure with the platinum figure in the quote, and the rows keep the
  `WT5` flag.

## 4. Dataset A spot-check

`aurate-2ct-round-lgd-solitaire` was re-read because it carries the only
range-valued weight in Dataset A: buy box `$2,858`, `Rate - 14k GOLD`,
`Color - Yellow`, `Size - 7`, `In Stock • Ready to Ship`,
`Exchange for size only. Final Sale!`; spec block `Weight: 5.5-8.5g`,
`SKU: AU5760`. Price and range reproduce; `weight_g` stays null because a range
is not a finished-ring weight. The remaining 18 Dataset A rows were last read on
2026-10-23 by pass P11 and were **not** re-opened here — they are not claimed as
re-verified by this pass.

## 5. Gates

All nine CI gates were run locally after the change and are green; see
`COORDINATION.md` §18 for the run record and the deployment result.

## 6. Recommended next hallucination hunt

1. **Dataset A's other 18 PDPs** — the only rows whose price has not been read
   since P11. Re-open each and compare against `price_quote`.
2. **Ring Concierge's 2.08 ct vs 5.63 ct page contradiction (F25)** — confirm the
   page still contradicts itself and whether the 7-day bridal window still applies.
3. **The five retailers' return pages** — policy pages are rewritten without
   notice; `returns_window_days` is the field most likely to rot.
4. **Menē** — it re-prices as the metal moves (PRC1). Re-read all four rows and
   expect movement rather than assuming the stored figure.
5. **Any new dataset** should carry, per row, the exact quote and the read date;
   a row without both is not verifiable and should not be published.
