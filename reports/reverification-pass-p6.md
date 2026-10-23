# Independent Re-Verification Pass P6 (`P8` in `verification.json`)

- **Date (UTC):** `2026-10-23`
- **Session / Branch:** `arena/a05b3c00-gold3` (`C8`–`C10` in `COORDINATION.md`)
- **Machine-readable log:** `data/reverification-p6.json` (`P8-01`–`P8-20` in `data/verification.json`)
- **Scope:** Full primary-source sweep across **all 181 unique `https://` citations** in `data/products.json` (Dataset A: 19 rows), `data/rings.json` + `data/sellers.json` + `data/flags.json` (Dataset B: 31 rows + 4 excluded + 16 sellers), `data/solitaire-rings.json` + `data/bands-and-high-karat.json` + `data/sellers-policies.json` + `data/spot-and-standards.json` (Dataset C: 21 rows + 5 sellers + 4 spot snapshots + 7 standards), and `verification/sources-manifest.json` — **including multi-chunk reads through chunk 5** and **100% closure of all 19 URLs previously left in `verification.json["not_rechecked"]`**.

---

## 1. Executive Summary of Findings

| Category | Count | Key Impact |
| --- | ---: | --- |
| Consolidated live checks (`P8-01`–`P8-20`) | **20** (covering **100+ live URLs**) | **1 confirmed, 15 corrected, 4 newly flagged**; `not_rechecked` reduced from **19 → 0** |
| Dead (`404`), `500`, or stale URLs caught & fixed | **9** | Included **2 hallucinated `404` product URLs** inside `data/flags.json` (`WAR1.source`, `SPEC5.source`) |
| Multi-chunk truncation errors reversed | **5 rows** | Recovered **`R13` `Total Weight: 6.5 grams`** (chunk 1), restored **`R26`/`R27` `± 5%`** (chunk 4), verified **`R24` `2.3g`** (chunk 5) & **`R25` `1.4g`** (chunk 2) |
| Cross-dataset Menē audit (`BND-01..03`, `SEL-MENE`) | **4 records** | Quarantined unverified static-HTML weights on `BND-01..03` to `null` per Hard Rule #2; removed false `"D+"` BBB grade on `SEL-MENE`; documented `10%` restocking fee |
| Dataset A live product-page audit (`products.json`) | **19 / 19 rows** | Opened all 6 remaining Aurate pages (all carry `Exchange for size only. Final Sale!` + `AU5093` `"2ct"` vs `1.8tcw` + `AU5107` `"3ct"` vs `3.6tcw`) and `RC 2.72` (`Made to Order`, `3-4 weeks`, `Waitlist`); **0 rows remain `PRICE_NOT_RECONFIRMED`** |
| Site & calculator defects fixed (`SD9`–`SD12`) | **4** | Fixed missing `data-cats` on 20 Dataset C rows in `combined.html`, added `19K` (`19/24`) fineness calculation, closed `SD6` on 13 Dataset C rows, and added stone carat deduction (`0.200 g/ct`) + seller tolerance band to `calculator.html` |

---

## 2. All 9 Dead, Broken, or Stale Official URLs Caught & Fixed

