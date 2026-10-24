# GOLD3 — Anti-Hallucination & Security Verification Report

- **Latest Audit Pass:** Pass #41 — `Scheduled Verification Pass`
- **Timestamp (UTC):** `2026-10-24T00:05:16Z`
- **Overall Result:** **PASS** (`0` integrity errors)
- **Unique Official HTTPS URLs Verified:** `187`
- **Catalog Entries Audited:** `21` rings + `5` sellers + `7` karat standards
- **Items Published on Flagged for Review (`flagged-for-review.html`):** `21` entries (`68` specific findings)

> **Mandatory Post-Review Recommendation:** Run `python3 scripts/run_security_audit.py --pass-label "Manual Review Check"` after every review pass and actively look for price drift, omitted weights, or hallucinations against the official links below.

## Latest Pass Check Breakdown

| Check ID | Check Name | Status | Count | Summary |
|---|---|---|---|---|
| `SEC-01` | Official HTTPS Source Allowlist & Row Link Completeness | **PASS** | `61` | Verified 61 HTTPS source links across 21 rings, 5 sellers, 7 karat standards, and 2 live spot feeds against strict official domain allowlist. |
| `SEC-02` | Verbatim Price & Gram-Weight Substring Proof (Anti-Hallucination Check) | **PASS** | `21` | Confirmed all 21 prices and all 5 published gram weights appear verbatim inside archived 2026-10-22 primary listing excerpts. |
| `SEC-03` | Zero-Inference Enforcement (Unverified Values Strictly Left Blank/Null) | **PASS** | `17` | Confirmed 17 items with unconfirmed metal gram weights or mixed-karat splits keep null numeric cells (never inferred) and carry explicit review flags. |
| `SEC-04` | NIST Troy-Ounce (31.1034768 g) & Raw Melt Arithmetic Audit | **PASS** | `11` | Mathematically verified spot conversion ($4,022.70 / 31.1034768 = $129.3328/g), all 7 karat tiers, and all 4 weight-complete rings to <= $0.02 tolerance. |
| `SEC-05` | Automated Irregularity, Plated-Control, BBB & Return-Exclusion Scanner | **PASS** | `68` | Cataloged 68 line-by-line review flags across 21 flagged ring entries for publication on flagged-for-review.html. |
| `SEC-06` | Static HTML Internal/External Link Integrity & Anchor Verification | **PASS** | `2413` | Parsed 24 HTML pages and verified 2413 links, stylesheets, scripts, and anchor targets with zero broken links. |
| `SEC-07` | Front-End Security, No-Hallucinations Top Banner & Zero-External-Script Check | **PASS** | `24` | Verified zero third-party script dependencies, strict rel='noopener noreferrer' on external links, zero eval() calls, and active Front-Page No-Hallucinations Mandate summary. |

## SHA-256 Integrity Digests (`data/*.json`)

| File | SHA-256 Digest |
|---|---|
| `data/bands-and-high-karat.json` | `954cb5aa552b14adc0bfc6b81196bea9d430dcb3dd7a0813707ef00e9c55d7f1` |
| `data/findings.json` | `91e122c7c5f3dd3abae2822ff6f3827681db95c108ee76a3370fb418955f35c9` |
| `data/flags.json` | `2ed55192f04d6c400c9cb389ba2e5b730c5d41b746d643ae819bd4dbf3bc91d3` |
| `data/gold-price.json` | `bdb3a741c6696f56ec713c090706cb98fefb53901fe284dfe105308a7d6a7e08` |
| `data/prices.json` | `ed6d29de4fe2696e94846f4cf974cc58d241d684fe941c13f5a44cd88a164a9e` |
| `data/products.json` | `a91177ad66b579ec31815c0115d3b06b84ed96b551d8623507a403b99b393601` |
| `data/retailers.json` | `b1b83094c3bbfff4e339e5170a3ad8a2425610ae2659edfb7435ca80659d1dbe` |
| `data/reverification-1162b2db.json` | `803157bd7daddc10ea8ab4773c5ee1df1b5573c259c53c18c74c025263cea4b3` |
| `data/reverification-57724486.json` | `8b185580a5ef8bafa536151f721d3cb516e66926f02762af704284b9c3e2e2f3` |
| `data/reverification-bfcd8465.json` | `46f99c832ef98244d5d535ef4389dabc9313f1f92833e11157a3b9a09ec2cae8` |
| `data/reverification-c-15b00e99.json` | `34ac65f9dc2ee5d078b5a4a7128eb41fd2e7316efbd4e5d125ebe71b0b946332` |
| `data/reverification-c-6ccbc523.json` | `a807951064276cd1fd9010379082733243c39cbf75a542d52e5e74bd0e64386d` |
| `data/reverification-dataset-c.json` | `2f35e1bb80f76cbc360f51dc2fec996c407f96fdd192b6386f33ad5cf4635e5c` |
| `data/reverification-fb7e5e3c.json` | `5b0dfdc516c0cd958d8d600ae85a28d7ad46e73aa743335110b4d1e60f3c792a` |
| `data/reverification-p15.json` | `ed96531e5576f223a77187091275b945ca35c9c5e1dbb9429d97b7973cbc7b6e` |
| `data/reverification-p17.json` | `14e3160dc5fe245c694c5099550cd65a4d638d28f30bf4c23d744f0c9b375b9d` |
| `data/reverification-p19.json` | `745f44157e3c7bdd7825a3875feac62ff7ca1e0ad2dc336e754c47134de58843` |
| `data/reverification-p3.json` | `b1dca1669099d66e45b08588f8827b24f59edd65e4f4b4a806ef2a02987b5d16` |
| `data/reverification-p4.json` | `2e5ce8fdff92d04a3e1570960caf0bb1daafc91b2d76209a97a0fb94635e801a` |
| `data/reverification-p5.json` | `1c5ba33b93efdaa14d423fff0be8ca20622f4436d900bc6208ee44e64158bdda` |
| `data/reverification-p6.json` | `dee30027715ce1f89f414ab0bff0140b3684ba009e6b7f1fa3fc3f7322a7b62e` |
| `data/rings.json` | `043e4eda28bfe50e5ea02dc3dde189acf1413edba23138a3cc1bdb419fa3cb5a` |
| `data/sellers-policies.json` | `bfdc4ea96fe5daaf26fed08c1811bb8b9bb012fbb986f4310ee5bce8290ca9a9` |
| `data/sellers.json` | `4d1bd09620f904e833139fa16f7be571e87ade0115df1826472447e324bc033f` |
| `data/solitaire-rings.json` | `201fcc8aa94282160cebcb2afb706ba4c64c40617b3d7cf7f370554885077dbc` |
| `data/sources.json` | `455599b1ce95a85a173d02dbb0bdb4275c6566edeb350073948af459b82ffd0e` |
| `data/spot-and-standards.json` | `b2b4203069b283be7a36228bf776aed7bda1e673435d1e2488c83e3fd890e03b` |
| `data/standards.json` | `6b745302667c70fb15800fb830471250551a37e238e507a8b993f8e3c4423ad8` |
| `data/verification-report.json` | `0eab2d1b6a328d384458a4840ce107c6f0f1c64dd8fd1af2d5f30e12e3105483` |
| `data/verification.json` | `f6bd6f5b5f2219e0bc803a13ae343b662fff33539f86b5fe5e0cf05da02b1448` |
