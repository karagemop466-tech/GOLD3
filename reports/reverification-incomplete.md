# Incomplete / Stale Verification Artifacts (`2026-10-23`)

This file is produced by the **CR-P15-2** resolution. It catalogues the verification reports that are
**historical captures and were not re-verified on the live-verified surface** by the current pass. It is a
pointer file, not a replacement: the content of each artifact below is preserved exactly where it lives.

- **Produced by:** `arena/1ee91485-gold3` (pass **P17**)
- **Reason this file exists:** `reports/reverification-1162b2db.md` was a merge-conflicted artifact that
  concatenated two reports (`<<<<<<< HEAD` … `=======` … `>>>>>>> origin/main`). The split keeps the
  **live-verified** half in [`reports/reverification-dataset-c.md`](reverification-dataset-c.md) and
  catalogues the **stale / not-re-verified** artifacts here.
- **Policy:** nothing is deleted and no value is restated. Each row below is marked with whether its content
  was re-verified on the live surface (`reverified`) or is retained only as a historical record
  (`historical — not re-verified`).

## A. Stale / historical artifacts — retained, not re-verified

| Artifact | Session | What it is | Status on the live-verified surface |
|---|---|---|---|
| [`reports/reverification-c-6ccbc523.md`](reverification-c-6ccbc523.md) | `arena/6ccbc523-gold3` (`PASS-C-6CCBC523`) | 63-URL Dataset C re-verification + anti-hallucination audit (2026-10-23T09:56Z) | **Superseded** by [`reverification-dataset-c.md`](reverification-dataset-c.md) and pass P17's live reads |
| [`reports/reverification-dataset-c-15b00e99.md`](reverification-dataset-c-15b00e99.md) | `arena/15b00e99-gold3` (`DC1`) | Dataset C & spot/retailer live re-verification audit (2026-10-23) | **Superseded** by [`reverification-dataset-c.md`](reverification-dataset-c.md) and pass P17's live reads |
| [`reports/revalidation-sess-692d.md`](revalidation-sess-692d.md) | `arena/692d8c94-gold3` | Independent re-validation of `main` @ `70746aa` (2026-10-22) | **Historical** — predates PR #33 / PR #66 and the P17 live reads; retained verbatim |

## B. Live-verified surface (the half of the split that stands)

| Artifact | Session | What it is |
|---|---|---|
| [`reports/reverification-dataset-c.md`](reverification-dataset-c.md) | `arena/2908bea4-gold3` (`V9`–`V10`) | The Dataset C & Dataset D live re-verification report — the live-verified half extracted from the conflicted file |
| [`reports/reverification-1162b2db.md`](reverification-1162b2db.md) | `arena/1162b2db-gold3` (P5) | The clean P5 primary-source report (de-conflicted; the duplicated Dataset C half is removed and linked instead) |
| [`data/reverification-p17.json`](../data/reverification-p17.json) | `arena/1ee91485-gold3` (P17) | 25 live checks re-opened on 2026-10-23T23:43-23:45Z (22 confirmed · 2 corrected · 1 flagged) |
| [`reports/reverification-pass-p17.md`](reverification-pass-p17.md) | `arena/1ee91485-gold3` (P17) | Human-readable companion to the P17 JSON |

## C. What P17 re-opened from the artifacts above

Pass P17 re-read the live pages behind the Dataset C surface and confirmed them verbatim: Wilson's `R12`,
Sarraf `R20`/`R21`/`R26`/`R27`, Mejuri `R01`/`BND-12`, Blue Nile `R08`/`SOL-01`, Ross-Simons
`R15`/`BND-04`/`BND-05`/`BND-06`/`BND-08`, Automic `R24`, and Brilliant Earth `SOL-05`. The two Menē rows that
moved again (`R30` $3,202; `BND-03` $2,445 with its page recovered) are recorded additively in
`data/reverification-p17.json` and in finding **F50** — the stale `weight_grams` values blanked by P5 remain
blank (`null`), and no stored figure was overwritten.

> **Standing recommendation.** Run `python3 scripts/run_security_audit.py --deterministic --session-id <session>`
> and `python3 scripts/verify_dataset_c.py` after every review or edit, then spot-check random cells in
> `solitaire-settings.html`, `bands-vintage-rings.html`, `sellers-policies.html` and `combined.html` against their
> linked official URLs to look for hallucinations, silent client-JS omissions, or live price drift.
