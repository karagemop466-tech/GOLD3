# Independent re-validation — session `sess-692d-gold` (`arena/692d8c94-gold3`)

**Date:** 2026-10-22 (UTC evening) · **Tree examined:** `main` @ `70746aa` (PR #26 merged)
**Purpose:** the standing hallucination-hunt pass, run independently of the sessions that produced the data.
Rule applied: pick a stored value, open the linked official page, and search for that exact value. If it is
not there verbatim, it is a defect. Nothing in this file was inferred; every "confirmed" below means the
value was seen on the live page during this pass.

---

## 1. Automated suites re-run on this tree (all green)

| Suite | Result |
|---|---|
| `python3 scripts/verify.py` | PASS — 0 errors, 0 warnings (Dataset A + B gates) |
| `python3 scripts/audit.py` | PASS — rows=22, **0 errors, 0 warnings**, 130 checks |
| `python3 scripts/run_security_audit.py` | PASS — SEC-01…SEC-07, 1,603 links verified, 24 pages |
| `node scripts/render-test.js` | PASS — **120/120** checks |
| `python3 scripts/report_verify.py` | PASS — 28 verification checks |
| `python3 scripts/build_site.py` | exit 0 — 18 pages, links/stylesheets/product URLs OK |
| `python3 scripts/build_ext_pages.py` | exit 0 — Dataset C pages rebuilt |
| GitHub Actions `Gate, build, audit and render` @ `70746aa` | **success** (all jobs, incl. Pages deploy) |

**Build determinism:** re-running the generators produced no *content* drift. The only differences were the
self-referential "Pass #N" counter and UTC timestamps the Dataset C tooling stamps into
`VERIFICATION_REPORT.md`, `verification/audit-log.json`, `verification/sources-manifest.json`,
`data/verified-data.js` and six generated pages; the `data_file_sha256` manifest was unchanged. Those run
artifacts were reverted rather than committed, so this pass does not churn another session's counter
(see note N2).

---

## 2. Live source re-openings (independent sample, 10 official pages)

Every stored value listed below was found **verbatim** on the live official page during this pass.

### Dataset B rows

| Row | Official source re-opened | Values searched for | Result |
|---|---|---|---|
| **R20** Sarraf.com 14k WG solitaire 0.94 ctw | https://www.sarraf.com/products/14k-white-gold-solitaire-ring-0-94-ctw.html | `Now: US$3,004.00`; `MSRP US$11,683.00`; `Was US$3,513.00`; `Material: 14K Solid Gold`; `Approximate Metal Weight: 3.80 grams`; `0.94 carat … round diamond solitaire is set in 14K white gold`; diamond `Natural`, color `G`, clarity `I 1`; return terms `Orders which are over 30 days of receipt do not qualify` and `Items that are damaged or are used do not qualify`; accuracy note `we strive to maintain an accuracy of ± 5%` | **confirmed** — all verbatim |
| **R21** Sarraf.com 10k 6mm comfort-fit band | https://www.sarraf.com/products/10k-gold-6mm-high-polished-comfort-fit-wedding-band.html | `Now: US$613.00`; `MSRP US$2,384.00`; `Was US$717.00`; `Material: 10K Solid Gold`; `Approximate Metal Weight: 8.30 grams`; `The weight listed is an approximate weight of a ring in size 10` | **confirmed** — all verbatim |
| **R22** Automic Gold 3ct radiant cathedral ring | https://www.automicgold.com/products/radiant-cut-lab-diamond-cathedral-ring | `$3,074`; `Material: 950 platinum and/or Solid 14k gold`; `Crafted from solid recycled 14k gold or 950 platinum`; `Item Weight: Approximately 5.4g for gold or 8.1g for platinum`; `Free returns (US only)`; `All engraved items are final sale`; lab diamond `VS/VVS`, `D/E/F`, `Approximately 3ct` | **confirmed** — all verbatim (the page's cookie-consent layer precedes the product block, exactly as the row's own verification note describes) |
| **R17** Tiffany® Setting 18k YG | stored URL https://www.tiffany.com/engagement/engagement-rings/the-tiffany-setting-engagement-ring-in-18k-yellow-gold-GRP10863/ | `Starting from $1,600`; `0.20 CT G VS1`; spec `Ring Style: 18k Yellow Gold and Platinum`; `This product is currently unavailable`; `Please note that this item is non returnable`; `this item can only be exchanged`; phone `(800) 843-3269` | **confirmed** — all verbatim. The stored URL redirected to `…/jewelry/rings/18k-rose-gold-and-platinum-diamond-rings-1712.html`, which is precisely what flag `RDR1` records; the redirect target is the same Tiffany Setting product page |

### Dataset A rows

| Row | Official source re-opened | Values searched for | Result |
|---|---|---|---|
| `mejuri-diamonds-band` | https://mejuri.com/products/diamonds-band?Material=Solid+Yellow+Gold+%2814k%29&Stone=Natural+Diamond | `$648`; `Solid Yellow Gold (14k), Natural Diamond`; `Handcrafted in 14k solid gold`; `free 30-day returns & exchanges starting from the day the shipment is delivered`; `Engraving … not eligible for returns` | **confirmed** — all verbatim |
| `ringconcierge-2-08-oval-lab-whisper-thin` | stored URL https://ringconcierge.com/products/2-08-oval-lab-diamond-in-whisper-thina-hidden-halo | `$6,038`; title `2.08 Oval Lab Diamond in Whisper Thin® Hidden Halo`; `2.08 Carat E VS1 Oval Lab Grown Diamond set in our Whisper Thin® Hidden Halo`; `Made to Order`; `COMPLIMENTARY LIFETIME WARRANTY` banner (flag F6); imagery captioned `Yellow Gold … band with Platinum Prongs` (flag F9) | **confirmed** — all verbatim. Note N4: a guessed slug variant (`…-engagement-ring`) 404s; the stored URL is exact — evidence it was copied from a live page, not synthesized |
| `catbird-classic-half-round-2mm` | https://www.catbirdnyc.com/catbird-classic-wedding-bands-solid-half-round-band-2mm.html | `from$550.00` | **confirmed** — verbatim (page also shows sold-out/waitlist badges on some sizes, consistent with the availability flags) |

### Policy, regulation and benchmark sources

| Source | Official page re-opened | What was searched | Result |
|---|---|---|---|
| Costco return policy (`RET1`) | https://customerservice.costco.com/app/answers/detail/a_id/1191 | `Precious metals are non-refundable.` (Document CU2573, Version 18.0, Published 10/02/2025); diamonds ≥1.00 ct need original paperwork (IGI/GIA), Jewelry Credit Memo, `Costco Graduate Gemologist will inspect for authenticity` | **confirmed** — verbatim; `RET1` stands: a gold ring from Costco fails the checklist's return requirement |
| 16 CFR 23.4(b) (vermeil) | eCFR official API: https://www.ecfr.gov/api/versioner/v1/full/2026-10-21/title-16.xml?part=23&section=23.4 (rendered page: https://www.ecfr.gov/current/title-16/chapter-I/subchapter-B/part-23/section-23.4) | `base of sterling silver coated or plated on all significant surfaces with gold, or gold alloy of not less than 10 karat fineness … minimum thickness throughout equivalent to two and one half (2½) microns` | **confirmed** — `standards.json` rule L3 and the `standards.html` wording table are accurate paraphrases (Title 16 up to date as of 10/21/2026) |
| GoldPrice.org spot snapshot | https://goldprice.org/ | stored: `Spot Gold Price: USD 4,026.79 / Ounce … Oct 22nd, 2026 at 07:07 NY Time` | **source confirmed live**; the page now reads `USD 4,024.39 / Ounce … Oct 22nd, 2026 at 07:41 NY Time` — the same page 34 minutes later, −0.06%. A dated intraday snapshot cannot re-show its old number; the quote format, publisher and timestamp convention all match, and the live value now sits within 0.001% of the WGC snapshot ($4,024.36), reinforcing the two-source cross-check |

**Not re-opened in this pass (honest scope):** Aurate's collection-page price grid (the fetch route's
chunk-continuation failed repeatedly — infrastructure, not the site; the product pages were confirmed live
and mid-sale, `20% OFF … code LAYERS`); Blue Nile product pages; WGC Goldhub; Dataset C's Menē/Brilliant
Earth rows (merged minutes before this pass and already gated by `verify.py` + the security suite). Those
values rest on the same-day captures recorded in `data/verification.json`, `verify.html` and §6 of
`COORDINATION.md`. Nothing observed in this pass contradicts them.

