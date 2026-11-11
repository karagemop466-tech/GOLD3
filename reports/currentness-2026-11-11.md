# Currentness and integrity review — 11 November 2026

## Scope and limitation

The repository already contains a static dashboard, 71 recorded listing rows across three datasets, dated product and gold-price captures, and a historical verification ledger. This session **did not re-verify those records line by line against their sources**: the sandbox permits outbound connections only to specified hosts, and requests to the seller and government websites failed. Current product prices, gold spot prices, availability, policies, specifications, the accuracy of the historical quotations, and external-link health are **unverified**. No new market or product figures were entered. The historical data are preserved as historical research, not endorsed as current or as definitively accurate.

Example URLs attempted without a successful response: [Blue Nile](https://www.bluenile.com/) and [eCFR 16 CFR Part 23](https://www.ecfr.gov/current/title-16/chapter-I/subchapter-B/part-23). GitHub's [Pages API](https://docs.github.com/en/rest/pages/pages#get-a-github-pages-site) reported the existing Pages site as built from `39e2a17bb13c87e74cafd5dd4891ebf0869140d4`; that deployment predates this review and does not contain its warnings.

## Irregularities and action

- All current values and external links require source re-checking. The dashboard and every generated page now display a currentness alert linking to a review flag. Previous dated prices and evidence remain accessible for historical context, not as confirmed current values.
- The main calculator used an unlabelled example weight, could show $0 for a missing weight, characterized below-melt prices as impossible, and offered unsourced markup categories. It now leaves missing/invalid weight calculations blank and describes price comparisons as estimates, not authenticity or market-value verdicts. The 5% tolerance is explicitly illustrative rather than a claim about Sarraf.
- Prior reports contain dated findings and alleged discrepancies; neither those allegations nor their resolution were independently confirmed during this session. Check each source link before relying on them.
- Archived observatory calculator and prior stored editorial claims were not independently audited line by line; the sitewide warning applies to generated main-site pages, not the archived standalone site.

## Local checks

Executed the data verification, Dataset C checks, both builders, requirements matrix and hallucination scan, audit, security audit, render test, report generator, and archived security/link tests. Local checks passed. `scripts/test_currentness.js` also tests warnings and calculator edge cases. These are offline structural, arithmetic and stored-quote consistency checks; despite names or console messages such as “verified” or “dead links,” they do **not** confirm live pages, official claims, source ownership, or external HTTP status. A passing check is not proof that there are no hallucinations. Run the suite after every review and actively look for unsupported claims.

## Required next step

In an environment with authorized access to all cited sites, reopen every row's official product and policy source and the market sources, verify each value and link, blank and flag any value that cannot be confirmed, rebuild and rerun the checks, then create/merge the integration PR and verify the new Pages deployment. No source verification or deployment success is claimed for this session.
