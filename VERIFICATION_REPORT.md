# GOLD3 — Anti-Hallucination & Security Verification Report

- **Latest Audit Pass:** Pass #20 — `Pass P6 (V10 + T16) post-PR-#39 additive integration`
- **Timestamp (UTC):** `2026-10-23T10:34:11Z`
- **Overall Result:** **PASS** (`0` integrity errors)
- **Unique Official HTTPS URLs Verified:** `186`
- **Catalog Entries Audited:** `21` rings + `5` sellers + `7` karat standards
- **Items Published on Flagged for Review (`flagged-for-review.html`):** `21` entries (`54` specific findings)

> **Mandatory Post-Review Recommendation:** Run `python3 scripts/run_security_audit.py --pass-label "Manual Review Check"` after every review pass and actively look for price drift, omitted weights, or hallucinations against the official links below.

## Latest Pass Check Breakdown

| Check ID | Check Name | Status | Count | Summary |
|---|---|---|---|---|
| `SEC-01` | Official HTTPS Source Allowlist & Row Link Completeness | **PASS** | `61` | Verified 61 HTTPS source links across 21 rings, 5 sellers, 7 karat standards, and 2 live spot feeds against strict official domain allowlist. |
| `SEC-02` | Verbatim Price & Gram-Weight Substring Proof (Anti-Hallucination Check) | **PASS** | `21` | Confirmed all 21 prices and all 5 published gram weights appear verbatim inside archived 2026-10-22 primary listing excerpts. |
| `SEC-03` | Zero-Inference Enforcement (Unverified Values Strictly Left Blank/Null) | **PASS** | `17` | Confirmed 17 items with unconfirmed metal gram weights or mixed-karat splits keep null numeric cells (never inferred) and carry explicit review flags. |
| `SEC-04` | NIST Troy-Ounce (31.1034768 g) & Raw Melt Arithmetic Audit | **PASS** | `11` | Mathematically verified spot conversion ($4,025.10 / 31.1034768 = $129.4100/g), all 7 karat tiers, and all 4 weight-complete rings to <= $0.02 tolerance. |
| `SEC-05` | Automated Irregularity, Plated-Control, BBB & Return-Exclusion Scanner | **PASS** | `54` | Cataloged 54 line-by-line review flags across 21 flagged ring entries for publication on flagged-for-review.html. |
| `SEC-06` | Static HTML Internal/External Link Integrity & Anchor Verification | **PASS** | `2078` | Parsed 24 HTML pages and verified 2078 links, stylesheets, scripts, and anchor targets with zero broken links. |
| `SEC-07` | Front-End Security, No-Hallucinations Top Banner & Zero-External-Script Check | **PASS** | `24` | Verified zero third-party script dependencies, strict rel='noopener noreferrer' on external links, zero eval() calls, and active Front-Page No-Hallucinations Mandate summary. |

## SHA-256 Integrity Digests (`data/*.json`)

| File | SHA-256 Digest |
|---|---|
| `data/bands-and-high-karat.json` | `e85e883faee88d0618c3710f16d191e4565f1408cf95a8db38c5c5ad0ed16f68` |
| `data/findings.json` | `f6978136820d8021d2818c5630cc88bb2360c98382c3aa062a0e1c9ca731f882` |
| `data/flags.json` | `daa2269c1766e152e79bdd15cae2733ae228fc9fb6ab18c2c3eccfecd3318ffc` |
| `data/gold-price.json` | `bdb3a741c6696f56ec713c090706cb98fefb53901fe284dfe105308a7d6a7e08` |
| `data/prices.json` | `639b30ebe844d1e7740046c0c1aa474117ab0a34d14df6077be23ca532226f0a` |
| `data/products.json` | `d4c36640860f639be29f18c6fe5c601389eb736ed8e1df2c1ae6cdeaa7a8efe7` |
| `data/retailers.json` | `4cefa585b777b303ec98910ceaab98ebe8621cc62f16e0096f268edddd7700e9` |
| `data/reverification-c-6ccbc523.json` | `52f4a6d610762be546e45e94fd1ffe2f17f201d16215625264fe45c84acc78f2` |
| `data/reverification-p3.json` | `b1dca1669099d66e45b08588f8827b24f59edd65e4f4b4a806ef2a02987b5d16` |
| `data/reverification-p4.json` | `2e5ce8fdff92d04a3e1570960caf0bb1daafc91b2d76209a97a0fb94635e801a` |
| `data/reverification-p5.json` | `1c5ba33b93efdaa14d423fff0be8ca20622f4436d900bc6208ee44e64158bdda` |
| `data/reverification-p6.json` | `46f99c832ef98244d5d535ef4389dabc9313f1f92833e11157a3b9a09ec2cae8` |
| `data/rings.json` | `09386daf132d124d5b676c2b3f0cff28d9c891deb98b8cf8694fafc1c488b399` |
| `data/sellers-policies.json` | `b035da051fc01076295ea9ef95b5a2cedcefaea431b8966810ab4fccb167d503` |
| `data/sellers.json` | `74d0ecc8bf1d96752f867c15817a69920138e92f4cd584652fe774f35d6cf5ec` |
| `data/solitaire-rings.json` | `43f014b01ffb974e7c628eb8090fb0760149bee5dd791c2fa6e5405395cd3fb7` |
| `data/sources.json` | `2e206f7ca3146203e98afe282557e7bfdab96f37f87d169ad397f5e4d2ef2852` |
| `data/spot-and-standards.json` | `25540d8e0c216fc68fb024546ba80e208c7be137acbc04c65900b0c767a8cdc8` |
| `data/standards.json` | `6b745302667c70fb15800fb830471250551a37e238e507a8b993f8e3c4423ad8` |
| `data/verification-report.json` | `35dc79ecb8d44e19827139d22d9725ac9a3b32ca10a1a68f535bf2cac318c91f` |
| `data/verification.json` | `62c107c42213ad4ee20b7c90c925e7ad8b06078393dc99c36b8d29b4c40ef29f` |
