# Re-verification Pass P4 — Fourth Independent Live Audit & Full Integration (`arena/bfcd8465-gold3`)

- **Session:** `arena/bfcd8465-gold3`
- **Date (UTC):** `2026-10-23`
- **Scope:**
  1. Live re-verification of Dataset B rows `R23`–`R31` and sellers `S-AUTOMIC`, `S-BRILLIANTEARTH`, `S-VRAI`, `S-LOCALECLECTIC`, `S-MENE` (`data/rings.json`, `data/sellers.json`, `data/flags.json`).
  2. Live re-verification of all 21 Dataset C ring listings (`data/solitaire-rings.json`, `data/bands-and-high-karat.json`), all 5 BBB profiles (`data/sellers-policies.json`), and regulatory/testing links (`data/spot-and-standards.json`).
  3. Resolution of all 9 open Change Requests (`CR-P3-1` through `CR-P3-9`) from `COORDINATION.md` §4.
  4. Resolution of cross-page count, footnote, and filter-toolbar defects (`SD7`, `SD8`) in `scripts/build_site.py`, `scripts/build_ext_pages.py`, and `README.md`.

---

## 1. Six Dead (`404`) or Redirecting Source URLs Caught and Repaired (`SRC1`, `F24`–`F27`)

| Location | Stored URL | Live HTTP Result | Live Official Replacement |
|---|---|---|---|
| `S-MENE.contact_source` (`data/sellers.json`) | `https://mene.com/contact-us` | `404 Page Not Found \| Menē (# Are you lost?)` | `https://mene.com/privacy-policy` & `https://mene.com/products/mene-classic-band-gold` |
| `S-VRAI.contact_source` (`data/sellers.json`) | `https://www.vrai.com/pages/contact-us` | `404 - Page not found` | `https://help.vrai.com/en/knowledge/when-is-your-customer-experience-team-available` |
| `S-LOCALECLECTIC.contact_source` (`data/sellers.json`) | `https://www.localeclectic.com/pages/contact-us` | `404 Not Found – local eclectic` | `https://www.localeclectic.com/pages/frequently-asked-questions` (form at `/pages/contact`) |
| `WAR1.source` (`data/flags.json`) | `https://www.sarraf.com/products/14k-white-gold-1-00-ctw-round-3-stone-diamond-engagement-ring-g-i1-3-80-gr.html` | `404 Error - Page not found` (`Sarraf - Not Found`) | `https://www.sarraf.com/products/14k-white-gold-solitaire-ring-0-94-ctw.html` |
| `SPEC5.source` (`data/flags.json`) | `https://www.automicgold.com/products/1-50ctw-pear-shaped-lab-grown-diamond-engagement-ring-bezel-set` | `404 Not Found – Automic Gold` | `https://www.automicgold.com/products/radiant-cut-lab-diamond-cathedral-ring` |
| `STD-05.official_url` (`data/spot-and-standards.json`) | `https://www.gia.edu/gems-gemology/summer-2025-lab-notes-gold-plated-gold0` | `404 - PAGE NOT FOUND` | `https://www.gia.edu/gems-gemology/summer-2025-lab-notes-gold-plated-gold` |
| `S-VRAI.policy_source` & `R28.sources` | `https://help.vrai.com/hc/en-us/articles/360000836514-What-is-your-return-policy` | Redirects to Help Center index `https://help.vrai.com/en/knowledge` | `https://www.vrai.com/returns-exchanges` & `https://help.vrai.com/en/knowledge/what-is-your-return-policy` |
| `S-BRILLIANTEARTH.policy_source` & `R29.sources` | `https://www.brilliantearth.com/returns/` | Serves homepage (`Sustainable Engagement Rings & Fine Jewelry`) | `https://www.brilliantearth.com/30-Day-Returns/` |

---

## 2. Seller Contact & Policy Corrections (`F24`–`F27`)

1. **VRAI (`S-VRAI`, `F24`):**
   - Stored phone `+1-855-383-8724` and email `hello@vrai.com` (cited to a 404 URL) did not match VRAI's live Help Center articles, which print **`Phone: +1.855.956.4488`** (`+1-855-956-4488`) and **`Email: help@vrai.com`**.
   - Two live VRAI Help Center articles contradict each other on response time: `when-is-your-customer-experience-team-available` states *"within 4 business days!"* while `can-i-speak-to-a-vrai-representative-on-the-phone-1` states *"within 1 business day!"*.
   - Live return policy adds a **$15,000 cash-refund cap**: *"Eligible items above $15,000 can be returned within 30 days for full credit to store."*