---

## 3. Hallucination verdict

**Zero discrepancies.** Across 10 independently re-opened official sources — the three newest
weight-bearing listings (R20–R22), the highest-risk policy claims (`RET1`, `RET6`), the controlling
regulation (16 CFR 23.4(b)) and the primary price benchmark — every stored value was found verbatim, and
every flag describing a page defect (`RDR1`, `F6`, `F9`, `AV1`-style availability) reproduced on the live
page. No value needed correction; no row needed deletion.

Historical context: real hallucinations *were* found and removed earlier the same day by
`arena/e6fe3e4f-gold3` (7 invented "also offered in …" phrases, deleted not softened) and by
`arena/698f08f6-gold3`/`arena/b3c924e6-gold3` (site arithmetic defects SD1–SD5). This pass re-checks the
post-correction tree and finds it clean.

## 4. Notes and irregularities (non-blocking)

- **N1 — contract wording vs schema.** `COORDINATION.md` §2 rule 3 names the timestamp field
  `price_captured_at`; the schema and `scripts/verify.py` (lines ~264-268) actually enforce
  `price_captured_on`. Doc wording corrected in this session's PR; the gate itself was always correct.
- **N2 — builders are not idempotent at the byte level.** The Dataset C tooling stamps a run counter
  ("Pass #9" → "#10") and timestamps into generated pages/reports on every execution. Committed state
  therefore changes whenever anyone re-runs the suite. Recommend (change request to whoever next owns
  `scripts/run_security_audit.py` / `scripts/build_ext_pages.py`): keep the counter in
  `verification/audit-log.json` only, or accept the churn knowingly. This pass reverted its run artifacts
  to avoid racing other sessions' counters; data hashes were verified unchanged.
