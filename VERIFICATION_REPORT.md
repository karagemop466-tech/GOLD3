# GOLD3 — Anti-Hallucination & Security Verification Report

- **Latest Audit Pass:** Pass #1 — `Pass 1: Primary Dataset, Verbatim Price & Melt Arithmetic Verification`
- **Timestamp (UTC):** `2026-10-22T23:24:31Z`
- **Overall Result:** **PASS** (`0` integrity errors)
- **Unique Official HTTPS URLs Verified:** `52`
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

## SHA-256 Integrity Digests (`data/*.json`)

| File | SHA-256 Digest |
|---|---|
| `data/bands-and-high-karat.json` | `fd6b7c175980cfad74b34145c03e2632e809c6a94de48ef399b96c55d8ea333c` |
| `data/sellers-policies.json` | `372689ba815fb011c15b17e52773385718f972b174023f8bd67e01bc10d27ea6` |
| `data/solitaire-rings.json` | `1b0d493a2835471df5bf8610622bf2f668a0c2d62e7961c112d46591ae19f769` |
| `data/spot-and-standards.json` | `77a3ff10db7fe885bc1f51eece4311fa6a62034f73ce2292d2e4bf1841b9a5ed` |
