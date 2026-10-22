# COORDINATION.md — Shared Task Board (`karagemop466-tech/GOLD3`)

> **ZERO-HALLUCINATIONS MANDATE:** Every figure, price, purity claim, gram weight, return policy, and standard in this repository MUST be verified line-by-line from an official, trusted source with a clickable source URL. Any value that cannot be confirmed directly from an official source MUST be left blank (`null` / empty cell) and flagged as `unverified` (`needs review`) on the **Flagged for Review** page. Never infer, estimate, interpolate, or fabricate values. Run automated security/anti-hallucination passes after every review and recommend checking for hallucinations.

## Session & Branch Coordination Protocol

- **Repository:** `https://github.com/karagemop466-tech/GOLD3`
- **Active Session ID:** `arena/cbea1001-gold3` (branch name fixed by Arena runtime environment; all commits/pushes from this session go to `arena/cbea1001-gold3` prior to PR integration into `main`).
- **Task Status Definitions:**
  - `unclaimed` — Available to be claimed by a session.
  - `in progress` — Actively claimed by the listed session ID; other sessions must not edit files in its scope.
  - `done` — Completed, verified line-by-line against official sources, and audited by anti-hallucination checks.
  - `needs review` — Published on the **Flagged for Review** (`flagged.html`) page with official source links for manual human inspection; does **not** block merge.
- **Conflict & Parallel Branch Policy:** Always fetch remote state and run `git pull --rebase` before pushing. Before final integration/merge to `main`, check `origin/main` and remote branches; if another session has merged work to `main`, integrate additively without discarding the other session's work, re-verify combined data line-by-line, and log any conflict resolution here.

---

## Shared Task Board

| Task ID | Task Description | Status | Owning Session ID | File Scope |
|---|---|---|---|---|
| **C1** | Repository review (`README.md`, commit history, GitHub Pages config, remote branch audit) & baseline irregularity logging | `done` | `arena/cbea1001-gold3` | `COORDINATION.md`, `data/repo-audit.json` |
| **C2** | Official gold spot benchmark price & US federal purity/hallmark/XRF standards verification | `done` | `arena/cbea1001-gold3` | `data/gold-benchmark.json`, `data/purity-standards.json` |
| **C3** | Official gold engagement ring product listings collection & line-by-line verification | `done` | `arena/cbea1001-gold3` | `data/rings.json` |
| **C4** | Seller reputation, contact info, return policies (custom/resized exclusions), payment protection & XRF inspection verification | `done` | `arena/cbea1001-gold3` | `data/sellers.json` |
| **C5** | Anti-hallucination security scanner, raw gold / melt math verifier, blank-cell enforcement & link checker | `done` | `arena/cbea1001-gold3` | `package.json`, `scripts/security-check.mjs`, `scripts/verify-links.mjs`, `data/flagged-items.json`, `data/audit-report.json` |
| **C6** | GitHub Pages dashboard landing page, category subpages, interactive gold weight/melt calculator & Flagged for Review page | `in progress` | `arena/cbea1001-gold3` | `.nojekyll`, `index.html`, `rings.html`, `calculator.html`, `sellers.html`, `checklist.html`, `analysis.html`, `security-audit.html`, `flagged.html`, `assets/styles.css`, `assets/app.js` |
| **C7** | Final integration session: merge/sync check against `origin/main`, full line-by-line re-verification pass, CI workflow, PR creation & merge, live GitHub Pages deployment check | `unclaimed` | — | `.github/workflows/verify.yml`, `README.md`, `COORDINATION.md` |

---

## Coordination & Verification Log

### 2026-10-22 — Session `arena/cbea1001-gold3` — Initial Inspection & Claim of Task C1
- Checked `origin/main` (`1c10511ef71d1c0855283762fb854c154039bc56`): `COORDINATION.md` did not exist on `main`; only `README.md` (`# GOLD3`, 7 bytes) was present.
- Checked remote branches via GitHub API (`https://api.github.com/repos/karagemop466-tech/GOLD3/branches`): observed parallel Arena session branches (`arena/1db649a6-gold3`, `arena/8aaa18bf-gold3`, `arena/b3c924e6-gold3`) also branching from `1c10511ef71d1c0855283762fb854c154039bc56`. None had merged to `main` at the time of inspection.
- Created `COORDINATION.md` and claimed **Task C1** (`Repository review & baseline irregularity logging`) under session `arena/cbea1001-gold3`.

