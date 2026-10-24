# Pass P17 — Dataset A, Seller-Policy & Anti-Inference Verification

**Date:** 2026-10-23
**Session / branch:** `arena/36ebce13-gold3`
**Evidence:** [`data/reverification-p17.json`](../data/reverification-p17.json)
**Combined ledger:** 253 checks across P1–P17

## No hallucinations — review commitment

**No hallucinations:** every confirmed value in this pass was read from the named official product/policy page or the identified independent review/market publisher. Missing values stay blank; conflicting statements stay flagged; no price, gram weight, carat, purity, availability, stone inclusion or solid construction was inferred. The deterministic security suite was run after the source review and again after integration.

## Result

- **31 checks:** 10 confirmed, 18 corrected, 3 flagged.
- **All 19 Dataset A listings re-read:** every stored numeric price confirmed; **0 price changes** and **0 published-weight changes**.
- **Combined verification ledger:** **253 checks** — 118 confirmed / 95 corrected / 40 flagged; all check IDs unique.
- **Published irregularities:** F50–F55. Existing Blue Nile Floral, Ring Concierge diamond and Aurate return/specification contradictions remain visible.
- **Final cited dead links in scoped reads:** 0. The one unqualified Aurate HTML 404 was replaced by a working official variant URL corroborated by two other official channels; no search snippet was used as price evidence.
- **Calculation anchor:** unchanged at **$4,022.22/oz**. Only the separately labelled live reference moved to **$3,995.88/oz**.

## Dataset A price register — all 19 rows freshly checked

