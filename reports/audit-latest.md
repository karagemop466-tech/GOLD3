# No-hallucination audit

Generated: **2026-10-22 23:18 UTC**  
Dataset: 9 entries (7 live-verified, 0 index-snapshot, 2 dead)

**Result: 10 passed · 2 warnings · 0 failed**

| Check | Status | Detail |
|---|---|---|
| `A1` Every entry links to an official seller page | **PASS** | 9/9 entries have an official URL and a registered seller. |
| `A2` No price exists without a quoted, dated source | **PASS** | 7 priced entries checked; 0 need attention. |
| `A3` Karat value appears verbatim in the quoted evidence | **PASS** | 9/9 karat values traced to a quote. |
| `A4` Solid-gold verdicts are backed by the seller's own wording | **PASS** | 2 verdicts checked. |
| `A5` Gram weights come from the seller, never from an estimate | **PASS** | 2 weight values checked. |
| `A6` Every derived figure is reproducible from stored inputs | **PASS** | Melt value = weight_g × karat/24 × (spot ÷ 31.1034768). Recomputed for 2 entries. |
| `A7` Price-drift detector: same item, different recorded prices | **WARN** | 4 of 9 entries have more than one recorded price observation. |
| `A8` No duplicate listings | **PASS** | 0 duplicate entries. |
| `A9` Dead listings are labelled, not silently kept | **INFO** | 2 dead listing(s) recorded and excluded from recommendations. |
| `A10` Spot price is dated by an official source | **PASS** | $4,024.36/ozt as of 2026-10-21 (1 day(s) old) — World Gold Council — Goldhub, Gold spot prices. |
| `A11` Every entry carries a recent re-check date | **PASS** | 0 entries older than 30 days. |
| `A12` Price magnitude sanity check | **PASS** | All stored prices fall in a credible range (limit $20,000 per fine gram). |
| `A13` Every seller has a linked, official return policy | **WARN** | 3/7 sellers documented. |

## Findings

| Severity | Item | Field | Finding |
|---|---|---|---|
| WARN | `RS-932728` | price | More than one price recorded for this item (list-price change, sale price, configuration or a stale index copy) — the live page value is the one used: $270 on 2026-10-22 (search-engine copy of the same page (stale)), $299 on 2026-10-22 (live product page) |
| WARN | `TIFFANY-40318275` | price | More than one price recorded for this item (list-price change, sale price, configuration or a stale index copy) — the live page value is the one used: $1,540 on 2026-10-22 (search-engine copy of a Tiffany product page (stale)), $1,560 on 2026-10-22 (search-engine copy of a Tiffany 1-carat gold landing page (stale)), $1,600 on 2026-10-22 (live product page), $1,650 on 2026-10-22 (search-engine copy of a Tiffany gold engagement-rings landing page (stale)) |
| WARN | `MJ-BDER` | price | More than one price recorded for this item (list-price change, sale price, configuration or a stale index copy) — the live page value is the one used: $2,900 on 2026-10-22 (live product page), $3,400 on 2026-10-22 (search-engine copy of the Mejuri engagement-ring collection page (stale)) |
| WARN | `CATBIRD-WOODLAND` | price | More than one price recorded for this item (list-price change, sale price, configuration or a stale index copy) — the live page value is the one used: $276 on 2026-10-22 (live product page (sale price)), $368 on 2026-10-22 (same live product page (regular price)) |
| WARN | `catbird` | returns | No official return-policy URL recorded for this seller. |
| WARN | `costco` | returns | No official return-policy URL recorded for this seller. |
| WARN | `james-allen` | returns | No official return-policy URL recorded for this seller. |
| WARN | `ross-simons` | returns | No official return-policy URL recorded for this seller. |
| INFO | `JA-41515` | availability | Listing is no longer purchasable (page returned 'not found' / 'not available') — kept for the record, excluded from the buy list. |
| INFO | `COSTCO-100423493` | availability | Listing is no longer purchasable (page returned 'not found' / 'not available') — kept for the record, excluded from the buy list. |

## Arithmetic reference

- Spot used: $4,024.36/ozt as of 2026-10-21
  (World Gold Council — Goldhub, Gold spot prices)
- Spot per gram: **$129.3862/g** (spot ÷ 31.1034768)
- Melt value of a ring = `weight_g × (karat ÷ 24) × spot_per_gram`
- Premium vs melt = `(price − melt) ÷ melt × 100%` — only computed when a complete-ring price is stored

_Source of every row is linked on the Flagged for Review and Rings pages._
