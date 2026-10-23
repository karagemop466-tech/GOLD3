# GOLD3 — Anti-Hallucination & Security Verification Report

- **Latest Audit Pass:** Pass #16 — `Pass C Re-Verification & Anti-Hallucination Sweep (2026-10-23)`
- **Timestamp (UTC):** `2026-10-23T10:16:48Z`
- **Overall Result:** **PASS** (`0` integrity errors)
- **Unique Official HTTPS URLs Verified:** `171`
- **Catalog Entries Audited:** `21` rings + `5` sellers + `7` karat standards
- **Items Published on Flagged for Review (`flagged-for-review.html`):** `17` entries (`40` specific findings)

> **Mandatory Post-Review Recommendation:** Run `python3 scripts/run_security_audit.py --pass-label "Manual Review Check"` after every review pass and actively look for price drift, omitted weights, or hallucinations against the official links below.

## Latest Pass Check Breakdown

| Check ID | Check Name | Status | Count | Summary |
|---|---|---|---|---|
| `SEC-01` | Official HTTPS Source Allowlist & Row Link Completeness | **PASS** | `61` | Verified 61 HTTPS source links across 21 rings, 5 sellers, 7 karat standards, and 2 live spot feeds against strict official domain allowlist. |
| `SEC-02` | Verbatim Price & Gram-Weight Substring Proof (Anti-Hallucination Check) | **PASS** | `21` | Confirmed all 21 prices and all 5 published gram weights appear verbatim inside archived 2026-10-22 primary listing excerpts. |
| `SEC-03` | Zero-Inference Enforcement (Unverified Values Strictly Left Blank/Null) | **PASS** | `17` | Confirmed 17 items with unconfirmed metal gram weights or mixed-karat splits keep null numeric cells (never inferred) and carry explicit review flags. |
| `SEC-04` | NIST Troy-Ounce (31.1034768 g) & Raw Melt Arithmetic Audit | **PASS** | `11` | Mathematically verified spot conversion ($4,025.10 / 31.1034768 = $129.4100/g), all 7 karat tiers, and all 4 weight-complete rings to <= $0.02 tolerance. |
| `SEC-05` | Automated Irregularity, Plated-Control, BBB & Return-Exclusion Scanner | **PASS** | `40` | Cataloged 40 line-by-line review flags across 17 flagged ring entries for publication on flagged-for-review.html. |
| `SEC-06` | Static HTML Internal/External Link Integrity & Anchor Verification | **PASS** | `1898` | Parsed 24 HTML pages and verified 1898 links, stylesheets, scripts, and anchor targets with zero broken links. |
| `SEC-07` | Front-End Security, No-Hallucinations Top Banner & Zero-External-Script Check | **PASS** | `24` | Verified zero third-party script dependencies, strict rel='noopener noreferrer' on external links, zero eval() calls, and active Front-Page No-Hallucinations Mandate summary. |

## SHA-256 Integrity Digests (`data/*.json`)

| File | SHA-256 Digest |
|---|---|
| `data/bands-and-high-karat.json` | `468c7359744b8f5bd7c51d298c8563f5808a482a5219754a17276b762046d5c2` |
| `data/findings.json` | `f09121b80be71c0ea36574a57147452511035b52968060ebe9d08407ceb1389e` |
| `data/flags.json` | `6a588c9a3c76af47044f8d6de0e44bdcd5c48299723df651a5dc6b41f0e9763d` |
| `data/gold-price.json` | `bdb3a741c6696f56ec713c090706cb98fefb53901fe284dfe105308a7d6a7e08` |
| `data/prices.json` | `639b30ebe844d1e7740046c0c1aa474117ab0a34d14df6077be23ca532226f0a` |
| `data/products.json` | `bac54f10685ad44ec13e3af7118d2e175ce1f67b71bcfe90325580a67ec073f3` |
| `data/retailers.json` | `4cefa585b777b303ec98910ceaab98ebe8621cc62f16e0096f268edddd7700e9` |
| `data/reverification-c-6ccbc523.json` | `52f4a6d610762be546e45e94fd1ffe2f17f201d16215625264fe45c84acc78f2` |
| `data/reverification-p3.json` | `b1dca1669099d66e45b08588f8827b24f59edd65e4f4b4a806ef2a02987b5d16` |
| `data/rings.json` | `238cf2fa864fd91c8e2a2ea90ba6d6a71bdd739704ef31609f533b23b1337b41` |
| `data/sellers-policies.json` | `b035da051fc01076295ea9ef95b5a2cedcefaea431b8966810ab4fccb167d503` |
| `data/sellers.json` | `4754237cf4aeda1d27c072d8f7a518230279b675c7fdc4b1cd9e505e828614a4` |
| `data/solitaire-rings.json` | `43f014b01ffb974e7c628eb8090fb0760149bee5dd791c2fa6e5405395cd3fb7` |
| `data/sources.json` | `1496e3741397057c11913b06d748bf838b6781b5686e7ab733d3ac5e76a49f41` |
| `data/spot-and-standards.json` | `25540d8e0c216fc68fb024546ba80e208c7be137acbc04c65900b0c767a8cdc8` |
| `data/standards.json` | `7d10a2520465c2b2734d236d9dfe93e4db44bc5d0649cb6cf82bb35cc94b668c` |
| `data/verification-report.json` | `84bbfb16f28043a82c2b221afe2cefde01abc7ceab4540ee53bc37809721cb45` |
| `data/verification.json` | `25db638f8498645c22831bd8a2275179ce34ea80b0ad8987553f8f714c7c1181` |
