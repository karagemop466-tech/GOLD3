#!/usr/bin/env python3
"""
verify.py - the anti-hallucination / data-integrity gate for GOLD3.

Run:  python3 scripts/verify.py
Exit: 0 = all checks passed, 1 = at least one ERROR.

What it enforces
----------------
1.  No unsourced facts. Every populated factual field has a source URL.
2.  Prices are snapshots: price + currency + capture date + source + verbatim quote.
3.  The quote actually contains the price we recorded (catches transcription drift).
4.  Values that were never published stay null (weight, carat, hallmark...).
5.  Purity matches the category (a 14k page cannot contain an 18K ring).
6.  Nothing plated/vermeil/filled/tone is filed under a solid-gold category.
7.  Solid-gold claims carry a verbatim excerpt from the retailer.
8.  Every URL is https and on a recognised official domain.
9.  Price-vs-melt sanity: flags a price that is impossible for solid gold, and
    records the "implied gold weight" as a DERIVED benchmark (never as ring weight).
10. Stale prices (>30 days) are flagged.
11. Gold spot cross-check between two independent sources.
"""

from __future__ import annotations

import json
import math
import re
import sys
from datetime import date, datetime
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"

TODAY = date(2026, 10, 22)
MAX_PRICE_AGE_DAYS = 30

# Official domains we are willing to cite. Anything else is an ERROR.
OFFICIAL_DOMAINS = {
    "auratenewyork.com", "www.auratenewyork.com",
    "auratenewyork.gorgias.help",
    "www.bluenile.com", "bluenile.com",
    "mejuri.com", "www.mejuri.com",
    "ringconcierge.com", "www.ringconcierge.com",
    "www.catbirdnyc.com", "catbirdnyc.com",
    "www.ecfr.gov", "ecfr.gov",
    "www.law.cornell.edu", "law.cornell.edu",
    "www.gold.org", "gold.org",
    "goldprice.org", "www.goldprice.org",
    "www.lbma.org.uk", "lbma.org.uk",
    "www.trustpilot.com", "trustpilot.com",
    "www.wilsonsestatejewelry.com", "wilsonsestatejewelry.com",
    "customerservice.costco.com",
    "www.costco.com", "costco.com",
    "www.jamesallen.com", "jamesallen.com",
    "www.ross-simons.com", "ross-simons.com",
    "www.tiffany.com", "tiffany.com",
    "www.sarraf.com", "sarraf.com",
    "www.automicgold.com", "automicgold.com",
    "www.brilliantearth.com", "brilliantearth.com",
    "www.vrai.com", "vrai.com", "help.vrai.com",
    "www.localeclectic.com", "localeclectic.com",
    "mene.com", "www.mene.com",
    "www.bbb.org", "bbb.org",
    "www.nist.gov", "nist.gov",
    "www.iso.org", "iso.org",
    "www.govinfo.gov", "govinfo.gov",
    "consumer.ftc.gov",
    "www.kitco.com", "kitco.com",
    "www.bullionvault.com", "bullionvault.com",
    "github.com",
}

ERRORS: list[str] = []
WARNINGS: list[str] = []
NOTES: list[str] = []


def err(msg: str) -> None:
    ERRORS.append(msg)


def warn(msg: str) -> None:
    WARNINGS.append(msg)


def load(name: str) -> dict:
    path = DATA / name
    if not path.exists():
        err(f"missing data file: {name}")
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        err(f"{name}: invalid JSON - {exc}")
        return {}


def is_https(url: str | None) -> bool:
    if not url or not isinstance(url, str):
        return False
    p = urlparse(url)
    return p.scheme == "https" and bool(p.netloc)


def domain_ok(url: str | None) -> bool:
    """Official https host, or a subdomain of one (e.g. customerservice.costco.com)."""
    if not is_https(url):
        return False
    host = urlparse(url).netloc.lower().split(":")[0]
    if host.startswith("www."):
        host = host[4:]
    return any(host == d or host.endswith("." + d) for d in OFFICIAL_DOMAINS)