### 2026-10-22 — Session `arena/cbea1001-gold3` — Completed Task C1 & Claimed Task C2
- **Task C1 Completed (`done`):** Audited `README.md` line 1 (`# GOLD3`, 7 bytes), initial commit `1c10511ef71d1c0855283762fb854c154039bc56`, GitHub Pages configuration (`https://karagemop466-tech.github.io/GOLD3/`, legacy `main:/`, build `1306662996`), and remote branch state.
- **Sources Verified:**
  - `https://github.com/karagemop466-tech/GOLD3/blob/1c10511ef71d1c0855283762fb854c154039bc56/README.md`
  - `https://github.com/karagemop466-tech/GOLD3/commit/1c10511ef71d1c0855283762fb854c154039bc56`
  - `https://github.com/karagemop466-tech/GOLD3/tree/1c10511ef71d1c0855283762fb854c154039bc56`
  - `https://karagemop466-tech.github.io/GOLD3/`
- **Irregularities Logged (`needs review`):** `REPO-01` (placeholder `README.md` with no ring data or checklist), `REPO-03` (legacy Pages lacking `index.html`/`.nojekyll`), `REPO-04` (missing initial `COORDINATION.md` on `main` with concurrent branches). Recorded in `data/repo-audit.json`.
- **Claimed Task C2 (`in progress`):** Scope `data/gold-benchmark.json`, `data/purity-standards.json`.

### 2026-10-22 — Session `arena/cbea1001-gold3` — Completed Task C2 & Claimed Task C3
- **Task C2 Completed (`done`):** Verified live 2026-10-22 gold spot prices, London/NY morning fixes, LBMA Q3 2026 auction benchmark, NIST troy ounce / gram / carat conversions, FTC 16 CFR Part 23 gold/vermeil/quality-mark rules, National Gold and Silver Stamping Act (`15 U.S.C. §§ 295, 297`), FTC Fair Credit Billing Act dispute protections, and ISO 23345:2021 (ED-XRF) / ISO 11426:2021 (fire assay) standards.
- **Sources Verified:**
  - `https://www.kitco.com/price/precious-metals` (Spot Bid `$4,025.10/oz`, Ask `$4,027.10/oz`, NY Fix `$4,050.93/oz`, London Fix `$4,084.05/oz` on Oct 22, 2026)
  - `https://www.bullionvault.com/gold-price-chart.do` (`$4,026.25/oz`, `$129.45/g` on 22 Oct 2026)
  - `https://www.lbma.org.uk/articles/lbma-precious-metals-market-report-q3-2026` (`$4,176.30/oz` on 30 Sep 2026 PM)
  - `https://www.nist.gov/pml/owm/metric-si/unit-conversion/precious-metals-conversion-information` & `https://www.nist.gov/document/precious-metals-conversion-information-march2015pdf` (`31.1034768 g/oz t`, `0.200 g/ct`)
  - `https://www.ecfr.gov/current/title-16/chapter-I/subchapter-B/part-23/section-23.3`, `section-23.4`, `section-23.1`, `section-23.0`
  - `https://www.govinfo.gov/content/pkg/USCODE-2024-title15/pdf/USCODE-2024-title15-chap8-sec295.pdf` & `sec297.pdf`
  - `https://consumer.ftc.gov/articles/using-credit-cards-and-disputing-charges`
  - `https://www.iso.org/standard/75272.html` (ISO 23345:2021) & `https://www.iso.org/standard/75771.html` (ISO 11426:2021)
- **Irregularities Logged:** None in statutory/benchmark sources; noted critical ISO 23345:2021 technical caveat that ED-XRF alone is unsuitable for thickly coated items without paired weight/density checks.
- **Claimed Task C3 (`in progress`):** Scope `data/rings.json`.

### 2026-10-22 — Session `arena/cbea1001-gold3` — Completed Task C3 & Claimed Task C4
- **Task C3 Completed (`done`):** Fetched and verified 22 live official ring product listings (`RING-01` through `RING-22`) across 7 major US/North American jewelry retailers (`Automic Gold`, `Sarraf.com`, `VRAI`, `Blue Nile`, `Brilliant Earth`, `Mejuri`, `Local Eclectic`, and `Menē`) on `2026-10-22` and wrote `data/rings.json`.
- **No-Hallucinations Enforcement:**
  - Verified exact published gram weights on 10 listings (`Automic Gold` `1.4g–6.1g`, `Sarraf.com` `2.50g–8.30g`, `VRAI` `2.30g–2.86g`).
  - Left `weight_grams` blank (`null`) and flagged `unverified` across 12 listings (`Blue Nile`, `Brilliant Earth`, `Mejuri`, `Local Eclectic`, and `Menē` static HTML where weight is inside a JS drawer).
  - Left `price_usd` blank (`null`) and flagged `unverified` on `VRAI` configurator endpoints (`RING-09`, `RING-10`) because live static HTML renders price client-side only (refused to copy cached search-snippet prices).
  - Left `hallmark_online_stated` blank (`null`) across all 22 rows because no retailer published verbatim interior karat + trademark stamp strings online (requiring post-arrival physical hallmark inspection per `15 U.S.C. § 297`).
