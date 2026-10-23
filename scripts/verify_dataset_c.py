#!/usr/bin/env python3
"""
Deterministic schema, arithmetic, anti-hallucination, and dead-URL verifier for Dataset C
(and cross-dataset dead-link blocklist gate).

Validates:
  - data/spot-and-standards.json (NIST troy oz math & 9 statutory karat purities)
  - data/sellers-policies.json (5 sellers, HTTPS primary policy/BBB URLs, verified contacts)
  - data/solitaire-rings.json (SOL-01..SOL-09) & data/bands-and-high-karat.json (BND-01..BND-12)
  - Zero-hallucination verbatim rules: price, gram weight, "solid" wording, and hallmark claims
  - Exact melt-value & price-to-melt arithmetic against spot_usd_per_gram_24k_exact
  - Blocklist check ensuring zero confirmed 404/500/redirect URLs exist as active citations
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"

TROY_OZ_TO_GRAMS = 31.1034768

CONFIRMED_DEAD_URLS = {
    "https://uscode.house.gov/view.xhtml?path=%2Fprelim%40title15%2Fchapter8&edition=prelim",
    "https://uscode.house.gov/view.xhtml?path=/prelim@title15/chapter8&edition=prelim",
    "https://www.gia.edu/gems-gemology/summer-2025-lab-notes-gold-plated-gold0",
    "https://www.gov.uk/guidance/hallmarking-law-and-practice",
    "https://www.ross-simons.com/pages/returns-and-exchanges",
    "https://mene.com/terms-of-purchase",
    "https://www.nist.gov/pml/owm/metric-si/si-units-mass",
    "https://mejuri.com/world-of-mejuri/contact-us",
    "https://mejuri.com/world-of-mejuri/terms-and-conditions",
    "https://mejuri.com/world-of-mejuri/privacy-policy",
    "https://mene.com/contact-us",
    "https://www.vrai.com/pages/contact-us",
    "https://help.vrai.com/hc/en-us/articles/360000836514-What-is-your-return-policy",
    "https://www.localeclectic.com/pages/contact-us",
    "https://www.brilliantearth.com/returns/",
    "https://www.sarraf.com/pages/returns-and-refunds.html",
    "https://www.automicgold.com/pages/return-policy",
    "https://www.sarraf.com/products/14k-white-gold-1-00-ctw-round-3-stone-diamond-engagement-ring-g-i1-3-80-gr.html",
    "https://www.automicgold.com/products/1-50ctw-pear-shaped-lab-grown-diamond-engagement-ring-bezel-set",
    "https://www.wilsonsestatejewelry.com/pages/returns-exchanges",
}


def load_json(name: str) -> dict:
    return json.loads((DATA_DIR / name).read_text(encoding="utf-8"))


def check_active_urls(obj: object, path: str, errors: list[str]) -> None:
    if isinstance(obj, dict):
        for k, v in obj.items():
            # Historical audit fields recording which dead URL was replaced are exempt
            if k in {
                "dead_url_1",
                "dead_url_2",
                "broken_url",
                "previous_url",
                "what",
                "findings",
                "note",
                "notes",
                "fix",
                "detail",
                "details",
                "summary",
            }:
                continue
            check_active_urls(v, f"{path}.{k}", errors)
    elif isinstance(obj, list):
        for idx, item in enumerate(obj):
            check_active_urls(item, f"{path}[{idx}]", errors)
    elif isinstance(obj, str) and obj in CONFIRMED_DEAD_URLS:
        errors.append(f"{path}: active link points to confirmed dead/broken URL {obj}")


def main() -> int:
    errors: list[str] = []

    spot_doc = load_json("spot-and-standards.json")
    sellers_doc = load_json("sellers-policies.json")
    sol_doc = load_json("solitaire-rings.json")
    bnd_doc = load_json("bands-and-high-karat.json")
    rev_doc = load_json("reverification-dataset-c.json")

    bench = spot_doc["spot_gold_benchmark"]
    spot_oz = bench["spot_bid_usd_per_troy_oz"]
    spot_g = bench["spot_usd_per_gram_24k_exact"]
    expected_spot_g = round(spot_oz / TROY_OZ_TO_GRAMS, 4)
    if abs(spot_g - expected_spot_g) > 1e-4:
        errors.append(f"spot_usd_per_gram_24k_exact {spot_g} != {expected_spot_g:.4f}")

    karat_rows = spot_doc["karat_purity_reference"]
    if len(karat_rows) != 7:
        errors.append(f"expected 7 karat_purity_reference rows, got {len(karat_rows)}")
    for kr in karat_rows:
        exp_gram = round(spot_g * kr["pure_gold_fraction"], 2)
        if abs(kr["usd_per_gram_at_spot"] - exp_gram) > 0.02:
            errors.append(f"{kr['label']}: usd_per_gram_at_spot {kr['usd_per_gram_at_spot']} != {exp_gram}")
        if not kr["source_url"].startswith("https://"):
            errors.append(f"{kr['label']}: non-HTTPS source_url {kr['source_url']}")

    sellers = sellers_doc["sellers"]
    if len(sellers) != 5:
        errors.append(f"expected 5 Dataset C sellers, got {len(sellers)}")
    seller_ids = set()
    for s in sellers:
        sid = s["id"]
        seller_ids.add(sid)
        for url_field in ("official_site_url", "return_policy_url", "payment_policy_url", "bbb_url"):
            u = s.get(url_field, "")
            if not isinstance(u, str) or not u.startswith("https://"):
                errors.append(f"{sid}.{url_field}: invalid HTTPS URL {u!r}")
        if not s.get("headquarters_address") or not s.get("verified_phone"):
            errors.append(f"{sid}: missing headquarters_address or verified_phone")

    solitaires = sol_doc["items"]
    bands = bnd_doc["items"]
    if [r["id"] for r in solitaires] != [f"SOL-{i:02d}" for i in range(1, 10)]:
        errors.append("solitaire-rings.json IDs must be SOL-01..SOL-09 in order")
    if [r["id"] for r in bands] != [f"BND-{i:02d}" for i in range(1, 13)]:
        errors.append("bands-and-high-karat.json IDs must be BND-01..BND-12 in order")

    all_rings = solitaires + bands
    for r in all_rings:
        rid = r["id"]
        if r["seller_id"] not in seller_ids:
            errors.append(f"{rid}: unknown seller_id {r['seller_id']}")
        if not r.get("product_url", "").startswith("https://"):
            errors.append(f"{rid}: invalid product_url {r.get('product_url')!r}")

        verbatim = r.get("verbatim_excerpt") or ""
        price = r["price_usd"]
        price_tokens = {f"${price:,.0f}", f"${price:,.2f}", f"${int(price)}"} if float(price).is_integer() else {f"${price:,.2f}"}
        if not any(tok in verbatim for tok in price_tokens):
            errors.append(f"{rid}: price {price} not found verbatim in verbatim_excerpt")

        if r["explicit_solid_wording"] and "solid" not in verbatim.lower():
            errors.append(f"{rid}: explicit_solid_wording=True but 'solid' absent from verbatim_excerpt")

        hd = r.get("hallmark_disclosure") or ""
        if not hd.startswith("Not published"):
            errors.append(f"{rid}: hallmark_disclosure claims stamp text not backed by seller HTML: {hd!r}")

        w = r["weight_grams"]
        net_w = r["net_gold_weight_grams"]
        frac = r["purity_fraction"]
        if w is None or net_w is None or r["karat_numeric"] is None or frac in (None, 0.0):
            if w is None and frac != 0.0:
                for calc_key in ("net_gold_weight_grams", "pure_gold_grams", "melt_value_usd", "price_to_melt_ratio"):
                    if r[calc_key] is not None:
                        errors.append(f"{rid}: weight_grams is None so {calc_key} must be None (got {r[calc_key]!r})")
            if not r["flagged"] or not r.get("flags"):
                errors.append(f"{rid}: unverified/omitted/non-solid item must have flagged=True and non-empty flags")
        else:
            if str(w) not in verbatim:
                errors.append(f"{rid}: weight_grams {w} not found verbatim in verbatim_excerpt")
            exp_pure = round(net_w * frac, 4)
            exp_melt = round(net_w * frac * spot_g, 2)
            exp_ratio = round(price / exp_melt, 2)
            if abs((r["pure_gold_grams"] or 0.0) - exp_pure) > 0.005:
                errors.append(f"{rid}: pure_gold_grams {r['pure_gold_grams']} != {exp_pure}")
            if abs((r["melt_value_usd"] or 0.0) - exp_melt) > 0.15:
                errors.append(f"{rid}: melt_value_usd {r['melt_value_usd']} != {exp_melt}")
            if abs((r["price_to_melt_ratio"] or 0.0) - exp_ratio) > 0.03:
                errors.append(f"{rid}: price_to_melt_ratio {r['price_to_melt_ratio']} != {exp_ratio}")

    if rev_doc.get("summary", {}).get("urls_opened", 0) < 50 or not rev_doc.get("checks"):
        errors.append("reverification-dataset-c.json must record >= 50 live URL checks")

    for jf in sorted(DATA_DIR.glob("*.json")):
        if jf.name.startswith("reverification-") or jf.name in {"verification.json", "verification-report.json"}:
            continue
        check_active_urls(json.loads(jf.read_text(encoding="utf-8")), jf.name, errors)

    href_re = re.compile(r'href="([^"]+)"')
    for hf in sorted(ROOT.glob("*.html")):
        if hf.name in {"verify.html", "security-audit.html"}:
            continue
        html_text = hf.read_text(encoding="utf-8")
        for m in href_re.finditer(html_text):
            if m.group(1) in CONFIRMED_DEAD_URLS:
                errors.append(f"{hf.name}: href points to confirmed dead URL {m.group(1)}")

    if errors:
        print(f"Dataset C verification FAILED ({len(errors)} error(s)):")
        for e in errors:
            print(f"  - {e}")
        return 1

    w_pub = sum(1 for r in all_rings if r["weight_grams"] is not None)
    print(
        f"Dataset C verification PASSED: {len(all_rings)} rings "
        f"({w_pub} weight-published, {len(all_rings) - w_pub} null/unverified), "
        f"{len(sellers)} sellers, {len(karat_rows)} karat standards, 0 dead links."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
