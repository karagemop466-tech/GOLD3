# COORDINATION — Gold Engagement Ring Buyer's Guide (GOLD3)

This file is the **shared task board** for all agent sessions working in this repo.
Read it before starting any work. Update it when you claim, finish, or hand off a task.

---

## 0. Session registry

| Session ID | Branch (actual) | Started (UTC) | Status |
|---|---|---|---|
| `sess-7f3a-gold` | `arena/b3c924e6-gold3` | 2026-10-22T23:10Z | active |

### Branch naming note (important)
The protocol below asks for `session-<id>/<task>` branches. **This sandbox pins each session to a
single pre-assigned branch** (`arena/b3c924e6-gold3` for `sess-7f3a-gold`); creating or pushing
other branches is not permitted by the environment. To keep the intent of the protocol (no
overlapping edits, no clobbering another session's work) we use **strict file-scope ownership**
instead of branch isolation, and every session must:

1. Claim a row in the task board below **before** editing.
2. Edit **only** files inside its claimed scope.
3. `git pull --rebase` before every push.
4. If a change is needed in a file owned by another session, log a **Change request** in §4
   instead of editing that file.

---

## 1. Task board

Status values: `unclaimed` · `in progress` · `done` · `needs review`

> `needs review` = published on the *Flagged for Review* page. Does **not** block anything.

| # | Task | Status | Owner | File scope | Updated (UTC) |
|---|---|---|---|---|---|
| T1 | Coordination board + repo scaffolding + data schema | in progress | `sess-7f3a-gold` | `COORDINATION.md`, `README.md`, `.gitignore`, `data/schema.md`, `scripts/` | 2026-10-22T23:10Z |
| T2 | Authority sources: FTC 16 CFR 23, hallmarking, gold-price anchors | unclaimed | — | `data/sources.json`, `sources.html` | — |
| T3 | Retailer profiles: returns, contact, reputation, hallmark policy | unclaimed | — | `data/retailers.json`, `retailers.html` | — |
| T4 | Product verification: 14K solid-gold entries | unclaimed | — | `data/products.json` (`category: 14k`) | — |
| T5 | Product verification: 18K solid-gold entries | unclaimed | — | `data/products.json` (`category: 18k`) | — |
| T6 | Excluded / non-solid-gold examples (plated, vermeil, filled, tone) | unclaimed | — | `data/products.json` (`category: excluded`) | — |
| T7 | Verification passes: hallucination + price-sanity + link checks | unclaimed | — | `scripts/verify.py`, `data/verification-report.json` | — |
| T8 | Static site build (dashboard, category pages, calculator) | unclaimed | — | `index.html`, `*.html`, `assets/`, `scripts/build_site.py` | — |
| T9 | Final integration: re-verify combined data, build, PR → `main`, deploy | unclaimed | — | all (integration window) | — |

**Claimed by `sess-7f3a-gold`:** T1 → T9 (single-session run; all rows claimed in sequence to avoid
duplicate work). If another session joins, it must claim only `unclaimed` rows and log the claim
here before editing.

---

## 2. Data contract (single source of truth)

* `data/products.json` — one object per **listing** (a specific product page at a specific retailer).
* `data/retailers.json` — one object per **merchant**.
* `data/sources.json` — authority/reference sources (government, benchmark, standards bodies).
* `data/prices.json` — dated gold-price snapshots used by the calculator.

**Hard rules (enforced by `scripts/verify.py`, which fails the build):**

1. **No unsourced values.** Any non-null field that states a fact must carry a `*_source` URL.
2. **No inferred numbers.** If the retailer does not publish a ring weight, `weight_g` stays
   `null` and `weight_status` is `unverified`. Shipping weights, "approx" figures pulled from
   other sizes/models, or guesses are forbidden.
3. **Prices are snapshots.** Every price carries `price`, `currency`, `price_captured_at`
   (ISO-8601 UTC), `price_source` (the exact page), and `price_quote` (verbatim text seen on
   that page). Prices without a capture timestamp are rejected.
4. **Solid gold must be quoted.** `solid_gold_evidence` must be a verbatim excerpt from the
   retailer's own page. "Looks solid", category assumptions, and search snippets are not evidence.
5. **Plated/vermeil/filled/overlay/tone items may never appear in a solid-gold category.**
6. **Every row links to an official source.** Retailer page, brand page, or `.gov`/standards body.
7. Prices older than 30 days are flagged `stale_price` and shown with a warning.

---

## 3. Verification log (append-only)

| UTC | Session | Task | What was checked | Result |
|---|---|---|---|---|
| 2026-10-22T23:10Z | `sess-7f3a-gold` | T1 | Repo was empty (only `README.md` with 7 bytes, "GOLD3"); no `COORDINATION.md` existed | Created board + claimed T1–T9 |

---

## 4. Change requests / conflicts

_None yet._

---

## 5. Handoff rule

If a session's claim is more than **60 minutes** old with no commits, any other session may take
over the task. Log the takeover here (who, when, what was already done) before editing.
