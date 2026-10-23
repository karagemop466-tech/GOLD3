# GOLD3 — Anti-Hallucination & Security Verification Report

- **Latest Audit Pass:** Pass #29 — `Pass P12 (spot re-anchor)`
- **Timestamp (UTC):** `2026-10-23T20:21:43Z`
- **Overall Result:** **PASS** (`0` integrity errors)
- **Unique Official HTTPS URLs Verified:** `180`
- **Catalog Entries Audited:** `21` rings + `5` sellers + `7` karat standards
- **Items Published on Flagged for Review (`flagged-for-review.html`):** `21` entries (`67` specific findings)

> **Mandatory Post-Review Recommendation:** Run `python3 scripts/run_security_audit.py --pass-label "Manual Review Check"` after every review pass and actively look for price drift, omitted weights, or hallucinations against the official links below.

## Latest Pass Check Breakdown

| Check ID | Check Name | Status | Count | Summary |
|---|---|---|---|---|
| `SEC-01` | Official HTTPS Source Allowlist & Row Link Completeness | **PASS** | `61` | Verified 61 HTTPS source links across 21 rings, 5 sellers, 7 karat standards, and 2 live spot feeds against strict official domain allowlist. |
| `SEC-02` | Verbatim Price & Gram-Weight Substring Proof (Anti-Hallucination Check) | **PASS** | `21` | Confirmed all 21 prices and all 5 published gram weights appear verbatim inside archived 2026-10-22 primary listing excerpts. |
| `SEC-03` | Zero-Inference Enforcement (Unverified Values Strictly Left Blank/Null) | **PASS** | `17` | Confirmed 17 items with unconfirmed metal gram weights or mixed-karat splits keep null numeric cells (never inferred) and carry explicit review flags. |
| `SEC-04` | NIST Troy-Ounce (31.1034768 g) & Raw Melt Arithmetic Audit | **PASS** | `11` | Mathematically verified spot conversion ($3,996.20 / 31.1034768 = $128.4808/g), all 7 karat tiers, and all 4 weight-complete rings to <= $0.02 tolerance. |
| `SEC-05` | Automated Irregularity, Plated-Control, BBB & Return-Exclusion Scanner | **PASS** | `67` | Cataloged 67 line-by-line review flags across 21 flagged ring entries for publication on flagged-for-review.html. |
| `SEC-06` | Static HTML Internal/External Link Integrity & Anchor Verification | **PASS** | `2205` | Parsed 24 HTML pages and verified 2205 links, stylesheets, scripts, and anchor targets with zero broken links. |
| `SEC-07` | Front-End Security, No-Hallucinations Top Banner & Zero-External-Script Check | **PASS** | `24` | Verified zero third-party script dependencies, strict rel='noopener noreferrer' on external links, zero eval() calls, and active Front-Page No-Hallucinations Mandate summary. |

## SHA-256 Integrity Digests (`data/*.json`)

| File | SHA-256 Digest |
|---|---|
| `data/bands-and-high-karat.json` | `f9c7b80ab561f9e8670e89c9fd832329e5e2b5f04503f80e2e3e78f2f7ccec0a` |
| `data/findings.json` | `97be00ae5026c3ec138d1a7b8e5aa83cd565ad277ea30004515eebe0b8fcf3e4` |
| `data/flags.json` | `6c8a96ba8bde89b563a7ee59ff41b05c73ebf6b8dc80084f70794c8cb57d9c8e` |
| `data/gold-price.json` | `f34e812d365b8fcf44eda952c27ccc98cdd59a4e61fd628f2d6c83f0bb01540f` |
| `data/prices.json` | `1e419a05f3ed13816e8f933ceb7bc309c43ce1296e95fa11ed53db4781de5d53` |
| `data/products.json` | `fd5ed020fb2571d90ff21a8fc7cf6075923b6f11e4e33666df27025544526b21` |
| `data/retailers.json` | `e780a16102e4278cd4c8803871c50f2527bb7a73baa5db24ead1558e5e5d50e8` |
| `data/reverification-1162b2db.json` | `803157bd7daddc10ea8ab4773c5ee1df1b5573c259c53c18c74c025263cea4b3` |
| `data/reverification-bfcd8465.json` | `46f99c832ef98244d5d535ef4389dabc9313f1f92833e11157a3b9a09ec2cae8` |
| `data/reverification-c-15b00e99.json` | `34ac65f9dc2ee5d078b5a4a7128eb41fd2e7316efbd4e5d125ebe71b0b946332` |
| `data/reverification-c-6ccbc523.json` | `52f4a6d610762be546e45e94fd1ffe2f17f201d16215625264fe45c84acc78f2` |
| `data/reverification-dataset-c.json` | `2f35e1bb80f76cbc360f51dc2fec996c407f96fdd192b6386f33ad5cf4635e5c` |
| `data/reverification-p3.json` | `b1dca1669099d66e45b08588f8827b24f59edd65e4f4b4a806ef2a02987b5d16` |
| `data/reverification-p4.json` | `2e5ce8fdff92d04a3e1570960caf0bb1daafc91b2d76209a97a0fb94635e801a` |
| `data/reverification-p5.json` | `1c5ba33b93efdaa14d423fff0be8ca20622f4436d900bc6208ee44e64158bdda` |
| `data/reverification-p6.json` | `dee30027715ce1f89f414ab0bff0140b3684ba009e6b7f1fa3fc3f7322a7b62e` |
| `data/rings.json` | `fd36fe00e0d452205a50e623b9311803e07daba21b3ae6e052fd144a252f0fe8` |
| `data/sellers-policies.json` | `6f2edb268c1efd391f4c98102d164665d40d1b2f56cc18702c4492bad6b8cd36` |
| `data/sellers.json` | `469d062f068d98d8293e22bd2257c1144c59f64ce732956cb58afc062e31afea` |
| `data/solitaire-rings.json` | `95da19678cf5bdeccb08a30cdec60aeaf9366efc0c6ba7922e7187bebb7c6e67` |
| `data/sources.json` | `6a5c601691169659a560ff01172bbcbccf1523884f86b20f057cea26f8ef797d` |
| `data/spot-and-standards.json` | `c1a3ca1589ca968176d44682cb676f1bd9f26cbd6fcea05cf7bc5a61b9157a67` |
| `data/standards.json` | `6b745302667c70fb15800fb830471250551a37e238e507a8b993f8e3c4423ad8` |
| `data/verification-report.json` | `d7870b2faca00ecfc1342578419804c148bc5ba6ce00a59533905f1b09d43061` |
| `data/verification.json` | `c09b582f260c080d2caf32ec418493cf35465de1a0300fb9901cb641d3321b33` |
