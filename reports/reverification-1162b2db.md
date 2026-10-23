# Archived verification report bundle — P17 conflict resolution

This file preserves two independently authored 2026-10-23 verification reports that were previously concatenated by unresolved Git conflict markers. Pass P17 removed the markers and retained both reports below without discarding evidence.

## Version A — Pass P5, session `arena/1162b2db-gold3`

# Pass P5 — Primary-Source Line-by-Line Re-Verification Report (`2026-10-23`)

- **Session:** `arena/1162b2db-gold3`
- **Tasks Completed:** `D1` (Dataset C 21-item re-audit), `D2` (Dataset A 19-PDP & retailer policy re-audit + `SRC2` closure), `D3` (Dataset B/D remaining `not_rechecked` backlog closure), `D4` (`--deterministic` audit gate closing `CR-692d-2` + full site rebuild)
- **Un-rechecked URLs Remaining Across Repository (`data/verification.json` `not_rechecked`):** **`0`**

## 1. Zero-Hallucinations Enforcement: Unconfirmed Values Blanked (`null`)

1. **Menē 24K Bands (`BND-01`, `BND-02`, `BND-03` — Finding `F24` & Site Defect `SD9`):**
   - Earlier captures stored `8.5 g` (`BND-01`), `7.9 g` (`BND-02`), and `12.0 g` (`BND-03`) from search snippets and derived `1.50x–1.56x` melt ratios, while `BND-02` and `BND-03` linked to the collection grid instead of individual product pages.
   - Live fetches on `2026-10-23` of `https://mene.com/rings/gold/classic-band-gold` (`$1,707`), `https://mene.com/rings/gold/narrow-flat-band-gold` (`$1,544`), `https://mene.com/rings/gold/wide-flat-band-gold` (`$2,465`; collection card `From $2,315`), and `/products/*.json` (`HTTP 404`) proved that zero gram figures appear in server-rendered HTML because Menē injects gram weights client-side via JavaScript.
   - All three `weight_grams`, `net_gold_weight_grams`, `pure_gold_grams`, `melt_value_usd`, and `price_to_melt_ratio` fields were set strictly to `null`, flagged as `unverified`, and removed from hardcoded presets/copy in `scripts/build_ext_pages.py`.
2. **Unprinted Hallmark Disclosures (`BND-08`..`BND-12`, `SOL-01`..`SOL-08` — Site Defect `SD10`):**
   - Extended Pass P4's `SD6b` cleanup across the remaining 13 Dataset C listings whose `hallmark_disclosure` previously stated seller stamp practices not printed on the cited pages.

## 2. Live Price Corrections & Policy Traps Caught on Individual PDPs

1. **Mejuri `R03` (`Slim Diamond Eternity Band` — Finding `F26`):**
   - Stored price in `data/rings.json` was `From $648` cited to `https://mejuri.com/collections/milestone-rings`. Opening the ring's own PDP `https://mejuri.com/products/slim-diamond-eternity-band` revealed the actual live price is **`From $898`** (`+$250` / `+38.6%`; `$648` belongs to Mejuri's separate `Diamonds Band`). Updated `R03` to `$898` with direct PDP citation.
2. **All Seven Aurate Engagement Rings (`AU5760`..`AU5107` — Finding `F25`):**
   - Opening all seven individual PDPs plus `https://auratenewyork.com/pages/terms-conditions-exchange-only-final-sale` revealed that **100% of audited Aurate engagement rings print `"Final Sale! / Exchange for size only."`** — zero refund, one size exchange only, 24-hour cancellation window, and a **30% cancellation fee after 24 hours**, completely overriding Aurate's standard 60-day return window.
   - Every Aurate PDP also prints shared multi-metal `Weight:` figures (`2.23g` to `5.9-8.9g`, left `null` in `weight_g` because shared across `14k`/`18k`/`platinum` variants) and conflicting clarity claims (`VVS Clarity` vs `VS Clarity and EF Color` vs `SI Clarity Only`), plus `"classic oval diamond"` body prose on emerald-cut `AU5093`.
