# GOLD3 — solid gold engagement ring research

**Live site: https://karagemop466-tech.github.io/GOLD3/**

A source-linked buying file for solid gold engagement rings. Each listing records the karat, the stated
gold weight, the price and the seller's return terms **with the exact quote and the date it was read**,
then computes what the gold in the ring is actually worth at the current spot price.

---

## Rule 0 — no hallucinated prices, ever

Every number on the site was **read from the seller's own product page** and stamped with the date it was read.

- If a seller does not publish a value, the table shows `—` and the item is listed on the
  [Flagged for review](https://karagemop466-tech.github.io/GOLD3/flagged.html) page. Nothing is estimated,
  averaged, inferred from a photo, or copied from a search-engine snippet.
- A value seen in a search-engine copy of a page is recorded as an *observation* only — it is never used as the price.
  That rule already caught a real discrepancy: Ross-Simons item 932728 showed **$270** in the cached copy and
  **$299** on the live page.
- `scripts/audit.py` re-checks all of this after every review pass and **fails the build** if a value has no
  quoted source. Warnings are published, not hidden.

## What is in the repo

| Path | What it is |
|---|---|
| `index.html` … `method.html` | The generated static site (GitHub Pages, no build step on the server) |
| `data/rings.json` | The ring dataset — one object per listing, each field with its evidence quote |
| `data/sellers.json` | Seller register: contact details, return terms, what is still unverified |
| `data/standards.json` | Quoted U.S. law: 16 CFR Part 23 (FTC jewellery guides), 15 U.S.C. §§ 294–297 |
| `data/spot.json` | Dated gold spot price record (World Gold Council / ICE Data Services) |
| `scripts/audit.py` | 14 no-hallucination + consistency checks → `reports/audit-latest.{md,json}` |
| `scripts/build.py` | Dependency-free site generator + internal link checker |
| `COORDINATION.md` | Shared task board for parallel agent sessions |

Rebuild everything:

```bash
python3 scripts/audit.py    # audit only, prints the report
python3 scripts/build.py    # regenerates every page from data/*.json, then link-checks
```

No third-party packages. Python 3.9+.

## Pages

- **Dashboard** — the no-hallucination pledge, headline numbers, and what the data already shows.
- **Ring list** — live-verified listings only, with fine-gold grams, melt value, premium vs melt and flags, plus an
  evidence appendix quoting the seller's wording for every field.
- **Sellers** — who publishes a gram weight, what their return rules actually say, what is still unknown.
- **Rules & law** — the FTC jewellery guides and the Stamping Act, quoted, plus raw gold value by karat.
- **Calculator** — weight + karat + spot → fine gold grams, melt value, and the markup you are being asked to pay.
- **Flagged for review** — every blank field, conflicting price and dead listing, with sources.
- **Method & audit** — the protocol, the latest automated audit run and the build's link-check results.

## Current findings (2026-10-22)

1. **Most sellers do not publish the ring's gram weight** — only 2 of 7 live-verified listings do
   (both Ross-Simons). Without it you cannot check the gold value before buying. This is the single biggest gap
   against the checklist, and it is why the audit treats a missing weight as data, not as a rounding problem.
2. **"Setting price" is not a price.** Blue Nile's $1,145 and James Allen's figures exclude the centre diamond,
   so they are never compared to a melt value on this site.
3. **A karat stamp is not a test.** 15 U.S.C. § 295 allows the real fineness to sit 3/1000 below the stamp
   (7/1000 when solder is included), and § 297(b) is the legal basis for requiring a maker's mark next to the karat.
4. **Prices move and listings die.** James Allen product URLs now redirect to Blue Nile with "sold out"; two Costco
   URLs return "Page Not Found". Dead listings are kept for the record and excluded from recommendations.
5. **Vermeil is everywhere in gold-looking jewellery.** Mejuri's "18k gold vermeil" is a 2.5-micron gold layer over
   sterling silver — the exact threshold in 16 CFR § 23.4. It is in the dataset as the counter-example.

## Sources used

- 16 CFR Part 23 — Guides for the Jewelry, Precious Metals, and Pewter Industries (eCFR, read 2026-10-22)
- 15 U.S.C. § 294, § 295, § 297 — National Gold and Silver Stamping Act (Cornell LII, read 2026-10-22)
- World Gold Council, Goldhub gold spot prices (USD 4,024.36/ozt as of 2026-10-21)
- Blue Nile, Ross-Simons, Mejuri, Tiffany & Co., Catbird product and policy pages (read 2026-10-22)

## Not advice

Research, not an appraisal, not legal or financial advice. Confirm the price on the seller's page yourself before
buying, and have an independent jeweller weigh and test the ring before you wear or resize it.
