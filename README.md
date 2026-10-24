# GOLD3 — Gold Engagement Ring Buyer's Guide

A verified, source-linked research project for buying a **solid gold engagement ring** online.
It publishes as a static site on GitHub Pages and is generated entirely from machine-readable data.

> ## Zero-hallucination policy — No Hallucinations Commitment
> **No hallucinations: every price, purity claim, weight and policy on this site is copied from a named official source page and
> stamped with the date it was read.** If a source does not publish a value, the value is left
> **blank** and marked **unverified** — it is never estimated, inferred, or filled in to make a row
> look complete. **Recommendation:** actively look for hallucinations on every review pass by clicking the official source link on every row, re-checking live prices/weights before buying, and running all automated security checks below.

**Price snapshots:** 22–23 October 2026 · **re-verified live:** 23 October 2026 (passes `P1`–`P19`, **265 logged checks**) · **71 rows** — Dataset A 19, Dataset B 31, Dataset C 21 · **16 sellers** · **19 published weights** (14 in Dataset B, 5 in Dataset C)

---

## What is on the site

| Page | Contents |
|---|---|
| `index.html` | Dashboard: zero-hallucination policy, key numbers, top findings, category links |
| `rings.html` | Every listing, filterable by karat / stone / budget, each with a source link |
| `14k.html`, `18k.html`, `lab-grown.html`, `under-1000.html` | Category views with gap counts |
| `excluded.html` | Vermeil and silver look-alikes, with the regulation that defines why they fail |
| `retailers.html` | Return windows, exclusions, contact details, Trustpilot scores **with sample sizes** |
| `calculator.html` | Melt value, break-even weight, price ÷ gold-value multiple, formula shown |
| `flagged.html` | Every irregularity and unverified cell, with evidence and the action to close it |
| `sources.html` | Full source register with verbatim quotes and read dates |
| `checklist.html` | The twelve-point buying checklist, each item tied to law or policy |
| `verify.html` | The verification log: every source URL reopened, what it confirmed, corrected or deleted, plus the defects found on this site and fixed |
| `sellers.html` | Seller register from the parallel dataset: return terms, exclusions, contact evidence, disclosure practice |
| `standards.html` | Karat arithmetic and the federal jewellery rules quoted with citations |
| `methodology.html` | The passes run in order, and how to re-run every check |
| `analysis.html` | Coverage of the checklist plus melt value versus asking price for rows that publish a weight |
| `requirements.html` | **Requirements compliance matrix**: all 71 listings scored cell by cell against the ten checklist requirements, every cell source-linked or blank |

## Data files (single source of truth)

| Path | Purpose |
|---|---|
| `data/products.json` | One record per listing: price, purity, evidence quote, sources, flags |
| `data/retailers.json` | Merchant policies, contact, review data, flags |
| `data/sources.json` | Authority sources (16 CFR Part 23, 15 U.S.C. 294–297, LBMA, gold price) |
| `data/prices.json` | Dated gold spot snapshots + the physical constants used |
| `data/findings.json` | Editorial findings, each with a source and a required action |
| `data/verification-report.json` | Machine-generated audit: metrics, derived benchmarks, errors |
| `data/verification.json` | The re-verification log: one entry per source URL, with outcome and what the page actually printed |

## Run every check

```bash
python3 scripts/verify.py           # gate: Dataset A + B source domains, quotes, arithmetic
python3 scripts/verify_dataset_c.py # gate: Dataset C schema, verbatim price/weight/solid/hallmark & dead-link blocklist
python3 scripts/build_ext_pages.py  # build Dataset C subpages (solitaire-settings, bands-vintage-rings, sellers-policies, etc.)
python3 scripts/build_site.py       # build the unified static site; fails on broken internal links
python3 scripts/audit.py            # independent audit: provenance, stray numbers, verification coverage
python3 scripts/run_security_audit.py # SEC-01..SEC-07 anti-hallucination, melt-math, allowlist & XSS suite
node scripts/render-test.js         # assert the built HTML contains the audited values
python3 scripts/report_verify.py    # regenerate reports/verification-report.md from data/
npm --prefix archive/session-cbea1001 test  # Node anti-hallucination, melt-math & link security suite
```

