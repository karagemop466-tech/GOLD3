# GOLD3 — Anti-Hallucination & Security Verification Report

- **Latest Audit Pass:** Pass #9 — `Pass 9: Post-PR22 Reconciled 62-Listing Multi-Suite Audit`
- **Timestamp (UTC):** `2026-10-22T23:41:27Z`
- **Overall Result:** **PASS** (`0` integrity errors)
- **Unique Official HTTPS URLs Verified:** `139`
- **Catalog Entries Audited:** `21` rings + `5` sellers + `7` karat standards
- **Items Published on Flagged for Review (`flagged-for-review.html`):** `17` entries (`37` specific findings)

> **Mandatory Post-Review Recommendation:** Run `python3 scripts/run_security_audit.py --pass-label "Manual Review Check"` after every review pass and actively look for price drift, omitted weights, or hallucinations against the official links below.

## Latest Pass Check Breakdown

| Check ID | Check Name | Status | Count | Summary |
|---|---|---|---|---|
| `SEC-01` | Official HTTPS Source Allowlist & Row Link Completeness | **PASS** | `61` | Verified 61 HTTPS source links across 21 rings, 5 sellers, 7 karat standards, and 2 live spot feeds against strict official domain allowlist. |
| `SEC-02` | Verbatim Price & Gram-Weight Substring Proof (Anti-Hallucination Check) | **PASS** | `21` | Confirmed all 21 prices and all 8 published gram weights appear verbatim inside archived 2026-10-22 primary listing excerpts. |
| `SEC-03` | Zero-Inference Enforcement (Unverified Values Strictly Left Blank/Null) | **PASS** | `14` | Confirmed 14 items with unconfirmed metal gram weights or mixed-karat splits keep null numeric cells (never inferred) and carry explicit review flags. |
| `SEC-04` | NIST Troy-Ounce (31.1034768 g) & Raw Melt Arithmetic Audit | **PASS** | `14` | Mathematically verified spot conversion ($4,025.10 / 31.1034768 = $129.4100/g), all 7 karat tiers, and all 7 weight-complete rings to <= $0.02 tolerance. |
| `SEC-05` | Automated Irregularity, Plated-Control, BBB & Return-Exclusion Scanner | **PASS** | `37` | Cataloged 37 line-by-line review flags across 17 flagged ring entries for publication on flagged-for-review.html. |
| `SEC-06` | Static HTML Internal/External Link Integrity & Anchor Verification | **PASS** | `1603` | Parsed 24 HTML pages and verified 1603 links, stylesheets, scripts, and anchor targets with zero broken links. |
| `SEC-07` | Front-End Security, No-Hallucinations Top Banner & Zero-External-Script Check | **PASS** | `24` | Verified zero third-party script dependencies, strict rel='noopener noreferrer' on external links, zero eval() calls, and active Front-Page No-Hallucinations Mandate summary. |

## SHA-256 Integrity Digests (`data/*.json`)

| File | SHA-256 Digest |
|---|---|
| `data/bands-and-high-karat.json` | `fd6b7c175980cfad74b34145c03e2632e809c6a94de48ef399b96c55d8ea333c` |
| `data/findings.json` | `e799e12dc1545194008a1208725280df918a537257d8c97a07161858dc6363f7` |
| `data/flags.json` | `ccd39bfde1f821f7c4eb1e82097f6534e1121da34cc5d6e3b94f6f32d86c2942` |
| `data/gold-price.json` | `bdb3a741c6696f56ec713c090706cb98fefb53901fe284dfe105308a7d6a7e08` |
| `data/prices.json` | `639b30ebe844d1e7740046c0c1aa474117ab0a34d14df6077be23ca532226f0a` |
| `data/products.json` | `9c2382eef4a8127bcbe5253befa3a772f289349d06b38ed962bcbaa66c9e79bd` |
| `data/retailers.json` | `fc2130447e547458e380d666c0b6598352464a2dedffbd8d0aefc7ce7ffabab3` |
| `data/rings.json` | `98cc7428e4d87611b8384e3669ae106792aa4b8a9560bfb3467b585990e5bd33` |
| `data/sellers-policies.json` | `372689ba815fb011c15b17e52773385718f972b174023f8bd67e01bc10d27ea6` |
| `data/sellers.json` | `985e661d40bd308cd397ff9e5404e0d9986490e7f9e53f27d80b82eb9455b07b` |
| `data/solitaire-rings.json` | `1b0d493a2835471df5bf8610622bf2f668a0c2d62e7961c112d46591ae19f769` |
| `data/sources.json` | `1496e3741397057c11913b06d748bf838b6781b5686e7ab733d3ac5e76a49f41` |
| `data/spot-and-standards.json` | `77a3ff10db7fe885bc1f51eece4311fa6a62034f73ce2292d2e4bf1841b9a5ed` |
| `data/standards.json` | `7d10a2520465c2b2734d236d9dfe93e4db44bc5d0649cb6cf82bb35cc94b668c` |
| `data/verification-report.json` | `3b4f41a2a73cdcd9af350de0a6f1dd63c5e246c68577341768c125d8b7cfca76` |
| `data/verification.json` | `d822faee039611e155042afca173a3beb432cf302a7813f970a6d19a6e3750b8` |
