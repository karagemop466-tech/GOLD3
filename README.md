# GOLD3 — Gold Engagement Ring Buyer's Guide

A verified, source-linked research project for buying a **solid gold engagement ring** online.
It publishes as a static site on GitHub Pages and is generated entirely from machine-readable data.

> ## Zero-hallucination policy
> **Every price, purity claim, weight and policy on this site is copied from a named source page and
> stamped with the date it was read.** If a source does not publish a value, the value is left
> **blank** and marked **unverified** — it is never estimated, inferred, or filled in to make a row
> look complete. Prices move daily; always re-check the linked page before buying.

**Captured:** 22 October 2026 · **19 listings** · **5 retailers** · **17 gold + 2 excluded**

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

## Data files (single source of truth)

| Path | Purpose |
|---|---|
| `data/products.json` | One record per listing: price, purity, evidence quote, sources, flags |
| `data/retailers.json` | Merchant policies, contact, review data, flags |
| `data/sources.json` | Authority sources (16 CFR Part 23, 15 U.S.C. 294–297, LBMA, gold price) |
| `data/prices.json` | Dated gold spot snapshots + the physical constants used |
| `data/findings.json` | Editorial findings, each with a source and a required action |
| `data/verification-report.json` | Machine-generated audit: metrics, derived benchmarks, errors |

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