All checks run in CI on every push and pull request (`.github/workflows/audit.yml`). The site is generated, so
editing HTML by hand is pointless: change `data/*.json` or `scripts/build_site.py`, then rebuild.

## What Pass P17 changed (23 October 2026)

All **19 Dataset A official product sources**, five seller-policy records, five Trustpilot profiles, Ross-Simons Item 571221 and four spot publishers were re-read: **31 checks — 10 confirmed, 18 corrected, 3 flagged**. Every Dataset A numeric price was confirmed with **zero price changes**; no published gram weight changed. See `reports/reverification-pass-p17.md` and `data/reverification-p17.json`.

* Removed unsupported assertions that Aurate's listed diamond mass was included in its listed ring weight. Ambiguous weights stay null, and conflicting bezel title/spec carat values are no longer assigned one numeric value.
* Corrected current Blue Nile stock/width pairs, Mejuri Stacker's `Width: 1 mm`, Aurate bezel dimensions/clarity, Ring Concierge metal provenance, seller-policy drift and Trustpilot sample counts.
* Replaced Mejuri's blanket no-hallmark flag with an explicit **alt-text-only purity stamp** warning: alt text is not visual verification and does not establish a maker's mark.
* Ross-Simons weights remain published but are correctly labelled **approximate**, not exact; weight, geometry and customer reviews are not treated as proof of solid construction.
* The live spot reference is corroborated by four feeds within **0.025%** and sits **0.65% below** the morning anchor. Calculations still use the dated **$4,022.22/oz** primary snapshot for reproducibility.
* Published findings **F50–F55** and added guards for duplicate flags, stale source wording and unsupported inclusion/solidity inferences.

## What the nineteenth pass changed (23 October 2026 — Pass P19)

**Ten official pages re-opened live across all three datasets — 8 confirmed, 0 corrected, 2 flagged** — plus the
site's first **requirements compliance matrix** (`requirements.html`, `data/requirements-matrix.json`), generated by
`scripts/requirements_matrix.py` and re-derived independently by the new `scripts/hallucination_scan.py`
(`reports/reverification-pass-p19.md`, `data/reverification-p19.json`, ledger `P19-01`…`P19-12`).

* **Every one of the 71 listings is now scored against all ten checklist requirements** — karat, the word "solid",
  hallmark, maker's mark, weight, seller reputation, return window, card payment, documentation and independent/XRF
  verification. A cell is either backed by an official page you can click, or left **blank and marked unverified**.
  The consequence is the honest headline: **0 of 71 rows clear all ten.** 19 publish a numeric weight, 3 a hallmark,
  2 a maker's mark and none records a seller offering an assay.
* **Nothing was inferred to close a gap.** The 52 rows without a numeric weight get no melt figure; the 13 without a verifiable
  payment method stay blank. `hallucination_scan.py` proves every stored price and gram weight appears verbatim in that
  row's own quote, so a cell cannot be filled from arithmetic alone.
* **Menē moved the Wrap Ring twice in one day** (`$3,228` → `$3,202`, 1.57% under the capture). The captured price is
  untouched and both live readings are stored (finding `F56`).
* **Two site defects fixed:** `SD25` (two dashboard tiles carried Dataset-A values under site-wide labels) and `SD26`
  (authority links in the first draft of the matrix did not match `data/sources.json`; 16 CFR Part 23 was cited under the
  wrong subchapter). Two authority pages were opened live and added to the register: **15 U.S.C. § 1666** (billing-error
  correction, the reason a credit card matters) and **16 CFR Part 435** (FTC mail/internet order rule).
* **New findings** `F56` (intra-day Menē repricing), `F57` (two gold-price anchors 0.012% apart and which page uses which)
  and `F58` (no listing clears all ten requirements).

## What the ninth pass changed (23 October 2026 — Pass P13)

