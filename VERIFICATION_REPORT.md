# GOLD3 — Anti-Hallucination & Security Verification Report

- **Latest Audit Pass:** Pass #22 — `Pass P9 — Complete Primary-Source Re-Verification (137 Checks, Aurate ×7, R03 PDP Fix, Zero Backlog)`
- **Timestamp (UTC):** `2026-10-23T10:36:53Z`
- **Overall Result:** **PASS** (`0` integrity errors)
- **Unique Official HTTPS URLs Verified:** `193`
- **Catalog Entries Audited:** `21` rings + `5` sellers + `7` karat standards
- **Items Published on Flagged for Review (`flagged-for-review.html`):** `21` entries (`63` specific findings)

> **Mandatory Post-Review Recommendation:** Run `python3 scripts/run_security_audit.py --pass-label "Manual Review Check"` after every review pass and actively look for price drift, omitted weights, or hallucinations against the official links below.

## Latest Pass Check Breakdown

| Check ID | Check Name | Status | Count | Summary |
|---|---|---|---|---|
| `SEC-01` | Official HTTPS Source Allowlist & Row Link Completeness | **PASS** | `61` | Verified 61 HTTPS source links across 21 rings, 5 sellers, 7 karat standards, and 2 live spot feeds against strict official domain allowlist. |
| `SEC-02` | Verbatim Price & Gram-Weight Substring Proof (Anti-Hallucination Check) | **PASS** | `21` | Confirmed all 21 prices and all 5 published gram weights appear verbatim inside archived 2026-10-22 primary listing excerpts. |
| `SEC-03` | Zero-Inference Enforcement (Unverified Values Strictly Left Blank/Null) | **PASS** | `17` | Confirmed 17 items with unconfirmed metal gram weights or mixed-karat splits keep null numeric cells (never inferred) and carry explicit review flags. |
| `SEC-04` | NIST Troy-Ounce (31.1034768 g) & Raw Melt Arithmetic Audit | **PASS** | `11` | Mathematically verified spot conversion ($4,025.10 / 31.1034768 = $129.4100/g), all 7 karat tiers, and all 4 weight-complete rings to <= $0.02 tolerance. |
| `SEC-05` | Automated Irregularity, Plated-Control, BBB & Return-Exclusion Scanner | **PASS** | `63` | Cataloged 63 line-by-line review flags across 21 flagged ring entries for publication on flagged-for-review.html. |
| `SEC-06` | Static HTML Internal/External Link Integrity & Anchor Verification | **PASS** | `2083` | Parsed 24 HTML pages and verified 2083 links, stylesheets, scripts, and anchor targets with zero broken links. |
| `SEC-07` | Front-End Security, No-Hallucinations Top Banner & Zero-External-Script Check | **PASS** | `24` | Verified zero third-party script dependencies, strict rel='noopener noreferrer' on external links, zero eval() calls, and active Front-Page No-Hallucinations Mandate summary. |

## SHA-256 Integrity Digests (`data/*.json`)

| File | SHA-256 Digest |
|---|---|
| `data/bands-and-high-karat.json` | `98aa4d2f5d54bb97e57dfc03c38ec75f93341ea451ba251dca02d60329332068` |
| `data/findings.json` | `93cb67ee542546a15f23589cb673f65614d31265d48a3647e765caa7da885bf3` |
| `data/flags.json` | `0f5b823c94cc7c94d49603a9403bcb28a2b2f69594f752e4cd30748d0d0dbaa0` |
| `data/gold-price.json` | `bdb3a741c6696f56ec713c090706cb98fefb53901fe284dfe105308a7d6a7e08` |
| `data/prices.json` | `74ac434deda76bda595af161d3d52c5777a71c3fbfe58003e251b802dc44f165` |
| `data/products.json` | `005445cd3fed062d1ccf0c6767a9fc6fc97e1f0e22f96e5927234aa415c8d89c` |
| `data/retailers.json` | `63cd624dc7354989c209bfd9939c448ae84ef52a84017e19808eb1f6f375ae0f` |
| `data/reverification-1162b2db.json` | `803157bd7daddc10ea8ab4773c5ee1df1b5573c259c53c18c74c025263cea4b3` |
| `data/reverification-c-6ccbc523.json` | `52f4a6d610762be546e45e94fd1ffe2f17f201d16215625264fe45c84acc78f2` |
| `data/reverification-dataset-c.json` | `2f35e1bb80f76cbc360f51dc2fec996c407f96fdd192b6386f33ad5cf4635e5c` |
| `data/reverification-p3.json` | `b1dca1669099d66e45b08588f8827b24f59edd65e4f4b4a806ef2a02987b5d16` |
| `data/reverification-p4.json` | `2e5ce8fdff92d04a3e1570960caf0bb1daafc91b2d76209a97a0fb94635e801a` |
| `data/reverification-p5.json` | `1c5ba33b93efdaa14d423fff0be8ca20622f4436d900bc6208ee44e64158bdda` |
| `data/rings.json` | `287a2adcce047c0ab98542e44cf28beff4ee3d9a2e429c7b36b455be970d1c2b` |
| `data/sellers-policies.json` | `56fdfb4fc6bb31f747e74e342defb37b9311326c34d60704724abbebe9917d4b` |
| `data/sellers.json` | `33ab30a0301db541df25ec21fbe9e73d6161360ec66d8b54b69261578632ff2e` |
| `data/solitaire-rings.json` | `67cc81d443f307e3728c1609c591f63e98f4855d732619bb4b573b5b43c71db4` |
| `data/sources.json` | `e59992bc2419cc8e9bed56c64b49c8ae91394ec5c8bbdf78881320caaf2fa77b` |
| `data/spot-and-standards.json` | `58902c71386b14704c28a9e15c23f05db8f4feb08692a44ce6ff0fd5dd0378f5` |
| `data/standards.json` | `6b745302667c70fb15800fb830471250551a37e238e507a8b993f8e3c4423ad8` |
| `data/verification-report.json` | `e5de1fdd3af6c70cd2e2deee94e32ad599ebab2d7c3d6313b707327ffd9d5e3f` |
| `data/verification.json` | `e3ad7faf68db178c71041e3d6ba32af7b4d21d531036f9030358d490fdfd6ce8` |
