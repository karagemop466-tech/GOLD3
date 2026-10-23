# Pass P12 — live re-verification on the post-PR-#50 tree

**Session:** `arena/57724486-gold3` · **Date:** 2026-10-23 (reads between 20:17Z and 20:35Z)
**Tree at start:** `main @ 253ab39` (PR #50 merged) · 71 rows across Datasets A (19), B (31), C (9 SOL + 12 BND) · 14 seller records · verification log at 185 checks
**Machine-readable evidence:** `data/reverification-57724486.json` (7 checks) · merged into `data/verification.json` as `P12-01`…`P12-07`

## No-hallucination rule applied in this pass

A value is recorded only if the cited page prints it. A number that could not be re-read is left
exactly as captured and flagged — it is never replaced by a nearby figure from another page, a
collection grid, a related-products widget or a search snippet.

## Result: 3 confirmed · 2 corrected · 2 flagged

| ID | Subject | Official URL read | Outcome | What the page actually printed |
|---|---|---|---|---|
| P12-01 | Gold spot anchor | https://goldprice.org/ | **flagged** | `Spot Gold Price: USD 3,997.22 / Ounce \| Spot Silver Price: USD 53.92 / Ounce Oct 23rd, 2026 at 04:17 NY Time`; header ticker `3,996.89 / -47.83 / -1.18%` |
| P12-02 | R20 Sarraf 14k WG solitaire 0.94 ctw | https://www.sarraf.com/products/14k-white-gold-solitaire-ring-0-94-ctw.html | **confirmed** | `Now: US$3,004.00` · `Material: 14K Solid Gold` · `Approximate Metal Weight: 3.80 grams` · `0.94 Ct.` · G / I 1 · `Natural` · ships 2–4 days |
| P12-03 | BND-01 Menē Classic Band 24k | https://mene.com/products/mene-classic-band-gold | **corrected** | `$1,694 USD` (stored 1,707) · `Metal: 24k Gold` · `Width: 5mm Thickness: 2mm` · Crafted-on-Demand |
| P12-04 | BND-02 Menē Narrow Flat Band 24k | https://mene.com/products/mene-narrow-flat-band-gold | **corrected** | `$1,532 USD` (stored 1,544) · `Metal: 24k Gold` · `Width: 4mm Thickness: 2mm` |
| P12-05 | BND-03 Menē Wide Flat Band 24k | https://mene.com/products/mene-wide-flat-band-gold | **flagged** | `500 Internal Server Error / Page Not Found \| Menē` — the product page could not be read at all |
| P12-06 | BND-04 Ross-Simons 2 mm 14kt band | https://www.ross-simons.com/products/571221 | **confirmed** | `$400` · `Item 571221` · `Metal 14kt Yellow Gold` · `Gold Weight 1.7 grams` · `All weights and measurements are approximate.` |
| P12-07 | R03 Mejuri Slim Diamond Eternity Band | https://mejuri.com/products/slim-diamond-eternity-band | **confirmed** | `From$898` · `Solid White Gold (14k), Natural Diamond` · `0.214 ct - 0.274 ct` · `Band Width: 1.1 mm` · `14k solid white gold pieces are finished with rhodium plating` · 30-day returns · 2-year warranty |

## 1. The spot anchor moved, and the page's own clock label runs backwards (F39)

The stored primary snapshot (`data/prices.json`, `goldprice-org-2026-10-23`) is **USD 4,022.22/oz**
labelled *"Oct 23rd, 2026 at 05:55 NY Time"*. The live page at 20:17Z printed **USD 3,997.22/oz**
labelled *"Oct 23rd, 2026 at 04:17 NY Time"*.

* The stored snapshot is **0.6215% higher** than the live reading, on the same market date.
* The stored snapshot was deliberately **not overwritten**. Every melt, break-even and
  price÷melt figure on the site is arithmetic on that documented number; silently replacing it
  would silently change every printed result, which is the failure mode this project exists to
  catch. Instead the live reading is kept as an explicitly labelled third entry with the role
  *live-check (shown for reference, not used in any calculation)*, so it is visible on
  `sources.html` beside the two calculation snapshots.
* The page's clock label (**04:17 NY**) is *earlier* than the label on the morning's capture
  (**05:55 NY**) although it was read some ten hours later. At least one of the two timestamps is
  not what it appears to be. Recorded as printed; no explanation is invented.
* Arithmetic shown on the site's own constants (1 troy oz = 31.1034768 g, 14K = 14/24):
  `4,022.22 → $129.3174/g pure → $75.4351/g at 14K`; `3,997.22 → $128.5136/g pure → $74.9663/g at 14K`.
  R20's 3.80 g 14K ring therefore holds **$286.65** of gold at the stored spot and **$284.87** at
  the live one — $1.78, i.e. the same 0.62%.

## 2. Menē re-priced two bands down *again* within one day, and a third page returned HTTP 500 (F40 / PRC1 / SRC3)

| Row | Stored | Live 2026-10-23T20:30Z | Action |
|---|---|---|---|
| BND-01 Classic Band | $1,707 (earlier same day; $1,720 on 2026-10-22) | **$1,694** | corrected, history kept in `live_recheck.history` |
| BND-02 Narrow Flat Band | $1,544 | **$1,532** | corrected |
| BND-03 Wide Flat Band | $2,465 | **page returned HTTP 500** | left as captured + flag `SRC3` |

Menē's own Recommended widgets (on the two pages that do load) print *"Wide Flat Band - Gold …
From $2,297"*. That is a **different number from a different surface**, so it was recorded as a
cross-check only. Substituting it for the product-page price would be an inference, not a source —
exactly the move this pass is looking for. `price_usd` therefore stays at its captured $2,465 and
the record says plainly that it is unconfirmed today.

## 3. Site defects found on our own tree and fixed (SD14, SD15)

* **SD14 — three published counts described the site as smaller than it is.** The dashboard lead
  and `combined.html`'s meta description said *"50 listings across 16 sellers"* and `rings.html`
  said *"the site carries 50 listings in total"*, while `combined.html` renders **71** rows and the
  navigation says *Combined (71)*. 50 is the Datasets A+B subtotal; it silently dropped the 21
  Dataset C settings and bands shown on the same page. All three strings are now computed from the
  loaded JSON and state both numbers.
* **SD15 — the verification log carried duplicate ids and a stale count.** Check ids `P11-01` and
  `P11-02` had each been allocated twice by two different sessions; `summary.checks` claimed **137**
  entries while the log held **185**; site-defect ids `SD6` and `SD10` each appeared twice and
  `SD12` was unused. Fixed: the second pass is now `P11b` with `P11b-01/P11b-02`, duplicate site
  defects renumbered (`SD12`, `SD13`, `SD17`), `summary` recomputed from the entries.
* **Guard rails added to `scripts/audit.py`** so this class cannot recur silently: the build now
  fails on duplicate verification check ids, on duplicate site-defect ids, and on a
  `summary.checks` that disagrees with the number of entries. Verified by injecting a duplicate into
  `data/verification.json` (audit reported 4 errors) and restoring it.

## 4. Gates run after the changes (all nine CI gates, locally, in workflow order)

| Gate | Result |
|---|---|
| `python3 scripts/verify.py` | **PASS** — 0 errors, 0 warnings, 12 notes |
| `python3 scripts/verify_dataset_c.py` | **PASS** — 21 rings (5 weight-published), 5 sellers, 7 standards, 0 dead links |
| `python3 scripts/build_ext_pages.py` | built (Dataset C subpages) |
| `python3 scripts/build_site.py` | built 18 pages · internal links and product URLs OK |
| `python3 scripts/audit.py` | `rows=31 errors=0 warnings=0 passed=176` |
| `python3 scripts/run_security_audit.py --session-id arena/57724486-gold3` | Pass #28 — SEC-01…SEC-07 **PASS** (2,199 links/anchors) |
| `node scripts/render-test.js` | **127/127** checks passed |
| `python3 scripts/report_verify.py` | report rebuilt — **192 checks** |
| root-HTML `<tr>` https-link gate | **922 rows, 0 missing** official links |
| `npm --prefix archive/session-cbea1001 test` | **PASS** — 156 internal, 270 external links |

## 5. Recommended next hallucination hunt

1. Re-read `data/gold-price.json` and `data/prices.json` on the day of purchase — the spot moved
   0.62% during this pass and the two files hold different dates (21 Oct vs 23 Oct).
2. Re-open `https://mene.com/products/mene-wide-flat-band-gold` (flag `SRC3`); if it recovers,
   capture the product-page price and retire the flag, or confirm the price in writing with care.
3. Re-read every Menē row again before quoting any figure — two of three moved twice in one day.
4. Sweep the remaining `SOL-01…SOL-09` rows on `bluenile.com` (not touched by this pass) against
   their live pages, since Blue Nile changed its returns policy wording in earlier passes.
5. Check that the new `live-check` snapshot role does not get picked up by any future calculation —
   `build_site.py` selects `role == "primary"` deliberately; any refactor must keep that.
