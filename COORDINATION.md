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
| T1 | Coordination board + repo scaffolding + data schema | done | `sess-7f3a-gold` | `COORDINATION.md`, `README.md`, `.gitignore`, `scripts/` | 2026-10-22T23:55Z |
| T2 | Authority sources: FTC 16 CFR 23, hallmarking, gold-price anchors | done | `sess-7f3a-gold` | `data/sources.json`, `data/prices.json`, `sources.html` | 2026-10-22T23:55Z |
| T3 | Retailer profiles: returns, contact, reputation, hallmark policy | done | `sess-7f3a-gold` | `data/retailers.json`, `retailers.html` | 2026-10-22T23:55Z |
| T4 | Product verification: 14K solid-gold entries | done | `sess-7f3a-gold` | `data/products.json` (14 x 14K) | 2026-10-22T23:55Z |
| T5 | Product verification: 18K solid-gold entries | done | `sess-7f3a-gold` | `data/products.json` (2 x 18K) | 2026-10-22T23:55Z |
| T6 | Excluded / non-solid-gold examples (plated, vermeil, filled, tone) | done | `sess-7f3a-gold` | `data/products.json` (2 excluded) | 2026-10-22T23:55Z |
| T7 | Verification passes: hallucination + price-sanity + link checks | done | `sess-7f3a-gold` | `scripts/verify.py`, `data/verification-report.json` | 2026-10-22T23:55Z |
| T8 | Static site build (dashboard, category pages, calculator) | done | `sess-7f3a-gold` | `index.html`, `*.html`, `assets/`, `scripts/build_site.py` | 2026-10-22T23:55Z |
| T9 | Final integration: re-verify combined data, build, PR → `main`, deploy | in progress | `sess-7f3a-gold` | all (integration window) | 2026-10-22T23:55Z |

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
| 2026-10-22T23:40Z | `sess-7f3a-gold` | T2 | Read 16 CFR 23.3 / 23.3(c)(1) / 23.4 on eCFR; 15 U.S.C. 294, 295, 297 on Cornell LII; LBMA price page; GoldPrice.org and World Gold Council spot pages | 5 regulation/statute sources + 2 independent spot snapshots captured; cross-check 0.06% apart |
| 2026-10-22T23:45Z | `sess-7f3a-gold` | T3 | Read returns pages for Aurate, Blue Nile, Mejuri, Ring Concierge, Catbird; Trustpilot profiles for all five | 15/30/30/20-day windows recorded with quotes; Mejuri's dedicated FAQ page is JavaScript-only (flagged F10); Ring Concierge has 7 reviews on an unclaimed profile (flagged F5) |
| 2026-10-22T23:50Z | `sess-7f3a-gold` | T4–T6 | Opened every product page or official category listing; copied price + purity + solid-gold wording | 19 records: 14 x 14K, 2 x 18K, 1 x 10K, 2 excluded. 0 of 17 publish a ring weight; 0 of 5 retailers state a hallmark policy |
| 2026-10-22T23:52Z | `sess-7f3a-gold` | T7 | First `verify.py` run | FAILED - self-caught metric definition error (solid_gold=true excluded 7 listings). Fixed; now PASS with 0 errors / 0 warnings / 11 notes |
| 2026-10-22T23:54Z | `sess-7f3a-gold` | T8 | Built 12 pages; checked internal links, stylesheet refs, product URL presence, tag balance, raw ampersands, leaked nulls | Build OK; 12 pages, 19 rows, no broken internal links |

---

## 4. Change requests / conflicts

_None. No other session joined; no merge conflicts occurred._

## 4a. Irregularities published for review (do not block the merge)

These are on `flagged.html` with source links and an action to close each one:

1. **F1 (high)** Blue Nile's 18K Floral Marquise page contradicts itself: spec says 18K White Gold, product description says 14k yellow gold.
2. **F2 (high)** 0 of 17 gold listings publish the finished ring weight in grams.
3. **F3 (high)** 0 of 5 retailers state a hallmark / maker's-mark policy (15 U.S.C. 297).
4. **F4 (medium)** 7 of 17 listings never use the word "solid"; another 7 rely on a brand-level statement only.
5. **F5 (medium)** Ring Concierge Trustpilot 2.7 is based on 7 reviews, unclaimed profile.
6. **F6 (medium)** Ring Concierge advertises "LIFETIME WARRANTY" while its refund policy states 3 years.
7. **F7 (medium)** Blue Nile excludes resized rings from returns and caps free returns at two per year.
8. **F8 (medium)** Aurate 15-day and Catbird 20-day return windows (+$9 fee at Catbird); Catbird international sales final.
9. **F9 (medium)** Ring Concierge rings mix a yellow-gold band with platinum prongs.
10. **F10 (low)** Mejuri's dedicated returns page could not be read (JavaScript-only); policy quoted from the product page.
11. **F11 (low)** No 18K Aurate price captured (collection page shows only a 14K "from" price).
12. **F12 (low)** Control check: the two spot sources agree to 0.06%.

Also flagged: Ring Concierge publishes no phone or email on the pages checked (`NO_DIRECT_CONTACT`).

---

## 5. Pull request and deploy record

| Step | Result | When (UTC) |
|---|---|---|
| Branch pushed | `arena/b3c924e6-gold3` | 2026-10-22T23:55Z |
| PR → `main` | _to be recorded_ | — |
| Merge | _to be recorded_ | — |
| GitHub Pages deploy | _to be recorded_ | — |

## 6. Handoff rule

If a session's claim is more than **60 minutes** old with no commits, any other session may take
over the task. Log the takeover here (who, when, what was already done) before editing.