3. **Retailer Spec Contradictions Caught (`F28`):**
   - **Blue Nile `item-203738`:** Title/specs state `Metal: 18K White Gold`, whereas body prose states `"crafted in luminous 14k yellow gold"`.
   - **Brilliant Earth `SOL-05` / `R29` (`BE1FM0126`):** Official `Ring Information` spec table prints `Band Width: 2 ct. tw.` alongside the existing resizing contradiction, and geo-routes non-US requests to `€1,250` (canonical US schema `$1,090`).
   - **VRAI `R28` (`Petite 4-Prong Solitaire — Plain band`):** `Metal weight: 2.3g` confirmed live, alongside static template bug printing `Pavé carat weight: 0.11ctw` on the Plain band page.

## 3. Broken Official URLs Eliminated (`F27` & `SD11`) & `CR-692d-2` Closed

- **`catbirdnyc.com/contact-us` (`HTTP 500`, `SRC2`):** Replaced with live `HTTP 200` `https://www.catbirdnyc.com/facts` (`customerservice@catbirdnyc.com`) and `https://www.catbirdnyc.com/media/files/return_form.pdf` (`141 Flushing Avenue, Building 77, Suite 709, Brooklyn, NY 11205`, `+1-718-599-2340`).
- **Government & GIA `HTTP 404`/`500` Links:** Replaced `uscode.house.gov` (`500`) with `law.cornell.edu/uscode/text/15/295` & `/297` (`200`), `gov.uk/guidance/hallmarking-law-and-practice` (`404`) with `gov.uk/government/publications/hallmarking-guidance-notes/hallmarking-is-the-law-guidance-summary` (`200`), and `gia.edu/gems-gemology/summer-2025-lab-notes-gold-plated-gold0` (`404`) with `gia.edu/dam/migrated-assets/docs/doc1/summer-2025-lab-notes.pdf` (`200`).
- **Four-Source Spot Gold Cross-Check (`2026-10-23`):** GoldPrice.org `$4,022.22/oz`, Kitco Bid `$4,022.70/oz` (London AM Fix `$4,026.66/oz`), BullionVault `$4,024.23/oz`, World Gold Council `$4,024.45/oz` (`0.055%` / `$2.23/oz` spread across all four independent feeds).
- **Deterministic Security Audit Gate (`CR-692d-2`):** Added `--deterministic` (`or GOLD3_DETERMINISTIC=1`) to `scripts/run_security_audit.py` so automated gate checks verify all `SEC-01`..`SEC-07` invariants with zero worktree diff.
---

## Version B — Dataset C & Dataset D pass, session `arena/2908bea4-gold3`

# Dataset C & Dataset D Independent Live Re-Verification Report (`V9`–`V10`)

