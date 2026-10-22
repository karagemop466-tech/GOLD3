# Verification report

- Pass date: **2026-10-22**
- Session: `arena/e6fe3e4f-gold3`
- URLs opened: **28** — confirmed 15, corrected 8, flagged 5

## Method

Every URL cited in data/rings.json, data/sellers.json and data/gold-price.json was opened again in this session on 2026-10-22. Each asserted value was compared against the text the page returned. A value that could not be found on the page was deleted or downgraded to unverified; a value that contradicted the page was corrected; a contradiction found on the page itself was raised as a flag.

## Passes

| # | Pass | What it did | Result |
|---|---|---|---|
| P1 | Fact pass | For every row, each stored number and quote was searched for in the freshly fetched page text. | 22/22 rows re-read; 9 rows corrected; 3 rows added. |
| P2 | Request pass | Checked that every row's product URL returns the product it claims to be — not a redirect to something else, not a sold-out placeholder, not a dead link. | 1 redirect (R17), 1 sold-out/back-order state (R18), 1 identifier mismatch (R10), 0 dead links. |
| P3 | Internet pass | Each cited URL was opened rather than trusted: host checked against the seller's own domain, and the exact wording quoted. | 28 URLs opened; 0 unreachable; 0 off-domain citations. |
| P4 | Hallucination pass | Deliberately hostile re-read: any figure that felt plausible but was not literally on the page was removed. This is what caught the 'white/rose gold & platinum also offered' phrases on five Blue Nile rows and two Mejuri rows. | 7 metal-option claims deleted; 1 price basis corrected; 1 temporary provenance flag retired. |

## Checks