| File & Field | Prior URL (Broken / Stale) | Live Status (`2026-10-23`) | Verified `200 OK` Primary Source Replacement |
| --- | --- | --- | --- |
| `data/flags.json` → `WAR1.source` | `https://www.sarraf.com/products/14k-white-gold-1-00-ctw-round-3-stone-diamond-engagement-ring-g-i1-3-80-gr.html` | **HTTP `404`** (`Sarraf - Not Found`, invented in Pass P3) | `https://www.sarraf.com/products/14k-white-gold-solitaire-ring-0-94-ctw.html` (`R20`, chunk 4 `#tab-warranty`) |
| `data/flags.json` → `SPEC5.source` | `https://www.automicgold.com/products/1-50ctw-pear-shaped-lab-grown-diamond-engagement-ring-bezel-set` | **HTTP `404`** (`404 Not Found – Automic Gold`, invented in Pass P3) | `https://www.automicgold.com/products/radiant-cut-lab-diamond-cathedral-ring` (`R22`) |
| `data/sellers.json` → `S-VRAI.contact_source` | `https://www.vrai.com/pages/contact-us` | **HTTP `404`** | `https://www.vrai.com/contact-us` (`help@vrai.com`, `+1.855.956.4488`) |
| `data/sellers.json` & `flags.json` → `S-VRAI` / `RET8` | `https://help.vrai.com/hc/en-us/articles/360000836514-What-is-your-return-policy` | Generic Help Center landing page (no terms) | `https://www.vrai.com/returns-exchanges` (`$300` engagement/engraved fee, `$50` band/MTO fee, `>$15,000` credit only) |
| `data/sellers.json` → `S-LOCALECLECTIC.contact_source` | `https://www.localeclectic.com/pages/contact-us` | **HTTP `404`** | `https://www.localeclectic.com/pages/contact` |
| `data/sellers.json` → `S-WE.policy_source` & manifest | `https://www.wilsonsestatejewelry.com/pages/returns-exchanges` | **HTTP `404`** | `https://www.wilsonsestatejewelry.com/policies/refund-policy` (exposed `SPEC6` shipping conflict) |
| `data/sellers.json` → `S-CB.contact_source` | `https://www.catbirdnyc.com/contact-us` | **HTTP `500`** (nginx error; `SRC2` retained) | `https://www.catbirdnyc.com/returns` + Brooklyn studio address at `https://www.catbirdnyc.com/catbird-sizing-and-repairs` |
| `data/spot-and-standards.json` → `STD-05` | `https://www.gia.edu/gems-gemology/summer-2025-lab-notes-gold-plated-gold0` | **HTTP `404`** (trailing `0` typo) | `https://www.gia.edu/gems-gemology/summer-2025-lab-notes-gold-plated-gold` |
| `data/spot-and-standards.json` → `STD-02` / `STD-03` | `https://uscode.house.gov/view.xhtml?req=granuleid:USC-prelim-title15-section295` & `297` | **HTTP `500`** server error | `https://www.law.cornell.edu/uscode/text/15/295` & `https://www.law.cornell.edu/uscode/text/15/297` |

*(Plus canonical path cleanups on `BND-09`–`BND-12` `/shop/products/` → `/products/`, `SEL-MENE.bbb_url` → `bbb.org/ca/on/toronto/profile/jewelry-designers/mene-inc-0107-1378080`, `auratenewyork.com/pages/terms-conditions-exchange-only-final-sale`, `ecfr.gov/current/title-16/chapter-I/subchapter-B/part-23`, and `gov.uk/government/publications/hallmarking-guidance-notes/hallmarking-is-the-law-guidance-summary`.)*

---

## 3. Multi-Chunk Primary-Source Discoveries

1. **`R13` (`Wilson's Estate Jewelry — Bailey Banks & Biddle 19K Art Deco Ring`):** Five prior passes marked `weight_g: null` (`W1`) because `- Total Weight: 6.5 grams` sits 4 lines into **chunk 1** immediately below `- Signed with maker's mark for Bailey Banks & Biddle`. Full read recovered `weight_g: 6.5` (`WT1`, total item weight including ~`0.20 ct` diamond and matte black enamel) and confirmed **2 of 31** Dataset B rows (`R12` and `R13`) state both karat stamp and maker's mark.
2. **`R20`, `R26`, `R27` (`Sarraf.com`):** Pass P5 read chunk 0 only and deleted `(±5% seller accuracy note)` on `R26` and `R27`. Reading **chunk 4** (`#tab-education`) confirmed Sarraf prints verbatim on all three product pages:
   > *"While being accurate is very important to us at Sarraf.com, due to factors beyond our control it is impossible to be exact each and every time, therefore we strive to maintain an accuracy of ± 5%."*
