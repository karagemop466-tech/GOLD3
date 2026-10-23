# Re-verification pass P3 — third independent live read of this repository

**Session** `arena/699d8e05-gold3` · **branch** `arena/699d8e05-gold3` · **date** 2026-10-22 (UTC)
**Repository state when the pass started** `main @ cdf62fd` — 22 Dataset-B rows, 19 Dataset-A products, 10 sellers, 13 retailers
**Machine-readable record** [`data/reverification-p3.json`](../data/reverification-p3.json) (38 checks, each with the verbatim evidence)
**Board entry** [`COORDINATION.md`](../COORDINATION.md) §1 row `V5`, §3 log, §4 change requests `CR-1`…`CR-9`

> **The rule this pass was run against** — the one printed in the banner at the top of the site's front page:
> *every number here was read off an official seller or government page and is linked; where a seller does not
> publish a value, the cell is empty and flagged, and it is never filled in with a guess.*
>
> This pass applied that rule **in both directions**. It filled empty cells only from official pages, and it also
> **deleted a number that a source did not support** and **corrected a claim that a source contradicted**.

**Method.** Every URL in §8 was opened live with a page reader on 2026-10-22 — no cached copies, no search-result
snippets, no recalled text. Each value this repository stores for that target was then searched for in the returned
text. Found verbatim → `confirmed`. Wrong, unsupported, or missing where the source does state it → `corrected`.
True but adverse → `flagged`. Nothing was averaged, rounded, or filled in from what a retailer usually says.

**Result:** 38 URLs opened · **26 confirmed · 8 corrected · 4 flagged** · 1 stored value deleted as unsupported ·
2 sellers' return policies moved from "Not verified" to sourced terms · 6 new findings (`F13`–`F18`) · 4 new flags
(`RET8`, `RET9`, `WAR1`, `SPEC2`) · 1 flag rewritten (`RET7`).

**Gates after the pass** (run in this order): `scripts/verify.py` **PASS** (0 errors / 0 warnings / 11 notes) ·
`scripts/audit.py` **rows=22 errors=0 warnings=0 passed=124** · `scripts/render-test.js` **110/110**.

---

## 1. The hallucination this pass found: a true fact about one seller, attached to another

`data/flags.json` → flag **`RET7`** read:

