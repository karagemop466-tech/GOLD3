# GOLD3 — Anti-Hallucination & Security Verification Report

- **Latest Audit Pass:** Pass #49 — `Pass P23/P24 live 2026-11-11 integration (arena/673783c8-gold3)`
- **Timestamp (UTC):** `2026-11-11T08:24:08Z`
- **Overall Result:** **PASS** (`0` integrity errors)
- **Unique Official HTTPS URLs Verified:** `191`
- **Catalog Entries Audited:** `21` rings + `5` sellers + `7` karat standards
- **Items Published on Flagged for Review (`flagged-for-review.html`):** `21` entries (`69` specific findings)

> **Mandatory Post-Review Recommendation:** Run `python3 scripts/run_security_audit.py --pass-label "Manual Review Check"` after every review pass and actively look for price drift, omitted weights, or hallucinations against the official links below.

## Latest Pass Check Breakdown

| Check ID | Check Name | Status | Count | Summary |
|---|---|---|---|---|
| `SEC-01` | Official HTTPS Source Allowlist & Row Link Completeness | **PASS** | `61` | Verified 61 HTTPS source links across 21 rings, 5 sellers, 7 karat standards, and 2 live spot feeds against strict official domain allowlist. |
| `SEC-02` | Verbatim Price & Gram-Weight Substring Proof (Anti-Hallucination Check) | **PASS** | `21` | Confirmed all 21 prices and all 5 published gram weights appear verbatim inside archived 2026-10-22 primary listing excerpts. |
| `SEC-03` | Zero-Inference Enforcement (Unverified Values Strictly Left Blank/Null) | **PASS** | `17` | Confirmed 17 items with unconfirmed metal gram weights or mixed-karat splits keep null numeric cells (never inferred) and carry explicit review flags. |
| `SEC-04` | NIST Troy-Ounce (31.1034768 g) & Raw Melt Arithmetic Audit | **PASS** | `11` | Mathematically verified spot conversion ($4,022.70 / 31.1034768 = $129.3328/g), all 7 karat tiers, and all 4 weight-complete rings to <= $0.02 tolerance. |
| `SEC-05` | Automated Irregularity, Plated-Control, BBB & Return-Exclusion Scanner | **PASS** | `69` | Cataloged 69 line-by-line review flags across 21 flagged ring entries for publication on flagged-for-review.html. |
| `SEC-06` | Static HTML Internal/External Link Integrity & Anchor Verification | **PASS** | `3470` | Parsed 25 HTML pages and verified 3470 links, stylesheets, scripts, and anchor targets with zero broken links. |
| `SEC-07` | Front-End Security, No-Hallucinations Top Banner & Zero-External-Script Check | **PASS** | `25` | Verified zero third-party script dependencies, strict rel='noopener noreferrer' on external links, zero eval() calls, and active Front-Page No-Hallucinations Mandate summary. |

## SHA-256 Integrity Digests (`data/*.json`)

