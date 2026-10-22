# GOLD3 — Verified Solid Gold Engagement Ring Research, Melt Value Calculator & Anti-Hallucination Audit

- **Live GitHub Pages Dashboard:** <https://karagemop466-tech.github.io/GOLD3/>
- **Coordination & Handoff Log:** [`COORDINATION.md`](COORDINATION.md)
- **Automated Security & Hallucination Report:** [`VERIFICATION_REPORT.md`](VERIFICATION_REPORT.md)

---

## Core Mandate: Zero-Hallucinations Policy & Line-by-Line Verification

1. **Zero Hallucinated Prices, Weights, or Specs:** Every ring price, metal gram weight, karat fineness, hallmark requirement, return policy rule, and live spot gold rate in this repository was verified directly from an official primary source on **`2026-10-22`** and linked on every table row.
2. **Never Infer Missing Values:** Whenever an official retailer listing omits a specification (for example, Blue Nile, Brilliant Earth, and Mejuri omitting gold gram weights on product pages, or Ross-Simons Item `993085` omitting the exact gram split between its `22kt` coin and `14kt` shank), the value is strictly left **`null` (`— Unverified`)** and published transparently on **[`flagged-for-review.html`](flagged-for-review.html)**.
3. **Mandatory Automated Security & Hallucination Passes:** After every data review or edit pass, run:
   ```bash
   python3 scripts/run_security_audit.py --pass-label "Post-Review Verification Pass"
   python3 scripts/build_site.py
   ```
   Always inspect [`flagged-for-review.html`](flagged-for-review.html) and [`security-audit.html`](security-audit.html) alongside live primary URLs to look for hallucinations, seller copy contradictions, or live retail price changes.

---

## Dashboard Pages (Served from Repository Root `/`)

| File | Purpose |
|---|---|
| [`index.html`](index.html) | Front-page executive summary, prominent **No-Hallucinations Mandate**, live KPIs (`$4,025.10/oz = $129.41/g`), embedded interactive Gold/Melt Calculator, key findings, and 21-row master comparison table |
| [`checklist-standards.html`](checklist-standards.html) | Complete **12-Point Online Gold Engagement Ring Buyer Checklist**, US/UK hallmarking statutes (`16 CFR Part 23`, `15 U.S.C. Ch. 8`, `UK Hallmarking Act 1973`), `9K–24K` fineness table, and post-arrival XRF testing protocol |
| [`solitaire-settings.html`](solitaire-settings.html) | Line-by-line audit of `9` solitaire engagement settings, GIA diamond rings, and `$29` gold-plated brass scam-control benchmark |
| [`bands-vintage-rings.html`](bands-vintage-rings.html) | Line-by-line audit of `12` pure `24K` bands, traditional `14K` solid bands, Italian signets, `22K` coin mount, and diamond eternity bands with exact melt multiples (`1.50x`–`3.96x`) |
| [`sellers-policies.html`](sellers-policies.html) | Independent reputation & policy audit across `5` jewelers (`Ross-Simons`, `Blue Nile`, `Brilliant Earth`, `Menē`, `Mejuri`): physical addresses, phones, BBB ratings (`A+` to `D-`), resized/engraved return exclusions, and `1.5%` bank wire chargeback traps |
| [`calculator.html`](calculator.html) | Dedicated interactive **Gold Purity, Gram/dwt/ozt Weight, GIA Stone Carat Deduction & Melt Value Calculator** with live dynamic `9K–24K` reference table |
| [`flagged-for-review.html`](flagged-for-review.html) | Complete transparency registry of all `16` flagged entries (`37` line-by-line notes), omitted gram weights, live page contradictions, and seller warnings |
| [`security-audit.html`](security-audit.html) | Chronological multi-pass verification log (`SEC-01`..`SEC-07`), SHA-256 dataset digests, and complete manifest of official HTTPS primary sources |

---

## Structured Primary Data & Verification Artifacts

- `data/spot-and-standards.json` — Verified `2026-10-22` spot gold quotes (Kitco & BullionVault), exact NIST mass conversion constants (`31.1034768 g/ozt`), `9K–24K` purity table, and statutory standards (`STD-01..STD-06`).
- `data/solitaire-rings.json` — `9` verbatim-verified solitaire listings (`SOL-01..SOL-09`).
- `data/bands-and-high-karat.json` — `12` verbatim-verified bands, signets & coin rings (`BND-01..BND-12`).
- `data/sellers-policies.json` — `5` verified jeweler corporate, BBB, return & payment audits (`SEL-*`).
- `verification/repo-audit.md` — Line-by-line audit of initial repository state (`1c10511`).
- `verification/sources-manifest.json` — SHA-256 data digests + deduplicated manifest of all official HTTPS sources.
- `verification/audit-log.json` — Machine-recorded history of every `run_security_audit.py` pass.
