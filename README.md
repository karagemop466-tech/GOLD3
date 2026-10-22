# GOLD3 — verified gold engagement rings

A source-verified workbench for buying a **solid gold engagement ring** online.

**No hallucinations.** Every number on the site is traceable to a linked official page, retrieved
**22 October 2026**. Where a seller does not publish a value, the cell is blank, marked
`unverified`, and listed on the Flagged for Review page. Nothing is estimated, averaged, or
carried over from "typical" industry practice.

Live site: **https://karagemop466-tech.github.io/GOLD3/**

---

## What is in here

| Path | What it is |
|---|---|
| `index.html` | Dashboard landing page. The no-hallucination policy is the first thing on it. |
| `rings.html` | Every verified listing: price, karat, weight, solid-gold verdict, stamp, returns, flags, sources. Filterable. |
| `sellers.html` | Return windows and exclusions, contact details, disclosure practices per seller. |
| `analysis.html` | Coverage of each requirement, and melt value vs asking price for rows that publish a weight. |
| `calculator.html` | Fine-gold content and melt value from a weight you supply and the dated spot price. |
| `standards.html` | The FTC jewellery guides and National Stamping Act rules the checklist rests on, with citations. |
| `flagged.html` | Everything unconfirmed or irregular, with severity, remedy and source. |
| `methodology.html` | The passes run, the sources used, and what the audit caught. |
| `data/gold-price.json` | The dated benchmark, with publisher, quote and caveats. |
| `data/rings.json` | The listing rows, each with verbatim quotes and source URLs. |
| `data/sellers.json` | Seller policy and contact facts. |
| `data/standards.json` | Karat fineness table and legal rules with citations. |
| `data/flags.json` | Flag definitions: what was found, why it matters, what to do. |
| `scripts/audit.py` | The anti-hallucination audit. |
| `reports/audit-report.md` | Output of the last audit run. |
| `scripts/render-test.js` | Runs every page's table against the real JSON in a DOM shim (20 checks). |
| `COORDINATION.md` | Shared task board for parallel agent sessions. |

## Run the checks

```bash
python3 scripts/audit.py          # exits non-zero on any error
node scripts/render-test.js       # renders every page against the real JSON
```

Both run in CI (`.github/workflows/audit.yml`) on every push and pull request. The site is published
by GitHub Pages from the `main` branch root, so a merge to `main` goes live directly.

The audit fails when a price does not appear in its own quoted source text, when a gram figure is
not present in its supporting quote, when a "solid gold" pass was awarded without the seller saying
"solid", when a flag is referenced but undefined, when a field is both verified and unverified, when
contact details appear without a source, when a karat fraction does not equal `n ÷ 24`, or when the
HTML prints a dollar figure that exists nowhere in the data.

## View the site locally

```bash
python3 -m http.server 8000
# then open http://localhost:8000/
```

The pages read `data/*.json` over HTTP, so serve them rather than opening the files directly.

## Headline findings

1. **Nobody publishes an independent assay.** Zero sellers in this study publish a per-item XRF scan
   or assay. The karat is always the seller's own claim, at most backed by a stamp — exactly the gap
   the checklist warns about.
2. **"18k" can mean a coating.** One listing with "18k" in its name is 18k gold *vermeil*: a gold
   layer over sterling silver, per 16 CFR 23.4.
3. **A headline price may be the setting only.** One major retailer prices the setting separately
   from the centre diamond.
4. **One retailer's return policy excludes precious metals** — which fails the return requirement
   outright, whatever the price.
5. **Only estate jewellers publish weights in grams**, and even then it is *total* item weight, so a
   melt calculation from it is an upper bound.

## Standing recommendation

Re-run the audit after every review, then do one deliberate human pass whose only job is to hunt for
hallucinations: pick any number on the site and try to find it on the linked page. If it is not
there, delete it and mark the field unverified. Better an empty cell than a confident error.

## Scope and disclaimer

Research, not appraisal, legal or financial advice. Listings, prices and policies change without
notice — re-check the linked source before buying. Every ring still needs independent verification
(XRF or assay) after delivery, before it is worn or resized.
