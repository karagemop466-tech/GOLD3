# GOLD3 — Anti-Hallucination & Security Verification Report

- **Latest Audit Pass:** Pass #20 — `Final Pre-PR Verification Pass P8 (arena/2908bea4-gold3)`
- **Timestamp (UTC):** `2026-10-23T10:26:32Z`
- **Overall Result:** **PASS** (`0` integrity errors)
- **Unique Official HTTPS URLs Verified:** `188`
- **Catalog Entries Audited:** `21` rings + `5` sellers + `7` karat standards
- **Items Published on Flagged for Review (`flagged-for-review.html`):** `21` entries (`53` specific findings)

> **Mandatory Post-Review Recommendation:** Run `python3 scripts/run_security_audit.py --pass-label "Manual Review Check"` after every review pass and actively look for price drift, omitted weights, or hallucinations against the official links below.

## Latest Pass Check Breakdown

| Check ID | Check Name | Status | Count | Summary |
|---|---|---|---|---|
| `SEC-01` | Official HTTPS Source Allowlist & Row Link Completeness | **PASS** | `61` | Verified 61 HTTPS source links across 21 rings, 5 sellers, 7 karat standards, and 2 live spot feeds against strict official domain allowlist. |
| `SEC-02` | Verbatim Price & Gram-Weight Substring Proof (Anti-Hallucination Check) | **PASS** | `21` | Confirmed all 21 prices and all 5 published gram weights appear verbatim inside archived 2026-10-22 primary listing excerpts. |
| `SEC-03` | Zero-Inference Enforcement (Unverified Values Strictly Left Blank/Null) | **PASS** | `17` | Confirmed 17 items with unconfirmed metal gram weights or mixed-karat splits keep null numeric cells (never inferred) and carry explicit review flags. |
| `SEC-04` | NIST Troy-Ounce (31.1034768 g) & Raw Melt Arithmetic Audit | **PASS** | `11` | Mathematically verified spot conversion ($4,025.10 / 31.1034768 = $129.4100/g), all 7 karat tiers, and all 4 weight-complete rings to <= $0.02 tolerance. |
| `SEC-05` | Automated Irregularity, Plated-Control, BBB & Return-Exclusion Scanner | **PASS** | `53` | Cataloged 53 line-by-line review flags across 21 flagged ring entries for publication on flagged-for-review.html. |
| `SEC-06` | Static HTML Internal/External Link Integrity & Anchor Verification | **PASS** | `2075` | Parsed 24 HTML pages and verified 2075 links, stylesheets, scripts, and anchor targets with zero broken links. |
| `SEC-07` | Front-End Security, No-Hallucinations Top Banner & Zero-External-Script Check | **PASS** | `24` | Verified zero third-party script dependencies, strict rel='noopener noreferrer' on external links, zero eval() calls, and active Front-Page No-Hallucinations Mandate summary. |

## SHA-256 Integrity Digests (`data/*.json`)

| File | SHA-256 Digest |
|---|---|
| `data/bands-and-high-karat.json` | `d7bcdc30e96312b051be27e5bb1b9f48d25f398611e96dc690c02fbc1575f749` |
| `data/findings.json` | `ab9bc570436602ab1166ad274e53a3b80dd1cb3c1b691cd1758e90950fb54873` |
| `data/flags.json` | `de635e0abb8780f2751da49a1c2fe91fa9cef2db7d79e993e7988e129925b933` |
| `data/gold-price.json` | `bdb3a741c6696f56ec713c090706cb98fefb53901fe284dfe105308a7d6a7e08` |
| `data/prices.json` | `639b30ebe844d1e7740046c0c1aa474117ab0a34d14df6077be23ca532226f0a` |
| `data/products.json` | `d4c36640860f639be29f18c6fe5c601389eb736ed8e1df2c1ae6cdeaa7a8efe7` |
| `data/retailers.json` | `fc2130447e547458e380d666c0b6598352464a2dedffbd8d0aefc7ce7ffabab3` |
| `data/reverification-dataset-c.json` | `2f35e1bb80f76cbc360f51dc2fec996c407f96fdd192b6386f33ad5cf4635e5c` |
| `data/reverification-p3.json` | `b1dca1669099d66e45b08588f8827b24f59edd65e4f4b4a806ef2a02987b5d16` |
| `data/reverification-p4.json` | `2e5ce8fdff92d04a3e1570960caf0bb1daafc91b2d76209a97a0fb94635e801a` |
| `data/reverification-p5.json` | `1c5ba33b93efdaa14d423fff0be8ca20622f4436d900bc6208ee44e64158bdda` |
| `data/rings.json` | `eb9c0e9b468fb7e8dc8d79dcdc4f511ee8362f55b00b921ef97aad016ad02344` |
| `data/sellers-policies.json` | `625afec49d153317c48bc463f0bec36971d3120cf962d170616f9fd85fc68699` |
| `data/sellers.json` | `2d504f540bea854eb7d83e169e8031b0e757fd9d2ac6c80e5422c10a3a006b2e` |
| `data/solitaire-rings.json` | `f08a0b070155f41ddb6dc7a23e1213b9ed05b8198098afce5cf63fecd940b29d` |
| `data/sources.json` | `e59992bc2419cc8e9bed56c64b49c8ae91394ec5c8bbdf78881320caaf2fa77b` |
| `data/spot-and-standards.json` | `ffabd0ca49e72bf9f6b7d47d8a40166324017d6a04906ea3589a2e555f065e7b` |
| `data/standards.json` | `6b745302667c70fb15800fb830471250551a37e238e507a8b993f8e3c4423ad8` |
| `data/verification-report.json` | `082b64519c8a8da51db345ac6c82731ca875cf178e395998dce0315db7622fde` |
| `data/verification.json` | `163f06038a2792c6a393890e96b1ca476803eb6948a0e3a4dd5cba053fa8dc3c` |
