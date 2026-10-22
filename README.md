# GOLD3 — Gold Engagement Ring Buyer's Guide

A verified, source-linked research project for buying a **solid gold engagement ring** online.
Everything is published as a static site (GitHub Pages) built from machine-readable data.

> ## ⚠️ Zero-hallucination policy
> **Every price, purity claim, weight and policy on this site is copied from a named source page and
> stamped with the date it was read.** If a source does not publish a value, the value is left
> **blank** and marked **Unverified** — it is never estimated, inferred, or filled in to make a row
> look complete. Prices move daily; always re-check the linked page before buying.

---

## What this repo contains

| Path | Purpose |
|---|---|
| `data/products.json` | Every verified listing (price, purity, evidence quote, source URL, capture time) |
| `data/retailers.json` | Merchant profiles: returns, contact, reputation, hallmark policy |
| `data/sources.json` | Authority sources (FTC, eCFR, LBMA/World Gold Council, labs) |
| `data/prices.json` | Dated gold spot-price snapshots used by the calculator |
| `scripts/verify.py` | **Security/verification gate**: fails on unsourced or inferred values |
| `scripts/build_site.py` | Builds the static site + reports from JSON data |
| `COORDINATION.md` | Shared task board for parallel agent sessions |
| `index.html` + `*.html` | Published dashboard and category pages |
| `flagged.html` | Everything unverified, irregular, or needing a human decision |
| `sources.html` | Full source register with links and read-dates |

## Buying checklist (the standard every listing is scored against)

1. **Purity** — confirmed karat (10K/14K/18K), not "gold tone".
2. **Solid gold** — listing explicitly says solid gold; *not* plated, vermeil, filled, overlay, tone.
3. **Hallmark** — karat stamp **plus** a maker's/manufacturer's mark.
4. **Weight** — ring weight in **grams**, provided by the seller.
5. **Seller reputation** — independent reviews/complaints, real contact details.
6. **Price** — compared with gold content at the current spot price; "too cheap" = red flag.
7. **Returns** — returnable after inspection; check resized/custom exclusions.
8. **Payment** — credit card preferred (chargeback protection).
9. **Documentation** — keep listing, receipt, description, purity claims.
10. **On arrival** — independent jeweler verifies purity + weight before wearing/resizing.
11. **Best verification** — XRF or other professional assay; the stamp alone proves nothing.
12. **Walk away** if the seller blocks independent verification or returns.

## Build & verify locally

```bash
python3 scripts/verify.py          # verification + hallucination/price-sanity gate
python3 scripts/build_site.py      # regenerates the site from data/*.json
python3 scripts/verify.py --check-links --offline   # link-register sanity check
```

`verify.py` exits non-zero if any record is unsourced, any price lacks a capture timestamp, or a
non-solid-gold item appears in a solid-gold category. That is the guardrail against invented data.

## Multi-session coordination

Read `COORDINATION.md` before editing anything. Claim a task, respect file scopes, and log sources,
verification performed, and irregularities when you finish.
