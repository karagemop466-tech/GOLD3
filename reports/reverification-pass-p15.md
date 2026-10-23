# Pass P15 — Additive Dataset C, NIST, Flag & Calculator Verification

**Date:** 2026-10-23  
**Session / branch:** `arena/db2fe957-gold3`  
**Integrated on:** `origin/main` @ `e50aa1f` (peer passes P12–P14 already merged)  
**Evidence:** [`data/reverification-p15.json`](../data/reverification-p15.json)

## No-hallucinations rule and integration scope

Every confirmed value below was found on the official page named beside it. Missing values stay blank; no price, weight, karat or conversion factor was inferred. This session’s earlier overlapping draft was dropped during rebase after peer P12–P14 landed. Their files, findings F39–F45, dated calculation anchor and live-check reference row are preserved. P15 contains only net-new checks and fixes; it does not reuse their pass or finding IDs.

## Result

- **11 checks:** 7 confirmed, 3 corrected, 1 flagged, 0 dead URLs.
- **Dataset C weights:** BND-04–BND-08 all matched the live official pages, including price. Combined with P14’s 14 Dataset B weight checks, current coverage is **19/19 published-weight rows**.
- **Findings published:** **F46** NIST attribution, **F47** VRAI SPEC7, **F48** Automic R23 lead times, **F49** calculator preset/product mismatch and hardcoded ratios.
- **Anchor decision preserved:** the site still calculates from its dated primary snapshot and displays the independently corroborated live-check reading separately. P15 did not promote or replace that anchor.
- **Verification ledger:** 222 checks across P1–P15 (108 confirmed / 77 corrected / 37 flagged), with no duplicate check or pass IDs.

## Dataset C weight rows re-read