| File | SHA-256 Digest |
|---|---|
| `data/bands-and-high-karat.json` | `fd6937fcdc6785958f20a52112d1dc1e0eac8032f8e60a3f81842172a9d4b4dd` |
| `data/findings.json` | `238e7a6ec008b9a47e0c0d438559a114192b906c86c2130dcb297f2755c4aaea` |
| `data/flags.json` | `b119d88253b6157652e618b972310acd353ae3392ebfbdda68a22dfaa28a4887` |
| `data/gold-price.json` | `bdb3a741c6696f56ec713c090706cb98fefb53901fe284dfe105308a7d6a7e08` |
| `data/prices.json` | `afddc25bfc0df2fa87ac7ef71d038bd49c10e48cd903ba263da0df092e97919a` |
| `data/products.json` | `baf5ea1095b53e202c1b76dff7469ea9e738f23a1c3c6cf71926be05c026a4ac` |
| `data/requirements-matrix.json` | `6c51cdcae9cc4b6c6af37ccd7c3c5fd4bfc75779193c1741ff0122351769efd6` |
| `data/retailers.json` | `64e46e6a236176f7752e9050ee58099a9bedd542b893af3fac7f88a1ac9f6913` |
| `data/reverification-1162b2db.json` | `803157bd7daddc10ea8ab4773c5ee1df1b5573c259c53c18c74c025263cea4b3` |
| `data/reverification-57724486.json` | `8b185580a5ef8bafa536151f721d3cb516e66926f02762af704284b9c3e2e2f3` |
| `data/reverification-673783c8.json` | `a57251faeeb67c0c23a46eecc6ca367468d91543aae20862f701aff6bc319c6a` |
| `data/reverification-bfcd8465.json` | `46f99c832ef98244d5d535ef4389dabc9313f1f92833e11157a3b9a09ec2cae8` |
| `data/reverification-c-15b00e99.json` | `34ac65f9dc2ee5d078b5a4a7128eb41fd2e7316efbd4e5d125ebe71b0b946332` |
| `data/reverification-c-6ccbc523.json` | `a807951064276cd1fd9010379082733243c39cbf75a542d52e5e74bd0e64386d` |
| `data/reverification-dataset-c.json` | `2f35e1bb80f76cbc360f51dc2fec996c407f96fdd192b6386f33ad5cf4635e5c` |
| `data/reverification-fb7e5e3c.json` | `5b0dfdc516c0cd958d8d600ae85a28d7ad46e73aa743335110b4d1e60f3c792a` |
| `data/reverification-p15.json` | `ed96531e5576f223a77187091275b945ca35c9c5e1dbb9429d97b7973cbc7b6e` |
| `data/reverification-p17.json` | `14e3160dc5fe245c694c5099550cd65a4d638d28f30bf4c23d744f0c9b375b9d` |
| `data/reverification-p17b.json` | `a2002e248403d51cb69b44b87c653b739f7dd6e209a31662489d322829100c48` |
| `data/reverification-p19.json` | `6878cb48508e91c3594fdf5411b23e076a1132a97ab75ae84a8cef89a81369ef` |
| `data/reverification-p21.json` | `fa03e9722cc65780757ed97f5a17fcffb63c96ef376278cb3cd71021a1615e81` |
| `data/reverification-p3.json` | `b1dca1669099d66e45b08588f8827b24f59edd65e4f4b4a806ef2a02987b5d16` |
| `data/reverification-p4.json` | `2e5ce8fdff92d04a3e1570960caf0bb1daafc91b2d76209a97a0fb94635e801a` |
| `data/reverification-p5.json` | `1c5ba33b93efdaa14d423fff0be8ca20622f4436d900bc6208ee44e64158bdda` |
| `data/reverification-p6.json` | `dee30027715ce1f89f414ab0bff0140b3684ba009e6b7f1fa3fc3f7322a7b62e` |
| `data/rings.json` | `6fceff7a8f57f66902f1a4b32164bfa93d72c7da5daabbee43bab8d59b7a5878` |
| `data/sellers-policies.json` | `bec0a673f9c901c4f393f21357d4a7e680da5ffadd667154e1bac9adef45f42f` |
| `data/sellers.json` | `9697ad84350a3d1255abebda2449373e738132e95b931ea1a98ddd136edb1806` |
| `data/solitaire-rings.json` | `bfb12ed71ed67bda446c43d310de2eb4cb85bf59022666ab5c949d856be68c27` |
| `data/sources.json` | `c92eee0fdd18d5d3dd80a3743dddac78e7b8ca6570f3789ce1acd8393f0b929b` |
| `data/spot-and-standards.json` | `ffe8847481412325ddeb0e67d22afb03de43718579ed36f2b8b3a51d173aecdf` |
| `data/standards.json` | `6b745302667c70fb15800fb830471250551a37e238e507a8b993f8e3c4423ad8` |
| `data/verification-report.json` | `d449713d9426c8459e2f0dc4647ec698a62930097847c4f574f8166da6b6ffbf` |
| `data/verification.json` | `bfa8244572cf556bdf0640243793bb5f51f30319fe4667a9952bff55693eb44a` |