2. **Menē (`S-MENE`, `F25`):**
   - Stored phone `+1-833-636-3465` had transposed two digits of `1-833-MENE-24K` (**`+1-833-636-3245`**, confirmed on `https://mene.com/terms-of-service`, `https://mene.com/products/mene-classic-band-gold`, and Menē's BBB profile).
   - Stored email `concierge@mene.com` corrected to **`service@mene.com`**, printed verbatim in Section F.2 of `https://mene.com/privacy-policy` and in the Customer Care Concierge block on Menē product pages.
3. **Automic Gold (`S-AUTOMIC`, `RET14`, `F26`):**
   - Reading all 6 chunks of `https://www.automicgold.com/pages/privacy-policy` showed that `+1-929-307-2378` is not printed anywhere on the page; `phone` set to `null` and `contact_source` repointed to `https://www.automicgold.com/pages/faq` (`care@automicgold.com`).
   - Reading chunk 4 of `https://www.automicgold.com/policies/refund-policy` (past the 4-chunk CookieYes banner) restored the verbatim `resize_policy` and uncovered a critical deadline: **`"To avoid a restocking fee, please mail your items within 14 days."`** (new flag `RET14`).
4. **Brilliant Earth (`S-BRILLIANTEARTH`, `F27`):**
   - `https://www.brilliantearth.com/contact/` uses a web form for customer care and prints only `marketing@brilliantearth.com`, `pr@brilliantearth.com`, `jobs@brilliantearth.com`, phone `800.691.0952`, and SMS `+1 415.520.6526` — not `customerservice@brilliantearth.com`. Set `email` to `null` (matching `SEL-BRILLIANTEARTH` in `data/sellers-policies.json`).
   - Return-window trigger on `https://www.brilliantearth.com/30-Day-Returns/` corrected from `"30 days from delivery"` to `"when your purchase is available for shipment or pickup"`.

---

## 3. Dataset C Live Sweep (`F28`)

- **Two new on-page contradictions caught:**
  - `SOL-05` / `R29` (Brilliant Earth Fairmined 2mm Six-Prong Solitaire `BE1FM0126`): in addition to the resizing contradiction (`SPEC3`), the Band Width selector prints **`Band Width: 2 ct. tw.`** (`1.5 ct. tw.` / `2 ct. tw.`), mislabelling millimeter width with carat total weight units.
  - `SOL-08` (Ross-Simons Item `251663`, a prong-set opal ring with a `10kt` vs `14kt` conflict): the page's own *Stone Story* section states **`"Opal sits at 5.5 to 6.5 on the Mohs scale, so that means bezel or halo, not prongs, on rings."`**
- **Ross-Simons 14K bands (`BND-04`–`BND-07`):** prices (`$400`, `$949`, `$1,195`, `$599`) and gram weights (`1.7g`, `4.2g`, `4.0g`, `2.1g`) confirmed verbatim; added Ross-Simons's on-page disclaimer `"All weights and measurements are approximate."` to every row's excerpt and assessment.
- **Menē 24K bands (`BND-01`–`BND-03`):** repointed `secondary_weight_source_url` from redirecting `/bands/gold` to `/collections/bands-gold` and direct product pages; noted that the gram figure sits inside Menē's client-side JS `Price breakdown` modal and documented the ~0.77% intraday bullion price movement on `2026-10-23` (`$1,720` → `$1,707`, `$1,556` → `$1,544`, `From $2,333` → `From $2,315`).

---

## 4. Open Change Requests (`CR-P3-1`..`CR-P3-9`) and Site Defects (`SD7`, `SD8`) Closed

- **`CR-P3-1`:** `R15`, `R16`, `R18` updated with sourced return terms from `S-RS` and `S-CB`, `POL1` removed from those rows, `RET11`/`RET12` attached, policy URLs added to `sources`, and Costco Document ID `CU2573` v18.0 (`10/02/2025`) added to `R10`.
- **`CR-P3-2`:** `PD1` removed from `R16` and retired from `data/flags.json`.
- **`CR-P3-3`:** `R18` `solid_gold_quote` scope labelled as product-image alt/title text.
- **`CR-P3-4`:** `RH1` (rhodium surface plating disclosure under 16 CFR 23.7) added to `R01`, `R03`, `R08`, `R09`.
- **`CR-P3-5` & `CR-P3-6`:** eCFR currency banner (`up to date as of 10/21/2026`), GovInfo `15 U.S.C. 297` link, and Costco `CU2573` v18.0 metadata added to `data/sources.json`.
- **`CR-P3-7`:** `scripts/verify.py` updated to permit `weight_status: "published as a range"` on a `null` weight; applied to `aurate-2ct-round-lgd-solitaire` (`Weight: 5.5-8.5g`).
- **`CR-P3-8` & `CR-P3-9`:** `data/verification.json` updated with Passes P5–P6 and checks `V38`–`V45`, and all 24 HTML pages rebuilt.
- **`SD7` & `SD8`:** Fixed stale nav/card counts (`Combined (71)`, `Flagged C (17)`), scoped the `index.html` melt-table footnote, and added `data-cats` attributes plus `Dataset C`, `24K`, and `Weight published` filter buttons to `combined.html`.