| ID | Source | Rows | Outcome | What the page said |
|---|---|---|---|---|
| V01 | [Gold spot price used by every calculation](https://www.gold.org/goldhub/data/gold-prices) | spot | **confirmed** | Page printed "4,024.36" USD/oz with "Data as of 21 October, 2026" and the ICE Data Services attribution. The stored 4,024.36 and the market date match exactly. |
| V02 | [Mejuri — Bold Diamond Eternity Ring](https://mejuri.com/products/bold-diamond-eternity-ring) | R01 | **corrected** | "From $2,900"; Material "Solid White Gold (14k)"; description "handcrafted in 14k solid gold featuring as many as 23 round brilliant cut diamonds". No gram weight anywhere on the page. The row's "(also offered in yellow gold)" parenthetical is not on the page and was deleted. |
| V03 | [Mejuri — Bold Diamond Half Eternity Ring](https://mejuri.com/products/bold-diamond-half-eternity-ring) | R02 | **corrected** | "$1,500"; "Solid Yellow Gold (14k)"; "14k solid gold". Confirmed, but the row had been priced off the collection page; the basis was corrected to product-level and the quote replaced. Page also shows "Only a few left". |
| V04 | [Mejuri — Slim Diamond Eternity Band (collection listing)](https://mejuri.com/collections/milestone-rings) | R03 | **corrected** | Collection grid printed "Slim Diamond Eternity Band From $648 Solid White Gold (14k), Natural Diamond". The product page itself was not opened, so the row stays listing-level, and the "(yellow gold also listed)" parenthetical was deleted because this page does not list it. |
| V05 | [Mejuri — Aurora Lab Grown Sapphire Eternity Ring](https://mejuri.com/products/aurora-lab-grown-sapphire-eternity-ring) | R04 | **confirmed** | "$228"; Material "18k Gold Vermeil, Lab Grown White Sapphire"; seller's own spec: "a thick layer of 18k solid gold plated on 91% recycled sterling silver". Vermeil, so it fails the solid-gold test. |
| V06 | [Mejuri — Duet Mixed Ring](https://mejuri.com/products/duet-mixed-ring) | R19 | **corrected** | "$178"; "18k Gold Vermeil, Sterling Silver". Verified live this pass, so the temporary L3 provenance flag was removed and price_usd moved into the verified set. |
| V07 | [Mejuri — standard return policy](https://mejuri.com/faq/return-exchanges/what-is-the-standard-return-policy) | R01, R02, R03, R04, R19 | **confirmed** | "free 30-day returns for customers in the US ..."; non-returnable list includes "Engraved and monogrammed products" and final-sale items. Product pages add that engraving is "not eligible for returns". |
| V08 | [Blue Nile — Petite Hidden Halo Solitaire Plus (item 192506)](https://www.bluenile.com/engagement-rings/design-your-own-ring/petite-hidden-halo-solitaire-plus-diamond-engagement-ring-in-14k-yellow-gold-item-192506) | R05 | **corrected** | "$1,255 (Setting Price)"; "Metal Type: 14K Yellow Gold"; Stock 502250y14. The stored claim that white/rose gold and platinum are "also offered" is not on the page, so that parenthetical was deleted. |
| V09 | [Blue Nile — Petite Solitaire (item 195639)](https://www.bluenile.com/engagement-rings/design-your-own-ring/petite-solitaire-engagement-ring-in-14k-yellow-gold-item-195639) | R06 | **corrected** | "$1,000 (Setting Price)"; "Metal Type: 14K Yellow Gold"; Stock 501130y14. Same unsupported metal-options parenthetical removed. |
| V10 | [Blue Nile — Criss Cross Solitaire by James Allen (item 311132)](https://www.bluenile.com/engagement-rings/design-your-own-ring/criss-cross-solitaire-engagement-ring-in-18k-yellow-gold-by-james-allen-item-311132) | R07 | **corrected** | "$2,320 (Setting Price)"; "Metal Type: 18K Yellow Gold"; Stock 505032y. Metal-options parenthetical removed. |
| V11 | [Blue Nile — Floral Marquise (item 203738)](https://www.bluenile.com/engagement-rings/design-your-own-ring/floral-marquise-diamond-engagement-ring-in-18k-white-gold-item-203738) | R08 | **flagged** | "$2,210 (Setting Price)"; "Metal Type: 18K White Gold"; "Rhodium Finish: Yes"; Stock 502820w. The product description on the same page says the ring is "artfully crafted from warmly lustrous 14k yellow gold" — a direct self-contradiction. New flag SPEC1. The unsupported metal-options parenthetical on this row was also deleted. |
| V12 | [Blue Nile — Riviera Pavé (item 195326)](https://www.bluenile.com/engagement-rings/design-your-own-ring/riviera-pave-diamond-engagement-ring-in-14k-white-gold-1-6-ct-tw-item-195326) | R09 | **corrected** | "$1,500 (Setting Price)"; "Metal Type: 14K White Gold"; "Rhodium Finish: Yes"; Stock 501590w14. Metal-options parenthetical removed. |
| V13 | [Blue Nile — Classic Simple Solitaire (item 195730)](https://www.bluenile.com/engagement-rings/design-your-own-ring/classic-simple-solitaire-engagement-ring-in-14k-white-gold-item-195730) | R14 | **confirmed** | "$1,145 (Setting Price)"; "Metal Type: 14K White Gold"; "Rhodium Finish: Yes"; Stock 502120w14. Matches the 2026-10-22 integration record exactly. |
| V14 | [Blue Nile — return policy](https://www.bluenile.com/policies/returns) | R05, R06, R07, R08, R09, R14 | **confirmed** | "within 30 days from the shipment date for a full refund or exchange"; exclusions include "Personalized jewelry, custom orders, engraved items, items resized after initial purchase ... clearance items and 'Final Sale' items"; "Two complimentary returns are allowed per customer, per year"; one free resize within 6 months if the design permits. |
| V15 | [Costco — 0.50 ctw diamond 14kt band](https://www.costco.com/p/-/round-brilliant-050-ctw-vs2-clarity-i-color-diamond-14kt-gold-band/100675127) | R10 | **flagged** | No price is displayed on the page as fetched, so the row's price stays blank. "Metal: 14kt White Gold ( Rhodium Plated ) or 14kt Yellow Gold". No gram weight. The page prints "Item 1596365" while the URL ends in 100675127 — new flag ID1. |
| V16 | [Costco — official return policy answer (Document ID CU2573, version 18.0, published 10/02/2025)](https://customerservice.costco.com/app/answers/detail/a_id/1191) | R10 | **confirmed** | Under the satisfaction guarantee's exceptions: "Precious metals are non-refundable." That is what makes this listing fail your return requirement. |
| V17 | [Wilson's Estate Jewelry — Mid-Century Old European solitaire](https://www.wilsonsestatejewelry.com/products/mid-century-old-european-diamond-14-karat-white-gold-vintage-solitaire-engagement-ring) | R11 | **confirmed** | "Sale price$3,725.00"; "Stamped for 14 karat gold"; "Total Weight: 6.1 grams"; Stock We-16935. No maker's mark is stated on this page. |
| V18 | [Wilson's Estate Jewelry — Art Deco Lotus (GIA)](https://www.wilsonsestatejewelry.com/products/art-deco-old-mine-cut-diamond-18-karat-white-gold-antique-lotus-engagement-ring-gia) | R12 | **confirmed** | "Sale price$5,350.00"; "Stamped for 18 karat gold"; "With partial maker's mark for Hedges & Co."; "Total Weight: 2.2 grams"; GIA Dossier 2215945495; Stock We-17036. |
| V19 | [Wilson's Estate Jewelry — Bailey Banks & Biddle 19K](https://www.wilsonsestatejewelry.com/products/bailey-banks-biddle-art-deco-diamond-enamel-19-karat-white-gold-vintage-fanning-engagement-ring) | R13 | **confirmed** | "Sale price$2,850.00"; "Stamped for 19 karat gold"; signed with a maker's mark for Bailey Banks & Biddle. No gram weight is stated on the page, so the cell stays blank. |
| V20 | [Ross-Simons — 2mm 18kt polished ring](https://www.ross-simons.com/products/985230) | R15 | **confirmed** | "$249", sizes 5-10 all "In-Stock"; spec block: "Metal 18kt Yellow Gold", "Gold Weight 0.7 grams", plus "All weights and measurements are approximate." |
| V21 | [Ross-Simons — Italian 14kt diamond-cut ring](https://www.ross-simons.com/products/932728) | R16 | **confirmed** | "$299", sizes 5-10 all "In-Stock"; "Metal 14kt Yellow Gold", "Gold Weight 0.8 grams"; page offers a 14kt white gold alternative (item 932726). |
| V22 | [Tiffany & Co. — The Tiffany Setting in 18k yellow gold](https://www.tiffany.com/engagement/engagement-rings/the-tiffany-setting-engagement-ring-in-18k-yellow-gold-GRP10863/) | R17 | **flagged** | "Starting from $1,600"; "Ring Style 18k Yellow Gold and Platinum"; "Availability: This product is currently unavailable"; "this item is non returnable" and "this item can only be exchanged". The URL redirected to /jewelry/rings/18k-rose-gold-and-platinum-diamond-rings-1712.html — new flag RDR1. |
| V23 | [Tiffany & Co. — return policy](https://www.tiffany.com/policy/return-policy.html) | R17 | **confirmed** | General policy: "Products are accepted for credit or exchange in the U.S. within 30 days of purchase", with "Personalized, altered, or engraved items are not eligible". It does not override the product page's own non-returnable statement, which is the narrower and controlling note for this ring. |
| V24 | [Catbird — Woodland Ring (Sofia Zakia)](https://www.catbirdnyc.com/woodland-ring.html) | R18 | **confirmed** | "$276.00 Regular Price$368.00", title "Woodland Ring in 14K Gold". Sold-out / waitlist badges are rendered on the page. No return policy and no gram weight on the page read. |
| V25 | [Sarraf.com — 14k white gold solitaire 0.94 ctw (new row R20)](https://www.sarraf.com/products/14k-white-gold-solitaire-ring-0-94-ctw.html) | R20 | **confirmed** | "Now: US$3,004.00" (MSRP US$11,683.00, Was US$3,513.00); "Material: 14K Solid Gold"; "Approximate Metal Weight: 3.80 grams"; SKU 238401-102 / Stock 147370; return clause of 30 days on the same page. The page also states the weight carries a ±5% tolerance. |
| V26 | [Sarraf.com — 10k 6mm comfort-fit band (new row R21)](https://www.sarraf.com/products/10k-gold-6mm-high-polished-comfort-fit-wedding-band.html) | R21 | **flagged** | "Now: US$613.00"; "Material: 10K Solid Gold"; "Approximate Metal Weight: 8.30 grams"; SKU IB-PBWB06-10KY / Stock 142684. Explicit caveat: "The weight listed is an approximate weight of a ring in size 10" — new flag WT4, because a size-5 buyer gets less metal than 8.30 g. |
| V27 | [Automic Gold — 3ct radiant lab diamond cathedral ring (new row R22)](https://www.automicgold.com/products/radiant-cut-lab-diamond-cathedral-ring) | R22 | **flagged** | "$3,074"; "Solid 14k Gold and 950 Platinum"; "Item Weight: Approximately 5.4g for gold or 8.1g for platinum"; "Free returns (US only)"; "All engraved items are final sale". New flags WT5 (one weight spans two metals) and POL2 (engraving kills the return). |
| V28 | [16 CFR Part 23 — FTC jewellery guides](https://www.ecfr.gov/current/title-16/chapter-I/subchapter-B/part-23) | standards | **confirmed** | eCFR states "Displaying title 16, up to date as of 10/21/2026". The sections this project cites all exist with the titles used: §23.3 gold content, §23.4 vermeil, §23.7 rhodium surface layer, §23.8 multiple precious metals, §23.10 quality marks, §23.18 weight and total weight. |

## Irregularities raised

| Row | What is irregular | Flag | Severity |
|---|---|---|---|
| R08 | Title/spec say 18K White Gold; the same page's description says 14k yellow gold. | `SPEC1` | medium |
| R17 | Product URL redirects to a different product path; page content still matches the ring. | `RDR1` | low |
| R10 | URL ends in 100675127, page prints "Item 1596365". | `ID1` | low |
| R21 | 8.30 g is stated to be the weight of a size 10 ring, while sizes 3-16 are sold. | `WT4` | medium |
| R22 | One weight line covers both 14k gold (5.4 g) and platinum (8.1 g). | `WT5` | medium |
| R20,R21 | Weights are explicitly approximate, with a stated ±5% tolerance. | `WT3` | medium |
| R17 | Product page says non-returnable and exchange-only, while the brand's general policy advertises 30-day returns. | `RET6` | high |
| R10 | Costco's official policy lists precious metals as non-refundable. | `RET1` | high |

## Deliberately not re-checked

- https://www.bluenile.com/engagement-rings — Collection page cited by four rows as context only; the product pages themselves were re-fetched and they carry every value used.
- https://www.lbma.org.uk/prices-and-data/lbma-precious-metal-prices — LBMA states its historical benchmark tables are licence-gated, so no LBMA figure is used anywhere in this project. The claim itself was not re-opened this pass.

## What no website can verify

- true karat of the actual object (needs XRF/assay)
- authenticity of a stamp
- hidden repairs on estate pieces
- seller complaint history

## Standing recommendation

Re-run `python3 scripts/audit.py` after every review, then repeat the hallucination pass by hand: pick any number in the dataset and try to find it on the linked page. If it is not there, delete it and mark the field unverified.