Seven official pages re-opened live — **5 confirmed · 1 corrected · 1 flagged** — plus **three site defects** found by auditing the
repo against its own data (`reports/reverification-pass-fb7e5e3c.md`, `data/reverification-fb7e5e3c.json`, ledger `P13-01`…`P13-07`).
This pass sits on top of `main` @ `7406ee9` and preserves the concurrent pass `P12` in full.

* **Mejuri prints a `Solid Yellow Gold (14k)` materials heading above a white-gold selection** on R01 and R03. New flag **`SPEC8`**;
  the misapplied `SPEC2` (which is the Local Eclectic 9k/10k contradiction) removed from R03.
* **`18k.html` claimed no complete verified 18K ring existed**, while Dataset B held four with live prices plus Dataset C settings.
  Both the 14K and 18K pages now list the Dataset B/C rows at that karat (31 and 13 rows) with a source link on every row.
* **Typed-in prose is gone**: the spot anchor, the weight-coverage sentence and the audit-check count in `combined.html` and
  `methodology.html` are derived from the data files at build time, so they cannot drift again — and the calculator now surfaces
  the labelled live-check spot reading (0.62% below the dated snapshot the melt values use).
* Every stored price, karat and gram weight on the seven re-read pages matched verbatim (R02, R15/R16, R20, R21, R31 confirmed;
  R01/R03 confirmed with the new heading flag).

## What the fourth verification pass changed (23 October 2026)

25 official URLs were re-opened on the merged tree: **15 confirmed, 8 corrected, 2 flagged**. Full log in
`data/reverification-p4.json`, human-readable in `reports/reverification-pass-p4.md`, and every check appended to
`data/verification.json` (which now holds **109 checks across three passes** and is what `verify.html` renders).

* **Four Menē prices had already moved** one day after capture (Wrap Ring $3,253 → $3,228; Classic Band $1,720 → $1,707;
  Narrow Flat "From $1,544"; Wide Flat "From $2,315"). New flag **`PRC1`**; a `live_recheck` block on each row records
  today's figure beside the captured one. Captured prices were **not** overwritten.
* **Seven band records asserted a hallmark no page prints.** The words came from general jewellery practice, not from
  the seller. Every `hallmark_disclosure` in `BND-01`…`BND-07` now reads "not published by the seller" (site defect `SD6`).
* **`POL1` removed from three rows** whose return policies are readable: Ross-Simons `R15`/`R16` now quote the 30-day
  guarantee, the $4.95 flat fee and the resize exclusion; Catbird `R18` quotes the 20-day window and $9 fee.
* **`PD1` retired** — the live page prints the price the record stores (site defect `SD7`).
* **`RH1` added to six white-gold rows** (`R01`, `R03`, `R08`, `R09`, `R10`, `R14`) with the seller's rhodium wording stored.
* **New flag `SRC2`**: Catbird's cited contact page returned **HTTP 500**, so its e-mail is not re-confirmed as of
  23 October 2026.
* `scripts/verify.py` now accepts a `weight_status` of "published as a range…" for a null weight, and `scripts/audit.py`
  lets a verification check point at a seller, a flag or a Dataset-A product instead of only an `R##` row.

## What the fifth pass changed (23 October 2026)

A targeted pass over **every row that publishes a finished weight**, because grams are the only seller figure the melt
calculator consumes. 7 checks: **3 confirmed · 3 corrected · 1 flagged** (`reports/reverification-pass-p5.md`).

* **R23** stored `"Approximately 6.1g"` where the page prints `6.1g (gold) or 9.2g (platinum)` — a metal-dependent weight
  was reading as unconditional.
* **R26 and R27** carried a `(±5% seller accuracy note)` that Sarraf does not print. The numbers were right; the
  justification was invented. Removed and replaced with the fact that no tolerance is published.
* **R12** confirmed as one of only three rows whose seller publishes a hallmark, and one of two that publishes a maker's
  mark (`Stamped for 18 karat gold`, `partial maker's mark for Hedges & Co.`).