- **N3 — Pages CDN lag observed.** A live read-back at 23:45 UTC served the pre-PR-#17 build
  ("38 listings / 10 sellers") while `main` already carried 41/12; a read-back minutes later served the
  current build ("62 listings · A:19 · B:22 · C:21, 14 sellers, 15 weights"), matching the tree exactly.
  Deployments are coherent; allow GitHub's CDN a few minutes after each build before judging the live site.
- **N4 — verifier near-miss, recorded for method.** When re-fetching Ring Concierge this session first
  appended a plausible slug suffix to a truncated display of the URL and got a 404. The *stored* URL was
  correct. Lesson re-affirmed: always fetch the exact stored URL; never reconstruct one — a 404 from a
  guessed URL is not evidence of a dead listing.
- **N5 — sale context on Aurate.** Aurate's storefront is running a time-boxed "20% OFF … LAYERS" sale at
  read-back time. The stored "From $X" snapshots are dated 2026-10-22 and remain as captured; a buyer
  re-checking during or after the sale may see different numbers. This is the documented snapshot
  behaviour, not drift in the data.

## 5. Standing recommendation (unchanged, re-endorsed)

After every review: re-run all five suites, then spend one deliberate pass hunting hallucinations — take
any number on the site and try to find it on the linked page. If it is not there verbatim, delete it and
mark the field unverified. Better an empty cell than a confident error.

*Report written by session `sess-692d-gold` (`arena/692d8c94-gold3`). Sole owner of this file.*