| Check | Listing | Stored price (USD) | Outcome | Official product |
|---|---|---:|---|---|
| P17-01 | Aurate New York — 2ct Round Lab Grown Diamond Solitaire Ring | $2,858 | corrected | [official source](https://auratenewyork.com/products/2ct-round-lab-grown-diamond-solitaire-ring?variant=46776936792236) |
| P17-02 | Aurate New York — 2ct Emerald Lab Grown Diamond Solitaire Ring | $2,638 | corrected | [official source](https://auratenewyork.com/products/2ct-emerald-lab-grown-diamond-solitaire-ring?variant=46776938266796) |
| P17-03 | Aurate New York — 1ct Round Lab Grown Diamond Bezel Ring | $1,498 | corrected | [official source](https://auratenewyork.com/products/1ct-round-lab-grown-diamond-bezel-ring) |
| P17-04 | Aurate New York — 2ct Emerald Lab Grown Diamond Bezel Ring | $1,968 | corrected | [official source](https://auratenewyork.com/products/2ct-emerald-lab-grown-diamond-bezel-ring) |
| P17-05 | Aurate New York — 2ct Oval Lab Grown Diamond Solitaire Ring | $2,858 | corrected | [official source](https://auratenewyork.com/products/2ct-oval-lab-grown-diamond-solitaire-ring?variant=46776937513132) |
| P17-06 | Aurate New York — 3ct Oval Lab Grown Diamond Solitaire Ring | $3,958 | corrected | [official source](https://auratenewyork.com/products/3ct-oval-lab-grown-diamond-solitaire-ring?variant=44854218981548) |
| P17-07 | Aurate New York — 3ct Pear Lab Grown Diamond Bezel Ring | $2,498 | corrected | [official source](https://auratenewyork.com/products/3ct-pear-lab-grown-diamond-bezel-ring) |
| P17-08 | Blue Nile — Petite Solitaire Engagement Ring in 14k Yellow Gold | $1,000 | confirmed | [official source](https://www.bluenile.com/engagement-rings/design-your-own-ring/petite-solitaire-engagement-ring-in-14k-yellow-gold-item-195639) |
| P17-09 | Blue Nile — Petite Hidden Halo Solitaire Plus Diamond Engagement Ring in 14k Yellow Gold | $1,255 | corrected | [official source](https://www.bluenile.com/engagement-rings/design-your-own-ring/petite-hidden-halo-solitaire-plus-diamond-engagement-ring-in-14k-yellow-gold-item-192506) |
| P17-10 | Blue Nile — Riviera Pavé Diamond Engagement Ring in 14k White Gold (1/6 ct. tw.) | $1,500 | corrected | [official source](https://www.bluenile.com/engagement-rings/design-your-own-ring/riviera-pave-diamond-engagement-ring-in-14k-white-gold-1-6-ct-tw-item-195326) |
| P17-11 | Blue Nile — Floral Marquise Diamond Engagement Ring in 18k White Gold | $2,210 | flagged | [official source](https://www.bluenile.com/engagement-rings/design-your-own-ring/floral-marquise-diamond-engagement-ring-in-18k-white-gold-item-203738) |
| P17-12 | Blue Nile (By James Allen) — Criss Cross Solitaire Engagement Ring In 18K Yellow Gold By James Allen | $2,320 | confirmed | [official source](https://www.bluenile.com/engagement-rings/design-your-own-ring/criss-cross-solitaire-engagement-ring-in-18k-yellow-gold-by-james-allen-item-311132) |
| P17-13 | Mejuri — Diamonds Band | $648 | confirmed | [official source](https://mejuri.com/products/diamonds-band?Material=Solid+Yellow+Gold+%2814k%29&Stone=Natural+Diamond) |
| P17-14 | Mejuri — Stacker Ring | $138 | corrected | [official source](https://mejuri.com/products/stacker-ring?Material=Solid+Yellow+Gold+%2810k%29) |
| P17-15 | Ring Concierge — 2.08 Oval Lab Diamond in Whisper Thin® Hidden Halo | $6,038 | flagged | [official source](https://ringconcierge.com/products/2-08-oval-lab-diamond-in-whisper-thina-hidden-halo) |
| P17-16 | Ring Concierge — 2.72 Round Lab Diamond in Whisper Thin® | $7,268 | corrected | [official source](https://ringconcierge.com/products/2-72-round-lab-diamond-in-whisper-thina) |
| P17-17 | Catbird — Catbird Classic Wedding Bands, Solid Half Round Band, 2mm | $550 | corrected | [official source](https://www.catbirdnyc.com/catbird-classic-wedding-bands-solid-half-round-band-2mm.html) |
| P17-18 | Mejuri — Dôme Figure Ring (18k Gold Vermeil) | $158 | confirmed | [official source](https://mejuri.com/products/dome-figure-ring?Material=18k+Gold+Vermeil) |
| P17-19 | Mejuri — Dôme Figure Ring (Sterling Silver) | $138 | confirmed | [official source](https://mejuri.com/products/dome-figure-ring?Material=Sterling+Silver) |

“Confirmed” applies to the numeric price and the specifications stated in the detailed evidence below; it does not erase a separate live contradiction or an unverified field. Setting-only and from-prices retain their existing labels.

## Corrections published for review

### F50 — Aurate weight scope and current bezel specifications

The previous records asserted that diamond mass was included in the listed ring weight and even calculated stone grams. The seller does not state that relationship. Those assertions were removed. Current bezel dimensions and VS1/VS2 specification text replace the stale values; the three title/spec carat conflicts now have `carat: null`, and all ambiguous gram figures keep `weight_g: null`. The live final-sale/free-returns conflict remains flagged.

### F51 — Mejuri Stacker evidence

The current page says `Width: 1 mm`, not 1.3mm/1.35mm, and uses current “Our 10k solid gold…” materials wording. Official image alt text mentions a “10K purity stamp,” so the blanket no-hallmark flag was false. The replacement warning explicitly says that alt text is neither visual verification nor evidence of a maker’s mark.

### F52 — Ross-Simons approximate weights and solidity

BND-04–BND-07 no longer call seller-disclaimed approximate weights “exact.” Claims that customer reviews, weight or geometry prove solid construction were removed. Published weights, prices and melt arithmetic did not change. BND-04 freshly confirms **$400 / 1.7g / 14kt yellow gold / 2mm**.

### F53 — Mejuri return policy

The unsupported blanket exclusion for bespoke/made-to-order pieces and the stale JavaScript-only-page flag were removed. Current official terms require complete sets, same-country returns and the SCS certificate for lab-grown diamond returns; engraved/monogrammed, piercing-appointment earrings, gift cards and final-sale items remain excluded.

### F54 — Blue Nile and Ring Concierge source drift

Hidden Halo is now stock **502250y14 / 1.60mm**; Riviera is **501590w14 / 2.00mm**. Both Ring Concierge pages explicitly state **14K Yellow Gold with Platinum Prongs**, so the false karat-not-in-body flags were removed. Duplicate issue flags were consolidated, while the 2.08/5.63ct conflict and 7-day product-specific return wording remain.

### F55 — Four-feed spot corroboration

GoldPrice.org **$3,995.88**, Kitco bid **$3,994.90**, BullionVault **$3,995.74**, and the World Gold Council tile **$3,995.47** span **$0.98 (0.025%)**. Their own timestamps differ and are preserved verbatim. The dated calculation anchor was deliberately not overwritten.

## Values deliberately left unresolved

- Blue Nile Floral: title/spec 18K white gold versus details prose 14k yellow gold.
- Ring Concierge 2.08: header/details 2.08 E VS1 versus description 5.63 D VVS2; product-specific 7-day returns versus general 30-day policy.
- Aurate: title/spec carat differences on three bezels, clarity/width conflicts on solitaires, final-sale wording beside Free Returns, and undefined metal-only versus total-item weight scope.
- Mejuri Stacker: seller alt text mentions a purity stamp, but no visual hallmark or maker’s-mark verification is claimed.
- Ross-Simons: published weights remain approximate; mixed-karat BND-08 still has no inferred gram split or single-karat melt value.

## Line-by-line P17 evidence

| Check | Row(s) | Outcome | Evidence | Source |
|---|---|---|---|---|
| P17-01 | aurate-2ct-round-lgd-solitaire | corrected | Official 14k yellow size-2.5 variant prints $2,858 and Made to Order. Specs print Weight 5.5-8.5g and 2tcw separately; no stone inclusion is stated. Updated variant provenance/quote and removed stale from-price and duplicate final-sale/range flags. | [official source](https://auratenewyork.com/products/2ct-round-lab-grown-diamond-solitaire-ring?variant=46776936792236) |
| P17-02 | aurate-2ct-emerald-lgd-solitaire | corrected | Official 14k yellow size-2.5 variant prints $2,638 and Made to Order; Weight 5.5-8.5g and 2tcw are separate statements. Removed unsupported stone inclusion and retained the live VVS/VS/SI and 1.8mm/2.75mm conflicts. | [official source](https://auratenewyork.com/products/2ct-emerald-lab-grown-diamond-solitaire-ring?variant=46776938266796) |
| P17-03 | aurate-1ct-round-lgd-bezel | corrected | Official AU5000 page confirms $1,498; current Specs print Width 9.05mm, Thickness 5.04mm, Weight 2.23g, 1 Round VS1/VS2 diamond and 1.05tcw. Title says 1ct; carat is null and weight scope remains unverified. | [official source](https://auratenewyork.com/products/1ct-round-lab-grown-diamond-bezel-ring) |
| P17-04 | aurate-2ct-emerald-lgd-bezel | corrected | Official AU5093 page confirms $1,968; current Specs print Width 11.42mm, Thickness 4.6mm, Weight 2.36g, 1 Emerald VS1/VS2 diamond and 1.8tcw. Title says 2ct; carat is null. Body copy's 'classic oval diamond' conflict remains flagged. | [official source](https://auratenewyork.com/products/2ct-emerald-lab-grown-diamond-bezel-ring) |
| P17-05 | aurate-2ct-oval-lgd-solitaire | corrected | Official 14k yellow size-2.5 variant confirms $2,858, now Made to Order; Weight 5.7-8.7g and 2tcw are separate statements. Updated stale in-stock wording and removed unsupported stone inclusion. | [official source](https://auratenewyork.com/products/2ct-oval-lab-grown-diamond-solitaire-ring?variant=46776937513132) |
| P17-06 | aurate-3ct-oval-lgd-solitaire | corrected | Official 14k yellow size-3 variant confirms $3,958, now Made to Order; Weight 5.9-8.9g and 3tcw are separate statements. Updated stale in-stock wording and removed unsupported stone inclusion. | [official source](https://auratenewyork.com/products/3ct-oval-lab-grown-diamond-solitaire-ring?variant=44854218981548) |
| P17-07 | aurate-3ct-pear-lgd-bezel | corrected | Official AU5107 page confirms $2,498; current Specs print Width 15.92mm, Thickness 6.10mm, Weight 3.33g, 1 Pear VS1/VS2 diamond and 3.6tcw. Title says 3ct; carat is null and weight scope remains unverified. | [official source](https://auratenewyork.com/products/3ct-pear-lab-grown-diamond-bezel-ring) |
| P17-08 | bluenile-petite-solitaire-14k-yg | confirmed | Official PDP confirms $1,000 (Setting Price), 14K Yellow Gold, stock 500990y14 and width 1.60mm. Centre stone remains excluded; solid wording and gram weight remain unverified. | [official source](https://www.bluenile.com/engagement-rings/design-your-own-ring/petite-solitaire-engagement-ring-in-14k-yellow-gold-item-195639) |
| P17-09 | bluenile-petite-hidden-halo-14k-yg | corrected | Official PDP confirms $1,255 (Setting Price) and current stock 502250y14 / Width 1.60mm. Corrected stale stock 500850y14 / 1.70mm and pointed price_source to the exact PDP. | [official source](https://www.bluenile.com/engagement-rings/design-your-own-ring/petite-hidden-halo-solitaire-plus-diamond-engagement-ring-in-14k-yellow-gold-item-192506) |
| P17-10 | bluenile-riviera-pave-14k-wg | corrected | Official PDP confirms $1,500 (Setting Price) and current stock 501590w14 / Width 2.00mm. Corrected stale stock 501050w14 / 1.60mm and pointed price_source to the exact PDP. | [official source](https://www.bluenile.com/engagement-rings/design-your-own-ring/riviera-pave-diamond-engagement-ring-in-14k-white-gold-1-6-ct-tw-item-195326) |
| P17-11 | bluenile-floral-marquise-18k-wg | flagged | Official PDP confirms $2,210 (Setting Price), stock 502820w and Width 1.70mm. The same-page conflict between title/spec 18K White Gold and details prose 14k yellow gold remains live and flagged; no metal choice was inferred. | [official source](https://www.bluenile.com/engagement-rings/design-your-own-ring/floral-marquise-diamond-engagement-ring-in-18k-white-gold-item-203738) |
| P17-12 | bluenile-criss-cross-18k-yg | confirmed | Official PDP confirms $2,320 (Setting Price) for the James Allen Criss Cross setting. Stored price and setting-only treatment remain unchanged. | [official source](https://www.bluenile.com/engagement-rings/design-your-own-ring/criss-cross-solitaire-engagement-ring-in-18k-yellow-gold-by-james-allen-item-311132) |
| P17-13 | mejuri-diamonds-band | confirmed | Official variant confirms $648, Solid Yellow Gold (14k), Natural Diamond, minimum 0.07ct, SI-I clarity, GHI color, 1.8mm stone and 2.8mm shank. Gram weight remains unpublished/null. | [official source](https://mejuri.com/products/diamonds-band?Material=Solid+Yellow+Gold+%2814k%29&Stone=Natural+Diamond) |
| P17-14 | mejuri-stacker-ring-10k | corrected | Official variant confirms $138, Solid Yellow Gold (10k), materials 'Our 10k solid gold...', and Width 1 mm. Removed stale 1.3mm/1.35mm dimensions and old quotation. Alt text mentions a 10K purity stamp, but no visual or maker's-mark verification is claimed. | [official source](https://mejuri.com/products/stacker-ring?Material=Solid+Yellow+Gold+%2810k%29) |
| P17-15 | ringconcierge-2-08-oval-lab-whisper-thin | flagged | Official PDP confirms $6,038 and Metal: 14K Yellow Gold with Platinum Prongs. Header/details say 2.08 E VS1 while description says 5.63 D VVS2; conflict remains flagged. Removed false karat-not-in-body flag, duplicate metal/production flags and stale product-level 30-day wording; 7-day FAQ remains. | [official source](https://ringconcierge.com/products/2-08-oval-lab-diamond-in-whisper-thina-hidden-halo) |
| P17-16 | ringconcierge-2-72-round-lab-whisper-thin | corrected | Official PDP confirms $7,268, 2.72 E VVS2, IGI, Metal: 14K Yellow Gold with Platinum Prongs and the 7-day ready-made return FAQ. Removed false karat-not-in-body flag and consolidated duplicate metal/production flags. | [official source](https://ringconcierge.com/products/2-72-round-lab-diamond-in-whisper-thina) |
| P17-17 | catbird-classic-half-round-2mm | corrected | Official PDP confirms 'from $550.00' and official 14k yellow-gold image text. No usable gram weight is published, so the unsupported 'lowest markup route' note was replaced with a factual no-ranking statement. | [official source](https://www.catbirdnyc.com/catbird-classic-wedding-bands-solid-half-round-band-2mm.html) |
| P17-18 | mejuri-dome-figure-vermeil | confirmed | Official variant confirms $158 and 18k Gold Vermeil; top width 5.8mm, top height 3.5mm and shank thickness 2mm. It remains excluded from solid-gold categories; no gold weight is inferred. | [official source](https://mejuri.com/products/dome-figure-ring?Material=18k+Gold+Vermeil) |
| P17-19 | mejuri-dome-figure-sterling | confirmed | Official variant confirms $138 and Sterling Silver; top width 5.8mm, top height 3.5mm and shank thickness 2mm. It remains an explicit no-gold control. | [official source](https://mejuri.com/products/dome-figure-ring?Material=Sterling+Silver) |
| P17-20 | aurate | confirmed | Official help centre confirms 15-day domestic / 21-day international windows and final-sale/exchange-only exclusions. Listing-specific final-sale wording remains controlling; Trustpilot's separate company-description 'FREE RETURNS' claim is not used to override it. | [official source](https://auratenewyork.gorgias.help/en-US/articles/returns-38636) |
| P17-21 | blue-nile | confirmed | Official policy confirms 30 days from shipment, original unworn condition, resized/custom/engraved/final-sale exclusions, RMA requirement and two complimentary returns per customer per year. | [official source](https://www.bluenile.com/policies/returns) |
| P17-22 | mejuri | corrected | Official FAQ and full terms confirm free 30-day returns in five named countries. Removed unsupported blanket bespoke/made-to-order exclusion and stale JavaScript-only flag; added complete-set, same-country and SCS-certificate requirements. | [official source](https://mejuri.com/company/returns-terms) |
| P17-23 | ring-concierge | flagged | General policy still says 30 days on most Fine Jewelry, while both engagement PDPs say 1 week (7 days) for eligible ready-made rings and final sale after customization/resizing. The stricter product-specific window remains recorded. | [official source](https://ringconcierge.com/policies/refund-policy) |
| P17-24 | catbird | corrected | Official returns page confirms 20 days, $9 return-shipping deduction and international/final-sale exclusions. Official Facts page confirms 'Catbird's solid gold is never plated'; corrected the source attribution from Trustpilot to Catbird's own page. | [official source](https://www.catbirdnyc.com/returns) |
| P17-25 | aurate | corrected | Trustpilot displays 4,876 reviews and TrustScore 4.1. Corrected the quote's stale 4,875 count; retained the claimed-profile and 98% negative-review response context. Trustpilot says it does not fact-check reviewer claims; AI-summary themes are labelled as reviewer allegations, not verified facts. | [independent market/review source](https://www.trustpilot.com/review/auratenewyork.com) |
| P17-26 | blue-nile | corrected | Trustpilot displays 1,937 reviews and TrustScore 4.0, with 97% negative-review responses. Updated from 1,932/1,928 and 99%. Trustpilot says it does not fact-check reviewer claims; AI-summary themes are labelled as reviewer allegations, not verified facts. | [independent market/review source](https://www.trustpilot.com/review/www.bluenile.com) |
| P17-27 | mejuri | corrected | Trustpilot displays 5,785 reviews and TrustScore 4.3, with 98% negative-review responses. Updated from 5,784/5,781 and 99%. Trustpilot says it does not fact-check reviewer claims; AI-summary themes are labelled as reviewer allegations, not verified facts. | [independent market/review source](https://www.trustpilot.com/review/mejuri.com) |
| P17-28 | ring-concierge | confirmed | Trustpilot still displays only 7 reviews, TrustScore 2.7 and an unclaimed profile with no history of asking for reviews; the tiny non-representative sample warning remains. Trustpilot says it does not fact-check reviewer claims; AI-summary themes are labelled as reviewer allegations, not verified facts. | [independent market/review source](https://www.trustpilot.com/review/ringconcierge.com) |
| P17-29 | catbird | confirmed | Trustpilot displays 56 reviews and TrustScore 2.2, claimed profile, 82% negative-review responses and no recent history of asking for reviews. Counts and score match the stored record. Trustpilot says it does not fact-check reviewer claims; AI-summary themes are labelled as reviewer allegations, not verified facts. | [independent market/review source](https://www.trustpilot.com/review/catbirdnyc.com) |
| P17-30 | BND-04, BND-05, BND-06, BND-07 | corrected | Item 571221 freshly confirms $400, 14kt Yellow Gold, 2mm and approximate Gold Weight 1.7 grams; sizes 5-9 are shown in stock. BND-04–BND-07 no longer call approximate weights exact, and weight/geometry/customer reviews are no longer used as proof of solid construction. No price, weight or melt value changed. | [official source](https://www.ross-simons.com/products/571221) |
| P17-31 | spot | confirmed | GoldPrice.org displayed $3,995.88/oz at label '07:41 NY Time'; Kitco bid $3,994.90 at '19:43 NY Time'; BullionVault $3,995.74 at '17:00:00 (GMT-04:00)'; WGC tile $3,995.47 with its historical dataset labelled 22 October. Numeric spread $0.98 (0.025%). Only the labelled live reference changed; primary $4,022.22/oz and all melt arithmetic remain fixed. | [independent market/review source](https://goldprice.org/) |

## Final gates

| Gate | Result |
|---|---|
| `verify.py` | **PASS** — 0 errors / 0 warnings / 12 disclosed notes |
| `verify_dataset_c.py` | **PASS** — 21 rings, 5 published weights, 16 null/unverified, 0 dead links |
| Both static builders | **PASS** — 18 unified pages plus Dataset C pages; internal links/styles/product URLs OK |
| `audit.py` | **PASS** — 31 rows, 0 errors / 0 warnings / 176 checks |
| `run_security_audit.py` | **PASS #40 + read-back clean-tree PASS** — SEC-01…SEC-07; SEC-06 checked 2,364 links/anchors |
| `render-test.js` | **PASS** — 165/165, including nine P17 regression guards |
| `report_verify.py` | **PASS** — 253 checks rendered |
| Root HTML official-link gate | **PASS** — 1,037/1,037 table rows carry an HTTPS source link |
| Archive suite | **PASS** — 7/7; 156 internal and 270 external links |
| JSON parse + `git diff --check` | **PASS** |

## Recommended next hallucination hunt

During P18, read the generated pages back against the JSON and deployed HTML, especially the landing-page “No hallucinations” summary, all 253 verification rows and F50–F55. Then independently sample the remaining Dataset B/C published-weight rows and any current prose mentioning availability, “exact” weight or stone inclusion. Confirm that removed claims do not survive in generated pages, refresh the live spot reference if the market has moved, and rerun the deterministic security suite after that review.
