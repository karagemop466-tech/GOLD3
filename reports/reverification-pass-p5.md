# Fifth verification pass — every published weight re-read

**Session:** `arena/6d6192d1-gold3` · **Date:** 23 October 2026 · **Scope:** the weight-bearing rows of Dataset B
**Result:** 7 checks — **3 confirmed · 3 corrected · 1 flagged**

## Why this pass exists

The fourth pass (`reports/reverification-pass-p4.md`) covered 25 URLs and deliberately skipped a list of rows. The
largest remaining risk was not a price but a **weight**: grams are the only input the melt calculator takes from a
seller, and every "price versus gold value" ratio on this site divides by them. A weight quoted without its qualifiers
("approximate", "total item weight", "for gold or for platinum") silently turns into a precise number the moment it
reaches a table.

So this pass re-opened every Dataset-B row that publishes a gram figure, and did nothing else.

## What was read

| Row | Seller | Stored | What the live page printed on 2026-10-23 | Outcome |
|---|---|---|---|---|
| R11 | Wilson's Estate Jewelry | $3,725 · 6.1 g | `Sale price$3,725.00` · `Stamped for 14 karat gold` · `Total Weight: 6.1 grams` · `7 Day Return Policy` | confirmed |
| R12 | Wilson's Estate Jewelry | $5,350 · 2.2 g | `Sale price$5,350.00` · `Stamped for 18 karat gold` · `With partial maker's mark for Hedges & Co.` · `Total Weight: 2.2 grams` · GIA Dossier 2215945495 | **confirmed** (see below) |
| R15 | Ross-Simons | $249 · 0.7 g | `$249.00` · `Gold Weight 0.7 grams` | confirmed (P4) |
| R16 | Ross-Simons | $299 · 0.8 g | `$299.00` · `Gold Weight 0.8 grams` | confirmed (P4) |
| R20 | Sarraf | $3,004 · 3.8 g | `Now: US$3,004.00` · `14K Solid Gold` · `Approximate Metal Weight: 3.80 grams` | confirmed (P4) |
| R21 | Sarraf | $613 · 8.3 g | `Now: US$613.00` · `10K Solid Gold` · `8.30 grams` · `The weight listed is an approximate weight of a ring in size 10` | confirmed (P4) |
| R22 | Automic Gold | $3,074 · 5.4 g | `$3,074` · `Crafted from solid recycled 14k gold` · `Item Weight Approximately 5.4g for gold or 8.1g for platinum` · `Returns can be made within 30 days of the delivery date` | confirmed |
| R23 | Automic Gold | $1,910 · 6.1 g | `$1,910` · `Solid 14k Gold and 950 Platinum` · `Item Weight Approximately 6.1g (gold) or 9.2g (platinum)` | **corrected** |
| R24 | Automic Gold | $875 · 2.3 g | `$875` · `Solid 14k Gold and 950 Platinum` · `crafted in solid recycled 14k gold` — the Details block fell past the end of the text read | **flagged** (weight not re-read) |
| R26 | Sarraf | $4,068 · 6.3 g | `Now: US$4,068.00` · `Material 18K Solid Gold` · `Approximate Metal Weight: 6.30 grams` | **corrected** |
| R27 | Sarraf | $695 · 2.5 g | `Now: US$695.00` · `Material 14K Solid Gold` · `Approximate Metal Weight: 2.50 grams` · `Solid and Pure 14k Yellow Gold` | **corrected** |
| R25 | Automic Gold | $551 · 1.4 g | not opened this pass | not re-checked |
| R28 | VRAI | price null · 2.3 g | price and weight render through JavaScript | not machine-verifiable |

Two practical notes about the reading itself. Every Automic Gold product page opens with a cookie-consent wall that
fills chunks 0–3; the product text starts in chunk 4, so four fetches were needed per page and the first three were
discarded. And the Sarraf pages print their specification block (material, weight, diamond grades) above the fold,
before any JavaScript — those are the most reliably citable pages in the dataset.

## The three corrections

1. **R23 — a weight that was really two weights.** The record stored `Item Weight: "Approximately 6.1g"` and stopped.
   The page prints `Approximately 6.1g (gold) or 9.2g (platinum)`. Storing the first half makes 6.1 g look like the
   ring's weight full stop, when it is the 14k-gold option's weight. It now carries both, exactly as the same seller's
   radiant ring already did.
2. **R26 — an unsupported tolerance.** The stored quote ended `(±5% seller accuracy note)`. The word "±5%" does not
   appear in the product specification block, the description or the sizing text; the seller prints only "Approximate
   Metal Weight". The annotation was removed rather than left to imply the seller had defined a tolerance, and replaced
   with the fact that no tolerance is published.
3. **R27 — the same annotation**, same fix.

Neither of the ±5% annotations changed a stored number, which is exactly why they were easy to miss: the figure was
right and the *justification* was invented. That is the failure mode this project calls a hallucination.

## One thing worth surfacing

**R12 is the only row in Dataset B where the seller publishes both a hallmark and a maker's mark** —
`Stamped for 18 karat gold` and `With partial maker's mark for Hedges & Co.` — and R11/R13 carry the hallmark alone.
Three of 31 rows, all from a single estate jeweller, satisfy checklist item 3 from a published statement rather than
from a photograph or a phone call. Everything else in the dataset is "not published by the seller". That ratio is the
finding: the hallmark requirement is met by asking, not by browsing.

## Authority text re-read

`16 CFR 23.10` was opened in full because the site's L4 rule leans on it for the maker's-mark requirement. Its title is
*Additional guidance for the use of quality marks*; it defines "quality mark" (gold, karat, carat, silver, vermeil,
platinum, plated, overlay, and their abbreviations) and its closing paragraph is the one the rule cites:

> Disclosure of identity of manufacturers, processors, or distributors. The National Stamping Act provides that any
> person, firm, corporation, or association … who applies or causes to be applied a quality mark … shall apply to the
> article the trademark or name of such person. [15 U.S.C. 297]

The citation was correct. The paragraph is now stored verbatim next to the rule in `data/standards.json`, so a reader
does not have to trust the paraphrase.

## What this pass did not verify

- `R24`'s 2.3 g — the Details block fell past the end of the text read. Price and solid-gold wording were confirmed; the
  weight was not, so the row is flagged and the value is left as previously captured.
- `R25` (Automic Gold flower ring) — not opened.
- `R28` (VRAI) — price and weight are rendered by JavaScript; the row stays flagged rather than being filled in from a
  rendered summary.
- Every row without a published weight, every policy page and every authority page other than 16 CFR 23.10.

## Gates after this pass

| Gate | Result |
|---|---|
| `scripts/verify.py` | PASS — 0 errors |
| `scripts/build_ext_pages.py` + `build_site.py` | OK |
| `scripts/audit.py` | PASS — 31 rows, 0 errors, 0 warnings, 173 passed |
| `scripts/run_security_audit.py` | PASS — SEC-01…SEC-07 |
| `node scripts/render-test.js` | 120/120 |
| `scripts/report_verify.py` | 116 verification checks |
| Row source-link enforcement | every root HTML table row carries an `https://` official link |

## Next hunt

1. `R25` and `R24`'s weight — two fetches, one pass.
2. Re-open the seven Aurate rows and Ring Concierge, still untouched since the third pass.
3. Replace `R03`'s collection-page citation with a product page, or drop the row.
4. Re-check Catbird's contact page (flag `SRC2`); if it stays down, decide whether the e-mail is citable at all.
5. Ask whether any seller publishes a weight *tolerance*; if one does, it belongs in the calculator's caveat rather than
   in a row annotation.
