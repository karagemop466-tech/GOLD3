# GOLD3 — Gold Engagement Ring Buyer's Guide

A verified, source-linked research project for buying a **solid gold engagement ring** online.
It publishes as a static site on GitHub Pages and is generated entirely from machine-readable data.

> ## Zero-hallucination policy — No Hallucinations Commitment
> **No hallucinations: every price, purity claim, weight and policy on this site is copied from a named official source page and
> stamped with the date it was read.** If a source does not publish a value, the value is left
> **blank** and marked **unverified** — it is never estimated, inferred, or filled in to make a row
> look complete. **Recommendation:** actively look for hallucinations on every review pass by clicking the official source link on every row, re-checking live prices/weights before buying, and running all automated security checks below.

**Captured:** 22–23 October 2026 · **71 listings across all three passes** (A: 19 + B: 31 + C: 21; 50 in Datasets A+B) · **16 sellers** · **21 published weights** (13 in Dataset B + 8 in Dataset C, plus 1 weight range in Dataset A)

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
python3 scripts/verify.py         # gate: source domains, quotes must contain their price, arithmetic
python3 scripts/build_site.py     # build the static site; fails on broken internal links
python3 scripts/audit.py          # independent audit: provenance, stray numbers, verification coverage
node scripts/render-test.js       # assert the built HTML contains the audited values
python3 scripts/report_verify.py  # regenerate reports/verification-report.md from data/
npm --prefix archive/session-cbea1001 test  # Node anti-hallucination, melt-math & link security suite
```

All checks run in CI on every push and pull request (`.github/workflows/audit.yml`). The site is generated, so
editing HTML by hand is pointless: change `data/*.json` or `scripts/build_site.py`, then rebuild.

## What the last verification pass changed

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
| **C** (parallel session `698f08f6`) | `data/solitaire-rings.json`, `data/bands-and-high-karat.json` | 21 rings (9 solitaires + 12 bands) | Blue Nile, Brilliant Earth, Ross-Simons, Menē, Mejuri | Verbatim primary listing excerpt, exact NIST melt value & BBB audit |

`scripts/verify.py` gates Datasets A & B; `scripts/audit.py` gates Dataset B and the rendered HTML; and `scripts/run_security_audit.py` gates Dataset C and all 24 HTML pages. Combined metrics land in `data/verification-report.json` (50 listings in Datasets A+B, 71 across Datasets A+B+C, 16 sellers, 21 published weights).

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