* **16 CFR 23.10** read in full: the maker's-mark paragraph the site cites is real and is now quoted verbatim next to
  the rule.

The verification log now holds **128 checks across independent passes P1–P8**.

## What the sixth pass changed (23 October 2026 — Dataset C & Dataset D sweep)

58 official URLs were opened live across all 21 Dataset C ring listings (`SOL-01`..`SOL-09`, `BND-01`..`BND-12`), all 5
Dataset C sellers + BBB profiles, all spot/statutory standards, and Dataset D (`R23`–`R31` + `S-BRILLIANTEARTH`,
`S-VRAI`, `S-LOCALECLECTIC`, `S-MENE`): **26 confirmed, 25 corrected, 7 flagged** (`data/reverification-dataset-c.json`,
`reports/reverification-dataset-c.md`, plus `P8-01`..`P8-12` in `data/verification.json`).

* **Menē `BND-01`..`BND-03` client-JS-only gram weights blanked to `null`.** Static HTML across `mene-classic-band-gold`,
  `mene-narrow-flat-band-gold`, `mene-wide-flat-band-gold`, and `collections/bands-gold` omits gram weights (`8.5`/`7.9`/`12`
  g render via client JS only) and omits the word `"solid"`. All three rows now have `weight_grams: null` and `melt_value_usd: null`
  while preserving `PRC1` & `SD6`.
* **13 remaining Dataset C rows had unsupported hallmark claims removed (`SD6` extension).** Neither `bluenile.com/services/warranty`,
  `brilliantearth.com/customer-service/warranty/`, nor any `SOL-01`..`SOL-08` or `BND-08`..`BND-12` product page prints hallmark
  text; all 21 Dataset C rows now state `"Not published by the seller"`.
* **8 dead/broken 404/500/redirect URLs repointed to live HTTP 200 official pages (`SRC1`)**:
  `uscode.house.gov` (HTTP 500 → GovInfo 15 U.S.C. §§ 295 & 297 PDFs), `gia.edu/...gold0` (404 → Summer 2025 Lab Notes PDF),
  `gov.uk/guidance/hallmarking-law-and-practice` (404 → `hallmarking-is-the-law-guidance-summary`), `brilliantearth.com/returns/`
  (404 → `/30-Day-Returns/`), `vrai.com/pages/contact-us` (404 → `/contact-us`), `help.vrai.com/hc/...` (redirect →
  `/en/knowledge/what-is-your-return-policy`), `localeclectic.com/pages/contact-us` (404 → `/pages/frequently-asked-questions`),
  and `mene.com/contact-us` (404 → `/customer-care/en-US`).
* **3 wrong seller phone/email records corrected & `R24`/`R25` weights verified:** `S-MENE` (`+1-833-636-3245`, `service@mene.com`),
  `S-VRAI` (`+1-855-956-4488`, `help@vrai.com`), `S-BRILLIANTEARTH` (`email: null`, web form + SMS `+1 415.520.6526`); `R24`
  chunk 1 confirmed `"Approximately 2.3g (gold) or 3.4g (platinum)"` and `R25` `"Approximately 1.4g (gold) or 2.0g (platinum)"` (`WT1`).
* **Added `scripts/verify_dataset_c.py`** to `.github/workflows/audit.yml` and made Dataset C nav/filter counts dynamic (`71` combined rows, `21` flagged).

## What the third verification pass changed

Every cited URL in the parallel dataset was reopened on 22 October 2026 and each stored value was searched for
in the page text. Outcome: **15 confirmed, 8 corrected, 5 flagged**, three listings added (Sarraf ×2, Automic
Gold), and seven metal-option phrases **deleted** because the fetched pages never printed them. The log is on
`verify.html`; the defects it found on this site (a dashboard table that squared the melt value, four pages
whose renderer no longer existed, one invented prose threshold) are recorded there too, with the fix.

## Two datasets, one site

Two agent sessions researched this repository on the same day, plus a third that merged an earlier draft. Both
surviving datasets are published rather than one being discarded:

