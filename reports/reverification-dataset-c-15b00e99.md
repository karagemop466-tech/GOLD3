# Dataset C & Spot/Retailer Live Re-Verification Audit (`2026-10-23`)

- **Session:** `arena/15b00e99-gold3` (`DC1`)
- **Date (UTC):** `2026-10-23`
- **Zero-Hallucination Standard:** Every listing, policy page, BBB profile, Trustpilot profile, spot feed, and statutory citation in `data/bands-and-high-karat.json`, `data/solitaire-rings.json`, `data/sellers-policies.json`, `data/spot-and-standards.json`, `data/prices.json`, and `data/retailers.json` was fetched live on `2026-10-23`. Every unconfirmed or JS-gated figure was set to `null` and flagged.

## 1. Live Spot Gold Benchmarks (`2026-10-23`)

| Feed | Quote (USD / troy oz) | Gram Equivalent (24K) | Timestamp | URL |
|---|---:|---:|---|---|
| **Kitco Spot Bid / Ask** | `$4,022.70` / `$4,024.70` | `$129.3328/g` | Oct 23, 2026 05:56 EST | https://www.kitco.com/price/precious-metals |
| **BullionVault Wholesale** | `$4,024.23` | `$129.38/g` | Oct 23, 2026 05:57 EDT | https://www.bullionvault.com/gold-price-chart.do |
| **GoldPrice.org** | `$4,022.22` | `$129.3174/g` | Oct 23, 2026 05:55 NY Time | https://goldprice.org/ |
| **World Gold Council** | `$4,024.45` | `$129.3891/g` | Data as of 22 Oct 2026 (read 23 Oct) | https://www.gold.org/goldhub/data/gold-prices |

## 2. Irregularities, Hallucination Removals & Broken-Link Fixes

1. **Menē JS-Gated Gram Weights Nulled (`BND-01`..`BND-03`):** Live static HTML fetches of `mene-classic-band-gold` (`$1,707`), `mene-narrow-flat-band-gold` (`$1,544`), `mene-wide-flat-band-gold` (`$2,465`), and `/collections/bands-gold` confirm gram weights are injected client-side per ring size (`.json` endpoints return `404`). Set `weight_grams`, `net_gold_weight_grams`, `pure_gold_grams`, `melt_value_usd`, and `price_to_melt_ratio` to `null`.
2. **Menē 10% Return Restocking Fee & Dual BBB Files (`SEL-MENE`):** Verified on `https://support.mene.com/hc/en-us/articles/4407022465633-What-is-your-return-policy` that 7-day returns refunded to original payment incur a **10% restocking fee** (full value only in Menē Credit). Documented both BBB Ontario files (`0107-1413670` `D+`, 1 complaint / 0 reviews; `0107-1378080` `Not Rated`, 0 complaints / 2 reviews `1.0/5`).
3. **Unprinted PDP Hallmark Claims Stripped (`BND-01`..`BND-12`, `SOL-01`..`SOL-08`):** Confirmed none of the 21 Dataset C product pages print internal shank hallmark stamps in static HTML; separated brand-level guides (Menē 24k guide, Brilliant Earth stamp guide) from PDP disclosures.
4. **Mejuri `BND-10` Carat Contradiction:** Prose states `"2mm stones totaling 0.532ct"` while the Specifications list directly beneath prints `"Carat Weight: 0.044-0.056 ct"`.
5. **Brilliant Earth `SOL-05` & Policy Corrections:** Documented `"Width: 2 ct. tw."` unit bug and `"This ring can only be purchased with a diamond"` rule on `BE1FM0126`; updated `SEL-BRILLIANTEARTH` to reflect the **$40 engraving-removal return option on rings** (vs final-sale non-ring engraving), **$35 USD wire fee** on US/CA wires, and `283` BBB complaints / `4.45/5` (`342` reviews).
6. **Ring Concierge 7-Day Bridal Return Window:** Engagement-ring PDPs restrict ready-made engagement rings and wedding bands to a **7-day** return window (vs 30 days in the general Fine Jewelry policy) and list `info@ringconcierge.com`.
7. **Broken Statutory, Lab & Retailer URLs Fixed:**
   - Replaced HTTP `500` `uscode.house.gov/.../prelim@title15/chapter8` links with `https://www.govinfo.gov/content/pkg/USCODE-2023-title15/html/USCODE-2023-title15-chap8.htm`.
   - Fixed HTTP `404` `STD-05` URL (`...gold-plated-gold0` -> `https://www.gia.edu/gems-gemology/summer-2025-lab-notes-gold-plated-gold`).
   - Repointed HTTP `500` `catbirdnyc.com/contact-us` to live `https://www.catbirdnyc.com/facts` (`200 OK`).
