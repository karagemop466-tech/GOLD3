# COORDINATION — GOLD3 (Gold Engagement Ring Verification Project)

**Shared task board for all agent sessions.** Read this before starting work.

- Repo: `karagemop466-tech/GOLD3`
- Primary session (this session): **`arena/8aaa18bf-gold3`** — Arena-assigned branch, cannot be renamed or switched.
- Rule: **No hallucinations.** Every value in this project must trace to an official/primary source URL
  that a human can open. If a value cannot be confirmed at an official source, it is left **blank** and
  marked `unverified` — never inferred, never estimated, never "typical".

---

## How to claim a task

1. Find a task below with status `unclaimed`.
2. Replace `unclaimed` with `in progress`, write your session ID, your branch/worktree name, and the
   **exact file scope** you will edit.
3. Commit and push that claim **immediately** (small commits only).
4. Never start a task another session has claimed (`in progress`) unless the claim is > 60 minutes old
   with zero commits — then take over and log the handoff.
5. If you need a file owned by another session, **log a request here**; do not edit it.
6. Run `git pull --rebase` before every push. Never discard another session's work on conflict; stop,
   resolve additively, and log what happened.
7. Shared outputs (`data/*.json`, `index.html`, navigation) are written **only** by the final
   integration session, after other tasks are `done`.

Branch naming: `session-<id>/<task>`. (This primary session is pinned by the platform to
`arena/8aaa18bf-gold3`, so it works there; its file scopes are still disjoint per task below.)

---

## Task board

| ID | Task | Status | Owner | File scope |
|----|------|--------|-------|-----------|
| T1 | Verified gold benchmark price (spot) with date + source | in progress | `arena/8aaa18bf-gold3` | `data/gold-price.json`, `data/sources.json` |
| T2 | Verified ring listings (price, karat, metal, solid-gold claim, weight) | unclaimed | — | `data/rings.json` |
| T3 | Seller verification (return policy, payment, hallmark/maker-mark, contact) | unclaimed | — | `data/sellers.json` |
| T4 | Regulatory standards (FTC 16 CFR 23 quality marks; hallmark law) | unclaimed | — | `data/standards.json`, `docs/methodology.md` |
| T5 | Anti-hallucination audit tooling + audit report | unclaimed | — | `scripts/`, `reports/` |
| T6 | Site build (landing, category pages, table, calculator, flagged page) | unclaimed | — | `index.html`, `rings.html`, `sellers.html`, `analysis.html`, `flagged.html`, `methodology.html`, `assets/` |
| T7 | Integration: re-verify combined data, link check, publish Pages, PR + merge | unclaimed | — | `.github/workflows/`, `data/*.json`, repo root |

Status values: `unclaimed` · `in progress` · `done` · `needs review`.
`needs review` = the item is published on the **Flagged for Review** page; it does **not** block merge.

---

## Log

### 2026-10-22 — Session `arena/8aaa18bf-gold3` — repo bootstrap
- Repo found with only a 7-byte `README.md` and one commit (`1c10511`). No prior data, no prior claims,
  no competing session work in `main`. Nothing to duplicate or conflict with.
- Created this board. Claiming T1 (in progress).
- Constraint recorded: sandbox shell egress is limited, but the research tools have open web access, so
  sourcing is done by fetching the official pages directly (not by scraping via `curl`).
- **Baseline finding for the whole project:** mainstream retailers publish karat + metal but almost
  never publish **ring metal weight in grams**, and almost never publish a per-item XRF assay. Those
  cells stay blank + flagged `unverified` by design. The melt-value calculator therefore takes weight
  as a **user input**, not a fabricated default.