> "Sarraf accepts returns within 30 days of receipt … **A cancelled order is charged a 3% card-processing fee
> (Wilson's terms state the same fee structure).**"

Sarraf's return policy was read **end to end** on the live page
([sarraf.com — 14k White Gold Solitaire Ring 0.94 ctw., return-policy block](https://www.sarraf.com/products/14k-white-gold-solitaire-ring-0-94-ctw.html#return-policy)).
**There is no 3% fee in it.** The fees Sarraf actually publishes are:

| What Sarraf's page says (verbatim) | Where |
|---|---|
| "Engraving and shipping Charges are nonrefundable" | return policy |
| "the $25.00 engraving fee is non-refundable" | return policy, engraved-ring question |
| "All jewelry returned for repair or replacement are subject to a Shipping and handling fee of $100.00 or 10% of purchase price which ever amount is greater." | warranty conditions |

The 3% fee **is real — but it is Wilson's**, confirmed verbatim on Wilson's own product page
([wilsonsestatejewelry.com](https://www.wilsonsestatejewelry.com/products/mid-century-old-european-diamond-14-karat-white-gold-vintage-solitaire-engagement-ring)):

> "Please note that orders cancelled prior to shipment will not be refunded for credit card processing fees
> incurred at the rate of **3%**."  *(stated twice on that page — domestic and international returns)*

**Action taken.** `RET7` was rewritten from Sarraf's own words, a `correction_note` on the flag records the
transplant and both sources, and the incident is published as **finding `F15`**. Nothing else was softened.

**Why this matters more than the 3%.** This is the failure mode the whole project exists to catch, in its most
convincing form: the sentence was *true*, *specific*, *numerical* and *plausible* — it was simply about a different
company. A pass that only checks "is this number on the page it is cited to?" misses it, because the number **was**
on a page this project had read. It was caught by reading one policy to the end instead of trusting a summary of it.

---

## 2. Two sellers moved from "Not verified" to sourced terms

Both records said *"Not verified — no official return-policy page was captured"* and carried flag `POL1`. Both
official pages exist and were read. `POL1` now applies only to James Allen, whose product URLs redirect to Blue Nile.

### Ross-Simons — [returns & exchanges](https://www.ross-simons.com/pages/returns-exchanges) · [customer care](https://www.ross-simons.com/pages/customer-care)

| Field | Now recorded (verbatim where quoted) |
|---|---|
| Return window | "**30-Day No-Risk Return Guarantee**" — "**30 days from the date you receive your order**"; "(shipping and handling charges are non-refundable)"; refunds processed within 4 business days |
| Fee | "a flat fee of **$4.95** for return shipping and handling" → new flag `RET8` |
| Exclusions | "Items must be returned in original, unused condition." · "**Merchandise that has been damaged, altered, or resized by a jeweler other than Ross-Simons cannot be accepted for return.**" → new flag `RET9` · gift returns are merchandise credit |
| Resize | no resize service offered on the returns page; a third-party resize voids the return |
| Phone | **800-835-0919**, 7 days a week 7:00am–11:00pm ET (stored as `+1-800-835-0919`; the printed form is kept in `phone_as_printed`) |
| Email | **customerservice@ross-simons.com** |
| Return address | 9 Ross Simons Dr., Cranston, RI 02920 |

### Catbird — [returns](https://www.catbirdnyc.com/returns) · [contact](https://www.catbirdnyc.com/contact-us)

| Field | Now recorded (verbatim where quoted) |
|---|---|
| Return window | "…for a refund or credit **within 20 days of the date your package was delivered**"; in-store purchases are store credit only, within 20 days |
| Fee | "**An $9 charge for return shipping will be deducted from your refund**" → `RET8` |
| Final sale | special orders, engraved items, Forever jewelry, earrings from piercing events, home & beauty, comestibles; "**All international sales are final.**" |
| Resize / repair | "**We can only accept repairs or resizing on jewelry bought from Catbird.**" |
| Email | **customerservice@catbirdnyc.com** ("Order Status, Availability, Product Details or Shipping Questions") |
| Phone | **left empty — none is published.** The contact page directs customers to a form ("We strive to respond to all emails within 24-48 hrs") and one channel even says "No phone calls please" |
| Address | Catbird, 141 Flushing Avenue, Suite 903, Brooklyn, NY 11205 |

**Cross-dataset inconsistency this exposed (`F17`).** `data/retailers.json` (Dataset A) already carried Catbird's
20-day window, $9 fee and final-sale list, quoted from the same URL — while `data/sellers.json` (Dataset B) said
"Not verified" for the same company. Two datasets describing one retailer had drifted apart. They now agree, and the
residual risk is recorded: any future policy edit has to be applied to both files.

**Also closed for Automic Gold (`F16`).** Its record said only "Free returns stated on the product page, US only".
The same page's Shipping & Returns section states: "**Returns can be made within 30 days of the delivery date. Free
return shipping on US orders. Engraved items are final sale and cannot be returned.**" — now stored verbatim
([product page](https://www.automicgold.com/products/radiant-cut-lab-diamond-cathedral-ring)).

---

## 3. The three newest rows, re-fetched by a second session

`R20`, `R21` and `R22` were added to Dataset B by another session earlier the same day. They are the only rows in
the study carrying fresh gram weights, which makes them the highest-value target for an independent read.
**Every stored value matched the live page verbatim.**

| Row | Stored | Live page (2026-10-22) | Verdict |
|---|---|---|---|
| `R20` Sarraf 14k WG solitaire | $3,004 · 3.80 g · "14K Solid Gold" | "Now: US$3,004.00" · "Approximate Metal Weight: 3.80 grams" · "Material: 14K Solid Gold" · 0.94 Ct · G · I 1 · Natural · SKU 238401-102 | confirmed |
| `R21` Sarraf 10k 6mm band | $613 · 8.30 g · "10K Solid Gold" | "Now: US$613.00" · "Approximate Metal Weight: 8.30 grams" · "Material: 10K Solid Gold" · "The weight listed is an approximate weight of a ring in size 10 Made in the USA" | confirmed (`WT4` is verbatim on the page) |
| `R22` Automic radiant | $3,074 · 5.4 g · "Solid 14k gold" | "$3,074" · "Item Weight: Approximately **5.4g for gold or 8.1g for platinum**" · "Material: 950 platinum and/or Solid 14k gold" | confirmed (`WT5` is right: 5.4 g is the gold version) |

Two things the pages state that the records did **not** carry, now added:

* **Sarraf's warranty is not free.** "…subject to a Shipping and handling fee of **$100.00 or 10% of purchase price
  which ever amount is greater**", original invoice required, chipped or missing stones excluded, "**Third Party
  alteration to the jewelry will automatically void the Lifetime Guarantee**", normal wear and tear excluded, and
  "*Sarraf reserves the right to modify this policy at any time and without notice*". → new flag **`WAR1`**.
* **Sarraf's tolerance note, found verbatim** (this is the source of `WT3`): "…due to factors beyond our control it is
  impossible to be exact each and every time, therefore **we strive to maintain an accuracy of ± 5%**."
* **Automic states its lead time two different ways on one page**: "Production time is **4-8 business days**" in the
  buy box vs "Production time is **1-2 weeks**. If you are adding engraving, production time is **2-3 weeks**." in the
  policy section. Both are recorded; neither was chosen. → new flag **`SPEC2`**.

---

## 4. Dataset A rows corrected

### `aurate-2ct-round-lgd-solitaire` — [live listing](https://auratenewyork.com/products/2ct-round-lab-grown-diamond-solitaire-ring)

| Field | Was | Now (and why) |
|---|---|---|
| `price_type` / `price_quote` / `price_source` | `from` · "From $2,858" · a collection page | `listed` · "$2,858" · the product page. The live page shows **$2,858 against a named in-stock variant**: "Rate - 14k GOLD", "Color - Yellow", "Size - 7", "In Stock • Ready to Ship" |
| `weight_status` note | "No ring weight in grams on the listing" | **The listing does publish one**: specs block "**Weight: 5.5-8.5g**". `weight_g` **stays null** — a 3 g range spanning the 14k / 18k / platinum versions is not this ring's weight, and a midpoint would be an invented number. The false note is corrected (`F14`) |
| returns | nothing at row level | The listing carries "**Exchange for size only.**" and "**Final Sale!**", both linking to Aurate's exchange-only terms — **while the same page shows a "Free Returns" badge** and "Lifetime Warranty" (`F13`, high) |
| self-contradiction | not recorded | Band width: copy says "a refined **1.8mm** width", specs say "Width: **2.75mm** / Thickness: 1.8mm". Clarity: copy says "**VVS** clarity", specs say "1 Round **VS**/EF", a quality badge says "**SI** Clarity Only". All three recorded verbatim, none chosen |
| documentation | absent | "All of our engagement diamond solitaire rings come with a certificate … run through one of two accredited institutions: **The Gemological Institute of America or The International Gemological Institute**. Trust but verify, always." — stored with quote and source, plus the caveat that *which* lab is not knowable before purchase |

### `ringconcierge-2-08-oval-lab-whisper-thin` — [live listing](https://ringconcierge.com/products/2-08-oval-lab-diamond-in-whisper-thina-hidden-halo)

Price **$6,038** and stone "**2.08 Carat E VS1 Oval Lab Grown Diamond**" confirmed unchanged. But the record called
it a "ready-to-ship configuration" — the live page says the opposite: **every size reads "Made to Order"**,
"**Estimated production time is 3-4 weeks**", and it offers a waitlist ("Receive a notification when this item is
back in stock!" / "Join the Waitlist"). The wording came from the *collection* the ring was found in
(`ready-to-ship-engagement-rings`); the product page contradicts it. Corrected, with the verbatim availability text
stored. Its existing `PURITY_NOT_IN_BODY_TEXT` and `MIXED_METAL` flags were re-confirmed as accurate — the karat
still appears only in image descriptions ("Yellow Gold … with Platinum Prongs"), never in the body text.

---

## 5. Re-confirmed, unchanged (a second session agreeing with the first is itself evidence)

| Target | What was re-read | Outcome |
|---|---|---|
| Gold spot | WGC live "**4,028.53** USD/oz", "Data as of **21 October, 2026**", "Market Data: Provided by ICE Data Services" | +0.10% vs the stored WGC snapshot of $4,024.36 (same publisher, same market date). **Not overwritten**: the stored snapshots are dated captures that every printed melt value reproduces. Third session to read the same live figure (`F18`) |
| LBMA | "A licence from IBA is required in order to obtain, use or redistribute real-time or historical benchmark data"; tables moved to the MyLBMA Portal; set twice daily 10:30 & 15:00 London | `data/prices.json`'s benchmark note is correct as written; no LBMA figure is reproduced |
| 16 CFR Part 23 | Banner: "Displaying title 16, **up to date as of 10/21/2026**. Title 16 was last amended 10/19/2026."; Authority 15 U.S.C. 45, 46; Source 83 FR 40667 | All 8 legal rules in `data/standards.json` reproduce |
| 16 CFR 23.4(b) | vermeil = sterling silver base, gold ≥ 10 karat, "**a minimum thickness throughout equivalent to two and one half (2½) microns (or approximately 100/1,000,000ths of an inch) of fine gold**" | Matches the site's 2.5-micron test. Corroborated from the trade side by Mejuri ("2.5 Micron Gold Plating") and Aurate ("we actually stand by the official vermeil 2.5 micron minimum guidelines") |
| 16 CFR 23.10 | quality-mark rule + "…shall apply to the article the trademark or name of such person. **15 U.S.C. 297**", which eCFR links at `https://www.govinfo.gov/link/uscode/15/297` | Basis of flag `H1`. The govinfo copy could not be added to `data/sources.json` without a domain-allowlist warning → `CR-6` |
| Blue Nile `203738` (`R08`) | spec "Metal **18K White Gold**", "Rhodium Finish Yes" vs description "artfully crafted from warmly lustrous **14k yellow gold**" | `SPEC1` / finding `F1` still live and still unresolved — only the seller can resolve it |
| Blue Nile returns | 30 days from shipment; exclusions include "items resized after initial purchase"; 2 free returns per year; 1 free resize ±2 sizes in 6 months; $150 missing-report fee | `S-BN` matches on every point; the resized-item exclusion is why `RET9` is attached to Blue Nile too |
| Costco `100675127` (`R10`) | **no price rendered**; "Item **1596365**" on a URL ending `/100675127`; "Metal: 14kt White Gold ( Rhodium Plated ) or 14kt Yellow Gold"; 0.50 ctw, 12 diamonds, VS2, I | `P2` and `ID1` both still true; `price_usd` correctly stays `null` rather than guessed |
| Costco CS `a_id/1191` | "**Precious metals are non-refundable.**"; ≥1.00 ct needs original IGI/GIA paperwork → Jewelry Credit Memo + 48-hour Graduate Gemologist inspection. Document ID **CU2573**, Version **18.0**, Published **10/02/2025** | `RET1` verbatim and current at that document version → `CR-5` asks for the metadata to be printed with the citation |
| Tiffany `GRP10863` (`R17`) | served at `/jewelry/rings/18k-rose-gold-and-platinum-diamond-rings-1712.html`; "Starting from $1,600"; "This product is currently unavailable"; "this item is non returnable … can only be exchanged"; (800) 843-3269 | `RDR1`, `FP1`, `AV1`, `RET6` all re-confirmed |
| Tiffany return policy | 30 days in the U.S.; ≥ $75,000 exchange only, no refunds; "Personalized, altered, or engraved items are not eligible"; refunds only in the country of purchase | `S-TI` matches |
| Wilson's `R11`/`R12`/`R13` | $3,725 / "Stamped for 14 karat gold" / "Total Weight: 6.1 grams"; $5,350 / "partial maker's mark for Hedges & Co." / 2.2 g / GIA 2215945495; $2,850 / "Stamped for **19 karat** gold" / "Signed with maker's mark for Bailey Banks & Biddle" | all three match; `K1` on the 19K row is still the right flag |
| Mejuri `R01`–`R04`, `R19` | "From$2,900" + "Solid White Gold (14k)"; $1,500; "From$648"; $228 "18k Gold Vermeil … 2.5 Micron Gold Plating"; $178 "18k Gold Vermeil, Sterling Silver" | all match; `S1` FAIL verdicts still backed by plating evidence; `L3`'s retirement is justified |
| Excluded listings (5) | Wilson's We-9330 "**SOLD OUT**"; Blue Nile platinum item 195271 "$2,150 / Metal Type: Platinum"; James Allen 17152 → redirects to a page titled "18K White Gold 0.25ct Pavé Bail Diamond **Pendant**", sold out; James Allen 41515 → "**This popular style is sold out**"; Costco 100423493 → "**Page Not Found!**" | all five exclusion reasons still true as of this pass |

**New rhodium finding (`CR-4`).** Mejuri's page states "**14k solid white gold pieces are finished with rhodium
plating**", and Blue Nile's spec tables for items `203738` and `195326` both say "**Rhodium Finish Yes**" — yet flag
`RH1` (the 16 CFR 23.7 disclosure flag) sits only on `R14`. Four rows (`R01`, `R03`, `R08`, `R09`) disclose a plated
surface on the live page without carrying the flag. Adding it means editing `data/rings.json`, which is inside open
PR #20's diff, so it is a change request rather than an edit.

---

## 6. Left empty on purpose

Better an empty cell than a confident error. These were **not** filled in, even though a plausible value exists:

* **Catbird phone** — none is published on the pages read.
* **Sarraf phone and email** — none is printed on the product or policy pages read.
* **Aurate `weight_g`** — the page publishes a range (5.5–8.5 g) across three metal options. No midpoint, no low end.
* **Costco `R10` price** — no price is rendered on the page.
* **Catbird / Automic checkout payment methods** — not read this pass. Automic's page loads a Klarna widget and
  Catbird's contact page loads one too; a widget is not proof of an accepted method, so nothing is asserted.
* **Every hallmark, maker's-mark and XRF/assay field the sellers do not publish** — still null, still flagged
  (`H1`, `X1`).
* **The live spot price as a new anchor** — recorded as corroboration only; overwriting the dated snapshots would
  silently change every melt value printed on the site.

---

## 7. Change requests (files inside another session's open PR)

Two PRs were open and being pushed while this pass ran — **#20** (`arena/8aaa18bf-gold3`: `data/rings.json`,
`data/retailers.json`, `scripts/audit.py`, `scripts/verify.py`, `scripts/page-check.js`, the workflow, every page)
and **#22** (`arena/e6fe3e4f-gold3`: `data/verification.json`, `verify.html`, `scripts/build_site.py`,
`scripts/render-test.js`, `README.md`). The board's rule is to log a change request instead of editing inside
another session's scope, so this pass touched only `data/flags.json`, `data/sellers.json`, `data/products.json`,
`data/findings.json` and its own two new files. The rest is filed in `COORDINATION.md` §4 as:

| # | File | Request |
|---|---|---|
| `CR-1` | `data/rings.json` | Fill `return_window` for `R15`, `R16`, `R18` from the sourced terms now on `S-RS`/`S-CB`, drop `POL1` from those rows, add the two policy URLs to each row's `sources`. Also add Costco's document metadata (CU2573 v18.0, 10/02/2025) to `R10` |
| `CR-2` | `data/rings.json` + `data/flags.json` | Retire `PD1`: the live Ross-Simons page reads $299, the same as the stored figure, so the cached-copy discrepancy did not reproduce. Remove it from `R16` **and** delete its definition in the same commit, or the audit reports an undefined flag |
| `CR-3` | `data/rings.json` | `R18`: label the quote's scope — "14k Yellow Gold" is the product-image alt/title text, not body copy. The verdict is already `UNVERIFIED`, so this is precision, not correction |
| `CR-4` | `data/rings.json` | Add `RH1` to `R01`, `R03`, `R08`, `R09` (Mejuri's rhodium-plating statement; Blue Nile's "Rhodium Finish Yes") |
| `CR-5` | `data/sources.json` + `sources.html` | Print the eCFR currency banner ("up to date as of 10/21/2026") with the 16 CFR citations, and the Costco document ID/version/date with `RET1` |
| `CR-6` | `scripts/verify.py` + `data/sources.json` | Add `govinfo.gov` to `OFFICIAL_DOMAINS` so the government's own copy of 15 U.S.C. 297 can be cited next to the Cornell LII copy without a warning |
| `CR-7` | `scripts/verify.py` | Let `weight_status` say "published as a range". Today a null weight must carry the literal token `"not published"`, which is why the Aurate record needs a `weight_note` to explain its own status string. `weight_g` stays null either way |
| `CR-8` | `data/verification.json` + `verify.html` | Append this pass's checks — `data/reverification-p3.json` already uses the log's entry shape (`id`, `url`, `findings`, `outcome`, `rows`) — and recompute the summary counts from the combined entries |
| `CR-9` | site pages via `scripts/build_site.py` | **Rebuild after this merge** so `sellers.html`, `retailers.html`, `flagged.html` and `analysis.html` pick up the corrected seller records and findings `F13`–`F18`. This session deliberately did not run the generator: `build_site.py` and every page it writes are inside both open PRs' diffs, and regenerating here would have collided with them. Until the rebuild, the data is ahead of the committed HTML |

---

## 8. Every URL opened in this pass (for manual review)

Each line is a page that was fetched live on 2026-10-22. Open it and search for the quoted text.

| # | URL | What it proves |
|---|---|---|
| 1 | https://www.gold.org/goldhub/data/gold-prices | live spot 4,028.53 USD/oz, "Data as of 21 October, 2026", ICE attribution |
| 2 | https://www.lbma.org.uk/prices-and-data/lbma-precious-metal-prices | IBA licence requirement; no public benchmark table to copy |
| 3 | https://www.ecfr.gov/current/title-16/chapter-I/subchapter-B/part-23 | Part 23 currency banner + §23.3(c)(1) karat and hollow-centre rules |
| 4 | https://www.ecfr.gov/current/title-16/chapter-I/subchapter-B/part-23/section-23.4 | §23.4(b) vermeil: sterling base, ≥10 karat, "two and one half (2½) microns" |
| 5 | https://www.ecfr.gov/current/title-16/chapter-I/subchapter-B/part-23/section-23.10 | §23.10 quality mark + maker's-mark requirement, citing 15 U.S.C. 297 |
| 6 | https://www.sarraf.com/products/14k-white-gold-solitaire-ring-0-94-ctw.html | `R20` $3,004 / 3.80 g / "14K Solid Gold" / 0.94 Ct G I1 Natural |
| 7 | https://www.sarraf.com/products/14k-white-gold-solitaire-ring-0-94-ctw.html#return-policy | 30-day terms, $25 engraving fee, third-party-resize exclusion, **no 3% fee** |
| 8 | https://www.sarraf.com/products/14k-white-gold-solitaire-ring-0-94-ctw.html#tab-warranty | $100-or-10% handling fee, third-party alteration voids the guarantee, ±5% weight tolerance |
| 9 | https://www.sarraf.com/products/10k-gold-6mm-high-polished-comfort-fit-wedding-band.html | `R21` $613 / 8.30 g / "10K Solid Gold" / size-10 reference weight |
| 10 | https://www.automicgold.com/products/radiant-cut-lab-diamond-cathedral-ring | `R22` $3,074 / "5.4g for gold or 8.1g for platinum" / 30-day window / engraved = final sale / two lead times |
| 11 | https://www.ross-simons.com/pages/returns-exchanges | 30-day guarantee, $4.95 fee, resize-by-another-jeweller exclusion |
| 12 | https://www.ross-simons.com/pages/customer-care | phone 800-835-0919, email customerservice@ross-simons.com |
| 13 | https://www.ross-simons.com/products/985230 | `R15` $249, "Gold Weight 0.7 grams", "All weights and measurements are approximate" |
| 14 | https://www.ross-simons.com/products/932728 | `R16` $299, "Gold Weight 0.8 grams" — `PD1` did not reproduce |
| 15 | https://www.catbirdnyc.com/returns | 20 days, $9 fee, final-sale list, "All international sales are final." |
| 16 | https://www.catbirdnyc.com/contact-us | customerservice@catbirdnyc.com, Brooklyn address, no published phone |
| 17 | https://www.catbirdnyc.com/woodland-ring.html | `R18` "$276.00 Regular Price $368.00", sold-out/waitlist assets |
| 18 | https://auratenewyork.com/products/2ct-round-lab-grown-diamond-solitaire-ring | $2,858 for a named in-stock variant, "Weight: 5.5-8.5g", "Exchange for size only. Final Sale!", GIA/IGI certificate text |
| 19 | https://ringconcierge.com/products/2-08-oval-lab-diamond-in-whisper-thina-hidden-halo | $6,038, 2.08 ct E VS1, every size "Made to Order", 3-4 weeks, waitlist |
| 20 | https://mejuri.com/products/bold-diamond-eternity-ring | `R01` "From$2,900", "Solid White Gold (14k)", "**14k solid white gold pieces are finished with rhodium plating**" |
| 21 | https://mejuri.com/collections/milestone-rings | `R02` $1,500 · `R03` "From$648" |
| 22 | https://mejuri.com/products/aurora-lab-grown-sapphire-eternity-ring | `R04` $228, "18k Gold Vermeil … 2.5 Micron Gold Plating" |
| 23 | https://mejuri.com/products/duet-mixed-ring | `R19` $178, "18k Gold Vermeil, Sterling Silver" |
| 24 | https://www.bluenile.com/engagement-rings/design-your-own-ring/floral-marquise-diamond-engagement-ring-in-18k-white-gold-item-203738 | `R08` $2,210, spec "18K White Gold" + "Rhodium Finish Yes" vs description "14k yellow gold" |
| 25 | https://www.bluenile.com/engagement-rings/design-your-own-ring/riviera-pave-diamond-engagement-ring-in-14k-white-gold-1-6-ct-tw-item-195326 | `R09` $1,500, "Rhodium Finish Yes" |
| 26 | https://www.bluenile.com/policies/returns | 30 days from shipment, resized-item exclusion, 2 free returns/year, free resize, $150 report fee |
| 27 | https://www.costco.com/p/-/round-brilliant-050-ctw-vs2-clarity-i-color-diamond-14kt-gold-band/100675127 | `R10` no price rendered, "Item 1596365", rhodium-plated or yellow 14kt |
| 28 | https://customerservice.costco.com/app/answers/detail/a_id/1191 | "**Precious metals are non-refundable.**", CU2573 v18.0 published 10/02/2025 |
| 29 | https://www.tiffany.com/engagement/engagement-rings/the-tiffany-setting-engagement-ring-in-18k-yellow-gold-GRP10863/ | `R17` "Starting from $1,600", unavailable, non-returnable/exchange-only, redirect path |
| 30 | https://www.tiffany.com/policy/return-policy.html | 30 days U.S., ≥$75,000 exchange only, engraved/altered excluded |
| 31 | https://www.wilsonsestatejewelry.com/products/mid-century-old-european-diamond-14-karat-white-gold-vintage-solitaire-engagement-ring | `R11` $3,725 / 6.1 g / "Stamped for 14 karat gold"; **the 3% cancellation fee, verbatim**; layaway terms |
| 32 | https://www.wilsonsestatejewelry.com/products/art-deco-old-mine-cut-diamond-18-karat-white-gold-antique-lotus-engagement-ring-gia | `R12` $5,350 / 2.2 g / Hedges & Co. maker's mark / GIA 2215945495 |
| 33 | https://www.wilsonsestatejewelry.com/products/bailey-banks-biddle-art-deco-diamond-enamel-19-karat-white-gold-vintage-fanning-engagement-ring | `R13` $2,850, "Stamped for 19 karat gold", Bailey Banks & Biddle mark |
| 34 | https://www.wilsonsestatejewelry.com/products/contemporary-0-92-ctw-diamond-14-karat-white-gold-engagement-ring-gia | excluded We-9330 still "SOLD OUT" |
| 35 | https://www.bluenile.com/engagement-rings/design-your-own-ring/french-pave-diamond-engagement-ring-in-platinum-1-4-ct-tw-item-195271 | excluded: $2,150, "Metal Type: Platinum" |
| 36 | https://www.jamesallen.com/engagement-rings/solitaire/14k-white-gold-knife-edge-solitaire-engagement-ring-item-17152 | excluded: redirects to Blue Nile and resolves to a **pendant**, sold out |
| 37 | https://www.jamesallen.com/engagement-rings/solitaire/14k-yellow-gold-15mm-comfort-fit-engagement-ring-item-41515 | excluded: "This popular style is sold out" |
| 38 | https://www.costco.com/4mm-diamond-cut-wedding-ring-14kt-gold.product.100423493.html | excluded: "Page Not Found!" |

---

## 9. Recommended next hallucination hunt

Standing recommendation, unchanged in substance and repeated here because this pass found something:

1. **Run the gates after every data change** — `verify.py` → `build_site.py` → `audit.py` → `render-test.js` →
   `report_verify.py`. They are mechanical and they catch arithmetic and provenance, not meaning.
2. **Then spend one pass whose only job is to hunt.** Pick any number or sentence on the site at random, open the
   linked official page, and search for it. If it is not there verbatim, delete it and mark the field `unverified`.
3. **Hunt specifically for transplanted facts** — the class found here. For every policy sentence attached to a
   seller, ask *"is this sentence on **this** seller's page, or on another seller's page that this project also
   read?"* Numbers that are true somewhere are the most dangerous kind, because they survive a spot check.
4. **Read policies to the end**, including warranty and fee sections. The Sarraf 3% error and the Sarraf $100/10%
   warranty fee were both in the part of the page that a summary skips.
5. **Check the two datasets against each other.** Catbird's policy existed in one and was "Not verified" in the
   other. Same-company disagreement between `data/retailers.json` and `data/sellers.json` is a cheap, high-yield test.
6. **Check claims *about* a source, not only values from it.** "No ring weight on the listing" is a factual assertion
   that the listing itself contradicted. Absence claims need the same evidence as presence claims.
7. **Never reconstruct a URL from memory.** During this pass, seven URLs were first written from recall with
   plausible slugs and only caught by diffing the new file's URLs against the URLs already recorded in `data/*.json`.
   A reconstructed URL inside an anti-hallucination record is itself a hallucination. Copy URLs; do not type them.
