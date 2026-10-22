# GOLD3 — Gold Engagement Ring Research

A small, source-first dashboard for comparing gold engagement-ring listings against the buyer's verification checklist. **No ring is marked qualified unless each required claim has direct evidence.** Values the sources do not establish remain blank and are published under [Flagged for Review](pages/flagged.html).

## No-hallucinations standard

- The landing page leads with **NO HALLUCINATIONS**.
- Retail prices are dated snapshots from each seller's first-party product page—not live guarantees. Reopen the linked listing before purchase.
- None of the three candidate pages gives a gold-only weight in grams, documents the physical karat/maker marks, or confirms that independent testing preserves return eligibility. No listing is fully cleared.
- No current gold quote or estimated raw-gold value is embedded. Fine-gold mass is calculated only after a seller-confirmed gold-only mass, karat, mass/karat-source date, and HTTPS link supporting both inputs are entered; raw-metal value remains blank until a separately dated quote and source link are supplied.
- A seller-page claim is not a physical purity test. Ask the seller for written product-specific details, preserve the listing and receipt, and have an independent jeweler or lab inspect/test the ring before wearing or resizing.
- The FTC/eCFR source is read in context: its “solid” example concerns hollow-center gold-alloy products; it is not a claim that every 14K item is hollow.

## Dashboard pages

- [Overview](index.html) — top summary, candidate snapshot, seller-contact/reputation signals, and the no-hallucinations policy.
- [Ring candidates](pages/rings.html) — sourced product table with dated retail prices and blank, flagged evidence gaps.
- [Checklist & verification](pages/verify.html) — one row per buyer requirement, current evidence, next step, and source links.
- [Gold calculator](pages/calculator.html) — nominal fine-gold mass and optional raw-metal arithmetic. No price or weight is prefilled.
- [Flagged for Review](pages/flagged.html) — open evidence gaps, time-sensitive items, source context, and recommended next checks.
- [Source library](pages/sources.html) — first-party product/policy pages, government references, professional test-method context, and third-party review platforms.

## Data and verification

Research snapshot date: **2026-10-22** (UTC). Structured data lives in `data/`:

- `rings.json` — candidate products and source-bound fields.
- `merchants.json` — official contact details and independently linked reputation snapshots.
- `checklist.json` — buyer requirements and current evidence status.
- `findings.json` — published flags and next actions.
- `sources.json` — source register, supported claims, review date, and scope caveats.
- `market.json` — explicit blank state for the unverified gold quote.

Run the source / security / no-hallucination / local-link pass after **every research review**:

```sh
node scripts/audit.mjs
node scripts/calculator-smoke.mjs
```

The audit validates data references, price timestamps and sources, blank/unverified states, the qualification gate, HTTPS/approved source hosts, local navigation, and unsafe HTML/JavaScript patterns. The calculator smoke test checks its evidence gates, nominal-purity arithmetic, troy-ounce conversion, and date/HTTPS handling without adding dependencies. It does **not** visit every external site, test a physical ring, independently establish that a retailer's claim is true, or replace a human review. Each external source was reviewed directly for this snapshot; recheck every live listing, policy, complaint, and rating before purchase.

## Run locally

No package installation is required. From the repository root:

```sh
python3 -m http.server 4173 --bind 0.0.0.0
```

Open `http://localhost:4173/` in a local browser. The site only fetches its own static JSON; product and source links open the cited external pages.

## GitHub Pages

`.github/workflows/pages.yml` runs the audit on pull requests and pushes to `main`; after validation, it deploys the static site to GitHub Pages. Expected project URL after Pages is enabled and deployment succeeds:

<https://karagemop466-tech.github.io/GOLD3/>

## Important scope note

This project is a research organizer, not a jeweler, assay lab, appraisal, legal opinion, or guarantee of seller conduct. Third-party reviews and complaints are linked as separate signals, not combined into an endorsement or finding about a specific ring. Missing information is an open question—not permission to infer a value.
