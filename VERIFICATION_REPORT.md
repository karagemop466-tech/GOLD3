# GOLD3 — Anti-Hallucination & Security Verification Report

- **Latest Audit Pass:** Pass #45 — `Pass P19 closeout`
- **Timestamp (UTC):** `2026-10-24T00:09:16Z`
- **Overall Result:** **PASS** (`0` integrity errors)
- **Unique Official HTTPS URLs Verified:** `190`
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
| `SEC-06` | Static HTML Internal/External Link Integrity & Anchor Verification | **PASS** | `3311` | Parsed 25 HTML pages and verified 3311 links, stylesheets, scripts, and anchor targets with zero broken links. |
| `SEC-07` | Front-End Security, No-Hallucinations Top Banner & Zero-External-Script Check | **PASS** | `25` | Verified zero third-party script dependencies, strict rel='noopener noreferrer' on external links, zero eval() calls, and active Front-Page No-Hallucinations Mandate summary. |

## SHA-256 Integrity Digests (`data/*.json`)

| File | SHA-256 Digest |
|---|---|
| `data/bands-and-high-karat.json` | `954cb5aa552b14adc0bfc6b81196bea9d430dcb3dd7a0813707ef00e9c55d7f1` |
| `data/findings.json` | `06c0f3f0bed86bfa43644a7412bdd3c3161bca2fa788fe8bfefe09c2bae61156` |
| `data/flags.json` | `4b2174a3d2dc67b580a56ee12cc4ce30e8ba0c34035163fa9106252fd23a0bed` |
| `data/gold-price.json` | `bdb3a741c6696f56ec713c090706cb98fefb53901fe284dfe105308a7d6a7e08` |
| `data/prices.json` | `3919c8376c0360f9c9a11cb46c53bc1346d994e76aa6d553831f0e5e64c8c15a` |
| `data/products.json` | `baf5ea1095b53e202c1b76dff7469ea9e738f23a1c3c6cf71926be05c026a4ac` |
| `data/requirements-matrix.json` | `89719c1f078f4a347de40f2688b00d2d526e175ced4baa389978b1ef17347e18` |
| `data/retailers.json` | `d75f6fa9153d9ad55fad0d6d7b592cf2abc55194d86972a29524ffa9c8828fcf` |
| `data/reverification-1162b2db.json` | `803157bd7daddc10ea8ab4773c5ee1df1b5573c259c53c18c74c025263cea4b3` |
| `data/reverification-57724486.json` | `8b185580a5ef8bafa536151f721d3cb516e66926f02762af704284b9c3e2e2f3` |
| `data/reverification-bfcd8465.json` | `46f99c832ef98244d5d535ef4389dabc9313f1f92833e11157a3b9a09ec2cae8` |
| `data/reverification-c-15b00e99.json` | `34ac65f9dc2ee5d078b5a4a7128eb41fd2e7316efbd4e5d125ebe71b0b946332` |
| `data/reverification-c-6ccbc523.json` | `a807951064276cd1fd9010379082733243c39cbf75a542d52e5e74bd0e64386d` |
| `data/reverification-dataset-c.json` | `2f35e1bb80f76cbc360f51dc2fec996c407f96fdd192b6386f33ad5cf4635e5c` |
| `data/reverification-fb7e5e3c.json` | `5b0dfdc516c0cd958d8d600ae85a28d7ad46e73aa743335110b4d1e60f3c792a` |
| `data/reverification-p15.json` | `ed96531e5576f223a77187091275b945ca35c9c5e1dbb9429d97b7973cbc7b6e` |
| `data/reverification-p17.json` | `14e3160dc5fe245c694c5099550cd65a4d638d28f30bf4c23d744f0c9b375b9d` |
| `data/reverification-p19.json` | `6878cb48508e91c3594fdf5411b23e076a1132a97ab75ae84a8cef89a81369ef` |
| `data/reverification-p21.json` | `fa03e9722cc65780757ed97f5a17fcffb63c96ef376278cb3cd71021a1615e81` |
| `data/reverification-p3.json` | `b1dca1669099d66e45b08588f8827b24f59edd65e4f4b4a806ef2a02987b5d16` |
| `data/reverification-p4.json` | `2e5ce8fdff92d04a3e1570960caf0bb1daafc91b2d76209a97a0fb94635e801a` |
| `data/reverification-p5.json` | `1c5ba33b93efdaa14d423fff0be8ca20622f4436d900bc6208ee44e64158bdda` |
| `data/reverification-p6.json` | `dee30027715ce1f89f414ab0bff0140b3684ba009e6b7f1fa3fc3f7322a7b62e` |
| `data/rings.json` | `bae35b6e4293acf80c671f08b1e8cc923a0bc24d09b4213bb767eb7d53748743` |
| `data/sellers-policies.json` | `bfdc4ea96fe5daaf26fed08c1811bb8b9bb012fbb986f4310ee5bce8290ca9a9` |
| `data/sellers.json` | `4d1bd09620f904e833139fa16f7be571e87ade0115df1826472447e324bc033f` |
| `data/solitaire-rings.json` | `201fcc8aa94282160cebcb2afb706ba4c64c40617b3d7cf7f370554885077dbc` |
| `data/sources.json` | `06cbb1e75962121b824f0be37d7447d74a848cdebe2693fe2c0f08b8f3c5fb74` |
| `data/spot-and-standards.json` | `b2b4203069b283be7a36228bf776aed7bda1e673435d1e2488c83e3fd890e03b` |
| `data/standards.json` | `6b745302667c70fb15800fb830471250551a37e238e507a8b993f8e3c4423ad8` |
| `data/verification-report.json` | `05c3273f4a55456fc8ea7531b05ae50251329b32cd34a532c82d78a10b55be4b` |
| `data/verification.json` | `4dc04e02524dab89c0b4a8bb172c455dd980f14b1f0a42cc6cf2b16e494bb5e9` |
