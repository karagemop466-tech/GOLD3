# Pass P5 — Primary-Source Line-by-Line Re-Verification Report (`2026-10-23`)

- **Session:** `arena/1162b2db-gold3`
- **Tasks Completed:** `D1` (Dataset C 21-item re-audit), `D2` (Dataset A 19-PDP & retailer policy re-audit + `SRC2` closure), `D3` (Dataset B/D remaining `not_rechecked` backlog closure), `D4` (`--deterministic` audit gate closing `CR-692d-2` + full site rebuild)
- **Un-rechecked URLs Remaining Across Repository (`data/verification.json` `not_rechecked`):** **`0`**

> **CR-P15-2 resolution (this file).** `reports/reverification-1162b2db.md` previously held this P5
> report **and** the Dataset C/D report concatenated inside an unresolved git merge conflict
> (`<<<<<<< HEAD` … `=======` … `>>>>>>> origin/main`). The split is now resolved:
> the live-verified Dataset C/D surface lives in **[`reports/reverification-dataset-c.md`](reverification-dataset-c.md)**,
> the stale/unverified capture artifacts are catalogued in
> **[`reports/reverification-incomplete.md`](reverification-incomplete.md)**, and this file is the
> clean P5 primary-source report only. No peer content was discarded.

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

## 4. Pass P17 follow-up on this session's live readings

Pass P17 re-opened several of this session's rows and confirmed them verbatim: Wilson's `R12`, Sarraf `R20`/`R21`/`R26`/`R27`,
Mejuri `R01`/`BND-12`, Blue Nile `R08`/`SOL-01`, Ross-Simons `R15`/`BND-04`/`BND-05`/`BND-06`/`BND-08`, Automic `R24` and
Brilliant Earth `SOL-05`. The Menē rows were the exception — see `F40`/`F50` and `data/reverification-p17.json`. The
`catbirdnyc.com/contact-us` replacement, the statutory/GIA repointing and the `--deterministic` gate are unchanged and
still live at `2026-10-23T23:45Z`.