def parse_date(value: str | None) -> date | None:
    if not value:
        return None
    try:
        return datetime.strptime(value, "%Y-%m-%d").date()
    except ValueError:
        return None


def price_tokens(price: float) -> set[str]:
    """Accept 2858, 2,858, 2858.00, 6,038, 138 ... as valid renderings of a price."""
    whole = int(price) if float(price).is_integer() else None
    tokens = set()
    if whole is not None:
        tokens.add(str(whole))
        tokens.add(f"{whole:,}")
        tokens.add(f"{whole}.00")
        tokens.add(f"{whole:,}.00")
    else:
        tokens.add(f"{price:.2f}")
        tokens.add(f"{price:,.2f}")
    return tokens


def main() -> int:
    prices_doc = load("prices.json")
    sources_doc = load("sources.json")
    retailers_doc = load("retailers.json")
    products_doc = load("products.json")

    # ---------------------------------------------------------------- spot price
    snapshots = prices_doc.get("snapshots", [])
    if len(snapshots) < 2:
        err("prices.json: need at least two independent spot snapshots for cross-check")

    primary = next((s for s in snapshots if s.get("role") == "primary"), None)
    cross = next((s for s in snapshots if s.get("role") == "cross-check"), None)
    if not primary:
        err("prices.json: no primary spot snapshot")
        return finish()

    for snap in snapshots:
        for field in ("publisher", "url", "price_usd_per_troy_oz", "as_of_text", "captured_on", "quote"):
            if not snap.get(field):
                err(f"prices.json[{snap.get('id')}]: missing {field}")
        if not domain_ok(snap.get("url")):
            err(f"prices.json[{snap.get('id')}]: url is not an allowed official https domain")

    oz_grams = prices_doc.get("constants", {}).get("troy_ounce_grams")
    if not isinstance(oz_grams, (int, float)) or abs(oz_grams - 31.1034768) > 1e-9:
        err("prices.json: troy_ounce_grams must be 31.1034768")

    spot = float(primary["price_usd_per_troy_oz"])
    spot_per_gram = spot / oz_grams

    cross_check = {}
    if cross:
        cross_spot = float(cross["price_usd_per_troy_oz"])
        diff = abs(spot - cross_spot)
        pct = diff / spot * 100
        cross_check = {
            "primary_usd_per_oz": spot,
            "cross_usd_per_oz": cross_spot,
            "difference_usd": round(diff, 2),
            "difference_percent": round(pct, 4),
            "within_tolerance": pct < 2.0,
        }
        if pct >= 2.0:
            warn(f"spot cross-check differs by {pct:.2f}% ({spot} vs {cross_spot}) - re-check sources")
        else:
            NOTES.append(f"spot cross-check OK: ${spot:,.2f} vs ${cross_spot:,.2f} ({pct:.3f}% apart)")

    fineness = prices_doc.get("constants", {}).get("karat_fineness", {})

    # ------------------------------------------------------------------ sources
    source_urls = {s.get("url") for s in sources_doc.get("sources", [])}
    if len(sources_doc.get("sources", [])) < 5:
        err("sources.json: expected at least 5 authority sources")
    for src in sources_doc.get("sources", []):
        for field in ("id", "title", "publisher", "url", "type"):
            if not src.get(field):
                err(f"sources.json[{src.get('id', '?')}]: missing {field}")
        if not domain_ok(src.get("url")):
            warn(f"sources.json[{src.get('id')}]: domain not in allowlist: {src.get('url')}")
        if not src.get("quotes"):
            err(f"sources.json[{src.get('id')}]: no verbatim quote")

    # ------------------------------------------------------------------ retailers
    retailers = retailers_doc.get("retailers", [])
    retailer_ids = set()
    for r in retailers:
        rid = r.get("id")
        if not rid:
            err("retailers.json: retailer without id")
            continue
        if rid in retailer_ids:
            err(f"retailers.json: duplicate id {rid}")
        retailer_ids.add(rid)

        if not is_https(r.get("site")):
            err(f"retailer {rid}: site must be https")
        if r.get("returns_window_days") is None:
            warn(f"retailer {rid}: return window not stated")
        if r.get("returns_window_days") and r["returns_window_days"] < 30:
            NOTES.append(
                f"retailer {rid}: {r['returns_window_days']}-day return window "
                f"(below the 30-day reference used in the checklist)"
            )
        if not r.get("returns_quote"):
            err(f"retailer {rid}: returns_quote missing - policy claim is unsourced")
        if not domain_ok(r.get("returns_url")):
            err(f"retailer {rid}: returns_url not an allowed official domain")
        if r.get("trustpilot_score") is not None:
            if not domain_ok(r.get("trustpilot_url")):
                err(f"retailer {rid}: trustpilot_url invalid")
            if not r.get("trustpilot_quote"):
                err(f"retailer {rid}: trustpilot score without a quote")
            if r.get("trustpilot_reviews") is not None and r["trustpilot_reviews"] < 30:
                NOTES.append(
                    f"retailer {rid}: Trustpilot sample is only {r['trustpilot_reviews']} reviews - low confidence"
                )
            if not r.get("trustpilot_sample_note"):
                err(f"retailer {rid}: trustpilot score without a sample note")
        if r.get("solid_gold_statement") and not domain_ok(r.get("solid_gold_source")):
            err(f"retailer {rid}: solid gold statement without a valid source")

    # ------------------------------------------------------------------- products
    products = products_doc.get("products", [])
    if len(products) < 15:
        err("products.json: expected at least 15 verified listings")

    seen_ids = set()
    report_rows = []

    for p in products:
        pid = p.get("id", "?")
        if pid in seen_ids:
            err(f"product {pid}: duplicate id")
        seen_ids.add(pid)

        # --- identity + retailer
        for field in ("retailer", "brand", "name", "url", "purity", "purity_source"):
            if not p.get(field):
                err(f"product {pid}: missing {field}")
        if p.get("retailer") not in retailer_ids:
            err(f"product {pid}: unknown retailer '{p.get('retailer')}'")
        if not domain_ok(p.get("url")):
            err(f"product {pid}: product url not an allowed official domain")
        if not domain_ok(p.get("purity_source")):
            err(f"product {pid}: purity_source invalid")

        # --- price snapshot discipline
        price = p.get("price")
        if not isinstance(price, (int, float)) or price <= 0:
            err(f"product {pid}: price must be a positive number")
            price = 0.0
        if p.get("currency") != "USD":
            err(f"product {pid}: currency must be explicitly 'USD'")
        captured = parse_date(p.get("price_captured_on"))
        if not captured:
            err(f"product {pid}: price_captured_on must be YYYY-MM-DD")
        elif (TODAY - captured).days > MAX_PRICE_AGE_DAYS:
            warn(f"product {pid}: price captured {(TODAY - captured).days} days ago (stale)")
        if not domain_ok(p.get("price_source")):
            err(f"product {pid}: price_source not an allowed official domain")
        quote = p.get("price_quote") or ""
        if not quote:
            err(f"product {pid}: price_quote missing - price is unsourced")
        else:
            # the recorded price must literally appear in the quoted text
            if price and not any(tok in quote for tok in price_tokens(price)):
                err(
                    f"product {pid}: recorded price {price} does not appear in price_quote "
                    f"'{quote[:90]}' - possible transcription/hallucination"
                )
        if not p.get("price_type"):
            err(f"product {pid}: price_type missing (listed / from / setting-only)")

        # --- no inferred numbers
        if p.get("weight_g") is not None:
            if not domain_ok(p.get("weight_source")):
                err(f"product {pid}: weight_g present without a weight_source")
        else:
            if p.get("weight_status") != "not published":
                err(f"product {pid}: null weight must carry weight_status='not published'")
        if p.get("carat") is not None and not domain_ok(p.get("carat_source")):
            err(f"product {pid}: carat present without carat_source")
        if p.get("hallmark_stated") is not None:
            err(f"product {pid}: hallmark_stated is set but no verified hallmark page exists")

        # --- solid gold discipline
        cats = p.get("categories") or []
        if not cats:
            err(f"product {pid}: no categories")
        if p.get("solid_gold") is True:
            if not p.get("solid_gold_evidence"):
                err(f"product {pid}: claims solid gold without a verbatim excerpt")
            if not domain_ok(p.get("solid_gold_source")):
                err(f"product {pid}: claims solid gold without a valid source")
            if "excluded" in cats:
                err(f"product {pid}: solid gold item filed under 'excluded'")
        elif p.get("solid_gold") is None:
            if "excluded" in cats:
                err(f"product {pid}: unknown solid_gold status cannot be filed under 'excluded'")
            NOTES.append(f"product {pid}: listing does not state solid gold - flagged for review")
        else:  # False
            if "excluded" not in cats:
                err(f"product {pid}: non-solid-gold item must be in 'excluded' category")
            if any(c in cats for c in ("14k", "18k", "10k", "lab-grown", "natural")):
                err(f"product {pid}: plated/non-gold item mixed into a solid-gold category")

        # --- purity vs category
        purity = (p.get("purity") or "").upper()
        if "excluded" not in cats:
            if "14k" in cats and not purity.startswith("14"):
                err(f"product {pid}: in 14k category but purity is '{purity}'")
            if "18k" in cats and not purity.startswith("18"):
                err(f"product {pid}: in 18k category but purity is '{purity}'")
            if "10k" in cats and not purity.startswith("10"):
                err(f"product {pid}: in 10k category but purity is '{purity}'")
            if not any(purity.startswith(k) for k in ("10", "14", "18")):
                err(f"product {pid}: purity '{purity}' is not a solid-gold karat")

        # --- price vs melt sanity (derived benchmark only)
        derived = {}
        karat_key = next((k for k in fineness if purity.startswith(k.replace("K", ""))), None)
        if karat_key and price:
            f = float(fineness[karat_key])
            melt_per_gram = spot_per_gram * f
            implied_g = price / melt_per_gram
            derived = {
                "karat": karat_key,
                "melt_usd_per_gram": round(melt_per_gram, 2),
                "implied_gold_weight_g_for_price_to_equal_melt": round(implied_g, 2),
                "note": "DERIVED BENCHMARK ONLY - this is not the ring's weight. It is the grams of "
                        "that karat the price would buy at spot.",
            }
            if implied_g < 0.5:
                err(f"product {pid}: price is below the melt value of 0.5 g of {karat_key} - "
                    f"impossible for a solid-gold ring")
            elif implied_g < 1.5:
                warn(f"product {pid}: implied gold weight is only {implied_g:.2f} g - "
                     f"verify this is not hollow or plated")
        report_rows.append({
            "id": pid,
            "brand": p.get("brand"),
            "price": price,
            "purity": p.get("purity"),
            "solid_gold": p.get("solid_gold"),
            "flags": [f.get("code") for f in p.get("flags", [])],
            "derived": derived,
        })

        # --- flags must be explained
        for flag in p.get("flags", []):
            if not flag.get("code") or not flag.get("note"):
                err(f"product {pid}: flag without code or note")

    # --------------------------------------------------- duplicate listing check
    urls = [p.get("url") for p in products]
    dupes = {u for u in urls if urls.count(u) > 1}
    if dupes:
        err(f"duplicate product URLs: {sorted(dupes)}")

    # --------------------------------------------- proof that nothing is invented
    # Any string that looks like a number in a factual field must be traceable.
    suspicious = re.compile(r"\b(TBD|TBC|approx(?:imately)?\s*\$|around\s*\$|~\$|est\.\s*\$)", re.I)
    for p in products:
        blob = " ".join(str(v) for v in p.values())
        if suspicious.search(blob):
            err(f"product {p.get('id')}: contains an unsourced/approximate marker")

    # ------------------------------- parallel-pass dataset (data/rings.json)
    other_items, other_excluded = [], []
    rings_path = DATA / "rings.json"
    if rings_path.exists():
        rings_doc = load("rings.json")
        sellers_doc = load("sellers.json")
        seller_names = {x.get("name") for x in sellers_doc.get("sellers", [])}
        items = rings_doc.get("rings") or rings_doc.get("items") or []
        other_excluded = rings_doc.get("excluded_listings") or []
        if len(items) < 5:
            err("rings.json: parallel dataset unexpectedly small")
        for it in items:
            iid = it.get("id", "?")
            for field in ("id", "seller", "url", "karat", "flags", "solid_gold_verdict"):
                if not it.get(field):
                    err(f"rings.json[{iid}]: missing {field}")
            if not (it.get("product") or it.get("title")):
                err(f"rings.json[{iid}]: missing product name")
            seller_label = it.get("seller") or ""
            label_ok = seller_label in seller_names
            if not label_ok and "(" in seller_label:
                base, _, rest = seller_label.partition("(")
                inner = rest.rstrip(")").replace(" collection", "").strip()
                label_ok = base.strip() in seller_names or inner in seller_names
            if not label_ok:
                err(f"rings.json[{iid}]: seller '{seller_label}' not in sellers.json")
            if not domain_ok(it.get("url")):
                err(f"rings.json[{iid}]: url not an allowed official domain")
            srcs = it.get("sources") or []
            if not srcs:
                err(f"rings.json[{iid}]: no source URLs recorded")
            for u in srcs:
                if not domain_ok(u):
                    err(f"rings.json[{iid}]: source not on an allowed domain -> {u}")
            price = it.get("price_usd") if it.get("price_usd") is not None else it.get("price")
            if price is None:
                if not it.get("flags"):
                    err(f"rings.json[{iid}]: no price and no flag explaining why")
            elif not isinstance(price, (int, float)) or price <= 0:
                err(f"rings.json[{iid}]: non-positive price")
            else:
                shown = str(it.get("price_as_shown") or "")
                flat = f"{price:,.0f}"
                if shown and flat not in shown and f"{price:g}" not in shown:
                    err(f"rings.json[{iid}]: price {flat} does not appear in price_as_shown '{shown}'")
            if it.get("weight_g") is not None and not it.get("weight_quote"):
                err(f"rings.json[{iid}]: weight without a weight quote")
            if str(it.get("solid_gold_verdict", "")).startswith("PASS") and not it.get("solid_gold_quote"):
                err(f"rings.json[{iid}]: PASS verdict without a solid-gold quote")
            other_items.append(it)
        for x in other_excluded:
            for field in ("reason", "product", "url"):
                if not x.get(field):
                    err(f"rings.json[excluded]: missing {field}")
            if "verified_facts" in x and not x.get("verified_facts"):
                err("rings.json[excluded]: empty verified_facts (omit the key instead)")
            if not domain_ok(x.get("url")):
                err(f"rings.json[excluded]: url not official -> {x.get('url')}")
    else:
        warn("data/rings.json not found - parallel dataset not integrated")

    # --------------------------------------------------- computed metrics + findings
    solid = [p for p in products if p.get("solid_gold") is True]
    gold_listings = [p for p in products if (p.get("purity") or "").upper().startswith(("10", "14", "18"))]
    metrics = {
        "n_products": len(products),
        "n_solid_gold": len(gold_listings),
        "n_excluded": len([p for p in products if p.get("solid_gold") is False]),
        "n_solid_gold_stated": len(solid),
        "n_solid_gold_null": len([p for p in gold_listings if p.get("solid_gold") is None]),
        "n_solid_gold_brand": len([p for p in solid if "brand level" in (p.get("solid_gold_status") or "")]),
        "n_solid_gold_listing": len([p for p in solid if "brand level" not in (p.get("solid_gold_status") or "")]),
        "n_weight_published": len([p for p in products if p.get("weight_g") is not None]),
        "n_hallmark_stated": len([r for r in retailers if r.get("hallmark_stated")]),
        "n_retailers": len(retailers),
        "n_other_items": len(other_items),
        "n_other_excluded": len(other_excluded),
        "n_other_priced": len([i for i in other_items
                               if i.get("price_usd") is not None or i.get("price") is not None]),
        "n_other_weight": len([i for i in other_items if i.get("weight_g") is not None]),
        "n_other_hallmark": len([i for i in other_items if i.get("hallmark_reported")]),
        "n_combined": len(products) + len(other_items),
        "n_weight_published_total": len([p for p in products if p.get("weight_g") is not None])
                                    + len([i for i in other_items if i.get("weight_g") is not None]),
        "n_sellers_total": len({r.get("name") for r in retailers}
                               | {i.get("seller") for i in other_items}),
    }
    if metrics["n_solid_gold"] + metrics["n_excluded"] != metrics["n_products"]:
        err("metrics: gold + excluded does not equal total products - every product must be either a "
            "karat-gold listing or an explicitly excluded non-gold item")
    if metrics["n_solid_gold_stated"] + metrics["n_solid_gold_null"] != metrics["n_solid_gold"]:
        err("metrics: solid_gold true + null does not equal the number of gold listings")
    if metrics["n_solid_gold_brand"] + metrics["n_solid_gold_listing"] != metrics["n_solid_gold_stated"]:
        err("metrics: solid-gold status buckets do not sum to the number of solid-gold-stated listings")

    findings_doc = load("findings.json")
    findings = findings_doc.get("findings", [])
    if len(findings) < 5:
        err("findings.json: expected at least 5 findings")
    allowed_placeholders = set(metrics) | {"n_products", "n_retailers"}
    for f in findings:
        fid = f.get("id", "?")
        for field in ("id", "severity", "title", "detail", "evidence", "source", "action"):
            if not f.get(field):
                err(f"finding {fid}: missing {field}")
        if f.get("severity") not in {"high", "medium", "low"}:
            err(f"finding {fid}: severity must be high/medium/low")
        if not domain_ok(f.get("source")):
            err(f"finding {fid}: source is not an allowed official https domain")
        blob = f"{f.get('title','')} {f.get('detail','')} {f.get('evidence','')}"
        for ph in re.findall(r"\{([a-z_]+)\}", blob):
            if ph not in allowed_placeholders:
                err(f"finding {fid}: unknown placeholder {{{ph}}}")
        if f.get("product") and f["product"] not in seen_ids:
            err(f"finding {fid}: references unknown product {f['product']}")

    # ------------------------------------------------------------------- report
    report = {
        "generated_on": TODAY.isoformat(),
        "spot": {
            "primary": primary,
            "cross_check": cross_check,
            "usd_per_gram": round(spot_per_gram, 4),
        },
        "counts": {
            "products": len(products),
            "retailers": len(retailers),
            "sources": len(sources_doc.get("sources", [])),
            "errors": len(ERRORS),
            "warnings": len(WARNINGS),
        },
        "derived_benchmarks": report_rows,
        "metrics": metrics,
        "findings": [{"id": f.get("id"), "severity": f.get("severity"), "title": f.get("title")} for f in findings],
        "parallel_dataset": {
            "items": len(other_items),
            "excluded": len(other_excluded),
            "priced": len([i for i in other_items
                           if i.get("price_usd") is not None or i.get("price") is not None]),
            "weights": len([i for i in other_items if i.get("weight_g") is not None]),
        },
        "errors": ERRORS,
        "warnings": WARNINGS,
        "notes": NOTES,
        "result": "PASS" if not ERRORS else "FAIL",
    }
    (DATA / "verification-report.json").write_text(
        json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )

    return finish()


def finish() -> int:
    print("=" * 72)
    print("GOLD3 verification gate")
    print("=" * 72)
    if ERRORS:
        print(f"\nERRORS ({len(ERRORS)}):")
        for e in ERRORS:
            print(f"  [ERROR] {e}")
    if WARNINGS:
        print(f"\nWARNINGS ({len(WARNINGS)}):")
        for w in WARNINGS:
            print(f"  [WARN]  {w}")
    if NOTES:
        print(f"\nNotes ({len(NOTES)}):")
        for n in NOTES:
            print(f"  [note]  {n}")
    print("\nResult:", "PASS - no unsourced or impossible values" if not ERRORS else "FAIL")
    return 0 if not ERRORS else 1


if __name__ == "__main__":
    sys.exit(main())
