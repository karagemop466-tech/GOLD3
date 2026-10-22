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
| `T-02` | Official Solid Gold Solitaire Engagement Rings & Settings Research & Line-by-Line Verification | `done` (`needs review` items logged for Flagged page) | `session-698f08f6` | `2026-10-22T23:15:00Z` | `data/solitaire-rings.json` | 9 live product URLs fetched verbatim (`SOL-01`..`SOL-09`) on `2026-10-22` |
| `T-03` | Official Solid Gold Bands, High-Karat Investment Rings & Vintage/Signet Rings Research & Weight Verification | `done` (`needs review` items logged for Flagged page) | `session-698f08f6` | `2026-10-22T23:15:00Z` | `data/bands-and-high-karat.json` | 12 live ring entries (`BND-01`..`BND-12`), including 8 official weight-disclosed rings (`1.7g`–`12.0g`) |
| `T-04` | Official Jeweler Reputation, Contact Info, Return Policies (Resized/Custom Exclusions) & Payment Protection Audit | `done` (`needs review` items logged for Flagged page) | `session-698f08f6` | `2026-10-22T23:15:00Z` | `data/sellers-policies.json` | 5 jewelers verified across official policy pages + BBB profiles (`2026-10-22`) |
| `T-05` | Automated Anti-Hallucination & Security Verification Suite (`scripts/run_security_audit.py`) | `in progress` | `session-698f08f6` | `2026-10-22T23:22:00Z` | `scripts/run_security_audit.py`, `verification/sources-manifest.json`, `verification/audit-log.json`, `VERIFICATION_REPORT.md` | Building executable multi-pass verification & security checker |
| `T-06` | Dashboard Landing Page, Category Subpages, Interactive Gold/Weight Calculator & Flagged-for-Review Page | `unclaimed` | — | — | `index.html`, `solitaire-settings.html`, `bands-vintage-rings.html`, `sellers-policies.html`, `calculator.html`, `checklist-standards.html`, `flagged-for-review.html`, `security-audit.html`, `assets/`, `data/verified-data.js`, `README.md`, `.nojekyll` | Reserved for integration step after `T-05` pass 1 completes |
| `T-07` | Final Integration, Multi-Pass Hallucination & Link Audit, PR to `main`, Merge & Live GitHub Pages Verification | `unclaimed` | — | — | Repository-wide final check + `COORDINATION.md` PR/merge log | Pending |

---

## Activity & Handoff Log

- **`2026-10-22T23:11:00Z` — `session-698f08f6` (`arena/698f08f6-gold3`):**
  - Initialized `COORDINATION.md` and claimed `T-01` (`8c2cda3`).
- **`2026-10-22T23:15:00Z` — `session-698f08f6` (`arena/698f08f6-gold3`):**
  - Completed `T-01` (`10ffe44`); verified Oct 22, 2026 live gold spot (**$4,025.10/oz Bid = $129.41/g** on Kitco; **$4,026.25/oz = $129.45/g** on BullionVault) and official US/UK/NIST/GIA standards.
- **`2026-10-22T23:22:00Z` — `session-698f08f6` (`arena/698f08f6-gold3`):**
  - Completed `T-02` (`data/solitaire-rings.json`), `T-03` (`data/bands-and-high-karat.json`), and `T-04` (`data/sellers-policies.json`) via direct live `fetch_page` verification on `2026-10-22`.
  - **Key Irregularities & Findings Flagged for Review (`flagged-for-review.html`):**
    1. **Ross-Simons Item `251663` (`https://www.ross-simons.com/products/251663`):** Direct karat contradiction on official page — heading/spec table state `10kt Yellow Gold` (41.67%) while description paragraph claims `Set in polished 14kt yellow gold` (58.33%).
    2. **Brilliant Earth `BE1FM0126` (`https://www.brilliantearth.com/Fairmined-2mm-Six-Prong-Solitaire-Ring-Gold-BE1FM0126-24910022/`):** Top banner displays `Free 1-Year Resizing`, whereas body text states `Due to the materials and distinctive design of this style, resizing is not available for this ring.`
    3. **Brilliant Earth `BE1199H6` (`https://www.brilliantearth.com/Six-Prong-Petite-Comfort-Fit-1.5mm-Solitaire-Ring-Gold-BE1199H6-1912137/`):** Live price repriced to **$850** (vs stale $650 snippet); uses mixed `18K Yellow Gold` shank with `14K White Gold` prongs; 1.5 mm ultra-thin shank warning.
    4. **Ross-Simons Item `993085` (`https://www.ross-simons.com/products/993085`):** Publishes `5.9 grams` total across mixed `22kt` coin + `14kt` shank without disclosing exact alloy gram split — left `pure_gold_grams: null` rather than inferred (`3.4417g–5.4083g` mathematical bounds documented).
    5. **Mejuri `Diamond Eternity Band` (`https://mejuri.com/shop/products/diamond-eternity-band?Material=Solid+Yellow+Gold+%2814k%29&Stone=Natural+Diamond`):** Body states `0.532ct` average weight while spec bullet prints `0.044 ct - 0.056 ct`; `Diamonds Band` repriced to **$648** (vs stale $498).
    6. **Seller BBB & Policy Risks:** Mejuri carries a **BBB `D-` rating** (`https://www.bbb.org/ca/on/toronto/profile/jewelry-manufacturers/mejuri-0107-1370644`); Menē carries a **7-day return window** (`https://mene.com/customer-care?hcUrl=%2Fen-US%2Farticles%2Freturns-319505`) and **BBB `D+` rating** (`https://www.bbb.org/ca/on/ontario/profile/jewelry-designers/mene-inc-0107-1413670`); Blue Nile & Brilliant Earth offer **1.5% bank wire discounts** that forfeit credit-card chargeback protection; all 5 sellers void returns on engraved/resized items.
    7. **Plated Control Benchmark (`SOL-09`, `https://www.ross-simons.com/products/241592`):** Live `$29` `"14kt Yellow Gold-Plated"` brass ring included as rejected control proving Checklist #2 & #6.
  - Claimed `T-05` (`scripts/run_security_audit.py` + `verification/sources-manifest.json`) and pushing immediately.
