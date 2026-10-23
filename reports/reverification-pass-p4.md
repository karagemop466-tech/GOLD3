# Fourth verification pass (P4) — live re-check of the merged tree

**Session:** `arena/6d6192d1-gold3` · **Date:** 2026-10-23 · **Tree at start:** `5663d5e` (`origin/main` after PR #32, branch 0 ahead / 0 behind)
**Machine-readable log:** `data/reverification-p4.json` · **Merged into:** `data/verification.json` (checks `P4-01`…`P4-25`)

This is the fourth independent pass on this repository and the first one run by a session that also acted as the
integration session. Every other session in `COORDINATION.md` had already merged and closed, so nothing was edited
while another session held a claim.

## What this pass did

Each check means: the official URL was opened on 2026-10-23, and the stored value was searched for in the text the page
returned. Nothing was carried forward from another session's notes. Where the fetch did not reach the part of the page
that holds a value, the check says so and the value keeps its original capture date.

| Result | Count |
|---|---|
| URLs opened | 25 |
| Confirmed as stored | 15 |
| Corrected (page differed from the record) | 8 |
| Flagged (page itself contradicts itself, or a cited page fails) | 2 |

## Findings that changed the data

### 1. Menē re-prices continuously — four captured prices had already moved (new flag `PRC1`)

All four Menē listings were re-read the day after capture and **every one was cheaper**:

| Record | Captured 2026-10-22 | Live 2026-10-23 | Source |
|---|---|---|---|
| `R30` Wrap Ring | $3,253 | **$3,228** | <https://mene.com/products/wrap-ring-gold> |
| `BND-01` Classic Band | $1,720 | **$1,707** (product page) / "From $1,664" (collection) | <https://mene.com/products/mene-classic-band-gold> |
| `BND-02` Narrow Flat Band | $1,556 | **From $1,544** | <https://mene.com/collections/bands-gold> |
| `BND-03` Wide Flat Band | $2,333 | **From $2,315** | <https://mene.com/collections/bands-gold> |

The seller's own product page says *"Products are sold by weight, not size."* The captured prices were **kept** and a
`live_recheck` block now records the figure the page printed today, because overwriting them would hide the movement
and break the dated-snapshot rule. GoldPrice.org printed **$4,022.22/oz** on the same day against the **$4,026.79/oz**
snapshot the melt values use — 0.11% apart, inside tolerance, so the stored snapshot was **not** changed.

### 2. Two rows were still marked "return policy not verified" (closed `CR-P3-1`)

`R15` and `R16` (Ross-Simons) and `R18` (Catbird) still said *"Not verified — no official return-policy page captured
for this seller"* and carried `POL1`, although both policies were read on 2026-10-22 and again on 2026-10-23. Both rows
now quote the seller's own wording, carry the policy URL in their source list, and `POL1` is gone from them.

* Ross-Simons: *"30-Day No-Risk Return Guarantee"* · *"resized by a jeweller other than Ross-Simons cannot be accepted
  for return"* · *"we may include a flat fee of $4.95 for return shipping and handling"* — <https://www.ross-simons.com/pages/returns-exchanges>
* Catbird: *"within 20 days"* · *"An $9 charge for return shipping will be deducted from your refund"* · final-sale list
  · *"All international sales are final."* — <https://www.catbirdnyc.com/returns>

### 3. `PD1` described nothing and was retired (closed `CR-P3-2`)

`PD1` claimed a price differed between the live page and a cached copy. The live page for `R16` prints **$299**, the same
figure the record stores. The flag was removed from the row and its definition deleted in the same commit.

### 4. Rhodium disclosure was missing from six white-gold rows (closed `CR-P3-4`)

16 CFR 23.7 requires a surface rhodium layer to be disclosed. Six rows sell white gold that the seller says is rhodium
finished and carried no `RH1`: `R01`, `R03` (Mejuri: *"14k solid white gold pieces are finished with rhodium plating"*),
`R08`, `R09`, `R14` (Blue Nile: *"Rhodium Finish Yes"*) and `R10` (Costco: *"14kt White Gold ( Rhodium Plated ) or 14kt
Yellow Gold"* — white-gold option only). Each row now stores the quote and the URL it came from. `R09` and `R03` rest on
the 2026-10-22 capture and say so.

### 5. Seven band records asserted a hallmark no page prints (site defect `SD6`)

`BND-01`…`BND-07` described *"14K quality mark + maker's trademark"* and *"Menē maker's mark + 24K stamp + Certificate of
Authenticity"* in the seller's voice. None of the cited pages contains a hallmark or maker's-mark statement. That is the
exact defect class this project exists to catch — an inference dressed as a quotation — and it was in our own file. Every
one of those fields now reads **"Not published by the seller"**, with the 16 CFR 23.10 / 15 U.S.C. 297 check stated as a
to-do. The legal citation itself was verified: § 23.10 does print the paragraph *"Disclosure of identity of
manufacturers, processors, or distributors."*

### 6. A cited contact page is failing (new flag `SRC2`)

Catbird's contact page returned **HTTP 500 Internal Server Error** (nginx) on two attempts, so the e-mail recorded
against `S-CB` could not be re-confirmed today. The same site's returns and product pages loaded normally in the same
session, so this is one broken page, not a dead domain. The value was left in place with a correction note and flagged
rather than silently deleted.

## What held up

Prices, karats and published gram weights were found **verbatim** on the official page for `R20` ($3,004 / 3.80 g /
14K Solid Gold), `R21` ($613 / 8.30 g / 10K Solid Gold, plus its "size 10, approximate" caveat), `R26` ($4,068 / 6.30 g /
18K Solid Gold), `R11` ($3,725 / 6.1 g / "Stamped for 14 karat gold"), `R15` ($249 / 0.7 g), `R16` ($299 / 0.8 g),
`R18` ($276), `R01` (From $2,900), `R14` ($1,145 setting price), `R08` ($2,210 setting price), `BND-04` ($400 / 1.7 g)
and `BND-11` ($648). Sarraf's `service@sarraf.com` and 888-472-7723 were confirmed on its About page, Automic's 30-day
window and final-sale list on its refund policy, and Costco's `R10` was confirmed to render **no price at all**, which is
why that cell stays blank.

Two live page contradictions also reproduced a day later, unchanged: `SPEC1` (Blue Nile's 18K white-gold floral marquise
page describing itself as *"warmly lustrous 14k yellow gold"* in the body copy) and `SPEC4` (Sarraf's About page saying
any non-engraved item can be returned "no questions asked" against its returns page's engraved-ring paragraph).

## What this pass did **not** verify

Stated here rather than implied anywhere else, and repeated in `data/verification.json` under `not_rechecked`:

* All seven **Aurate** rows, the **Ring Concierge** rows, `R02`, `R17` (Tiffany), `R19`, `R28` (VRAI), `R29` (Brilliant
  Earth), `R31` (Local Eclectic) and bands `BND-05`…`BND-08` were **not re-opened** in this pass. Their values remain the
  2026-10-22 capture.
* `R03`'s $648 sits on a **collection** page. The fetch returned only the first part of that page, so the card could not
  be located; `R03` is recorded as not re-checked rather than claimed as confirmed.
* `R22`'s **weight** was not re-read — the fetch ended mid-line at *"Item Weight Appr…"*. Its price and solid-gold
  wording were confirmed.
* `CR-P3-5` is only **half closed**: the eCFR currency banner was recorded against every eCFR citation, but the Costco
  document metadata (Document ID / version / date) does not appear on the Costco product page, so it was **not** added.

## Gates run after the changes

| Gate | Result |
|---|---|
| `scripts/verify.py` | PASS — 0 errors, 0 warnings |
| `scripts/build_ext_pages.py` + `scripts/build_site.py` | built, internal links and product URLs OK |
| `scripts/audit.py` | PASS — 31 rows, 0 errors, 0 warnings, 173 checks |
| `scripts/run_security_audit.py` | PASS — SEC-01…SEC-07 |
| `node scripts/render-test.js` | PASS — 120/120 |
| `scripts/report_verify.py` | PASS — 109 verification checks |
| Row-link gate | every root HTML table row carries an `https://` official link |

## Recommended next hallucination hunt

1. Re-open the rows listed under "did not verify" — a pass that says what it skipped is only useful if the next one
   picks it up.
2. Fetch every URL in `verification/sources-manifest.json` and fail on any non-200. Two dead links were found by accident
   in P3 and one live 500 in P4; nobody has yet swept the manifest systematically.
3. Re-read `R03` on a full fetch, or replace it with a product-page URL.
4. Re-check Catbird's contact page and, if it stays broken, decide whether `S-CB`'s e-mail is citable at all.
5. Re-read `R22`'s weight and `R09`/`R03`'s rhodium wording on the seller's page.
