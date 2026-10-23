# GOLD3 — Anti-Hallucination & Security Verification Report

- **Latest Audit Pass:** Pass #17 — `Pass P5 — Complete Primary-Source Re-Verification (Dataset C + Dataset A + SRC2 + Backlog Zeroed)`
- **Timestamp (UTC):** `2026-10-23T10:24:55Z`
- **Overall Result:** **PASS** (`0` integrity errors)
- **Unique Official HTTPS URLs Verified:** `182`
- **Catalog Entries Audited:** `21` rings + `5` sellers + `7` karat standards
- **Items Published on Flagged for Review (`flagged-for-review.html`):** `17` entries (`40` specific findings)

> **Mandatory Post-Review Recommendation:** Run `python3 scripts/run_security_audit.py --pass-label "Manual Review Check"` after every review pass and actively look for price drift, omitted weights, or hallucinations against the official links below.

## Latest Pass Check Breakdown

| Check ID | Check Name | Status | Count | Summary |
|---|---|---|---|---|
| `SEC-01` | Official HTTPS Source Allowlist & Row Link Completeness | **PASS** | `58` | Verified 58 HTTPS source links across 21 rings, 5 sellers, 7 karat standards, and 2 live spot feeds against strict official domain allowlist. |
| `SEC-02` | Verbatim Price & Gram-Weight Substring Proof (Anti-Hallucination Check) | **PASS** | `21` | Confirmed all 21 prices and all 5 published gram weights appear verbatim inside archived 2026-10-22 primary listing excerpts. |
| `SEC-03` | Zero-Inference Enforcement (Unverified Values Strictly Left Blank/Null) | **PASS** | `17` | Confirmed 17 items with unconfirmed metal gram weights or mixed-karat splits keep null numeric cells (never inferred) and carry explicit review flags. |
| `SEC-04` | NIST Troy-Ounce (31.1034768 g) & Raw Melt Arithmetic Audit | **PASS** | `11` | Mathematically verified spot conversion ($4,025.10 / 31.1034768 = $129.4100/g), all 7 karat tiers, and all 4 weight-complete rings to <= $0.02 tolerance. |
| `SEC-05` | Automated Irregularity, Plated-Control, BBB & Return-Exclusion Scanner | **PASS** | `40` | Cataloged 40 line-by-line review flags across 17 flagged ring entries for publication on flagged-for-review.html. |
| `SEC-06` | Static HTML Internal/External Link Integrity & Anchor Verification | **PASS** | `2049` | Parsed 24 HTML pages and verified 2049 links, stylesheets, scripts, and anchor targets with zero broken links. |
| `SEC-07` | Front-End Security, No-Hallucinations Top Banner & Zero-External-Script Check | **PASS** | `24` | Verified zero third-party script dependencies, strict rel='noopener noreferrer' on external links, zero eval() calls, and active Front-Page No-Hallucinations Mandate summary. |

## SHA-256 Integrity Digests (`data/*.json`)

| File | SHA-256 Digest |
|---|---|
| `data/bands-and-high-karat.json` | `8a6695401327872cb01fbd8613885ab814d2a5435240a4c67d93a2c9a4cb5c4b` |
| `data/findings.json` | `0417588c66b919a89d42a334f1a5d1466789fdd5ddb960aaf3892fa242ef2913` |
| `data/flags.json` | `26522de93e14d6af91ac953c3810b13c1e5a0fd5503c1fe5e706f440c7a45c96` |
| `data/gold-price.json` | `bdb3a741c6696f56ec713c090706cb98fefb53901fe284dfe105308a7d6a7e08` |
| `data/prices.json` | `ccc479435e7574322ac3b19c64d38cf35f893dd652ddcfeeee5f0554d6a2e905` |
| `data/products.json` | `640a0e9cee590b7af0f8d8fca5c43b7822b138afaf9212e002caa65039e849f9` |
| `data/retailers.json` | `e218ca02d5bbe681202edf6c8e1a0baeedfd270a56309985c535211645420eab` |
| `data/reverification-c1.json` | `803157bd7daddc10ea8ab4773c5ee1df1b5573c259c53c18c74c025263cea4b3` |
| `data/reverification-p3.json` | `b1dca1669099d66e45b08588f8827b24f59edd65e4f4b4a806ef2a02987b5d16` |
| `data/reverification-p4.json` | `2e5ce8fdff92d04a3e1570960caf0bb1daafc91b2d76209a97a0fb94635e801a` |
| `data/rings.json` | `b7f7b2273c57db874ee872a01171abf9fea366e95dc5b09ef7190c24be45bdb7` |
| `data/sellers-policies.json` | `e710fdd58a6425fc4dbc36ca7064d8059a067a34fe9a3edb50186c571db93707` |
| `data/sellers.json` | `6446f2bc065f0132f33f756c77de8be9c83fef7c338b83daca9e9a2ce1b5e1a6` |
| `data/solitaire-rings.json` | `5d3a790750cb48e5a51ef7f6505298dd7452a1ac80a2c22e0fdf8ae758cae60d` |
| `data/sources.json` | `e59992bc2419cc8e9bed56c64b49c8ae91394ec5c8bbdf78881320caaf2fa77b` |
| `data/spot-and-standards.json` | `dc4b3de1958cbedf5f50237040f73aaa63eebcbf1c594876a47471b56b141fb8` |
| `data/standards.json` | `7d10a2520465c2b2734d236d9dfe93e4db44bc5d0649cb6cf82bb35cc94b668c` |
| `data/verification-report.json` | `a37fb239d0311214475de966c6348bc64da737ae53ad246ffc97083c199afb89` |
| `data/verification.json` | `56a410cf3eb8aa5a420e909bcbae94904d03132a04f4947e888fb65f620ec0e3` |
