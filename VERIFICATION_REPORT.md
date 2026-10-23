# GOLD3 — Anti-Hallucination & Security Verification Report

- **Latest Audit Pass:** Pass #29 — `Pass P13 (spot promotion)`
- **Timestamp (UTC):** `2026-10-23T20:24:17Z`
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
| `SEC-04` | NIST Troy-Ounce (31.1034768 g) & Raw Melt Arithmetic Audit | **PASS** | `11` | Mathematically verified spot conversion ($3,996.20 / 31.1034768 = $128.4808/g), all 7 karat tiers, and all 4 weight-complete rings to <= $0.02 tolerance. |
| `SEC-05` | Automated Irregularity, Plated-Control, BBB & Return-Exclusion Scanner | **PASS** | `68` | Cataloged 68 line-by-line review flags across 21 flagged ring entries for publication on flagged-for-review.html. |
| `SEC-06` | Static HTML Internal/External Link Integrity & Anchor Verification | **PASS** | `2220` | Parsed 24 HTML pages and verified 2220 links, stylesheets, scripts, and anchor targets with zero broken links. |
| `SEC-07` | Front-End Security, No-Hallucinations Top Banner & Zero-External-Script Check | **PASS** | `24` | Verified zero third-party script dependencies, strict rel='noopener noreferrer' on external links, zero eval() calls, and active Front-Page No-Hallucinations Mandate summary. |

## SHA-256 Integrity Digests (`data/*.json`)

| File | SHA-256 Digest |
|---|---|
| `data/bands-and-high-karat.json` | `29443c551ae1071341d687d2d3b89b14fef1164f03e931a05e359edc793b0a03` |
| `data/findings.json` | `b856d88b67553a2732599f58ced0c961a79ccacbbcbcd263f099afc178725e66` |
| `data/flags.json` | `0cb02371eeb777773cbe3cc1f80a3990642d4c57d55a64fc60b43bd0ab8160da` |
| `data/gold-price.json` | `bb59a47fe878f3df426172a15cd9dd185a0445866dcad0388984d361b3e328df` |
| `data/prices.json` | `e7bb06d360f94d9da0457a0ffd7eda5625c61383e85973373363321e424249ac` |
| `data/products.json` | `fd5ed020fb2571d90ff21a8fc7cf6075923b6f11e4e33666df27025544526b21` |
| `data/retailers.json` | `e780a16102e4278cd4c8803871c50f2527bb7a73baa5db24ead1558e5e5d50e8` |
| `data/reverification-1162b2db.json` | `803157bd7daddc10ea8ab4773c5ee1df1b5573c259c53c18c74c025263cea4b3` |
| `data/reverification-57724486.json` | `8b185580a5ef8bafa536151f721d3cb516e66926f02762af704284b9c3e2e2f3` |
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
| `data/sellers.json` | `4d1bd09620f904e833139fa16f7be571e87ade0115df1826472447e324bc033f` |
| `data/solitaire-rings.json` | `f21c1887b52bae6c0882f7ba8fb8a99341e6d7cb6fdf6f5b412f230f7f2554d0` |
| `data/sources.json` | `6a5c601691169659a560ff01172bbcbccf1523884f86b20f057cea26f8ef797d` |
| `data/spot-and-standards.json` | `5e041d1369fe432ad1b3fb05470fc4fc01c37c8c3208a9dbfa646fd93d2b7bb0` |
| `data/standards.json` | `6b745302667c70fb15800fb830471250551a37e238e507a8b993f8e3c4423ad8` |
| `data/verification-report.json` | `2598a50d4ebfffb61a8817984113d23bfdf25460a0f7be3db31a8b9b33b0be3a` |
| `data/verification.json` | `59507df20e20dc3979b9b1512da8f01f722de8d85ee017a907ff42c35ab9b57b` |