- **Date (UTC):** `2026-10-23`
- **Session / Branch:** `arena/2908bea4-gold3`
- **Starting `origin/main` tip:** `796362b` (post-PR #33)
- **URLs Re-Opened Live:** **58 official primary URLs** (`26` confirmed · `25` corrected · `7` flagged)
- **Zero-Hallucination Mandate:** Every stored price, gram weight, karat fineness, hallmark statement, return/payment exclusion, BBB figure, contact phone/email, and statutory link across Dataset C (`SOL-01`..`SOL-09`, `BND-01`..`BND-12`, `SEL-01`..`SEL-05`, `spot-and-standards.json`, `scripts/build_ext_pages.py`) and Dataset D (`R23`–`R31`, `S-BRILLIANTEARTH`, `S-VRAI`, `S-LOCALECLECTIC`, `S-MENE`) was checked verbatim against live HTTP 200 official pages on `2026-10-23`. Every value not printed on the cited page was blanked to `null` or rewritten as `Not published by the seller`.

---

## 1. Key Findings & Corrections Applied

### A. Menē `BND-01`..`BND-03` Client-JS Weights Blanked to `null` (Zero-Inference Enforcement)
- Opening `https://mene.com/products/mene-classic-band-gold`, `https://mene.com/products/mene-narrow-flat-band-gold`, `https://mene.com/products/mene-wide-flat-band-gold`, and `https://mene.com/collections/bands-gold` (`https://mene.com/bands/gold`) live confirmed that Menē's `"Price breakdown"` gram weights (`8.5`, `7.9`, `12.0` g) are populated **client-side via JavaScript only** and **do not appear anywhere in server-rendered HTML** (matching `R30` in `data/rings.json`).
- Per the project's Standing Anti-Hallucination Rule (*"pick any number in the dataset and try to find it on the linked page; if it is not there, delete it and mark the field unverified"*), `weight_grams`, `net_gold_weight_grams`, `pure_gold_grams`, `melt_value_usd`, and `price_to_melt_ratio` on `BND-01`, `BND-02`, and `BND-03` were blanked to `null`, `explicit_solid_wording` was set to `false` (pages print `"24k Gold"`, never `"solid"`), and PR #33's `PRC1` `live_recheck` blocks were preserved intact.

### B. Unsupported Hallmark Claims Eliminated Across Remaining 13 Dataset C Rows (`SD6` Extension)
- PR #33 fixed unsupported hallmark claims on `BND-01`..`BND-07` (`SD6`), but `SOL-01`..`SOL-08` and `BND-08`..`BND-12` still asserted stamps (`"per Blue Nile warranty"`, `"Brilliant Earth trademark & 18K stamp"`, `"Fairmined limited-edition 18K hallmark"`, `"14K & Mejuri hallmark inside band"`) that appear **nowhere** on the product pages or on `bluenile.com/services/warranty` or `brilliantearth.com/customer-service/warranty/`.
- All 13 remaining rows now explicitly state `Not published by the seller` and instruct buyers to verify karat + maker's mark (`16 CFR § 23.10` / `15 U.S.C. § 297`) under a 10x loupe upon arrival.

### C. New Live Product-Page Irregularities Caught
- **`SOL-05` (`BE1FM0126`, Brilliant Earth Fairmined 2mm Solitaire):** In addition to the `"Free 1-Year Resizing"` banner vs `"resizing is not available"` contradiction, the live Ring Information table prints **`"Band Width: 2 ct. tw."`** (carat weight unit inside the millimeter Band Width field). Pinned `?currency=USD` on `SOL-04`..`SOL-06` so international viewers are not geo-rendered EUR prices.
- **`SOL-07` (`Ross-Simons 990022`, 14kt White Gold):** Added `16 CFR § 23.7` white-gold rhodium plating notice (`RH1` parity).
- **`BND-04`..`BND-08` (`Ross-Simons`):** Removed unprinted `(1/16 inch)` from `BND-04` (`Width: 2 mm` on live page) and added Ross-Simons' verbatim `"All weights and measurements are approximate."` caveat (`WT3` parity).

### D. Broken Statutory, Lab-Note & Seller Links Repointed to Live HTTP 200 Official Pages

| Scope | Broken / Stale URL or Value | Status | Verified HTTP 200 Replacement (`2026-10-23`) |
|---|---|---|---|
| `spot-and-standards.json` (`18K`, `14K`, `STD-01`) & `checklist-standards.html` Rule 03 | `https://uscode.house.gov/view.xhtml?path=%2Fprelim%40title15%2Fchapter8&edition=prelim` | HTTP 500 | `https://www.govinfo.gov/content/pkg/USCODE-2023-title15/pdf/USCODE-2023-title15-chap8-sec295.pdf` & `...sec297.pdf` |
| `spot-and-standards.json` (`STD-05`) | `https://www.gia.edu/gems-gemology/summer-2025-lab-notes-gold-plated-gold0` | HTTP 404 | `https://www.gia.edu/dam/migrated-assets/docs/doc1/summer-2025-lab-notes.pdf` (pp. 291–293 `"Gold-Plated Gold"`) |
| `scripts/build_ext_pages.py` Rule 10 | `https://www.gov.uk/guidance/hallmarking-law-and-practice` | HTTP 404 | `https://www.gov.uk/government/publications/hallmarking-guidance-notes/hallmarking-is-the-law-guidance-summary` |
| `S-MENE` (`data/sellers.json`) | `https://mene.com/contact-us`, `+1-833-636-3465`, `concierge@mene.com` | 404 + wrong phone/email | `https://mene.com/customer-care/en-US`, `+1-833-636-3245` (`1-833-MENE-24K`), `service@mene.com` |
| `S-VRAI` & `R28` (`data/sellers.json`, `rings.json`) | `https://www.vrai.com/pages/contact-us`, `hello@vrai.com`, `+1-855-383-8724`, `help.vrai.com/hc/...` | 404 + wrong phone/email + redirect | `https://www.vrai.com/contact-us`, `help@vrai.com`, `+1-855-956-4488`, `https://help.vrai.com/en/knowledge/what-is-your-return-policy` |
| `S-LOCALECLECTIC` (`data/sellers.json`) | `https://www.localeclectic.com/pages/contact-us` | HTTP 404 | `https://www.localeclectic.com/pages/frequently-asked-questions` (prints `hello@localeclectic.com`) |
| `S-BRILLIANTEARTH` & `R29` (`data/sellers.json`, `rings.json`) | `https://www.brilliantearth.com/returns/`, `customerservice@brilliantearth.com` | 404 + unprinted email | `https://www.brilliantearth.com/30-Day-Returns/`, `email: null` (web form + `800.691.0952` + SMS `+1-415-520-6526` on `/contact/`) |

### E. Seller Policy & BBB Updates (`2026-10-23` Live Reads)
- **Brilliant Earth (`SEL-BRILLIANTEARTH`):** Corrected bank-wire fee disclosure—`"All bank wire orders are subject to a $35 USD processing fee"` (not only CA/intl wires!), meaning wires under `$2,334` lose money or barely break even while forfeiting credit card chargeback rights; added `$40` engraving removal fee, `$250` missing cert fee, `7-day` RSA expiry, comparative purchasing ban, and updated BBB to `4.45/5` (`342` reviews, `283` complaints/3yr, March 2026 BBB complaint pattern review).
- **Menē (`SEL-MENE`):** Documented up to `10%` original-payment restocking fee (`+5%` missing CoA fee), `60-day` buyback lockout, and BBB `mene-inc-0107-1413670` (`Not Accredited`, `0` reviews, `1` unanswered `2025-03-20` complaint citing `0.43g` short weight and missing `24k` stamp).
- **Ross-Simons, Blue Nile, Mejuri:** Updated live BBB review/complaint counts (`4.43/5` on `544` reviews; `1.0/5` on `25` reviews + `$150` missing cert fee; `D-` `1.0/5` on `6` reviews + `$20` EU / `$30` RoW return fees + `60 Bloor St W` HQ on Terms of Use).

---

## 2. Standing Recommendation

Always run **both** `python3 scripts/run_security_audit.py --session-id <session>` **and** `python3 scripts/verify_dataset_c.py` after every review or edit, then manually spot-check random cells in `solitaire-settings.html`, `bands-vintage-rings.html`, `sellers-policies.html`, and `combined.html` against their linked official URLs to look for hallucinations, silent client-JS omissions, or live price drift.
---

**Resolution:** `2026-10-23T23:46:52Z` by `arena/bd0ed905-gold3` (P17). No report text from either side was deleted; only the three conflict-marker lines were replaced by these section headings. See CR-P15-2 in COORDINATION.md.
