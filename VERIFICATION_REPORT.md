# GOLD3 — Anti-Hallucination & Security Verification Report

- **Latest Audit Pass:** Pass #15 — `P3 final integration audit (dead citations repointed)`
- **Timestamp (UTC):** `2026-10-23T00:15:08Z`
- **Overall Result:** **PASS** (`0` integrity errors)
- **Unique Official HTTPS URLs Verified:** `164`
- **Catalog Entries Audited:** `21` rings + `5` sellers + `7` karat standards
- **Items Published on Flagged for Review (`flagged-for-review.html`):** `17` entries (`37` specific findings)

> **Mandatory Post-Review Recommendation:** Run `python3 scripts/run_security_audit.py --pass-label "Manual Review Check"` after every review pass and actively look for price drift, omitted weights, or hallucinations against the official links below.

## Latest Pass Check Breakdown

| Check ID | Check Name | Status | Count | Summary |
|---|---|---|---|---|
| `SEC-01` | Official HTTPS Source Allowlist & Row Link Completeness | **PASS** | `61` | Verified 61 HTTPS source links across 21 rings, 5 sellers, 7 karat standards, and 2 live spot feeds against strict official domain allowlist. |
| `SEC-02` | Verbatim Price & Gram-Weight Substring Proof (Anti-Hallucination Check) | **PASS** | `21` | Confirmed all 21 prices and all 8 published gram weights appear verbatim inside archived 2026-10-22 primary listing excerpts. |
| `SEC-03` | Zero-Inference Enforcement (Unverified Values Strictly Left Blank/Null) | **PASS** | `14` | Confirmed 14 items with unconfirmed metal gram weights or mixed-karat splits keep null numeric cells (never inferred) and carry explicit review flags. |
| `SEC-04` | NIST Troy-Ounce (31.1034768 g) & Raw Melt Arithmetic Audit | **PASS** | `14` | Mathematically verified spot conversion ($4,025.10 / 31.1034768 = $129.4100/g), all 7 karat tiers, and all 7 weight-complete rings to <= $0.02 tolerance. |
| `SEC-05` | Automated Irregularity, Plated-Control, BBB & Return-Exclusion Scanner | **PASS** | `37` | Cataloged 37 line-by-line review flags across 17 flagged ring entries for publication on flagged-for-review.html. |
| `SEC-06` | Static HTML Internal/External Link Integrity & Anchor Verification | **PASS** | `1892` | Parsed 24 HTML pages and verified 1892 links, stylesheets, scripts, and anchor targets with zero broken links. |
| `SEC-07` | Front-End Security, No-Hallucinations Top Banner & Zero-External-Script Check | **PASS** | `24` | Verified zero third-party script dependencies, strict rel='noopener noreferrer' on external links, zero eval() calls, and active Front-Page No-Hallucinations Mandate summary. |

## SHA-256 Integrity Digests (`data/*.json`)

| File | SHA-256 Digest |
|---|---|
| `data/bands-and-high-karat.json` | `fd6b7c175980cfad74b34145c03e2632e809c6a94de48ef399b96c55d8ea333c` |
| `data/findings.json` | `ab9bc570436602ab1166ad274e53a3b80dd1cb3c1b691cd1758e90950fb54873` |
| `data/flags.json` | `6a588c9a3c76af47044f8d6de0e44bdcd5c48299723df651a5dc6b41f0e9763d` |
| `data/gold-price.json` | `bdb3a741c6696f56ec713c090706cb98fefb53901fe284dfe105308a7d6a7e08` |
| `data/prices.json` | `639b30ebe844d1e7740046c0c1aa474117ab0a34d14df6077be23ca532226f0a` |
| `data/products.json` | `bac54f10685ad44ec13e3af7118d2e175ce1f67b71bcfe90325580a67ec073f3` |
| `data/retailers.json` | `fc2130447e547458e380d666c0b6598352464a2dedffbd8d0aefc7ce7ffabab3` |
| `data/reverification-p3.json` | `605b62ab0bd0f220f2fe2c7c88d282f8305a58525f43bec643b9c557b123019b` |
| `data/rings.json` | `238cf2fa864fd91c8e2a2ea90ba6d6a71bdd739704ef31609f533b23b1337b41` |
| `data/sellers-policies.json` | `372689ba815fb011c15b17e52773385718f972b174023f8bd67e01bc10d27ea6` |
| `data/sellers.json` | `4754237cf4aeda1d27c072d8f7a518230279b675c7fdc4b1cd9e505e828614a4` |
| `data/solitaire-rings.json` | `1b0d493a2835471df5bf8610622bf2f668a0c2d62e7961c112d46591ae19f769` |
| `data/sources.json` | `1496e3741397057c11913b06d748bf838b6781b5686e7ab733d3ac5e76a49f41` |
| `data/spot-and-standards.json` | `77a3ff10db7fe885bc1f51eece4311fa6a62034f73ce2292d2e4bf1841b9a5ed` |
| `data/standards.json` | `7d10a2520465c2b2734d236d9dfe93e4db44bc5d0649cb6cf82bb35cc94b668c` |
| `data/verification-report.json` | `a58a48d836389be639184621d736fc01e4cf527e7e80a34f9e3c43ddd056282e` |
| `data/verification.json` | `25db638f8498645c22831bd8a2275179ce34ea80b0ad8987553f8f714c7c1181` |
