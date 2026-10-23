# Pass P13 — live spot promotion and full weight-bearing re-read

- **Session:** `arena/438a583e-gold3`
- **Date:** 2026-10-23, reads taken at 20:17Z / 16:17 NY Time
- **Method:** every value below was read off the page named beside it. Where a
  page returned a figure, the figure is quoted verbatim; where it returned
  nothing (a JavaScript-only price), the value stays null and is recorded as
  unverified rather than estimated.
- **Checks:** `P13-01` … `P13-12` in `data/verification.json`
  (204 checks across 14 passes after this one).
- **Renumbered:** drafted as pass `P12`, but session `arena/57724486-gold3` merged its own
  `P12` (PR #51) while this pass was in flight. Every id here moved to `P13` and the new
  finding to `F41`. Their seven checks, their Menē corrections, flag `SRC3`, defects
  `SD14`/`SD15` and their three `audit.py` guards are preserved unchanged.

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

## 2. What was recomputed

`scripts/refresh_spot_anchor.py` (new, committed) does the arithmetic rather than
a human editing five JSON files:

- `data/prices.json` — new primary snapshot `goldprice-org-2026-10-23T2017Z`
  ($3,997.22) and cross-check `world-gold-council-2026-10-23T2017Z` ($3,996.31).
  The two superseded snapshots are kept, relabelled `history`, so the audit trail
  and the sources page still show what was quoted earlier.
- `data/spot-and-standards.json` — Kitco bid/ask/day-range/timestamp refreshed;
  USD/gram recomputed as `3,996.20 ÷ 31.1034768 = 128.4808`; all **7** karat
  tiers recomputed; BullionVault cross-check refreshed.
- `data/bands-and-high-karat.json` / `data/solitaire-rings.json` — the **4**
  weight-complete melt rows recomputed and the spot reference updated:

  | Row | Weight | Melt before | Melt after | Price ÷ melt |
  |---|---|---|---|---|
  | BND-04 | 1.7 g | $128.26 | **$127.41** | 3.12 → 3.14 |
  | BND-05 | 4.2 g | $316.87 | **$314.78** | 2.99 → 3.01 |
  | BND-06 | 4.0 g | $301.77 | **$299.78** | 3.96 → 3.99 |
  | BND-07 | 2.1 g | $158.43 | **$157.39** | 3.78 → 3.81 |

  The 16 rows with no published weight keep `pure_gold_grams` / `melt_value_usd`
  null. A re-anchor is not a licence to fill them in.
- `data/gold-price.json` — Dataset A/B anchor moved to the WGC reading.
- `data/findings.json` (F12 control check, F39 new), `data/sources.json`
  (verbatim spot quotes), `data/products.json` and `data/flags.json` (narrative
  references that quoted the superseded figure).
- `scripts/build_site.py` — the "where the two datasets agree" paragraph had a
  hard-coded `$4,024.36` / `$4,026.79`; it now renders whatever the snapshots say,
  so it cannot drift again.
- `scripts/audit.py` — the stray-number rule now also accepts a figure that
  appears in the append-only pass log, because the security-audit page renders
  its own past output verbatim (`$4,022.70 / 31.1034768 = $129.3328/g` from the
  09:56Z pass). Historical pass output is a record, not a new claim; it should
  not be rewritten, and the page should not be flagged for printing it.

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
