# GOLD3 — Anti-Hallucination & Security Verification Report

- **Latest Audit Pass:** Pass #16 — `Pass P4 re-verification & CR-P3-1..9 integration`
- **Timestamp (UTC):** `2026-10-23T10:16:44Z`
- **Overall Result:** **PASS** (`0` integrity errors)
- **Unique Official HTTPS URLs Verified:** `172`
- **Catalog Entries Audited:** `21` rings + `5` sellers + `7` karat standards
- **Items Published on Flagged for Review (`flagged-for-review.html`):** `17` entries (`39` specific findings)

> **Mandatory Post-Review Recommendation:** Run `python3 scripts/run_security_audit.py --pass-label "Manual Review Check"` after every review pass and actively look for price drift, omitted weights, or hallucinations against the official links below.

## Latest Pass Check Breakdown

| Check ID | Check Name | Status | Count | Summary |
|---|---|---|---|---|
| `SEC-01` | Official HTTPS Source Allowlist & Row Link Completeness | **PASS** | `61` | Verified 61 HTTPS source links across 21 rings, 5 sellers, 7 karat standards, and 2 live spot feeds against strict official domain allowlist. |
| `SEC-02` | Verbatim Price & Gram-Weight Substring Proof (Anti-Hallucination Check) | **PASS** | `21` | Confirmed all 21 prices and all 8 published gram weights appear verbatim inside archived 2026-10-22 primary listing excerpts. |
| `SEC-03` | Zero-Inference Enforcement (Unverified Values Strictly Left Blank/Null) | **PASS** | `14` | Confirmed 14 items with unconfirmed metal gram weights or mixed-karat splits keep null numeric cells (never inferred) and carry explicit review flags. |
| `SEC-04` | NIST Troy-Ounce (31.1034768 g) & Raw Melt Arithmetic Audit | **PASS** | `14` | Mathematically verified spot conversion ($4,025.10 / 31.1034768 = $129.4100/g), all 7 karat tiers, and all 7 weight-complete rings to <= $0.02 tolerance. |
| `SEC-05` | Automated Irregularity, Plated-Control, BBB & Return-Exclusion Scanner | **PASS** | `39` | Cataloged 39 line-by-line review flags across 17 flagged ring entries for publication on flagged-for-review.html. |
| `SEC-06` | Static HTML Internal/External Link Integrity & Anchor Verification | **PASS** | `1920` | Parsed 24 HTML pages and verified 1920 links, stylesheets, scripts, and anchor targets with zero broken links. |
| `SEC-07` | Front-End Security, No-Hallucinations Top Banner & Zero-External-Script Check | **PASS** | `24` | Verified zero third-party script dependencies, strict rel='noopener noreferrer' on external links, zero eval() calls, and active Front-Page No-Hallucinations Mandate summary. |

## SHA-256 Integrity Digests (`data/*.json`)

| File | SHA-256 Digest |
|---|---|
| `data/bands-and-high-karat.json` | `dfefd801f1d3c3a15acce77e4f8ef487d2032fef8570f8026bd8fbb330ba9644` |
| `data/findings.json` | `85dfc1dd390215b1da1c3a85eb699e343fd7581d866e8c55cec0061426356e85` |
| `data/flags.json` | `ec2f06c6ccc921cb54328b322a28f9e97dd93d01583e8ff1abb885c072a35f41` |
| `data/gold-price.json` | `bdb3a741c6696f56ec713c090706cb98fefb53901fe284dfe105308a7d6a7e08` |
| `data/prices.json` | `639b30ebe844d1e7740046c0c1aa474117ab0a34d14df6077be23ca532226f0a` |
| `data/products.json` | `2d0ca7ed16ea275024a347ff9d178e0f4cbf8e5ddb3428cf5beebfab8b8396b6` |
| `data/retailers.json` | `fc2130447e547458e380d666c0b6598352464a2dedffbd8d0aefc7ce7ffabab3` |
| `data/reverification-p3.json` | `b1dca1669099d66e45b08588f8827b24f59edd65e4f4b4a806ef2a02987b5d16` |
| `data/reverification-p4.json` | `46f99c832ef98244d5d535ef4389dabc9313f1f92833e11157a3b9a09ec2cae8` |
| `data/rings.json` | `384951978799809668181a4a548cdcc85c2f4c038ebb93c6e727e1d2c7cc4e43` |
| `data/sellers-policies.json` | `372689ba815fb011c15b17e52773385718f972b174023f8bd67e01bc10d27ea6` |
| `data/sellers.json` | `90259e42f45a423366b4c7fe4676a4d15efe5772d57ecd834e6db806dc475e06` |
| `data/solitaire-rings.json` | `1f24aa389723b9c395b2f0ed103fe3b5fa60b4b658e5196806370aa06ff6ffaa` |
| `data/sources.json` | `e9f8a68dc22397b9e6d0bc24dbc8c079dd62a58a794a3d1a4362b69f2c2df236` |
| `data/spot-and-standards.json` | `060e3a9379792d784c93800ca93120d2bb6089d0544ff27cb23114a84230a9f0` |
| `data/standards.json` | `7d10a2520465c2b2734d236d9dfe93e4db44bc5d0649cb6cf82bb35cc94b668c` |
| `data/verification-report.json` | `32c2828bc87735fffb7d3d4f7a60be8c8b494c035c134afcc7a6e58920e343ea` |
| `data/verification.json` | `9efc32e804a90276fbbb296c3982939303dcbba8c8f9a0f14cc66539ea5c7a5b` |
