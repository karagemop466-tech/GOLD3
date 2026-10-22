# No-hallucination audit

Generated: **2026-10-22 23:15 UTC**  
Dataset: 4 entries (3 live-verified, 0 index-snapshot, 1 dead)

**Result: 10 passed · 2 warnings · 0 failed**

| Check | Status | Detail |
|---|---|---|
| `A1` Every entry links to an official seller page | **PASS** | 4/4 entries have an official URL and a registered seller. |
| `A2` No price exists without a quoted, dated source | **PASS** | 3 priced entries checked; 0 need attention. |
| `A3` Karat value appears verbatim in the quoted evidence | **PASS** | 4/4 karat values traced to a quote. |
| `A4` Solid-gold verdicts are backed by the seller's own wording | **PASS** | 1 verdicts checked. |
| `A5` Gram weights come from the seller, never from an estimate | **PASS** | 1 weight values checked. |
| `A6` Every derived figure is reproducible from stored inputs | **PASS** | Melt value = weight_g × karat/24 × (spot ÷ 31.1034768). Recomputed for 1 entries. |
| `A7` Price-drift detector: same item, different recorded prices | **WARN** | 1 of 4 entries have more than one recorded price observation. |
| `A8` No duplicate listings | **PASS** | 0 duplicate entries. |
| `A9` Dead listings are labelled, not silently kept | **INFO** | 1 dead listing(s) recorded and excluded from recommendations. |
| `A10` Spot price is dated by an official source | **PASS** | $4,024.36/ozt as of 2026-10-21 (1 day(s) old) — World Gold Council — Goldhub, Gold spot prices. |
| `A11` Every entry carries a recent re-check date | **PASS** | 0 entries older than 30 days. |
| `A12` Price magnitude sanity check | **PASS** | All stored prices fall in a credible range (limit $20,000 per fine gram). |
| `A13` Every seller has a linked, official return policy | **WARN** | 5/6 sellers documented. |

## Findings

| Severity | Item | Field | Finding |
|---|---|---|---|
| WARN | `RS-932728` | price | Conflicting prices recorded for the same item: $270 on 2026-10-22 (search-engine copy of the same page (stale)), $299 on 2026-10-22 (live product page) |
| WARN | `costco` | returns | No official return-policy URL recorded for this seller. |
| INFO | `COSTCO-100423493` | availability | Listing is no longer purchasable (page returned 'not found' / 'not available') — kept for the record, excluded from the buy list. |

## Arithmetic reference

- Spot used: $4,024.36/ozt as of 2026-10-21
  (World Gold Council — Goldhub, Gold spot prices)
- Spot per gram: **$129.3862/g** (spot ÷ 31.1034768)
- Melt value of a ring = `weight_g × (karat ÷ 24) × spot_per_gram`
- Premium vs melt = `(price − melt) ÷ melt × 100%` — only computed when a complete-ring price is stored

_Source of every row is linked on the Flagged for Review and Rings pages._
