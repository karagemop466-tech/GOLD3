# GOLD3 — Anti-Hallucination & Security Verification Report

- **Latest Audit Pass:** Pass #31 — `Pass P14 final integration`
- **Timestamp (UTC):** `2026-10-23T20:28:55Z`
- **Overall Result:** **PASS** (`0` integrity errors)
- **Unique Official HTTPS URLs Verified:** `180`
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
| `SEC-06` | Static HTML Internal/External Link Integrity & Anchor Verification | **PASS** | `2328` | Parsed 24 HTML pages and verified 2328 links, stylesheets, scripts, and anchor targets with zero broken links. |
| `SEC-07` | Front-End Security, No-Hallucinations Top Banner & Zero-External-Script Check | **PASS** | `24` | Verified zero third-party script dependencies, strict rel='noopener noreferrer' on external links, zero eval() calls, and active Front-Page No-Hallucinations Mandate summary. |

## SHA-256 Integrity Digests (`data/*.json`)

| File | SHA-256 Digest |
|---|---|
| `data/bands-and-high-karat.json` | `8061e893bb6b94c3886cb8d5dca41ed8260f75506ca140e5f06440fd27d3a99e` |
| `data/findings.json` | `4ef211019dfd301ad7d451d026f468d6e2364cb31ec0cecf04dc175e26044be0` |
| `data/flags.json` | `36f7e0a0f1672b7dc84bf4165f3bb43c73e716a7ea7d05a0d3d204ecc8dc5c0b` |
| `data/gold-price.json` | `bdb3a741c6696f56ec713c090706cb98fefb53901fe284dfe105308a7d6a7e08` |
| `data/prices.json` | `accd2ecb513d2ea1a956d762eb2119b722e8fe6cf15dd42dff4df227e980262f` |
| `data/products.json` | `b710535c3310aded606c436d9207276ac91c399d879522aa4861c7c751ef7194` |
| `data/retailers.json` | `e780a16102e4278cd4c8803871c50f2527bb7a73baa5db24ead1558e5e5d50e8` |
| `data/reverification-1162b2db.json` | `803157bd7daddc10ea8ab4773c5ee1df1b5573c259c53c18c74c025263cea4b3` |
| `data/reverification-57724486.json` | `8b185580a5ef8bafa536151f721d3cb516e66926f02762af704284b9c3e2e2f3` |
| `data/reverification-bfcd8465.json` | `46f99c832ef98244d5d535ef4389dabc9313f1f92833e11157a3b9a09ec2cae8` |
| `data/reverification-c-15b00e99.json` | `34ac65f9dc2ee5d078b5a4a7128eb41fd2e7316efbd4e5d125ebe71b0b946332` |
| `data/reverification-c-6ccbc523.json` | `52f4a6d610762be546e45e94fd1ffe2f17f201d16215625264fe45c84acc78f2` |
| `data/reverification-dataset-c.json` | `2f35e1bb80f76cbc360f51dc2fec996c407f96fdd192b6386f33ad5cf4635e5c` |
| `data/reverification-fb7e5e3c.json` | `5b0dfdc516c0cd958d8d600ae85a28d7ad46e73aa743335110b4d1e60f3c792a` |
| `data/reverification-p3.json` | `b1dca1669099d66e45b08588f8827b24f59edd65e4f4b4a806ef2a02987b5d16` |
| `data/reverification-p4.json` | `2e5ce8fdff92d04a3e1570960caf0bb1daafc91b2d76209a97a0fb94635e801a` |
| `data/reverification-p5.json` | `1c5ba33b93efdaa14d423fff0be8ca20622f4436d900bc6208ee44e64158bdda` |
| `data/reverification-p6.json` | `dee30027715ce1f89f414ab0bff0140b3684ba009e6b7f1fa3fc3f7322a7b62e` |
| `data/rings.json` | `0d68ca150089fc6ed7a93f54f8f2a901197f3ec6c8d98bf6bca8d56e132529da` |
| `data/sellers-policies.json` | `6f2edb268c1efd391f4c98102d164665d40d1b2f56cc18702c4492bad6b8cd36` |
| `data/sellers.json` | `4d1bd09620f904e833139fa16f7be571e87ade0115df1826472447e324bc033f` |
| `data/solitaire-rings.json` | `b14736e9308d559ca542081e0b9dda7b325588b6558486aa288d27753ef5b8d8` |
| `data/sources.json` | `6a5c601691169659a560ff01172bbcbccf1523884f86b20f057cea26f8ef797d` |
| `data/spot-and-standards.json` | `fb7febce8b15501221a57f89e4f244635d645ac122963315373bc0137f39a171` |
| `data/standards.json` | `6b745302667c70fb15800fb830471250551a37e238e507a8b993f8e3c4423ad8` |
| `data/verification-report.json` | `732a7f0c45f805c0200d958fcc38a0adaa83a556f4c97797b8fa4337162cdf50` |
| `data/verification.json` | `74d6c1e06c05e5bcc96984096855c07b66253a168385e2d1d137cec6eed606e8` |
