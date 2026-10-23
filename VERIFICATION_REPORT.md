# GOLD3 — Anti-Hallucination & Security Verification Report

- **Latest Audit Pass:** Pass #20 — `Pass P6 (V10 + T16) final pre-PR verification`
- **Timestamp (UTC):** `2026-10-23T10:30:26Z`
- **Overall Result:** **PASS** (`0` integrity errors)
- **Unique Official HTTPS URLs Verified:** `180`
- **Catalog Entries Audited:** `21` rings + `5` sellers + `7` karat standards
- **Items Published on Flagged for Review (`flagged-for-review.html`):** `21` entries (`53` specific findings)

> **Mandatory Post-Review Recommendation:** Run `python3 scripts/run_security_audit.py --pass-label "Manual Review Check"` after every review pass and actively look for price drift, omitted weights, or hallucinations against the official links below.

## Latest Pass Check Breakdown

| Check ID | Check Name | Status | Count | Summary |
|---|---|---|---|---|
| `SEC-01` | Official HTTPS Source Allowlist & Row Link Completeness | **PASS** | `61` | Verified 61 HTTPS source links across 21 rings, 5 sellers, 7 karat standards, and 2 live spot feeds against strict official domain allowlist. |
| `SEC-02` | Verbatim Price & Gram-Weight Substring Proof (Anti-Hallucination Check) | **PASS** | `21` | Confirmed all 21 prices and all 8 published gram weights appear verbatim inside archived 2026-10-22 primary listing excerpts. |
| `SEC-03` | Zero-Inference Enforcement (Unverified Values Strictly Left Blank/Null) | **PASS** | `14` | Confirmed 14 items with unconfirmed metal gram weights or mixed-karat splits keep null numeric cells (never inferred) and carry explicit review flags. |
| `SEC-04` | NIST Troy-Ounce (31.1034768 g) & Raw Melt Arithmetic Audit | **PASS** | `14` | Mathematically verified spot conversion ($4,025.10 / 31.1034768 = $129.4100/g), all 7 karat tiers, and all 7 weight-complete rings to <= $0.02 tolerance. |
| `SEC-05` | Automated Irregularity, Plated-Control, BBB & Return-Exclusion Scanner | **PASS** | `53` | Cataloged 53 line-by-line review flags across 21 flagged ring entries for publication on flagged-for-review.html. |
| `SEC-06` | Static HTML Internal/External Link Integrity & Anchor Verification | **PASS** | `2076` | Parsed 24 HTML pages and verified 2076 links, stylesheets, scripts, and anchor targets with zero broken links. |
| `SEC-07` | Front-End Security, No-Hallucinations Top Banner & Zero-External-Script Check | **PASS** | `24` | Verified zero third-party script dependencies, strict rel='noopener noreferrer' on external links, zero eval() calls, and active Front-Page No-Hallucinations Mandate summary. |

## SHA-256 Integrity Digests (`data/*.json`)

| File | SHA-256 Digest |
|---|---|
| `data/bands-and-high-karat.json` | `b07beb61da3f406ff14f8074964605f44924e0d7015c980316250bb3f4a54a1a` |
| `data/findings.json` | `85dfc1dd390215b1da1c3a85eb699e343fd7581d866e8c55cec0061426356e85` |
| `data/flags.json` | `daa2269c1766e152e79bdd15cae2733ae228fc9fb6ab18c2c3eccfecd3318ffc` |
| `data/gold-price.json` | `bdb3a741c6696f56ec713c090706cb98fefb53901fe284dfe105308a7d6a7e08` |
| `data/prices.json` | `639b30ebe844d1e7740046c0c1aa474117ab0a34d14df6077be23ca532226f0a` |
| `data/products.json` | `d4c36640860f639be29f18c6fe5c601389eb736ed8e1df2c1ae6cdeaa7a8efe7` |
| `data/retailers.json` | `fc2130447e547458e380d666c0b6598352464a2dedffbd8d0aefc7ce7ffabab3` |
| `data/reverification-p3.json` | `b1dca1669099d66e45b08588f8827b24f59edd65e4f4b4a806ef2a02987b5d16` |
| `data/reverification-p4.json` | `2e5ce8fdff92d04a3e1570960caf0bb1daafc91b2d76209a97a0fb94635e801a` |
| `data/reverification-p5.json` | `1c5ba33b93efdaa14d423fff0be8ca20622f4436d900bc6208ee44e64158bdda` |
| `data/reverification-p6.json` | `46f99c832ef98244d5d535ef4389dabc9313f1f92833e11157a3b9a09ec2cae8` |
| `data/rings.json` | `09386daf132d124d5b676c2b3f0cff28d9c891deb98b8cf8694fafc1c488b399` |
| `data/sellers-policies.json` | `372689ba815fb011c15b17e52773385718f972b174023f8bd67e01bc10d27ea6` |
| `data/sellers.json` | `d1c903710413f7406e7f3ced2da0331c50f1ef9f606a764718288083f9b5ab64` |
| `data/solitaire-rings.json` | `1f24aa389723b9c395b2f0ed103fe3b5fa60b4b658e5196806370aa06ff6ffaa` |
| `data/sources.json` | `2e206f7ca3146203e98afe282557e7bfdab96f37f87d169ad397f5e4d2ef2852` |
| `data/spot-and-standards.json` | `060e3a9379792d784c93800ca93120d2bb6089d0544ff27cb23114a84230a9f0` |
| `data/standards.json` | `6b745302667c70fb15800fb830471250551a37e238e507a8b993f8e3c4423ad8` |
| `data/verification-report.json` | `e9c5a2e8f2ebf0c6c3e1aa60b21b844f3ed10fe7f92240e7448998a8b7255dfb` |
| `data/verification.json` | `62c107c42213ad4ee20b7c90c925e7ad8b06078393dc99c36b8d29b4c40ef29f` |
