# GOLD3 — Anti-Hallucination & Security Verification Report

- **Latest Audit Pass:** Pass #20 — `Pass P6 Full Multi-Chunk & Manifest Audit`
- **Timestamp (UTC):** `2026-10-23T10:34:07Z`
- **Overall Result:** **PASS** (`0` integrity errors)
- **Unique Official HTTPS URLs Verified:** `169`
- **Catalog Entries Audited:** `21` rings + `5` sellers + `7` karat standards
- **Items Published on Flagged for Review (`flagged-for-review.html`):** `21` entries (`50` specific findings)

> **Mandatory Post-Review Recommendation:** Run `python3 scripts/run_security_audit.py --pass-label "Manual Review Check"` after every review pass and actively look for price drift, omitted weights, or hallucinations against the official links below.

## Latest Pass Check Breakdown

| Check ID | Check Name | Status | Count | Summary |
|---|---|---|---|---|
| `SEC-01` | Official HTTPS Source Allowlist & Row Link Completeness | **PASS** | `61` | Verified 61 HTTPS source links across 21 rings, 5 sellers, 7 karat standards, and 2 live spot feeds against strict official domain allowlist. |
| `SEC-02` | Verbatim Price & Gram-Weight Substring Proof (Anti-Hallucination Check) | **PASS** | `21` | Confirmed all 21 prices and all 5 published gram weights appear verbatim inside archived 2026-10-22 primary listing excerpts. |
| `SEC-03` | Zero-Inference Enforcement (Unverified Values Strictly Left Blank/Null) | **PASS** | `17` | Confirmed 17 items with unconfirmed metal gram weights or mixed-karat splits keep null numeric cells (never inferred) and carry explicit review flags. |
| `SEC-04` | NIST Troy-Ounce (31.1034768 g) & Raw Melt Arithmetic Audit | **PASS** | `11` | Mathematically verified spot conversion ($4,025.10 / 31.1034768 = $129.4100/g), all 7 karat tiers, and all 4 weight-complete rings to <= $0.02 tolerance. |
| `SEC-05` | Automated Irregularity, Plated-Control, BBB & Return-Exclusion Scanner | **PASS** | `50` | Cataloged 50 line-by-line review flags across 21 flagged ring entries for publication on flagged-for-review.html. |
| `SEC-06` | Static HTML Internal/External Link Integrity & Anchor Verification | **PASS** | `2066` | Parsed 24 HTML pages and verified 2066 links, stylesheets, scripts, and anchor targets with zero broken links. |
| `SEC-07` | Front-End Security, No-Hallucinations Top Banner & Zero-External-Script Check | **PASS** | `24` | Verified zero third-party script dependencies, strict rel='noopener noreferrer' on external links, zero eval() calls, and active Front-Page No-Hallucinations Mandate summary. |

## SHA-256 Integrity Digests (`data/*.json`)

| File | SHA-256 Digest |
|---|---|
| `data/bands-and-high-karat.json` | `c421e2497f9c42980798258f5d067aa4dcf9944519105f1f20598068a60f1641` |
| `data/findings.json` | `450ceed5cae30ea506e7a3cb840c03ea38799d07498b75796c602eb48bf281c4` |
| `data/flags.json` | `5f6c8dd215946bf138b325d3bc4de00c63d1a4a75b1153d02861b0e2fb829ebe` |
| `data/gold-price.json` | `bdb3a741c6696f56ec713c090706cb98fefb53901fe284dfe105308a7d6a7e08` |
| `data/prices.json` | `639b30ebe844d1e7740046c0c1aa474117ab0a34d14df6077be23ca532226f0a` |
| `data/products.json` | `d889b4262ba4dbb4e6bb56a3baa1d51bb3d74da0a3e2de28174df21456fe2e31` |
| `data/retailers.json` | `4cefa585b777b303ec98910ceaab98ebe8621cc62f16e0096f268edddd7700e9` |
| `data/reverification-c-6ccbc523.json` | `52f4a6d610762be546e45e94fd1ffe2f17f201d16215625264fe45c84acc78f2` |
| `data/reverification-p3.json` | `b1dca1669099d66e45b08588f8827b24f59edd65e4f4b4a806ef2a02987b5d16` |
| `data/reverification-p4.json` | `2e5ce8fdff92d04a3e1570960caf0bb1daafc91b2d76209a97a0fb94635e801a` |
| `data/reverification-p5.json` | `1c5ba33b93efdaa14d423fff0be8ca20622f4436d900bc6208ee44e64158bdda` |
| `data/reverification-p6.json` | `dee30027715ce1f89f414ab0bff0140b3684ba009e6b7f1fa3fc3f7322a7b62e` |
| `data/rings.json` | `63f27efe4afdcc101df7eff75768944a027f06e073a160157576128872701f82` |
| `data/sellers-policies.json` | `47610080c25407b04f47756cff62e1cf6ded67c54166ad3d2f8d04dcb5787b73` |
| `data/sellers.json` | `442359af49d66993a1ba67c4f6a35f95b5a7332e65380e167fbd8c2a50b1669d` |
| `data/solitaire-rings.json` | `d4d429ea423ff34090ccb54b27bbcc47530a8382db198b3f6433ad7820d13829` |
| `data/sources.json` | `e59992bc2419cc8e9bed56c64b49c8ae91394ec5c8bbdf78881320caaf2fa77b` |
| `data/spot-and-standards.json` | `25540d8e0c216fc68fb024546ba80e208c7be137acbc04c65900b0c767a8cdc8` |
| `data/standards.json` | `6b745302667c70fb15800fb830471250551a37e238e507a8b993f8e3c4423ad8` |
| `data/verification-report.json` | `ab053bd8a180d423d3673aa415ed1b5afe1eef0c9646c3bc198ed5a444d0cd17` |
| `data/verification.json` | `7e3b42e377e05853713a275ec8be227affb9794cce5ecb787ad6d93427741926` |
