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
| **C2** | Official gold spot benchmark price & US federal purity/hallmark/XRF standards verification | `in progress` | `arena/cbea1001-gold3` | `data/gold-benchmark.json`, `data/purity-standards.json` |
| **C3** | Official gold engagement ring product listings collection & line-by-line verification | `unclaimed` | — | `data/rings.json` |
| **C4** | Seller reputation, contact info, return policies (custom/resized exclusions), payment protection & XRF inspection verification | `unclaimed` | — | `data/sellers.json` |
| **C5** | Anti-hallucination security scanner, raw gold / melt math verifier, blank-cell enforcement & link checker | `unclaimed` | — | `package.json`, `scripts/security-check.mjs`, `scripts/verify-links.mjs`, `data/flagged-items.json`, `data/audit-report.json` |
| **C6** | GitHub Pages dashboard landing page, category subpages, interactive gold weight/melt calculator & Flagged for Review page | `unclaimed` | — | `.nojekyll`, `index.html`, `rings.html`, `calculator.html`, `sellers.html`, `checklist.html`, `analysis.html`, `security-audit.html`, `flagged.html`, `assets/styles.css`, `assets/app.js` |
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