| Row | Official product | Weight | Price | Result | Source |
|---|---|---:|---:|---|---|
| BND-04 | Women's 2mm 14kt Yellow Gold Band | 1.7 g | $400 | confirmed | [official source](https://www.ross-simons.com/products/571221) |
| BND-05 | Men's 4mm 14kt Yellow Gold Band | 4.2 g | $949 | confirmed | [official source](https://www.ross-simons.com/products/571212) |
| BND-06 | Italian 14kt Yellow Gold Diamond-Cut Dome Ring | 4 g | $1,195 | confirmed | [official source](https://www.ross-simons.com/products/823796) |
| BND-07 | Italian 14kt Yellow Gold Fleur-De-Lis Signet Ring | 2.1 g | $599 | confirmed | [official source](https://www.ross-simons.com/products/964717) |
| BND-08 | Men's 22kt Yellow Gold American Eagle Coin Ring in 14kt Yellow Gold | 5.9 g | $3,295 | confirmed | [official source](https://www.ross-simons.com/products/993085) |

BND-08 remains mixed-karat (`14kt and 22kt Gold`), so no single-karat melt value is inferred from its 5.9 g total. Ross-Simons labels its weights approximate; that qualification stays attached to every row.

## Corrections published for review

### F46 — NIST attribution

The prior evidence record said the NIST *Precious Metals Conversion Information* page “explicitly confirms 1 oz t = 31.1034768 g.” The live page prints Handbook 130 §2.17 and a PDF link, not that figure. [NIST SP 811 Appendix B.9](https://www.nist.gov/pml/special-publication-811/nist-guide-si-appendix-b-conversion-factors/nist-guide-si-appendix-b9) prints troy ounce = `3.110 348 E+01 g` and the boldface/exact grain factor `6.479 891 E-05 kg`. Exactly 480 grains per troy ounce gives `480 × 0.06479891 = 31.1034768 g`. The constant is unchanged; the source and derivation are now explicit. **CR-P15-1** requests correction of the peer’s historical evidence file without overwriting it.

### F47 — VRAI SPEC7

SPEC7 had named Signature 6-Prong, linked a different URL and mentioned $1,460 although it is attached only to R28 Petite 4-Prong. The [actual R28 page](https://www.vrai.com/configure/setting-to-diamond/petite-4-prong-ring/round-brilliant-yellow-gold-41015509221469) confirms `Band: Plain band` beside `Pavé carat weight: 0.11ctw`, plus `Metal weight: 2.3g`. It shows no static price, so `R28.price_usd` remains null. SPEC7 now names/links the correct row and asserts no price.

### F48 — Automic R23 production times

The [Coffin Ring page](https://www.automicgold.com/products/coffin-ring) confirms $1,910 and `Approximately 6.1g (gold) or 9.2g (platinum)`. Its buy box says `1 to 5 business days`; Details says `1-2 weeks` (2–3 weeks engraved). `SPEC5` was added to R23.

### F49 — Calculator provenance

The BND-06 preset said “Ross-Simons 6mm 14K Flat,” but the [official product](https://www.ross-simons.com/products/823796) is “Italian 14kt Yellow Gold Diamond-Cut Dome Ring,” 3/4 inch wide. All four real presets now derive product names, weights, prices and ratios from `bands-and-high-karat.json`; the two simulated controls remain explicitly labelled simulations. The displayed ratio range is computed from the same data (**2.99x–3.96x** under the preserved dated anchor), not typed into the template.

## SD24 — Post-deploy read-back follow-up

After PR #64 deployed, the live pages confirmed P15 but exposed three stale prose surfaces: `verify.html` session attribution stopped at P14, F2 still presented the A+B subset as “14 of 50” beside the 71-row site, and README said “P1–P14 / 211 checks.” The follow-up appends P15 attribution, computes full A+B+C counts in `verify.py` (F2 now says **19 of 71**), updates README to **P1–P15 / 222 checks**, and adds three regression guards. No listing value changed.

## Line-by-line P15 evidence

| Check | Row(s) | Outcome | Evidence | Official link |
|---|---|---|---|---|
| P15-01 | standards | flagged | Live page returns HTTP 200 and reproduces NIST Handbook 130 sec. 2.17 with a linked conversion PDF, but prints no troy-ounce-to-gram figure. Corrected the attribution in spot-and-standards.json and published F46; the peer historical evidence file was not overwritten (CR-P15-1). | [official source](https://www.nist.gov/pml/owm/metric-si/unit-conversion/precious-metals-conversion-information) |
| P15-02 | standards | confirmed | Live page prints 'ounce (troy or apothecary) (oz) -> gram (g) \| 3.110 348 \| E+01' and 'grain (gr) -> kilogram (kg) \| 6.479 891 \| E-05' in boldface (exact). Exactly 480 grains per troy ounce gives 480 x 0.06479891 = 31.1034768 g, so the constant remains valid. | [official source](https://www.nist.gov/pml/special-publication-811/nist-guide-si-appendix-b-conversion-factors/nist-guide-si-appendix-b9) |
| P15-03 | R28 | corrected | Both chunks print 'Band: Plain band', 'Metal: 18k Yellow Gold', 'Metal weight: 2.3g' and 'Pavé carat weight: 0.11ctw'. No price appears in static text, so price_usd stays null. SPEC7 had named Signature 6-Prong, linked another URL and mentioned $1,460; corrected and published as F47. | [official source](https://www.vrai.com/configure/setting-to-diamond/petite-4-prong-ring/round-brilliant-yellow-gold-41015509221469) |
| P15-04 | R23 | corrected | Chunk 4 confirms $1,910 and 'Approximately 6.1g (gold) or 9.2g (platinum)'. The buy box says 'Production time is 1 to 5 business days' while Details says '1-2 weeks' (2-3 weeks engraved). Added SPEC5 to R23 and published F48; no weight or price changed. | [official source](https://www.automicgold.com/products/coffin-ring) |
| P15-05 | BND-04 | confirmed | Live page prints 'Gold Weight 1.7 grams', 'Metal 14kt Yellow Gold' and $400 verbatim. All weights and measurements are labelled approximate by the seller. | [official source](https://www.ross-simons.com/products/571221) |
| P15-06 | BND-05 | confirmed | Live page prints 'Gold Weight 4.2 grams', 'Metal 14kt Yellow Gold' and $949 verbatim. | [official source](https://www.ross-simons.com/products/571212) |
| P15-07 | BND-06 | confirmed | Live page prints 'Gold Weight 4.0 grams', 'Metal 14kt Yellow Gold', Width 3/4 inch and $1,195 verbatim. The page also shows a cart-level promotional banner; the stored list price is unchanged. | [official source](https://www.ross-simons.com/products/823796) |
| P15-08 | BND-07 | confirmed | Live page prints 'Gold Weight 2.1 grams', 'Metal 14kt Yellow Gold', Width 1/2 inch and $599 verbatim. | [official source](https://www.ross-simons.com/products/964717) |
| P15-09 | BND-08 | confirmed | Live page prints 'Gold Weight 5.9 grams', 'Metal 14kt and 22kt Gold' and $3,295 verbatim. The single 5.9 g figure spans two finenesses, so the mixed-karat caveat remains and no single-karat melt value is inferred. | [official source](https://www.ross-simons.com/products/993085) |
| P15-10 | standards | confirmed | At the P15 live read, Kitco printed bid 3,996.00 / ask 3,998.00 at 'Oct 23, 2026 - 16:18 NY Time', 14K = 2,330.87 USD/oz, 128.47 USD/g and 'A troy ounce is 31.1034768 grams'. 3996.00 x 14/24 = 2331.00 and 3996.00/31.1034768 = 128.4744, agreeing to rounding. This is corroboration only; the peer-reviewed dated calculation anchor is preserved. | [official source](https://www.kitco.com/price/precious-metals/gold) |
| P15-11 | BND-06 | corrected | The official product is 'Italian 14kt Yellow Gold Diamond-Cut Dome Ring' (3/4 inch wide), not the template's 'Ross-Simons 6mm 14K Flat'. Calculator presets now derive the real product name, weight, price and ratio from Dataset C JSON; published as F49. | [official source](https://www.ross-simons.com/products/823796) |

## Final gates

| Gate | Result |
|---|---|
| `verify.py` | **PASS** — 0 errors / 0 warnings / 12 notes |
| `verify_dataset_c.py` | **PASS** — 21 rings, 5 weight-published, 16 null/unverified, 0 dead links |
| Both static builders | **PASS** — internal links, stylesheets and product URLs OK |
| `audit.py` | **PASS** — 31 rows, 0 errors / 0 warnings / 176 checks |
| `run_security_audit.py` | **PASS #36** — SEC-01…SEC-07, 0 errors; SEC-06 checked 2,355 links/anchors |
| `render-test.js` | **PASS** — 156/156, including six P15 and three SD24 guards |
| `report_verify.py` | **PASS** — 222 checks rendered |
| Root HTML official-link gate | **PASS** — 1,014/1,014 rows carry an `https://` official link |
| Archive suite | **PASS** — 7/7; 156 internal and 270 external links |
| `git diff --check` + JSON parse | **PASS** |

## Other irregularity logged, not blocking

**CR-P15-2:** `reports/reverification-1162b2db.md` already contained unresolved merge markers (`<<<<<<< HEAD`, `=======`, `>>>>>>> origin/main`) before P15. It is not used by the site build and was not edited; the board requests an additive cleanup preserving both report versions.

## Recommended next hallucination hunt

After every review, rerun all gates and actively look for values absent from their own source. Next targets: the 52 rows without published weights; the full 161-URL manifest for dead links; seller return/BBB/Trustpilot drift; Aurate and Ring Concierge final-sale wording; Menē JS-only weights; VRAI configurable-template specs; and cleanup of CR-P15-1/CR-P15-2. Never carry an old spot or listing price forward as “current.”