3. **`R03` (`Mejuri Slim Diamond Eternity Band`, new flag `PRC2`):** Reading all 4 chunks of `/collections/milestone-rings` confirmed `Slim Diamond Eternity Band ... From $648` in **chunk 2**, then clicking through to the live 14k Solid White Gold product page (`?Material=Solid+White+Gold+%2814k%29&Stone=Natural+Diamond`) revealed **`From $898` (`+38.6%`)** at the exact same moment plus `"14k solid white gold pieces are finished with rhodium plating"`.
4. **`R24` (`Automic Gold Claddagh Ring`, chunk 5) & `R25` (`Gemstone Flower Ring`, chunks 1–2):** Verified verbatim `"Approximately 2.3g (gold) or 3.5g (platinum)"` (`$875`, added `WT5`) and `"Approximately 1.4g (gold) or 2.1g (platinum)"` (`$551`, conflicting `'Production time is 4-8 business days'` vs `'Production time is 1-2 weeks'`, added `SPEC5`).

---

## 4. Newly Uncovered Retailer Contradictions (`F24`–`F30`)

- **All 7 Aurate Engagement Listings (`F24`):** Every single Aurate ring displays `"Exchange for size only. Final Sale!"` (`30%` cancellation fee after 24 hours at `/pages/terms-conditions-exchange-only-final-sale`) next to a `"Free Returns"` badge. On top of that, **`AU5093`** is titled `"2ct Emerald Lab Grown Diamond Bezel Ring"` (`$1,968`) while Specs print **`1.8tcw` (`-10%`)**, and **`AU5107`** is titled `"3ct Pear Lab Grown Diamond Bezel Ring"` (`$2,498`) while Specs print **`3.6tcw`** alongside one static `Weight: 3.33g` shared across 14k gold, 18k gold, and platinum.
- **Wilson's Standalone Refund Policy vs Product Tab (`F29` / `SPEC6`):** `/policies/refund-policy` states *"You must ship the package back to us, insured for the retail value"*, contradicting the product-page Domestic Returns tab (*"Returns within the US are complimentary!"* via prepaid QR label).
- **VRAI Plain vs Pavé Spec Contradiction (`SPEC7`):** `R28` selects `Band: Plain` (`$1,460`) while Details prints `Pavé carat weight: 0.11ctw`.
- **Menē Static-HTML Weight & BBB Audit (`F27` / `SD7`):** Neither `/collections/bands-gold` nor the three individual band pages (`$1,707`, `$1,544`, `$2,465`) contain any gram numbers in static HTML (gram breakdown sits behind a client-side JS modal). Unverified static weights on `BND-01..03` were quarantined to `null` per Hard Rule #2, `SEL-MENE`'s false `"D+"` BBB rating was corrected to `"Not Rated"` (`0107-1413670` & `0107-1378080`), and Menē's `10%` restocking fee + `±0.5g` / `±1.0g` weight tolerances were recorded.

---

## 5. Recommended Manual Hallucination Checks for Human Reviewers

Even with 8 automated verification gates passing (`verify.py`, `build_ext_pages.py`, `build_site.py`, `audit.py`, `run_security_audit.py`, `render-test.js`, `report_verify.py`, row-level `https://` anchor check, and unit tests), automated scripts cannot judge physical metallurgy or JS-only checkout state. Before spending money:

1. **Click the row's official source link live** on checkout day and verify the variant price, karat, and availability match your cart (`PRC1`, `PRC2`).
2. **Capture a dated screenshot of the JS weight/price breakdown** on sites like Menē or VRAI where static HTML omits gram numbers.
3. **Never infer net gold weight from "Total Weight"** on set rings (`WT1` on `R05`, `R13`, and Aurate bezels) — deduct `0.200 g × carat weight` on `calculator.html`.
4. **Weigh on a `0.01 g` scale AND run non-destructive multi-point XRF** inside the return window **before** resizing, engraving, or wearing (`RET12`, `POL2`, `STD-05`).
