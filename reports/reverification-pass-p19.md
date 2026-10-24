# Pass P19 — independent re-verification and the first requirements compliance matrix

- **Session:** `arena/76359c22-gold3`
- **Date (UTC):** 2026-10-23
- **Live read window:** 23:35Z – 23:46Z
- **Base:** `85ac1fa` (`main`, after PR #66), branch `arena/76359c22-gold3`
- **Machine-readable log:** `data/reverification-p19.json`, appended to `data/verification.json` as `P19-01`…`P19-12`
- **New artefacts:** `scripts/requirements_matrix.py`, `scripts/hallucination_scan.py`, `data/requirements-matrix.json`, `requirements.html`

## 0. Renumbering and merge note

This pass was claimed as `P17` at 21:10Z, but peer session `arena/36ebce13-gold3` merged its own `P17`
(PR #69) — including its own `data/reverification-p17.json`, `reports/reverification-pass-p17.md` and findings
`F56`–`F55` — while this pass was running. Under the §1 protocol the peer version is kept and this pass renumbered:
the pass id became **`P19`**, its checks `P19-01`…`P19-12`, its findings **`F56`–`F58`**, and its artefacts
`data/reverification-p19.json` / `reports/reverification-pass-p19.md`. Nothing was discarded and no peer file was
reset to an older version; `origin/main` was merged and every conflict resolved in the peer's favour for generated
artefacts, which were then rebuilt from data.

## 1. What this pass did

Two things, both aimed at the same question — *can every number on this site be traced to a page a buyer can open?*

1. **A rotating live sample.** Ten official pages were re-opened, spread across Dataset A (3), Dataset B (5), Dataset C (4) and the gold benchmark, deliberately steering around the rows P14 and P15 had re-read minutes earlier (except `BND-08`, whose published weight made a second look worthwhile).
2. **A requirements compliance matrix.** The checklist has ten requirements. Until now the site carried them as prose and per-row flags. Every one of the 71 listings is now scored cell by cell — karat, the word "solid", hallmark, maker's mark, weight, seller reputation, return window, card payment, documentation and independent/XRF verification — and every cell is either backed by an official page or left **blank and marked unverified**.

## 2. Live results — 12 checks: 10 confirmed, 0 corrected, 2 flagged

| Check | Subject | Outcome | What the page printed |
|---|---|---|---|
| `P19-01` | Mejuri Diamonds Band (`mejuri-diamonds-band` / `BND-11`) | confirmed | `$648`, `Solid Yellow Gold (14k), Natural Diamond`, free 30-day returns, engraving not eligible for returns, no weight, no hallmark |
| `P19-02` | Catbird Woodland Ring (`R18`) | confirmed | `$276.00 Regular Price $368.00`, sold-out badge, no material paragraph, no weight, no hallmark |
| `P19-03` | Tiffany Setting (`R17`) | confirmed | `Starting from $1,600`, `18k Yellow Gold and Platinum`, **both** "non returnable" and "can only be exchanged", "currently unavailable" |
| `P19-04` | Local Eclectic Simple Knot (`R31`) | confirmed | `$239`, badge `9k Solid Gold` against bullet `10k solid yellow gold` — the karat genuinely cannot be settled from the listing |
| `P19-05` | Menē Wrap Ring (`R30`) | **flagged** | `$3,202` — 1.57% below the capture and 0.81% below the earlier reading the same day (finding `F56`) |
| `P19-06` | Mejuri Diamond Eternity Band (`BND-10`) | confirmed | `From $1,100`, prose "average carat weight of 0.532ct" against spec "0.044 ct - 0.056 ct" |
| `P19-07` | Ross-Simons 990022 (`SOL-07`) | confirmed | `Sale price $2,819` (original `$3,995`), `14kt White Gold`, GIA `#2225975086`, no static metal weight |
| `P19-08` | Ross-Simons 993085 (`BND-08`) | confirmed | `$3,295`, `Gold Weight 5.9 grams`, `Metal 14kt and 22kt Gold` (mixed karat, so no melt figure is computable) |
| `P19-09` | Ring Concierge 2.08 oval (`ringconcierge-2-08-…`) | confirmed | `Regular price$6,038`, `2.08 Carat E VS1`, `Made to Order`, `3-4 weeks`, no "solid" wording |
| `P19-SPOT` | Gold benchmark | **flagged** | `Spot Gold Price: USD 3,995.88 / Ounce … Oct 23rd, 2026 at 07:41 NY Time` — 0.66% below the stored dated anchor; clock label again behind the read time |
| `P19-11` | 15 U.S.C. § 1666, 16 CFR Part 435 | confirmed | Both opened live to support the payment and returns requirements; quotes added to `data/sources.json` |
| `P19-12` | Requirements matrix | confirmed | Independent re-derivation by `scripts/hallucination_scan.py` agrees with the stored matrix cell for cell |

**No stored price, karat or gram weight was contradicted by a live page in this pass.** The two flags are a moving seller price and a moving spot price — both recorded, neither overwritten.

## 3. The requirements matrix — what it proves

| Requirement | Good | Partial | Fail | Blank / unverified |
|---|---|---|---|---|
| 1. Karat stated | 67 | 4 | 0 | 0 |
| 2. Word "solid" used | 19 | 7 | 4 | 41 |
| 3. Hallmark disclosed | 3 | 0 | 0 | 68 |
| 4. Maker's mark disclosed | 2 | 0 | 0 | 69 |
| 5. Finished weight in grams | 19 | 0 | 0 | 52 |
| 6. Independent reputation | 46 | 10 | 0 | 15 |
| 7. Usable return window | 38 | 24 | 9 | 0 |
| 8. Credit card accepted | 29 | 29 | 0 | 13 |
| 9. Documentation captured | 71 | 0 | 0 | 0 |
| 10. Independent / XRF check | 0 | 7 | 0 | 64 |

- **0 of 71 rows** are "good" on all ten. That is the headline, and it is the honest one: the failure is structural, not cosmetic.
- **6 rows** are "good" on the four facts a seller fully controls — karat, the word "solid", a gram weight and a usable return window; **7** more reach at least "partial" on those four.
- **19 of 71** rows publish a numeric gram weight, so 19 carry a price-to-melt multiple at the dated anchor (range **1.37× – 25.07×**). The other 52 are left blank rather than back-calculated; four Aurate ranges were blanked by peer pass P17 as unscoped weight, so the matrix counts zero "partial" weights.
- **3** rows document a hallmark and **2** a maker's mark (Wilson's estate pieces). No seller publishes a hallmark *policy*.
- **13** rows leave card acceptance unverified and **9** are final sale or non-returnable — the two columns that most often decide whether a buyer can test the ring at all.
- **0** rows record a seller offering XRF or an assay; 7 record a seller statement only (Wilson's "stamped for X karat", Menē's own certificate).

## 4. Three site defects found and fixed

| ID | Defect | Fix |
|---|---|---|
| `SD25` | `index.html` printed "Weights in this pass" and "Hallmark policies" with Dataset-A-only values while the sub-labels described the whole site. | Relabelled "Dataset A weights" and "Retailer hallmark policies", moved the 19-of-71 figure into the sub-line, added a "Checklist cells verified" tile and a link to the new page. |
| `SD26` | The first draft of the matrix cited five authority pages at paths that are not the ones registered in `data/sources.json`, including 16 CFR Part 23 under subchapter A instead of subchapter B. | Every authority link now points at a page registered and quoted in `data/sources.json`, or at the two pages opened live this pass. `HS-09` in the new scan enforces https + an action for all ten. |
| `SD27` | CI built the pages before running `audit.py`, so the SD21 date guard failed on the first run after UTC midnight — a guard-ordering bug, not a site defect. | The workflow rebuilds both page sets immediately after the audit, and the guard derives its expected date from `reports/audit-report.md` instead of a typed literal. |

## 5. New gates

```bash
python3 scripts/requirements_matrix.py   # regenerate data/requirements-matrix.json from data/
python3 scripts/hallucination_scan.py    # HS-01..HS-10: re-derive, read the page back, fail on any mismatch
```

`hallucination_scan.py` is the anti-hallucination check the brief asks for after every review. It regenerates the matrix from `data/*.json`, compares it with the published copy, then asserts that `requirements.html` prints only values the data holds — and it proves that **every stored price and every stored gram weight appears verbatim in that row's own quote**, which is the difference between a sourced figure and an invented one.

Both are wired into `.github/workflows/audit.yml`, so a stale or contradicted cell fails CI before it can reach Pages.

## 6. Numbers changed on this pass

| Value | Before | After | Where |
|---|---|---|---|
| Verification checks | 222 | **234** | `data/verification.json`, `verify.html` |
| Confirmed / corrected / flagged | 108 / 77 / 37 | **118 / 77 / 39** | same |
| Site defects recorded | 22 | **24** | same |
| Findings | 49 | **52** (`F56`–`F58`) | `data/findings.json`, `flagged.html` |
| Authority sources | 12 | **14** (`usc-1666`, `cfr-435`) | `data/sources.json`, `sources.html` |

## 7. Recommended next hallucination hunt

1. The **48 rows with no published weight** remain the largest gap; ask each seller for a gram weight and keep the reply as a quote.
2. **Re-read the 13 rows whose payment is unverified** — the payments page, not the product page, is where a card list lives.
3. **Spot drift:** the live reading has now been below the dated anchor all day (`F39`, `F45`, this pass). Do not hand-edit the anchor; run `scripts/refresh_spot_anchor.py` against one dated capture.
4. **Menē** re-prices intra-day (`F56`): never quote a Menē price without the minute it was read.
5. Re-run `scripts/hallucination_scan.py` after any data change; a matrix that disagrees with its own page is the failure mode this pass exists to prevent.
