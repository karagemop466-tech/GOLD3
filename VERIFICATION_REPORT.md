# GOLD3 — Anti-Hallucination & Security Verification Report

- **Latest Audit Pass:** Pass #26 — `Pass P9c — Restored Exact PDP price_source on All 7 Aurate + 2 Ring Concierge Rows After 3-Way Merge`
- **Timestamp (UTC):** `2026-10-23T10:48:51Z`
- **Overall Result:** **PASS** (`0` integrity errors)
- **Unique Official HTTPS URLs Verified:** `179`
- **Catalog Entries Audited:** `21` rings + `5` sellers + `7` karat standards
- **Items Published on Flagged for Review (`flagged-for-review.html`):** `21` entries (`63` specific findings)

> **Mandatory Post-Review Recommendation:** Run `python3 scripts/run_security_audit.py --pass-label "Manual Review Check"` after every review pass and actively look for price drift, omitted weights, or hallucinations against the official links below.

## Latest Pass Check Breakdown

| Check ID | Check Name | Status | Count | Summary |
|---|---|---|---|---|
| `SEC-01` | Official HTTPS Source Allowlist & Row Link Completeness | **PASS** | `61` | Verified 61 HTTPS source links across 21 rings, 5 sellers, 7 karat standards, and 2 live spot feeds against strict official domain allowlist. |
| `SEC-02` | Verbatim Price & Gram-Weight Substring Proof (Anti-Hallucination Check) | **PASS** | `21` | Confirmed all 21 prices and all 5 published gram weights appear verbatim inside archived 2026-10-22 primary listing excerpts. |
| `SEC-03` | Zero-Inference Enforcement (Unverified Values Strictly Left Blank/Null) | **PASS** | `17` | Confirmed 17 items with unconfirmed metal gram weights or mixed-karat splits keep null numeric cells (never inferred) and carry explicit review flags. |
| `SEC-04` | NIST Troy-Ounce (31.1034768 g) & Raw Melt Arithmetic Audit | **PASS** | `11` | Mathematically verified spot conversion ($4,022.70 / 31.1034768 = $129.3328/g), all 7 karat tiers, and all 4 weight-complete rings to <= $0.02 tolerance. |
| `SEC-05` | Automated Irregularity, Plated-Control, BBB & Return-Exclusion Scanner | **PASS** | `63` | Cataloged 63 line-by-line review flags across 21 flagged ring entries for publication on flagged-for-review.html. |
| `SEC-06` | Static HTML Internal/External Link Integrity & Anchor Verification | **PASS** | `2175` | Parsed 24 HTML pages and verified 2175 links, stylesheets, scripts, and anchor targets with zero broken links. |
| `SEC-07` | Front-End Security, No-Hallucinations Top Banner & Zero-External-Script Check | **PASS** | `24` | Verified zero third-party script dependencies, strict rel='noopener noreferrer' on external links, zero eval() calls, and active Front-Page No-Hallucinations Mandate summary. |

## SHA-256 Integrity Digests (`data/*.json`)

| File | SHA-256 Digest |
|---|---|
| `data/bands-and-high-karat.json` | `45fb55cde7cba506ea62b7b6423a98db0b2eeed15b11d2c116c90b704769129f` |
| `data/findings.json` | `4fd26cbc03e5ad7d697b825f259236fcd019bb03009d0f44e594dafeefe1e101` |
| `data/flags.json` | `a966192e8ad89dfa77b43a43313591fe09e14b1b08da2fcf9ee1371f8bb9e743` |
| `data/gold-price.json` | `bdb3a741c6696f56ec713c090706cb98fefb53901fe284dfe105308a7d6a7e08` |
| `data/prices.json` | `509ec5ee9ef43541fc4298458e8b1b79ecb522a4eeddd5204c3863f29d7d9e58` |
| `data/products.json` | `b710535c3310aded606c436d9207276ac91c399d879522aa4861c7c751ef7194` |
| `data/retailers.json` | `e780a16102e4278cd4c8803871c50f2527bb7a73baa5db24ead1558e5e5d50e8` |
| `data/reverification-1162b2db.json` | `803157bd7daddc10ea8ab4773c5ee1df1b5573c259c53c18c74c025263cea4b3` |
| `data/reverification-c-15b00e99.json` | `34ac65f9dc2ee5d078b5a4a7128eb41fd2e7316efbd4e5d125ebe71b0b946332` |
| `data/reverification-c-6ccbc523.json` | `52f4a6d610762be546e45e94fd1ffe2f17f201d16215625264fe45c84acc78f2` |
| `data/reverification-dataset-c.json` | `2f35e1bb80f76cbc360f51dc2fec996c407f96fdd192b6386f33ad5cf4635e5c` |
| `data/reverification-p3.json` | `b1dca1669099d66e45b08588f8827b24f59edd65e4f4b4a806ef2a02987b5d16` |
| `data/reverification-p4.json` | `2e5ce8fdff92d04a3e1570960caf0bb1daafc91b2d76209a97a0fb94635e801a` |
| `data/reverification-p5.json` | `1c5ba33b93efdaa14d423fff0be8ca20622f4436d900bc6208ee44e64158bdda` |
| `data/reverification-p6.json` | `dee30027715ce1f89f414ab0bff0140b3684ba009e6b7f1fa3fc3f7322a7b62e` |
| `data/rings.json` | `777f8cf0a4541306d8ed2b563b82dff7f00c3b37a131887fb30ae7216dada3d5` |
| `data/sellers-policies.json` | `6f2edb268c1efd391f4c98102d164665d40d1b2f56cc18702c4492bad6b8cd36` |
| `data/sellers.json` | `f7dce3e60e468657e02b356b32fbcc875ee6504a5a73e2c98acbf36e67da9c13` |
| `data/solitaire-rings.json` | `b14736e9308d559ca542081e0b9dda7b325588b6558486aa288d27753ef5b8d8` |
| `data/sources.json` | `7bb6c9ab27bad24c82e780193a3dad5b7610e09df66ca36f69b65dc05b9da48c` |
| `data/spot-and-standards.json` | `fb7febce8b15501221a57f89e4f244635d645ac122963315373bc0137f39a171` |
| `data/standards.json` | `6b745302667c70fb15800fb830471250551a37e238e507a8b993f8e3c4423ad8` |
| `data/verification-report.json` | `6b7c03bfd8b7004218fcd7ab4285b972fe342e814d692ffec842b0794ddc31a7` |
| `data/verification.json` | `4bd1bb0b47a643fb60c782ecc189963b9833dd3c655579e2b1d152ee56396595` |