- **Real-World Irregularities Discovered & Logged (`needs review`):**
  - `RING-13` (`Blue Nile` Stock `501290y`, `$1,375`): Live H1/spec state `18K Yellow Gold`, while Product Details body states `"14k yellow gold engagement ring"`; `claimed_karat` left `null` (`unverified`).
  - `RING-21` (`Local Eclectic` `Solid Gold Simple Knot Ring`, `$239`): Live material callout badge states `"9k Solid Gold"` (below traditional US `10K` karat-gold floor under `16 CFR § 23.3(b)`), while bullet text states `"10k solid yellow gold"`; `claimed_karat` left `null` and disqualified.
  - `RING-22` (`Mejuri` `Daily Stacker Ring`, `$118`, `18k Gold Vermeil`): Disqualified control case whose live copy contains the substring `"18k solid gold"` inside `"a thick layer of 18k solid gold plated on 91% recycled sterling silver"`.
  - `RING-07` (`Sarraf.com` Stock `151105`, `$695`): Copy calls 14K alloy `"Solid and Pure 14k Yellow Gold"` (`16 CFR § 23.3` reserves unqualified/pure gold for 24K).
  - `RING-14` (`Brilliant Earth` `BE1FM0126-18KY`, `$1,090`): Displays `"Free 1-Year Resizing"` trust badge alongside Product Details exclusion `"resizing is not available for this ring"`, plus UI unit bug `"Band Width: 2 ct. tw."`.
- **Claimed Task C4 (`in progress`):** Scope `data/sellers.json`.

### 2026-10-22 — Session `arena/cbea1001-gold3` — Completed Task C4 & Claimed Task C5
- **Task C4 Completed (`done`):** Verified all 8 jewelry retailers (`Automic Gold`, `Sarraf.com`, `Blue Nile`, `Brilliant Earth`, `VRAI`, `Mejuri`, `Local Eclectic`, `Menē`) line-by-line against official return/payment/contact/terms pages and Better Business Bureau (`bbb.org`) profiles in `data/sellers.json`.
- **Key Verified Findings & Irregularities Logged (`needs review`):**
  - `SELLER-VRAI`: BBB Los Angeles profile (`bbb.org/us/ca/los-angeles/profile/jewelry-advisory-service/vrai-1216-652149`) carries an **`F` rating** (failure to respond to 5 complaints) and official VRAI return help center imposes a **`$300 USD` recycling fee** on setting-only or engraved engagement ring returns to original payment method; static credit card brand list left `null` (`unverified`).
  - `SELLER-LOCALECLECTIC`: Official FAQ (`localeclectic.com/pages/frequently-asked-questions`) advertises 90-day returns, but restricts original-payment-method refunds to **14 days from delivery** (days 15–90 yield store credit only, minus return shipping label cost); phone number omitted on website Contact Us page (`+1-888-232-8306` verified via BBB Chicago profile); static credit card brand list left `null` (`unverified`).
  - `SELLER-MENE`: Official Sep 2, 2026 Terms of Service (`mene.com/terms-of-service`) limit returns to **7 days from receipt**, default self-service returns to non-cash `Menē Credit` (subject to expiry), permit **up to a 10% restocking fee** on discretionary original-payment refunds, and deduct **5%** if the Certificate of Authenticity is missing.
  - `SELLER-BLUENILE`: Official return clock starts on **shipment date** (not delivery date), and resizing after initial purchase voids return eligibility (`bluenile.com/policies/returns`).
  - `SELLER-AUTOMIC`: BBB main profile shows `A+` while BBB `/overview-of-bbb-ratings` subpage displays `NR`.
- **Claimed Task C5 (`in progress`):** Scope `package.json`, `scripts/security-check.mjs`, `scripts/verify-links.mjs`, `data/flagged-items.json`, `data/audit-report.json`.

### 2026-10-22 — Session `arena/cbea1001-gold3` — Completed Task C5 & Claimed Task C6
- **Task C5 Completed (`done`):** Built zero-dependency Node.js anti-hallucination security scanner (`scripts/security-check.mjs`), link/anchor/asset verifier (`scripts/verify-links.mjs`), `package.json` scripts, generated `data/flagged-items.json` (`33` flagged/needs-review items with official URLs), and produced `data/audit-report.json`.
- **Automated Security & Hallucination Pass #1 Result:** `PASS (7/7 checks)` across `89` JSON records and `114` official HTTPS links (`SEC-01` through `SEC-07`), confirming 100% blank-cell (`null`) enforcement on unconfirmed fields, exact NIST `31.1034768 g/oz t` raw-gold melt math, vermeil/9K trap disqualification, and live HTTP 200 status on GitHub source URLs.
- **Claimed Task C6 (`in progress`):** Scope `.nojekyll`, `index.html`, `rings.html`, `calculator.html`, `sellers.html`, `checklist.html`, `analysis.html`, `security-audit.html`, `flagged.html`, `assets/styles.css`, `assets/app.js`.



