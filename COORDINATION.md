# COORDINATION.md — Shared Task Board (`karagemop466-tech/GOLD3`)

> **Zero-Hallucination & Official Source Mandate:** Every price, gram weight, karat fineness, hallmark requirement, return policy rule, and spot gold rate in this repository **must** be verified directly from an official trusted primary source and linked verbatim. Any attribute not explicitly published by the official source **must remain blank (`null`)** and be marked **Unverified / Needs Review** on the **Flagged for Review** page (`flagged-for-review.html`). Automated security & hallucination detection passes (`scripts/run_security_audit.py`) must run after every review pass.

---

## Active Session Registry & Branch Protocol

| Session ID | Branch | Role | Started (UTC) | Status | Notes |
|---|---|---|---|---|---|
| `session-698f08f6` | `arena/698f08f6-gold3` | Primary Research, Verification, Audit & Final Integration Session | `2026-10-22T23:11:00Z` | `active` | Arena session bound to fixed branch `arena/698f08f6-gold3`; monitors `origin` via `git fetch --all --prune` and `git pull --rebase` before every push to detect any concurrent session branches. |

---

## Shared Task Board

| Task ID | Task Description | Status | Owning Session ID | Claimed At (UTC) | File Scope (Non-Overlapping) | Verification Status |
|---|---|---|---|---|---|---|
| `T-01` | Initial Repository Line-by-Line Audit, NIST/FTC/USC Gold Hallmarking Standards & Current Spot Gold Price Verification | `done` | `session-698f08f6` | `2026-10-22T23:11:00Z` | `COORDINATION.md`, `verification/repo-audit.md`, `data/spot-and-standards.json` | Verified against 8 primary sources (`2026-10-22T23:13:00Z`) |
| `T-02` | Official Solid Gold Solitaire Engagement Rings & Settings Research & Line-by-Line Verification | `in progress` | `session-698f08f6` | `2026-10-22T23:15:00Z` | `data/solitaire-rings.json` | Fetching & verifying official jeweler product pages |
| `T-03` | Official Solid Gold Bands, High-Karat Investment Rings & Vintage/Signet Rings Research & Weight Verification | `in progress` | `session-698f08f6` | `2026-10-22T23:15:00Z` | `data/bands-and-high-karat.json` | Fetching & verifying official jeweler product pages |
| `T-04` | Official Jeweler Reputation, Contact Info, Return Policies (Resized/Custom Exclusions) & Payment Protection Audit | `in progress` | `session-698f08f6` | `2026-10-22T23:15:00Z` | `data/sellers-policies.json` | Fetching & verifying official return/payment/BBB pages |
| `T-05` | Automated Anti-Hallucination & Security Verification Suite (`scripts/run_security_audit.py`) | `unclaimed` | — | — | `scripts/run_security_audit.py`, `verification/sources-manifest.json`, `verification/audit-log.json`, `VERIFICATION_REPORT.md` | Pending |
| `T-06` | Dashboard Landing Page, Category Subpages, Interactive Gold/Weight Calculator & Flagged-for-Review Page | `unclaimed` | — | — | `index.html`, `solitaire-settings.html`, `bands-vintage-rings.html`, `sellers-policies.html`, `calculator.html`, `checklist-standards.html`, `flagged-for-review.html`, `security-audit.html`, `assets/`, `data/verified-data.js`, `README.md`, `.nojekyll` | Reserved for integration step after data tasks complete |
| `T-07` | Final Integration, Multi-Pass Hallucination & Link Audit, PR to `main`, Merge & Live GitHub Pages Verification | `unclaimed` | — | — | Repository-wide final check + `COORDINATION.md` PR/merge log | Pending |

---

## Activity & Handoff Log

- **`2026-10-22T23:11:00Z` — `session-698f08f6` (`arena/698f08f6-gold3`):**
  - Initialized `COORDINATION.md` and claimed `T-01` (`8c2cda3`).
- **`2026-10-22T23:15:00Z` — `session-698f08f6` (`arena/698f08f6-gold3`):**
  - Completed `T-01` (`verification/repo-audit.md`, `data/spot-and-standards.json`).
  - **Sources Verified in `T-01`:**
    1. Kitco Live World Spot Gold (`https://www.kitco.com/price/precious-metals`): **$4,025.10/oz Bid ($129.41/g)** at `Oct 22, 2026 19:13 EDT`.
    2. BullionVault Live Wholesale Spot (`https://www.bullionvault.com/gold-price-chart.do`): **$4,026.25/oz ($129.45/g)** at `Oct 22, 2026 19:12:56 GMT-04:00` (0.029% cross-feed agreement).
    3. U.S. Code Title 15, Ch. 8 (`https://uscode.house.gov/view.xhtml?path=%2Fprelim%40title15%2Fchapter8&edition=prelim`): `15 U.S.C. § 295` fineness tolerances (0.003 unsoldered / 0.007 soldered) & `15 U.S.C. § 297(b)` mandatory registered manufacturer trademark alongside any karat stamp.
    4. U.S. FTC Jewelry Guides `16 CFR Part 23` (`https://www.ecfr.gov/current/title-16/chapter-I/subchapter-B/part-23`): 10K minimum karat gold threshold, vermeil >= 2.5 microns on sterling silver, electroplate/gold-filled rules.
    5. UK Hallmarking Act 1973 & GOV.UK Guidance (`https://www.legislation.gov.uk/ukpga/1973/43`, `https://www.gov.uk/government/publications/hallmarking-guidance-notes/hallmarking-is-the-law-guidance-summary`): 375/585/750/916/999 fineness marks & 1.0g gold statutory hallmark threshold.
    6. NIST OWM & SP 811 (`https://www.nist.gov/pml/owm/metric-si/unit-conversion/precious-metals-conversion-information`): exact `31.1034768 g/oz t`, `1.55517384 g/dwt`, `0.2 g/ct`.
    7. GIA *Gems & Gemology* Winter 2024 XRF Chemical Analysis (`https://www.gia.edu/gems-gemology/winter-2024-chemical-analysis`), Summer 2025 Lab Notes "Gold-Plated Gold" (`https://www.gia.edu/gems-gemology/summer-2025-lab-notes-gold-plated-gold0`), and Bench Tip #9 Touchstone Testing (`https://www.gia.edu/bench-tip-use-the-touchstone-method-for-testing-purity-karat-gold`).
  - **Irregularities Logged in `T-01`:** Initial repo commit `1c10511` contained only stub `# GOLD3` without trailing newline or sources.
  - Claimed `T-02`, `T-03`, and `T-04` and pushing immediately.
