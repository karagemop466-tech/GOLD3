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
| `T-01` | Initial Repository Line-by-Line Audit, NIST/FTC/USC Gold Hallmarking Standards & Current Spot Gold Price Verification | `in progress` | `session-698f08f6` | `2026-10-22T23:11:00Z` | `COORDINATION.md`, `verification/repo-audit.md`, `data/spot-and-standards.json` | Pending official source verification |
| `T-02` | Official Solid Gold Solitaire Engagement Rings & Settings Research & Line-by-Line Verification | `unclaimed` | — | — | `data/solitaire-rings.json` | Pending |
| `T-03` | Official Solid Gold Bands, High-Karat Investment Rings & Vintage/Signet Rings Research & Weight Verification | `unclaimed` | — | — | `data/bands-and-high-karat.json` | Pending |
| `T-04` | Official Jeweler Reputation, Contact Info, Return Policies (Resized/Custom Exclusions) & Payment Protection Audit | `unclaimed` | — | — | `data/sellers-policies.json` | Pending |
| `T-05` | Automated Anti-Hallucination & Security Verification Suite (`scripts/run_security_audit.py`) | `unclaimed` | — | — | `scripts/run_security_audit.py`, `verification/sources-manifest.json`, `verification/audit-log.json`, `VERIFICATION_REPORT.md` | Pending |
| `T-06` | Dashboard Landing Page, Category Subpages, Interactive Gold/Weight Calculator & Flagged-for-Review Page | `unclaimed` | — | — | `index.html`, `solitaire-settings.html`, `bands-vintage-rings.html`, `sellers-policies.html`, `calculator.html`, `checklist-standards.html`, `flagged-for-review.html`, `security-audit.html`, `assets/`, `data/verified-data.js`, `README.md`, `.nojekyll` | Reserved for integration step after data tasks complete |
| `T-07` | Final Integration, Multi-Pass Hallucination & Link Audit, PR to `main`, Merge & Live GitHub Pages Verification | `unclaimed` | — | — | Repository-wide final check + `COORDINATION.md` PR/merge log | Pending |

---

## Activity & Handoff Log

- **`2026-10-22T23:11:00Z` — `session-698f08f6` (`arena/698f08f6-gold3`):**
  - Inspected repository root and remote branches (`git fetch --all --prune`, `gh pr list --state all`, `gh api repos/karagemop466-tech/GOLD3/branches`, `gh api repos/karagemop466-tech/GOLD3/pages`).
  - Confirmed `COORDINATION.md` did not exist yet; only `README.md` (`# GOLD3`, 7 bytes, commit `1c10511ef71d1c0855283762fb854c154039bc56`) existed on `main`.
  - Confirmed GitHub Pages is configured on `main` (`/`), `https://karagemop466-tech.github.io/GOLD3/` (`https_enforced: true`).
  - Claimed `T-01` (`COORDINATION.md`, `verification/repo-audit.md`, `data/spot-and-standards.json`) and pushing claim immediately before beginning source fetching.