| Set | File | Rows | Sellers | Evidence model |
|---|---|---|---|---|
| **A** (this session) | `data/products.json` | 19 (17 gold + 2 excluded) | Aurate, Blue Nile, Catbird, Mejuri, Ring Concierge | Verbatim price quote + capture date per row |
| **B** (parallel sessions `8aaa18bf`, `e6fe3e4f`, `cbea1001`) | `data/rings.json` | 31 rings + 5 excluded look-alikes | Blue Nile, Brilliant Earth, Catbird, Costco, James Allen, Local Eclectic, Mejuri, Menē, Ross-Simons, Sarraf, Automic Gold, Tiffany, VRAI, Wilson's Estate Jewelry | Per-field quote for karat, solid-gold claim, weight, hallmark, plus a flag legend |

`scripts/verify.py` gates **both**. For Dataset B it checks official-domain sources, a per-listing source list, that the
numeric price appears inside `price_as_shown`, that any weight carries a weight quote, that a `PASS` solid-gold verdict
carries a quote, and that each excluded look-alike states a reason and an official URL. Combined metrics land in
`data/verification-report.json` (41 listings, 12 sellers, 7 published weights).

`combined.html` shows both sets with an A/B badge so nothing is misattributed. Dataset B's own pages
(`sellers.html`, `standards.html`, `methodology.html`, `analysis.html`, `verify.html`) are generated from the same
JSON by `scripts/build_site.py` - never hand-edited - and the earlier sessions' standalone suites under
`archive/session-982bfc88/` and `archive/session-cbea1001/` (including the interactive stone-carat deduction & post-arrival ED-XRF assay tolerance calculator) are preserved unchanged.

## Build and verify

```bash
python3 scripts/verify.py       # must print PASS - exits 1 on any error
python3 scripts/build_site.py   # refuses to build unless the report says PASS
```

`build_site.py` also fails on broken internal links, missing product URLs, or `TODO` markers.

### What `verify.py` actually checks

1. Every populated factual field carries a source URL on a recognised official domain (https only).
2. Every price has a currency, a capture date, a source page, and a **verbatim quote**.
3. **The recorded price must literally appear inside that quote** — this is the transcription /
   hallucination check. `$2,858` in the data must match `From $2,858` on the page.
4. Unpublished values stay `null` (`weight_g`, `carat`, `hallmark`) — a value without a source is an error.
5. Purity matches the category: a 14K page cannot contain an 18K ring.
6. Plated / vermeil / silver items can only exist in the `excluded` category.
7. A "solid gold" claim without a verbatim retailer excerpt is an error.
8. **Price-vs-melt sanity:** computes the break-even weight for every price. A price below the melt
   value of 0.5 g of its own karat is rejected as impossible; under 1.5 g raises a warning.
9. Prices older than 30 days are flagged stale.
10. Two independent gold spot sources must agree within 2%.
11. Findings must have a severity, an official source, an action, and only known placeholders.
12. Metric arithmetic must reconcile (gold + excluded = total; status buckets sum correctly).

## Verification status and limits

* **Verified:** each price/policy quote was read from the retailer's own page on 22 Oct 2026.
* **Cross-checked:** gold spot from GoldPrice.org ($4,026.79/oz) and the World Gold Council
  ($4,024.36/oz) — 0.06% apart.
* **Not verified, deliberately blank:** finished ring weights (0 of 17), hallmarks (0 of 5 retailers),
  per-retailer payment methods, and 18K Aurate prices.
* **Known limitation:** this sandbox has no outbound HTTP except a small allowlist, so there is no
  automated nightly link-checker. Every URL in the dataset was opened during the research pass and
  is recorded with its read date. Re-verify by opening the links.
* **Not advice:** no affiliate links, no sponsored placements, no endorsements. A listing appears
  because it could be verified, not because it is recommended.

## Multi-session coordination

Read `COORDINATION.md` before editing. Claim a task, respect file scopes, log sources and
verification performed, and record any irregularity you could not close.
