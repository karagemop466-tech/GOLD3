# GOLD3 — Anti-Hallucination & Security Verification Report

- **Latest Audit Pass:** Pass #23 — `Pass P10 (V13 + T16) post-PR-#43 additive integration`
- **Timestamp (UTC):** `2026-10-23T10:42:27Z`
- **Overall Result:** **PASS** (`0` integrity errors)
- **Unique Official HTTPS URLs Verified:** `196`
- **Catalog Entries Audited:** `21` rings + `5` sellers + `7` karat standards
- **Items Published on Flagged for Review (`flagged-for-review.html`):** `21` entries (`67` specific findings)

> **Mandatory Post-Review Recommendation:** Run `python3 scripts/run_security_audit.py --pass-label "Manual Review Check"` after every review pass and actively look for price drift, omitted weights, or hallucinations against the official links below.

## Latest Pass Check Breakdown

| Check ID | Check Name | Status | Count | Summary |
|---|---|---|---|---|
| `SEC-01` | Official HTTPS Source Allowlist & Row Link Completeness | **PASS** | `61` | Verified 61 HTTPS source links across 21 rings, 5 sellers, 7 karat standards, and 2 live spot feeds against strict official domain allowlist. |
| `SEC-02` | Verbatim Price & Gram-Weight Substring Proof (Anti-Hallucination Check) | **PASS** | `21` | Confirmed all 21 prices and all 5 published gram weights appear verbatim inside archived 2026-10-22 primary listing excerpts. |
| `SEC-03` | Zero-Inference Enforcement (Unverified Values Strictly Left Blank/Null) | **PASS** | `17` | Confirmed 17 items with unconfirmed metal gram weights or mixed-karat splits keep null numeric cells (never inferred) and carry explicit review flags. |
| `SEC-04` | NIST Troy-Ounce (31.1034768 g) & Raw Melt Arithmetic Audit | **PASS** | `11` | Mathematically verified spot conversion ($4,025.10 / 31.1034768 = $129.4100/g), all 7 karat tiers, and all 4 weight-complete rings to <= $0.02 tolerance. |
| `SEC-05` | Automated Irregularity, Plated-Control, BBB & Return-Exclusion Scanner | **PASS** | `67` | Cataloged 67 line-by-line review flags across 21 flagged ring entries for publication on flagged-for-review.html. |
| `SEC-06` | Static HTML Internal/External Link Integrity & Anchor Verification | **PASS** | `2098` | Parsed 24 HTML pages and verified 2098 links, stylesheets, scripts, and anchor targets with zero broken links. |
| `SEC-07` | Front-End Security, No-Hallucinations Top Banner & Zero-External-Script Check | **PASS** | `24` | Verified zero third-party script dependencies, strict rel='noopener noreferrer' on external links, zero eval() calls, and active Front-Page No-Hallucinations Mandate summary. |

## SHA-256 Integrity Digests (`data/*.json`)

| File | SHA-256 Digest |
|---|---|
| `data/bands-and-high-karat.json` | `1aeba52985145d977952b81130bfb7fea13bbc473181dffd21eb398f2fb4b8ba` |
| `data/findings.json` | `4b5355f7da4ee91f3eaae8d04bf508406f6593f287a0bbaced4e623e37e5f636` |
| `data/flags.json` | `fe070ea088abfbd85112b49e3c7f9ab61f693f17a68bde494e0a433ef766f92a` |
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
| `data/reverification-p6.json` | `46f99c832ef98244d5d535ef4389dabc9313f1f92833e11157a3b9a09ec2cae8` |
| `data/rings.json` | `d1f4630a1dff2c442eed0785a6e1b0177db3ebac0c6ed36fe69999f340e11560` |
| `data/sellers-policies.json` | `56fdfb4fc6bb31f747e74e342defb37b9311326c34d60704724abbebe9917d4b` |
| `data/sellers.json` | `9d15afa16eabfce061b559e8d5d97d5023ed66e48078b917b850b31d68789f14` |
| `data/solitaire-rings.json` | `67cc81d443f307e3728c1609c591f63e98f4855d732619bb4b573b5b43c71db4` |
| `data/sources.json` | `2e206f7ca3146203e98afe282557e7bfdab96f37f87d169ad397f5e4d2ef2852` |
| `data/spot-and-standards.json` | `58902c71386b14704c28a9e15c23f05db8f4feb08692a44ce6ff0fd5dd0378f5` |
| `data/standards.json` | `6b745302667c70fb15800fb830471250551a37e238e507a8b993f8e3c4423ad8` |
| `data/verification-report.json` | `fc9537e41c19232159ba0aa49a1632130dfb11d5b6ab4e4de0d4e48feb5763d0` |
| `data/verification.json` | `3381a3e09e20934ef529234f691cebdfc9f66215d633bf0e964d4549f67bf5ff` |
