# GOLD3 — Gold Engagement Ring Buyer's Guide

A verified, source-linked research project for buying a **solid gold engagement ring** online.
It publishes as a static site on GitHub Pages and is generated entirely from machine-readable data.

> ## Zero-hallucination policy — No Hallucinations Commitment
> **No hallucinations: every price, purity claim, weight and policy on this site is copied from a named official source page and
> stamped with the date it was read.** If a source does not publish a value, the value is left
> **blank** and marked **unverified** — it is never estimated, inferred, or filled in to make a row
> look complete. **Recommendation:** actively look for hallucinations on every review pass by clicking the official source link on every row, re-checking live prices/weights before buying, and running all automated security checks below.

**Prices captured:** 22 October 2026 · **re-verified live:** 23 October 2026 (fifth pass — 100% primary-source coverage) · **71 listings across all verified sets** (19 Dataset A + 31 Dataset B/D + 21 Dataset C) · **16 sellers** · **17 published weights** across the combined study (`not_rechecked: []`)

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
python3 scripts/verify.py                           # gate: source domains, quotes must contain their price, arithmetic
python3 scripts/build_ext_pages.py                  # build Dataset C subpages + Flagged for Review + Security Audit pages
python3 scripts/build_site.py                       # build unified dashboard & subpages; fails on broken internal links
python3 scripts/audit.py                            # independent audit: provenance, stray numbers, verification coverage
python3 scripts/run_security_audit.py --deterministic  # SEC-01..SEC-07 security & anti-hallucination audit (0 git diff churn)
node scripts/render-test.js                         # assert all built HTML pages contain the audited values (120/120)
python3 scripts/report_verify.py                    # regenerate reports/verification-report.md (121 checks) from data/
npm --prefix archive/session-cbea1001 test          # Node anti-hallucination, melt-math & link security suite
```

All checks run in CI on every push and pull request (`.github/workflows/audit.yml`). The site is generated, so
editing HTML by hand is pointless: change `data/*.json` or `scripts/build_site.py`, then rebuild.

## What the fifth verification pass changed (23 October 2026)

Every remaining URL across **Dataset C** (`SOL-01`..`SOL-09`, `BND-01`..`BND-12`, all 5 seller policies, all 4 BBB
profiles, all 4 live gold spot benchmarks + LBMA, and all statutory/NIST/GIA citations), **Dataset A** (`AU5760`,
`AU5769`, `AU5000`, `AU5093`, `AU5763`, `AU5764`, `AU5107`, Blue Nile ×5, Catbird, Mejuri, Ring Concierge ×2, all 5
seller contact/policy pages, and all 5 Trustpilot profiles), and **Dataset B/D** (`R02`, `R03`, `R17`, `R19`, `R22`,
`R28`, `R31`, `BND-05`..`BND-08`) was opened live on **23 October 2026**, reducing `not_rechecked` to **`[]` (zero)**.
Full Dataset C audit log in `data/reverification-c1.json` (`reports/reverification-dataset-c.md`) and Pass P5 entries
`V5-01`..`V5-12` appended to `data/verification.json` (**121 checks across four logged passes**):

* **Three unconfirmed Menē weights deleted, not softened (`F24`, `SD9`).** Live `mene.com` PDPs (`BND-01` `$1,707`,
  `BND-02` `$1,544`, `BND-03` `$2,465` — Wide Flat Band live PDP vs `$2,315` collection grid) render gram weight only via
  client-side JS and block `/products/*.json` (`404`). Stored snippet weights (`8.5g`, `7.9g`, `12.0g`) and derived melt
  multiples (`1.56x`, `1.52x`, `1.50x`) were set to `null` / `unverified` and removed from hardcoded calculator presets.
* **Thirteen unprinted hallmark assertions corrected (`SD9`).** `BND-08`..`BND-12` and `SOL-01`..`SOL-08` now record
  `"Not published by the seller"` instead of generic `"14K stamp"` assumptions.
* **All seven Aurate lab-grown engagement ring PDPs enforce `"Final Sale! / Exchange for size only."` (`F25`, `RET14`).**
  Live PDPs override Aurate's 60-day general return policy, add a 30% MTO cancellation fee after 24 hours
  (`auratenewyork.com/pages/terms-conditions-exchange-only-final-sale`), share multi-metal gram ranges across 14K/18K/Pt,
  and show clarity/shape contradictions (`AU5093` Cushion headline vs `"classic oval diamond"` description).
* **Mejuri `R03` (`Slim Diamond Eternity Band`) live PDP reads `"From $898"`, not `$648` (`F26`, flag `FP1`).** Opening
  the direct PDP reveals `$898` (+38.6% over the `$648` figure captured from the collection grid alongside `Diamonds Band`).
* **Four dead/broken external links repaired (`F27`, `SD10`, `SRC2` closed).** Catbird `/contact-us` (`500`) repointed
  to live `catbirdnyc.com/facts` (`customerservice@catbirdnyc.com`) + `return_form.pdf` (`141 Flushing Avenue, Building
  77, Suite 709, Brooklyn, NY 11205`, `+1-718-599-2340`); `uscode.house.gov` (`500`), `gov.uk/guidance/...` (`404`), and
  `gia.edu/.../gold-plated-gold0` (`404`) repointed to live `HTTP 200` Cornell LII, GOV.UK Statutory Guidance, and GIA
  Summer 2025 *Gems & Gemology* PDF citations.
* **Deterministic security audit (`CR-692d-2` closed).** `python3 scripts/run_security_audit.py --deterministic` re-runs
  all `SEC-01`..`SEC-07` checks with zero timestamp/counter churn (`git diff` empty).

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
