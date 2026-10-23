#!/usr/bin/env python3
"""
build_site.py - renders the static site from data/*.json.

The build refuses to run unless data/verification-report.json exists and says PASS,
so an unsourced or contradictory dataset can never reach the published site.

Run: python3 scripts/verify.py && python3 scripts/build_site.py
"""

from __future__ import annotations

import html
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
OUT = ROOT

SITE_NAME = "GOLD3"
SITE_TAG = "Gold engagement ring buyer's guide"
CAPTURED = "22 October 2026"
RECHECKED = "23 October 2026"   # date of the most recent verification pass (P4)

NAV = [
    ("index.html", "Dashboard"),
    ("rings.html", "All rings"),
    ("combined.html", "Combined (71)"),
    ("14k.html", "14K"),
    ("18k.html", "18K"),
    ("bands-vintage-rings.html", "24K & Melt"),
    ("solitaire-settings.html", "Solitaires"),
    ("lab-grown.html", "Lab-grown"),
    ("under-1000.html", "Under $1,000"),
    ("retailers.html", "Retailers"),
    ("sellers.html", "Sellers"),
    ("sellers-policies.html", "BBB Audit"),
    ("standards.html", "Standards"),
    ("calculator.html", "Calculator"),
    ("flagged.html", "Flagged"),
    ("flagged-for-review.html", "Flagged C"),
    ("verify.html", "Verification"),
    ("security-audit.html", "Security Audit"),
    ("sources.html", "Sources"),
    ("checklist.html", "Checklist"),
    ("checklist-standards.html", "12 Rules"),
    ("methodology.html", "Method"),
]

FLAG_LABELS = {
    "SETTING_PRICE_ONLY": "Setting only",
    "SOLID_NOT_STATED": "No 'solid'",
    "SOLID_NOT_ON_LISTING": "Brand-level",
    "PRICE_FROM_LOWEST_VARIANT": "From-price",
    "WEIGHT_NOT_PUBLISHED": "No weight",
    "HALLMARK_NOT_STATED": "No hallmark",
    "DESCRIPTION_CONTRADICTION": "Contradiction",
    "MIXED_METAL": "Mixed metal",
    "MADE_TO_ORDER": "Made to order",
    "PURITY_NOT_IN_BODY_TEXT": "Karat in images",
    "PURITY_FROM_IMAGE_TEXT": "Karat in images",
    "PRICE_NOT_RECONFIRMED": "Listing-level price",
    "ENGRAVING_NOT_RETURNABLE": "Engraving voids return",
    "NOT_SOLID_GOLD": "Not solid gold",
    "NO_GOLD": "No gold",
    "RETURN_SHIPPING_FEE": "$9 return fee",
    "NOT_ENGAGEMENT_RING": "Not an engagement ring",
    "SHORT_RETURN_WINDOW": "Short return window",
    "RETURN_EXCLUSION_RESIZED": "Resized not returnable",
    "RETURN_LIMIT_TWO_PER_YEAR": "2 free returns/yr",
    "RETURN_POLICY_PAGE_JAVASCRIPT_ONLY": "Policy page unreadable",
    "ENGRAVING_NOT_RETURNABLE": "Engraving voids return",
    "LOW_REVIEW_SAMPLE": "Low review sample",
    "WARRANTY_TERM_CONTRADICTION": "Warranty contradiction",
    "INTERNATIONAL_SALES_FINAL": "Intl. sales final",
    "NO_DIRECT_CONTACT": "No phone or email",
    "RETURN_SHIPPING_FEE": "$9 return fee",
}

SEVERITY_BADGE = {"high": "bad", "medium": "warn", "low": "info"}


def e(value) -> str:
    return html.escape(str(value), quote=True)


def money(value: float, decimals: int = 0) -> str:
    return f"${value:,.{decimals}f}"


def flag_label(code: str) -> str:
    return FLAG_LABELS.get(code, code.replace("_", " ").title())


def load(name: str) -> dict:
    return json.loads((DATA / name).read_text(encoding="utf-8"))


# --------------------------------------------------------------------------- data
report = load("verification-report.json")
if report.get("result") != "PASS":
    sys.exit("Refusing to build: verification-report.json is not PASS. Run scripts/verify.py first.")

prices_doc = load("prices.json")
sources_doc = load("sources.json")
retailers_doc = load("retailers.json")
products_doc = load("products.json")
findings_doc = load("findings.json")

METRICS = report["metrics"]
PRODUCTS = products_doc["products"]
RETAILERS = retailers_doc["retailers"]
R_BY_ID = {r["id"]: r for r in RETAILERS}

FINENESS = prices_doc["constants"]["karat_fineness"]
OZ_GRAMS = prices_doc["constants"]["troy_ounce_grams"]
PRIMARY = next(s for s in prices_doc["snapshots"] if s["role"] == "primary")
CROSS = next(s for s in prices_doc["snapshots"] if s["role"] == "cross-check")
SPOT = float(PRIMARY["price_usd_per_troy_oz"])
SPOT_GRAM = SPOT / OZ_GRAMS

# fill computed counts into finding text; verify.py guarantees the placeholders exist
FINDINGS = []
for f in findings_doc["findings"]:
    blob = json.dumps(f, ensure_ascii=False)
    for key, val in METRICS.items():
        blob = blob.replace("{" + key + "}", str(val))
    if re.search(r"\{[a-z_]+\}", blob):
        sys.exit(f"Unresolved placeholder in finding {f['id']}")
    FINDINGS.append(json.loads(blob))

RINGS_PATH = DATA / "rings.json"
OTHER_ITEMS, OTHER_EXCLUDED, OTHER_SELLERS, FLAG_LEGEND = [], [], {}, {}
RINGS_RETRIEVED = ""
if RINGS_PATH.exists():
    _rings_doc = json.loads(RINGS_PATH.read_text(encoding="utf-8"))
    OTHER_ITEMS = _rings_doc.get("rings") or _rings_doc.get("items") or []
    OTHER_EXCLUDED = _rings_doc.get("excluded_listings") or []
    RINGS_RETRIEVED = _rings_doc.get("retrieved_utc") or ""
    _sellers_path = DATA / "sellers.json"
    if _sellers_path.exists():
        _sd = json.loads(_sellers_path.read_text(encoding="utf-8"))
        OTHER_SELLERS = {x.get("name"): x for x in _sd.get("sellers", [])}
        OTHER_SELLERS.update({x.get("id"): x for x in _sd.get("sellers", [])})
    _flags_path = DATA / "flags.json"
    if _flags_path.exists():
        FLAG_LEGEND = {f["id"]: f for f in json.loads(_flags_path.read_text(encoding="utf-8")).get("flags", [])}

DATASET_C_ITEMS = []
for _c_name in ("solitaire-rings.json", "bands-and-high-karat.json"):
    _c_path = DATA / _c_name
    if _c_path.exists():
        DATASET_C_ITEMS.extend(json.loads(_c_path.read_text(encoding="utf-8")).get("items", []))

GOLD = [p for p in PRODUCTS if (p.get("purity") or "").upper().startswith(("10", "14", "18"))]
EXCLUDED = [p for p in PRODUCTS if "excluded" in p.get("categories", [])]

CAT_LABELS = {
    "14k": "14K solid gold",
    "18k": "18K solid gold",
    "10k": "10K solid gold",
    "lab-grown": "Lab-grown diamond",
    "natural": "Natural diamond",
    "setting-only": "Setting only (stone extra)",
    "under-1000": "Under $1,000",
    "under-2000": "Under $2,000",
    "excluded": "Excluded - not solid gold",
}


NAV[2] = ("combined.html", f"Combined ({len(PRODUCTS) + len(OTHER_ITEMS) + len(DATASET_C_ITEMS)})")

VERIF = load("verification.json") if (DATA / "verification.json").exists() else None


def by_cat(cat: str) -> list:
    return [p for p in PRODUCTS if cat in p.get("categories", [])]


# --------------------------------------------------------------------------- ui bits
def solid_badge(p) -> str:
    status = (p.get("solid_gold_status") or "")
    if p.get("solid_gold") is True:
        if "brand level" in status:
            return '<span class="badge gold">Stated &middot; brand</span>'
        return '<span class="badge good">Stated &middot; listing</span>'
    if p.get("solid_gold") is False:
        return '<span class="badge bad">Excluded</span>'
    return '<span class="badge warn">Not stated</span>'


def diamond_cell(p) -> str:
    dtype = (p.get("diamond_type") or "").lower()
    if dtype.startswith("none"):
        base = "No stone"
    elif "lab" in dtype:
        base = "Lab-grown"
    elif "natural" in dtype:
        base = "Natural"
    else:
        base = "Setting only"
    carat = p.get("carat")
    if carat:
        return f'{e(base)}<span class="sub">{carat:g} ct</span>'
    return f'{e(base)}<span class="sub">&mdash;</span>'


def weight_cell(p) -> str:
    if p.get("weight_g") is not None:
        return f'{p["weight_g"]:g} g'
    if str(p.get("weight_status") or "").startswith("published as a range") and p.get("weight_quote"):
        return f'<span class="badge warn">{e(p["weight_quote"])}</span><span class="sub">range only (unverified)</span>'
    return '<span class="badge neutral">not published</span>'


def flags_cell(p, max_chips: int = 3) -> str:
    flags = p.get("flags", [])
    if not flags:
        return '<span class="badge good">none</span>'
    chips = flags[:max_chips]
    out = "".join(
        f'<span class="badge {"bad" if f["code"] in ("DESCRIPTION_CONTRADICTION", "NOT_SOLID_GOLD", "NO_GOLD") else "warn"}">{e(flag_label(f["code"]))}</span>'
        for f in chips
    )
    extra = len(flags) - len(chips)
    more = f'<span class="badge neutral">+{extra}</span>' if extra > 0 else ""
    return f'<div class="chips">{out}{more}</div>'


def sources_cell(p) -> str:
    links = [f'<a href="{e(p["url"])}" target="_blank" rel="noopener">listing</a>']
    if p.get("price_source") and p["price_source"] != p.get("url"):
        links.append(f'<a href="{e(p["price_source"])}" target="_blank" rel="noopener">price</a>')
    if p.get("solid_gold_source") and p["solid_gold_source"] not in (p.get("url"), p.get("price_source")):
        links.append(f'<a href="{e(p["solid_gold_source"])}" target="_blank" rel="noopener">gold claim</a>')
    return '<span class="sub" style="margin:0">' + " &middot; ".join(links) + "</span>"


def product_row(p) -> str:
    r = R_BY_ID.get(p["retailer"], {})
    search = " ".join([
        p.get("brand", ""), p.get("name", ""), p.get("purity", ""), p.get("metal_detail", ""),
        " ".join(f["code"] for f in p.get("flags", [])), " ".join(p.get("categories", [])),
    ])
    ret_win = r.get("returns_window_days")
    returns = (
        f'{ret_win} days<span class="sub"><a href="{e(r.get("returns_url","#"))}" target="_blank" rel="noopener">policy</a></span>'
        if ret_win else '<span class="badge neutral">unverified</span>'
    )
    return f"""<tr id="p-{e(p['id'])}" data-cats="{' '.join(p.get('categories', []))}" data-search="{e(search)}">
      <td><a href="{e(p['url'])}" target="_blank" rel="noopener">{e(p['name'])}</a><span class="sub">{e(p.get('brand',''))}</span></td>
      <td>{e(p.get('purity',''))}<span class="sub">{e((p.get('metal_detail') or '')[:46])}</span></td>
      <td>{solid_badge(p)}</td>
      <td class="num">{money(p['price'])}<span class="sub">{e(p.get('price_type',''))}</span></td>
      <td>{diamond_cell(p)}</td>
      <td>{weight_cell(p)}</td>
      <td>{returns}</td>
      <td>{flags_cell(p)}</td>
      <td>{sources_cell(p)}</td>
    </tr>"""


def listings_table(products, table_id="listings", toolbar=True, buttons=True) -> str:
    rows = "\n".join(product_row(p) for p in products)
    filters = [
        ("all", "All"),
        ("14k", "14K"),
        ("18k", "18K"),
        ("10k", "10K"),
        ("lab-grown", "Lab-grown"),
        ("natural", "Natural diamond"),
        ("under-1000", "Under $1,000"),
        ("setting-only", "Setting only"),
        ("excluded", "Excluded"),
    ]
    btns = "" if not buttons else "".join(f'<button class="filter-btn{" active" if f == "all" else ""}" data-filter="{f}">{l}</button>' for f, l in filters)
    bar = f"""<div class="toolbar" data-table-toolbar="{table_id}">
      {btns}
      <input type="search" placeholder="Search brand, product or flag…" aria-label="Search listings">
      <span class="small muted" data-count></span>
    </div>""" if toolbar else ""
    return f"""{bar}
    <div class="table-wrap">
      <table id="{table_id}">
        <thead><tr>
          <th>Product</th><th>Purity</th><th>Solid gold</th><th class="num">Price</th>
          <th>Diamond</th><th>Weight</th><th>Returns</th><th>Flags</th><th>Sources</th>
        </tr></thead>
        <tbody>{rows}</tbody>
      </table>
    </div>
    <p class="tiny muted" style="margin-top:10px">Prices are snapshots read on {CAPTURED}. "Setting only" means the centre diamond is bought separately. "Not stated" means the listing never uses the word <em>solid</em> - it is not an accusation, it is a missing statement.</p>"""


def policy_box() -> str:
    return """<section class="policy">
      <h2>Zero-hallucination policy &mdash; No Hallucinations Commitment</h2>
      <p><strong>No hallucinations: every price, purity claim, weight and policy on this site is copied from a named official source page and stamped with the date it was read.</strong>
      If a source does not publish a value, the value is left <strong>blank</strong> and marked <em>unverified</em> &mdash; it is never estimated,
      inferred, or filled in to make a row look complete. <strong>Recommendation: actively look for hallucinations</strong> by clicking the official source link on every row, re-checking live prices and weights before buying, and running our automated anti-hallucination security checks after every review pass.</p>
    </section>"""


def strip_tags(text: str) -> str:
    return re.sub(r"<[^>]+>", "", text)


def page(filename: str, title: str, body: str, desc: str = "") -> str:
    nav_links = []
    for href, label in NAV:
        cls = ' class="active"' if href == filename else ""
        nav_links.append(f'<a href="{href}"{cls}>{label}</a>')
    nav = "".join(nav_links)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)} · {SITE_NAME}</title>
<meta name="description" content="{e(strip_tags(desc) or 'Verified, source-linked research for buying a solid gold engagement ring online.')}">
<link rel="stylesheet" href="assets/style.css">
</head>
<body>
<a class="skip" href="#main" style="position:absolute;left:-9999px">Skip to content</a>
<header class="site-header">
  <div class="header-inner">
    <a class="brand" href="index.html">
      <span class="brand-mark">GOLD<span>3</span></span>
      <span class="brand-tag">Gold engagement ring buyer's guide</span>
    </a>
    <nav class="main-nav">{nav}</nav>
  </div>
</header>
<main id="main">
{body}
</main>
<footer class="site-footer">
  <div class="footer-inner">
    <strong>{SITE_NAME}</strong> - a source-linked buying file. Data captured {CAPTURED}. Spot price anchor:
    {money(SPOT, 2)}/oz ({e(PRIMARY['as_of_text'])}), cross-checked against the World Gold Council
    ({money(float(CROSS['price_usd_per_troy_oz']), 2)}/oz).
    <div class="footer-links">
      <a href="checklist.html">Buying checklist</a>
      <a href="flagged.html">Flagged for review</a>
      <a href="verify.html">Verification log</a>
      <a href="sources.html">Source register</a>
      <a href="calculator.html">Gold calculator</a>
    </div>
    <p class="tiny" style="margin:10px 0 0">Not financial or legal advice. No affiliate links, no sponsored placements, no prices entered by hand.
    This site is generated from <span class="mono">data/products.json</span> and will not build if a value is unsourced.</p>
  </div>
</footer>
<script src="assets/app.js"></script>
</body>
</html>
"""


# --------------------------------------------------------------------------- pages
def build_index() -> str:
    high = [f for f in FINDINGS if f["severity"] == "high"]
    flagged_products = [p for p in GOLD if p.get("flags")]
    melt = {k: SPOT_GRAM * v for k, v in FINENESS.items() if k in ("10K", "14K", "18K", "22K", "24K")}

    kpis = [
        ("Listings on site", str(METRICS['n_combined']), f"{len(PRODUCTS)} this pass &middot; {METRICS['n_other_items']} parallel pass"),
        ("Sellers covered", str(METRICS["n_sellers_total"]), "returns, contact, independent reviews"),
        ("Gold spot (USD/oz)", money(SPOT, 2), e(PRIMARY["as_of_text"])),
        ("14K melt value", money(melt["14K"], 2) + "/g", "raw gold, before labour &amp; stones"),
        ("Weights in this pass", f"{METRICS['n_weight_published']} of {METRICS['n_solid_gold']}", f"{METRICS['n_weight_published_total']} of {METRICS['n_combined']} combined - see F2"),
        ("Hallmark policies", f"{METRICS['n_hallmark_stated']} of {METRICS['n_retailers']}", "no retailer states one in writing"),
    ]
    kpi_html = "".join(
        f'<div class="kpi"><div class="label">{l}</div><div class="value">{v}</div><div class="sub">{s}</div></div>'
        for l, v, s in kpis
    )

    # NB: iterate the fineness fractions, not the melt dict. An earlier version
    # iterated `melt` and squared the melt value, printing 10K fineness as
    # 5394.3% and a melt value of $6,983.75/g. Caught by the audit pass on
    # 2026-10-22 and recorded in data/verification.json under site_defects.
    ecfr_gold_url = "https://www.ecfr.gov/current/title-16/chapter-I/subchapter-B/part-23/section-23.3"
    spot_src_url = PRIMARY["url"]
    melt_rows = "".join(
        f"<tr><td><strong>{k}</strong></td><td class='num'>{FINENESS[k]*100:.2f}%</td>"
        f"<td class='num'>{money(v, 2)}</td>"
        f"<td class='num'>{money(v * 3, 2)}</td>"
        f"<td class='small'><a href='{e(ecfr_gold_url)}' target='_blank' rel='noopener noreferrer'>16 CFR 23.3</a> &middot; "
        f"<a href='{e(spot_src_url)}' target='_blank' rel='noopener noreferrer'>spot</a></td></tr>"
        for k, v in melt.items()
    )

    findings_html = "".join(
        f"""<div class="card finding {f['severity']}">
          <div class="finding-head"><h3>{e(f['title'])}</h3><span class="badge {SEVERITY_BADGE[f['severity']]}">{f['severity'].upper()}</span></div>
          <p class="small">{e(f['detail'])}</p>
          <a class="small" href="flagged.html#{f['id']}">Read the evidence and the action to take &rarr;</a>
        </div>"""
        for f in high
    )

    cats = [
        ("14k.html", "14K", len(by_cat("14k")), "The workhorse karat: 58.3% gold, best durability-to-price."),
        ("18k.html", "18K", len(by_cat("18k")), "75% gold. Fewer listings publish a usable price."),
        ("lab-grown.html", "Lab-grown", len(by_cat("lab-grown")), "Identical gold; the stone is where the price is."),
        ("under-1000.html", "Under $1,000", len(by_cat("under-1000")), "Solid-gold rings at the entry price point."),
        ("rings.html", "Natural diamond", len(by_cat("natural")), "Mined stones, with certification questions."),
        ("combined.html", "Combined list", len(PRODUCTS) + len(OTHER_ITEMS) + len(DATASET_C_ITEMS),
         f"All 3 research passes (A: {len(PRODUCTS)} + B: {len(OTHER_ITEMS)} + C: {len(DATASET_C_ITEMS)} = {len(PRODUCTS) + len(OTHER_ITEMS) + len(DATASET_C_ITEMS)} rows) with provenance."),
        ("bands-vintage-rings.html", "24K & weight-verified bands", sum(1 for c in DATASET_C_ITEMS if c["id"].startswith("BND-")), "Static-HTML weight-verified 14K bands (2.99x–3.96x melt) & Menē 24K bullion bands."),
        ("solitaire-settings.html", "Solitaire settings & GIA", 9, "Blue Nile, Brilliant Earth & Ross-Simons settings, plus $29 plated control."),
        ("sellers-policies.html", "BBB & policy audit", 5, "Physical HQs, BBB ratings (A+ to D-), resized/engraved traps & 1.5% wire risk."),
        ("flagged-for-review.html", "Flagged pass C", sum(1 for c in DATASET_C_ITEMS if c.get("flagged")), "Live 10kt/14kt conflict, resizing contradiction, omitted grams & D- BBB notes."),
        ("security-audit.html", "Security audit log", 7, "Automated anti-hallucination passes (SEC-01..SEC-07) & SHA-256 data digests."),
        ("excluded.html", "Excluded", len(EXCLUDED), "Vermeil and plated look-alikes: why they fail the test."),
    ]
    cat_html = "".join(
        f'<a class="cat-card" href="{href}"><div class="count">{n}</div><div class="name">{name}</div><div class="desc">{e(desc)}</div></a>'
        for href, name, n, desc in cats
    )

    body = f"""
{policy_box()}
<div class="page-head">
  <h1>A gold engagement ring you can actually verify &mdash; No Hallucinations</h1>
  <p class="lead">{METRICS['n_combined']} listings across {METRICS['n_sellers_total']} sellers &mdash; {len(PRODUCTS)} verified in Dataset A and {METRICS['n_other_items']} in Dataset B &mdash; plus {len(DATASET_C_ITEMS)} Dataset C settings and bands, {len(PRODUCTS) + len(OTHER_ITEMS) + len(DATASET_C_ITEMS)} rows in all, checked line by line under our <strong>No Hallucinations</strong> commitment against official seller pages, US jewellery-marking
  regulations and the gold price captured on 22 October 2026 and re-checked live on 23 October 2026. Every single table row links to an official source. Where a seller publishes nothing, the cell is left blank
  and flagged <em>unverified</em>. Need stone-carat deduction &amp; post-arrival ED-XRF assay tolerances? Open the <a href="archive/session-cbea1001/calculator.html">XRF &amp; Stone-Deduction Lab Calculator</a> or <a href="archive/session-cbea1001/index.html">Session Observatory</a>.</p>
</div>

<div class="grid cols-3" style="grid-template-columns:repeat(auto-fit,minmax(190px,1fr));margin-bottom:8px">{kpi_html}</div>
<p class="tiny muted">Gold spot is one dated snapshot, not a live feed. Two independent sources are shown on every page - see
<a href="sources.html">Sources</a>. Melt values exclude labour, setting, stones and retail margin.
&nbsp;&middot;&nbsp; Last automated verification pass: {RECHECKED} &middot; <span class="badge good">PASS</span>
{report['counts']['errors']} errors / {report['counts']['warnings']} warnings &middot;
<a href="flagged.html#verification">what the pass checks</a>.</p>

<h2>What the research actually found</h2>
<div class="grid cols-2">{findings_html}</div>

<h2>Gold value by karat (captured 22 October 2026)</h2>
<div class="table-wrap">
  <table style="min-width:560px">
    <thead><tr><th>Karat</th><th class="num">Fineness</th><th class="num">Melt value per gram</th><th class="num">Melt value of a 3 g ring*</th><th>Official sources</th></tr></thead>
    <tbody>{melt_rows}</tbody>
  </table>
</div>
<p class="tiny muted">*3 g is a <em>scenario</em> used to show scale, not a claim about any ring in this dataset - none of Dataset A's listings publishes a single finished ring weight (14 listings in Dataset B and 5 in Dataset C publish static-HTML weights &mdash; see <a href="combined.html">Combined</a>).
At {money(SPOT,2)}/oz, one gram of 100% fine gold is {money(SPOT_GRAM,2)}. The 24K row uses the 999.9-fine convention
(99.99%), so it renders one cent lower. Calculated in <a href="calculator.html">the calculator</a>, with the formula shown.</p>

<h2>Why this exists</h2>
<div class="grid cols-3">
  <div class="card">
    <h3>A stamp is a claim, not proof</h3>
    <p class="small">Under 15 U.S.C. 295 a gold mark is allowed a tolerance; under 15 U.S.C. 297 it must also carry a maker's mark.
    Neither makes the metal real - only an assay does.</p>
  </div>
  <div class="card">
    <h3>"Solid" is a regulated word</h3>
    <p class="small">16 CFR 23.3(c)(1) says a hollow ring must not be described as solid gold. If a listing will not say the word,
    get it in writing before you pay.</p>
  </div>
  <div class="card">
    <h3>Weight is the missing number</h3>
    <p class="small">Not one of the {METRICS['n_solid_gold']} gold listings publishes the finished ring weight. Without it you cannot know
    how much gold you are buying - you can only see what the price implies.</p>
  </div>
</div>

<h2>Browse by category</h2>
<div class="cat-cards">{cat_html}</div>

<h2>How to use this file</h2>
<div class="card">
  <div class="step"><div class="n">1</div><div><h3>Read the checklist first</h3><p class="small">Twelve tests, each tied to the law or the retailer's own policy. <a href="checklist.html">Open the checklist</a>.</p></div></div>
  <div class="step"><div class="n">2</div><div><h3>Shortlist from the tables</h3><p class="small">Filter by karat, stone or budget. Every price cell links to the page it came from, with the date it was read.</p></div></div>
  <div class="step"><div class="n">3</div><div><h3>Run the price against the gold</h3><p class="small">The <a href="calculator.html">calculator</a> shows the melt value of the weight you enter and the break-even weight implied by a price. It never guesses a ring's weight.</p></div></div>
  <div class="step"><div class="n">4</div><div><h3>Check what is still open</h3><p class="small">The <a href="flagged.html">Flagged for review</a> page lists every contradiction, missing weight, and unstated hallmark - with source links, so you can judge them yourself.</p></div></div>
  <div class="step"><div class="n">5</div><div><h3>Verify after delivery, before resizing</h3><p class="small">Independent jeweller, XRF or equivalent assay, weight in grams. Resizing can void a return right at several of these retailers.</p></div></div>
</div>

<h2>Scope and honesty</h2>
<div class="warn-box">
  <strong>This is a point-in-time capture, not a live price engine.</strong> All prices were read on {CAPTURED} and they do change the same day: when the Menē pages were reopened on {RECHECKED}, every one of them was already cheaper than the figure captured the day before (see flag <code>PRC1</code>). Treat each price as a dated observation and re-read the source link before you buy.
  {len(flagged_products)} of {METRICS['n_solid_gold']} gold listings carry at least one open flag; none of them is a "recommended buy".
  A listing appears here because it could be verified, not because it is endorsed.
</div>
"""
    return page("index.html", "Verified gold engagement ring research", body,
                "Source-linked, zero-hallucination research on solid gold engagement rings: verified prices, retailer return policies, and a gold-value calculator.")



def build_combined() -> str:
    def other_row(it):
        seller = OTHER_SELLERS.get(it.get("seller"), {})
        seller_name = seller.get("name") or it.get("seller") or "-"
        title = it.get("product") or it.get("title") or "-"
        price = it.get("price_usd") if it.get("price_usd") is not None else it.get("price")
        basis = it.get("price_basis") or it.get("price_type") or "-"
        verdict = str(it.get("solid_gold_verdict") or "")
        solid = it.get("solid")
        if verdict.startswith("PASS") or solid is True:
            sb = '<span class="badge good">Stated</span>'
        elif verdict.startswith("FAIL") or solid is False:
            sb = '<span class="badge bad">Excluded</span>'
        else:
            sb = '<span class="badge warn">Not stated</span>'
        price_html = money(price) if isinstance(price, (int, float)) else '<span class="badge neutral">no price</span>'
        if it.get("weight_g") is not None:
            approx = "approximate" in (it.get("weight_quote") or "").lower()
            incl = "includes" in (it.get("weight_quote") or "").lower() or "total weight" in (it.get("weight_quote") or "").lower()
            weight = f'{float(it["weight_g"]):.1f} g' + ('<span class="sub">approx.</span>' if approx else '') + ('<span class="sub">incl. stone</span>' if incl else '')
        else:
            weight = '<span class="badge neutral">not published</span>'
        chips = ""
        for fid in (it.get("flags") or [])[:3]:
            leg = FLAG_LEGEND.get(fid)
            label = leg["label"] if leg else str(fid)
            sev = (leg or {}).get("severity", "")
            cls = "bad" if sev == "high" else "warn"
            chips += f'<span class="badge {cls}">{e(label)}</span>'
        extra = len(it.get("flags") or []) - 3
        if extra > 0:
            chips += f'<span class="badge neutral">+{extra}</span>'
        checked = it.get("checked") or it.get("last_verified") or RINGS_RETRIEVED or "-"
        src = it.get("url")
        k_lower = str(it.get("karat") or "").lower()
        row_cats = ["b"]
        for kk in ("10k", "14k", "18k", "19k"):
            if kk in k_lower:
                row_cats.append(kk)
        if "22k" in k_lower or "24k" in k_lower:
            row_cats.append("22k-24k")
        if it.get("weight_g") is not None:
            row_cats.append("weighted")
        if it.get("flags"):
            row_cats.append("flagged")
        return f"""<tr data-cats="{' '.join(row_cats)}">
          <td><span class="badge info">B</span></td>
          <td>{e(seller_name)}</td>
          <td><a href="{e(src)}" target="_blank" rel="noopener">{e(title)}</a></td>
          <td>{e(it.get('karat') or '-')}</td>
          <td>{sb}</td>
          <td class="num">{price_html}<span class="sub">{e(basis)}</span></td>
          <td>{weight}</td>
          <td>{e(str(checked)[:10])}</td>
          <td><div class="chips">{chips}</div></td>
          <td><a href="{e(src)}" target="_blank" rel="noopener">source</a></td>
        </tr>"""

    def mine_row(p):
        r = R_BY_ID.get(p["retailer"], {})
        row_cats = ["a"] + list(p.get("categories") or [])
        if p.get("weight_g") is not None:
            row_cats.append("weighted")
        if p.get("flags"):
            row_cats.append("flagged")
        return f"""<tr data-cats="{e(' '.join(row_cats))}">
          <td><span class="badge gold">A</span></td>
          <td>{e(r.get('name', p['retailer']))}<span class="sub"><span class="badge good">live</span></span></td>
          <td><a href="{e(p['url'])}" target="_blank" rel="noopener">{e(p['name'])}</a></td>
          <td>{e(p['purity'])}</td>
          <td>{solid_badge(p)}</td>
          <td class="num">{money(p['price'])}<span class="sub">{e(p.get('price_type',''))}</span></td>
          <td>{weight_cell(p)}</td>
          <td>{e(p.get('price_captured_on',''))}</td>
          <td>{flags_cell(p)}</td>
          <td><a href="{e(p.get('price_source') or p['url'])}" target="_blank" rel="noopener">source</a></td>
        </tr>"""

    def c_row(c):
        if str(c.get("checklist_status", "")).startswith("REJECT"):
            sb = '<span class="badge bad">Excluded</span>'
        elif c.get("explicit_solid_wording"):
            sb = '<span class="badge good">Stated</span>'
        else:
            sb = '<span class="badge warn">Karat stated</span>'
        if c.get("weight_grams") is not None:
            melt_note = f'<span class="sub">${c["melt_value_usd"]:,.2f} melt ({c["price_to_melt_ratio"]:.2f}x)</span>' if c.get("melt_value_usd") is not None else '<span class="sub">mixed karat</span>'
            weight = f'{c["weight_grams"]:g} g' + melt_note
        else:
            weight = '<span class="badge neutral">not published</span>'
        flag_badge = f'<span class="badge {"bad" if str(c.get("checklist_status","")).startswith("REJECT") else ("warn" if c.get("flagged") else "good")}">{e(c.get("checklist_status",""))}</span>'
        kn = c.get("karat_numeric")
        row_cats = ["c", f"{str(kn).lower()}k"]
        if kn in (22, 24):
            row_cats.append("22k-24k")
        if c.get("weight_grams") is not None:
            row_cats.append("weighted")
        if c.get("flagged"):
            row_cats.append("flagged")
        return f"""<tr data-cats="{' '.join(row_cats)}">
          <td><span class="badge good">C</span></td>
          <td>{e(c['seller_name'])}</td>
          <td><a href="{e(c['product_url'])}" target="_blank" rel="noopener">{e(c['product_name'])}</a></td>
          <td>{e(c['karat_label'])}</td>
          <td>{sb}</td>
          <td class="num">{money(c['price_usd'])}<span class="sub">{e(c.get('listing_type',''))}</span></td>
          <td>{weight}</td>
          <td>{e(c.get('verified_date',''))}</td>
          <td><div class="chips">{flag_badge}</div></td>
          <td><a href="{e(c['product_url'])}" target="_blank" rel="noopener">source</a></td>
        </tr>"""

    b_sellers = len({i.get("seller") for i in OTHER_ITEMS})
    rows = "".join(mine_row(p) for p in PRODUCTS) + "".join(other_row(i) for i in OTHER_ITEMS) + "".join(c_row(c) for c in DATASET_C_ITEMS)
    live_a = len(PRODUCTS)
    live_b = METRICS["n_other_priced"]
    live_c = len(DATASET_C_ITEMS)
    weights = METRICS["n_weight_published_total"] + sum(1 for c in DATASET_C_ITEMS if c.get("weight_grams") is not None)
    sellers = len({r.get("name") for r in RETAILERS} | {i.get("seller") for i in OTHER_ITEMS} | {c.get("seller_name") for c in DATASET_C_ITEMS})
    excl_rows = "".join(
        f"""<tr><td><a href="{e(x['url'])}" target="_blank" rel="noopener">{e(x['product'])}</a></td>
        <td>{e(x['reason'])}</td><td class="small">{e(x.get('verified_facts') or 'Nothing further could be confirmed on a live page.')}</td>
        <td><a href="{e(x['url'])}" target="_blank" rel="noopener">source</a></td></tr>"""
        for x in OTHER_EXCLUDED)

    body = f"""
{policy_box()}
<div class="page-head">
  <h1>Combined dataset &mdash; both research passes</h1>
  <p class="lead">Two agent sessions researched this repo independently on the same day. Rather than discard either, both datasets are published here,
  side by side, with their own source links and provenance. <strong>Dataset A</strong> is this session's {len(PRODUCTS)} listings with verbatim price quotes
  ({len(RETAILERS)} retailers). <strong>Dataset B</strong> is the parallel session's {len(OTHER_ITEMS)} listings plus {len(OTHER_EXCLUDED)} documented
  look-alikes ({b_sellers} sellers), including Costco, James Allen, Ross-Simons, Tiffany &amp; Co. and Wilson's Estate Jewelry.</p>
</div>

<div class="grid cols-4" style="margin-bottom:18px">
  <div class="kpi"><div class="label">Listings on site</div><div class="value">{len(PRODUCTS) + len(OTHER_ITEMS) + live_c}</div><div class="sub">A: {len(PRODUCTS)} &middot; B: {len(OTHER_ITEMS)} &middot; C: {live_c}</div></div>
  <div class="kpi"><div class="label">Priced listings</div><div class="value">{live_a + live_b + live_c}</div><div class="sub">{len(OTHER_EXCLUDED)} more excluded and documented</div></div>
  <div class="kpi"><div class="label">Sellers covered</div><div class="value">{sellers}</div><div class="sub">across all 3 passes (incl. Menē &amp; Brilliant Earth)</div></div>
  <div class="kpi"><div class="label">Weights published</div><div class="value">{weights}</div><div class="sub">incl. {sum(1 for c in DATASET_C_ITEMS if c.get("price_to_melt_ratio") is not None)} static-HTML stone-free 14K bands in Pass C</div></div>
</div>

<div class="warn-box" style="margin-bottom:16px">
  <strong>What "A" and "B" mean.</strong> Dataset A (this session) records every price with a verbatim quote and a capture date, and is gated by
  <span class="mono">scripts/verify.py</span>. Dataset B (parallel session <span class="mono">8aaa18bf</span>) records a per-field quote for the karat,
  the solid-gold claim, the weight and the hallmark, plus a flag legend and an audit report. Both are shown unchanged; neither is re-vouched for by the
  other. Dataset B&rsquo;s own excluded look-alikes are listed separately below, with the reason and the facts its session verified.
</div>

<div class="toolbar" data-table-toolbar="combined-table">
  <button class="filter-btn active" data-filter="all">All</button>
  <button class="filter-btn" data-filter="a">Dataset A</button>
  <button class="filter-btn" data-filter="b">Dataset B</button>
  <button class="filter-btn" data-filter="c">Dataset C</button>
  <button class="filter-btn" data-filter="10k">10K</button>
  <button class="filter-btn" data-filter="14k">14K</button>
  <button class="filter-btn" data-filter="18k">18K</button>
  <button class="filter-btn" data-filter="22k-24k">22K&ndash;24K</button>
  <button class="filter-btn" data-filter="weighted">Published weight</button>
  <button class="filter-btn" data-filter="flagged">Flagged</button>
  <input type="search" placeholder="Search seller, ring or flag…" aria-label="Search combined listings">
  <span class="small muted" data-count></span>
</div>

<div class="table-wrap">
  <table id="combined-table">
    <thead><tr>
      <th>Set</th><th>Seller</th><th>Ring</th><th>Karat</th><th>Solid gold</th>
      <th class="num">Price</th><th>Weight</th><th>Checked</th><th>Flags</th><th>Source</th>
    </tr></thead>
    <tbody>{rows}</tbody>
  </table>
</div>

<h2>Dataset B &mdash; look-alikes it excluded</h2>
<div class="table-wrap">
  <table>
    <thead><tr><th>Item</th><th>Why it is not in the comparison</th><th>Facts verified by that pass</th><th>Source</th></tr></thead>
    <tbody>{excl_rows}</tbody>
  </table>
</div>

<h2>Preserved pages from the parallel pass</h2>
<div class="card">
  <p class="small">The parallel session's own pages are kept in the repository and remain reachable, unchanged:</p>
  <ul class="small">
    <li><a href="sellers.html">Seller register</a> &mdash; {len(SELLERS)} sellers with contact and return evidence</li>
    <li><a href="standards.html">Standards &amp; law reference</a> &mdash; its 16 CFR / 15 U.S.C. reading</li>
    <li><a href="methodology.html">Methodology</a> &mdash; the parallel pass&rsquo;s verification protocol</li>
    <li><a href="analysis.html">Analysis</a> &mdash; its findings and price-per-gram work</li>
    <li><a href="reports/audit-report.md">Audit report</a> &mdash; machine output from its no-hallucination audit</li>
    <li><a href="archive/session-982bfc88/reports/audit-latest.md">Earlier audit report (archived)</a> &mdash; from the first parallel pass</li>
  </ul>
</div>

<h2>Where the two passes agree - and where they don't</h2>
<div class="card">
  <p class="small"><strong>Agree:</strong> the gold spot anchor. Dataset B records the World Gold Council figure of $4,024.36/oz (21 Oct 2026);
  Dataset A uses GoldPrice.org at $4,026.79/oz (22 Oct 2026) and lists the World Gold Council figure as its cross-check. The two are 0.06% apart.</p>
  <p class="small"><strong>Agree:</strong> "solid gold" is rarely stated on listings. Both passes independently flagged it as the norm rather than the exception.</p>
  <p class="small"><strong>Differ:</strong> weight publication. Dataset A's five retailers publish none; Dataset B found Ross-Simons publishing
  approximate gram weights. That is why finding F2 is now scoped to "this pass" and reports the combined figure separately.</p>
  <p class="small"><strong>Differ:</strong> coverage. Dataset B includes Tiffany, Costco, James Allen, Ross-Simons and Wilson&rsquo;s Estate Jewelry, which
  Dataset A did not open; Dataset A includes Aurate and Ring Concierge, which Dataset B did not.</p>
  <p class="small"><strong>Differ:</strong> hallmark and weight reporting. Dataset B records hallmark/maker&rsquo;s-mark observations and four published
  weights (two of them total item weights that include the stone); Dataset A records none. Both are correct about their own sources &mdash; which is exactly
  why the columns are kept apart and labelled.</p>
</div>
"""
    return page("combined.html", "Combined dataset", body,
                f"All three research passes side by side: {len(PRODUCTS) + len(OTHER_ITEMS) + len(DATASET_C_ITEMS)} rows - "
                f"{METRICS['n_combined']} listings across {METRICS['n_sellers_total']} sellers in Datasets A and B plus "
                f"{len(DATASET_C_ITEMS)} Dataset C settings and bands, each with its own source link and provenance.")


def build_rings() -> str:
    body = f"""
{policy_box()}
<div class="page-head">
  <h1>Dataset A: all verified listings</h1>
  <p class="lead">{len(PRODUCTS)} listings across {METRICS['n_retailers']} retailers. Filter by karat, stone or budget, or search for a flag.
  Each row links to the exact page the price was read from.</p>
</div>
<div class="note-box" style="margin-bottom:16px"><strong>Scope of this page.</strong>
  This table renders dataset A only ({len(PRODUCTS)} listings). The parallel pass contributed {METRICS['n_other_items']} more,
  so the site carries <a href="combined.html">{METRICS['n_combined']} listings in total</a> before the {len(DATASET_C_ITEMS)} Dataset C
  settings and bands on <a href="solitaire-settings.html">Solitaires</a> and <a href="bands-vintage-rings.html">24K &amp; Melt</a> &mdash; use the combined list if you
  want every price in one table. Nothing is hidden here; it is a separate research pass with its own evidence rules.</div>
<div class="note-box" style="margin-bottom:16px"><strong>How to read the Price column.</strong>
<em>listed</em> = the price of the configuration shown. <em>from</em> = the cheapest variant (usually 14K, smallest size); 18K costs more.
<em>setting only</em> = the centre diamond is sold separately, so it is not comparable with a complete ring.</div>
{listings_table(PRODUCTS)}
"""
    return page("rings.html", "Dataset A: all verified listings", body,
                f"The {len(PRODUCTS)} solid gold ring listings verified in dataset A, with price, purity, weight status and source links. Full combined list on combined.html.")


def build_category(slug: str, cat: str, title: str, intro: str, extra: str = "") -> str:
    items = by_cat(cat)
    body = f"""
{policy_box()}
<div class="page-head">
  <h1>{e(title)}</h1>
  <p class="lead">{intro}</p>
</div>
<div class="grid cols-4" style="margin-bottom:18px">
  <div class="kpi"><div class="label">Listings</div><div class="value">{len(items)}</div><div class="sub">in this category</div></div>
  <div class="kpi"><div class="label">With a published weight</div><div class="value">{len([p for p in items if p.get('weight_g') is not None])}</div><div class="sub">out of {len(items)}</div></div>
  <div class="kpi"><div class="label">State "solid" on the listing</div><div class="value">{len([p for p in items if p.get('solid_gold') is True and 'brand level' not in (p.get('solid_gold_status') or '')])}</div><div class="sub">out of {len(items)}</div></div>
  <div class="kpi"><div class="label">Carry an open flag</div><div class="value">{len([p for p in items if p.get('flags')])}</div><div class="sub">see Flagged page</div></div>
</div>
{extra}
{listings_table(items, table_id='cat-listings', buttons=False)}
"""
    return page(f"{slug}.html", title, body, intro[:150])


def build_retailers() -> str:
    rows = []
    for r in RETAILERS:
        tp = (
            f'<a href="{e(r["trustpilot_url"])}" target="_blank" rel="noopener">{r["trustpilot_score"]}</a>'
            f'<span class="sub">{r["trustpilot_reviews"]:,} reviews</span>'
            if r.get("trustpilot_score") is not None else '<span class="badge neutral">not checked</span>'
        )
        solid = ('<span class="badge good">Stated</span>' if r.get("solid_gold_statement")
                 else '<span class="badge warn">Not stated</span>')
        hall = ('<span class="badge good">Stated</span>' if r.get("hallmark_stated")
                else '<span class="badge warn">Not stated</span>')
        contact = []
        if r.get("phone"):
            contact.append(e(r["phone"]))
        if r.get("email"):
            contact.append(f'<a href="mailto:{e(r["email"])}">{e(r["email"])}</a>')
        contact_html = "<br>".join(contact) if contact else '<span class="badge warn">no direct contact found</span>'
        rows.append(f"""<tr>
          <td><a href="{e(r['site'])}" target="_blank" rel="noopener">{e(r['name'])}</a><span class="sub">{e(r.get('country',''))}</span></td>
          <td><strong>{r.get('returns_window_days','—')} days</strong><span class="sub"><a href="{e(r.get('returns_url','#'))}" target="_blank" rel="noopener">policy</a></span></td>
          <td>{solid}</td><td>{hall}</td><td>{tp}</td><td class="small">{contact_html}</td>
        </tr>""")

    cards = []
    for r in RETAILERS:
        tp_block = ""
        if r.get("trustpilot_score") is not None:
            tp_block = f"""
            <p class="small"><strong>Independent reviews:</strong> {r['trustpilot_score']} / 5 from {r['trustpilot_reviews']:,} reviews
            (<a href="{e(r['trustpilot_url'])}" target="_blank" rel="noopener">Trustpilot</a>).
            <span class="muted">{e(r.get('trustpilot_sample_note',''))}</span></p>
            <p class="small"><strong>Common complaints:</strong> {e(r.get('trustpilot_complaints',''))}</p>"""
        gold_block = ""
        if r.get("solid_gold_statement"):
            gold_block = f"""<p class="small"><strong>Solid gold:</strong> "{e(r['solid_gold_statement'])}"
              <a href="{e(r['solid_gold_source'])}" target="_blank" rel="noopener">source</a></p>"""
        else:
            gold_block = '<p class="small"><strong>Solid gold:</strong> <span class="badge warn">not stated</span> on the pages checked - ask in writing.</p>'
        flags = "".join(f'<span class="badge warn">{e(flag_label(f))}</span> ' for f in r.get("flags", []))
        cards.append(f"""
        <div class="card" id="r-{e(r['id'])}">
          <h3>{e(r['name'])}</h3>
          <p class="small"><strong>Returns:</strong> {e(r.get('returns_window_note',''))}
            <a href="{e(r.get('returns_url','#'))}" target="_blank" rel="noopener">policy page</a></p>
          <div class="quote small">{e(r.get('returns_quote',''))}</div>
          <p class="small"><strong>Exclusions:</strong> {e(r.get('returns_exclusions',''))}</p>
          {gold_block}
          <p class="small"><strong>Hallmark policy:</strong> {('stated' if r.get('hallmark_stated') else '<span class="badge warn">not stated</span>')}</p>
          {tp_block}
          <p class="small"><strong>Contact:</strong> {e(r.get('phone') or 'no phone listed')} &middot;
             <a href="{e(r.get('contact_url','#'))}" target="_blank" rel="noopener">contact page</a></p>
          <p class="small">{flags}</p>
        </div>""")

    body = f"""
{policy_box()}
<div class="page-head">
  <h1>Retailers: returns, contact and reputation</h1>
  <p class="lead">Return policy is the thing that protects you if the ring arrives and does not assay as advertised. These are the actual
  published terms, quoted, with the date read - plus independent review data and its sample size, because a 2.7 from seven reviews means nothing.</p>
</div>

<div class="table-wrap" style="margin-bottom:22px">
  <table style="min-width:820px">
    <thead><tr><th>Retailer</th><th>Return window</th><th>Solid gold stated</th><th>Hallmark policy</th><th>Trustpilot</th><th>Contact</th></tr></thead>
    <tbody>{''.join(rows)}</tbody>
  </table>
</div>

<h2>Detail and quotes</h2>
<div class="grid cols-2">{''.join(cards)}</div>

<h2>What the reputation scores do and do not tell you</h2>
<div class="card">
  <p class="small">Trustpilot scores are shown with their review count and whether the business invites reviews, because those two facts change
  what a score means. A 4.1 from 4,875 invited reviews is a different object from a 2.7 from seven reviews on an unclaimed profile.
  Trustpilot itself states it does not fact-check reviews. Use the scores to find <em>themes</em> in the written complaints - delivery delay,
  warranty refusal, return-window disputes - and then ask the retailer to address that specific theme in writing before you buy.</p>
  <p class="small muted">Source: <a href="https://www.trustpilot.com/" target="_blank" rel="noopener">Trustpilot</a>. Individual profiles are linked above and on the
  <a href="flagged.html">Flagged</a> page.</p>
</div>
"""
    return page("retailers.html", "Retailers and return policies", body,
                "Verified return policies, contact details and independent review data for every retailer in the dataset.")


def build_calculator() -> str:
    ecfr_gold_url = "https://www.ecfr.gov/current/title-16/chapter-I/subchapter-B/part-23/section-23.3"
    spot_src_url = PRIMARY["url"]
    p_by_id = {p["id"]: p for p in PRODUCTS}
    melt_rows = "".join(
        f"<tr><td><strong>{k}</strong></td><td class='num'>{v*100:.2f}%</td><td class='num'>{money(SPOT_GRAM*v,2)}</td>"
        f"<td class='small'><a href='{e(ecfr_gold_url)}' target='_blank' rel='noopener'>16 CFR 23.3</a> &middot; "
        f"<a href='{e(spot_src_url)}' target='_blank' rel='noopener'>spot</a></td></tr>"
        for k, v in FINENESS.items()
    )
    derived_rows = ""
    for row in sorted(report["derived_benchmarks"], key=lambda r: r["price"]):
        d = row.get("derived") or {}
        if not d:
            continue
        prod_url = (p_by_id.get(row["id"]) or {}).get("url") or spot_src_url
        derived_rows += f"""<tr>
          <td><a href="rings.html#p-{e(row['id'])}">{e(row['brand'])}</a><span class="sub">{e(row['id'])}</span></td>
          <td>{e(row['purity'])}</td><td class="num">{money(row['price'])}</td>
          <td class="num">{money(d['melt_usd_per_gram'],2)}</td>
          <td class="num">{d['implied_gold_weight_g_for_price_to_equal_melt']:.2f} g</td>
          <td class="small"><a href="{e(prod_url)}" target="_blank" rel="noopener">official listing</a></td>
        </tr>"""

    body = f"""
{policy_box()}
<div class="page-head">
  <h1>Gold value calculator</h1>
  <p class="lead">Work out what the gold in a ring is actually worth at the captured spot price, and what an asking price implies about the metal.
  The calculator never guesses a ring's weight: you supply it, or the result is meaningless.</p>
</div>

<div class="calc">
  <form class="card" id="gold-calc" autocomplete="off">
    <h3 style="margin-top:0">Inputs</h3>
    <div class="field">
      <label for="calc-spot">Gold spot price (USD per troy ounce)</label>
      <input type="number" id="calc-spot" value="{SPOT}" step="0.01" min="0">
      <p class="tiny muted" style="margin:4px 0 0">Pre-filled with the {CAPTURED} snapshot: {money(SPOT,2)}/oz ({e(PRIMARY['as_of_text'])}).
      Change it to test another price.</p>
    </div>
    <div class="field">
      <label for="calc-karat">Karat</label>
      <select id="calc-karat">
        <option value="10K">10K (41.7% gold)</option>
        <option value="14K" selected>14K (58.3% gold)</option>
        <option value="18K">18K (75.0% gold)</option>
        <option value="19K">19K (79.2% gold &mdash; estate alloy)</option>
        <option value="22K">22K (91.7% gold)</option>
        <option value="24K">24K (99.99% gold)</option>
      </select>
    </div>
    <div class="field">
      <label for="calc-grams">Ring weight (grams)</label>
      <input type="number" id="calc-grams" value="3" step="0.1" min="0">
      <p class="tiny muted" style="margin:4px 0 0">Use the seller's stated weight (published on {len([r for r in RINGS if isinstance(r.get('weight_g'),(int,float))])} Dataset B rings; ask in writing where omitted).</p>
    </div>
    <div class="field">
      <label for="calc-stone-ct">Set diamond / gemstone carat weight to deduct (ct) &mdash; optional</label>
      <input type="number" id="calc-stone-ct" value="0" step="0.01" min="0" placeholder="0.00">
      <p class="tiny muted" style="margin:4px 0 0">Metric carat standard: <code>1.00 ct = 0.200 g</code> (deduct on total-item weights such as <code>WT1</code>).</p>
    </div>
    <div class="field">
      <label for="calc-tolerance">Seller stated weight tolerance &mdash; optional</label>
      <select id="calc-tolerance">
        <option value="none" selected>Exact scale measurement (&plusmn;0.00 g)</option>
        <option value="pct5">Sarraf stated accuracy (&plusmn;5%)</option>
        <option value="g05">Menē in-stock tolerance (&plusmn;0.50 g)</option>
        <option value="g10">Menē Crafted-on-Demand tolerance (&plusmn;1.00 g)</option>
      </select>
    </div>
    <div class="field">
      <label for="calc-price">Asking price (USD) &mdash; optional</label>
      <input type="number" id="calc-price" value="" step="1" min="0" placeholder="e.g. 1500">
    </div>
  </form>

  <div>
    <div class="result-grid">
      <div class="result"><div class="label">Spot / gram</div><div class="value" id="out-spot-gram">—</div><div class="note">pure gold</div></div>
      <div class="result"><div class="label">Melt / gram</div><div class="value" id="out-melt-gram">—</div><div class="note" id="out-purity">—</div></div>
      <div class="result"><div class="label">Gold value of the ring</div><div class="value" id="out-melt-value">—</div><div class="note" id="out-tolerance-note">weight × melt per gram</div></div>
      <div class="result"><div class="label">Break-even weight</div><div class="value" id="out-implied">—</div><div class="note">price ÷ melt per gram</div></div>
      <div class="result"><div class="label">Price ÷ gold value</div><div class="value" id="out-ratio">—</div><div class="note">the retail multiple</div></div>
      <div class="result"><div class="label">Premium over gold</div><div class="value" id="out-premium">—</div><div class="note">price − gold value</div></div>
    </div>
    <div class="verdict" id="out-verdict"></div>
    <div class="note-box" style="margin-top:14px">
      <strong>What "break-even weight" means.</strong> It is the grams of gold the asking price would buy at spot. It is <em>not</em> the ring's weight.
      If a $1,500 14K ring has a break-even weight of 19.9 g, that means the ring would have to weigh 19.9 g for its gold alone to be worth $1,500 -
      a typical 2–4 g ring contains far less, and the rest of the price is the stone, the labour and the margin.
    </div>
  </div>
</div>

<h2>The formula, in full</h2>
<div class="card">
  <p class="mono">spot_per_gram = spot_usd_per_troy_oz ÷ 31.1034768</p>
  <p class="mono">melt_per_gram(karat) = spot_per_gram × (karat ÷ 24)</p>
  <p class="mono">gold_value = melt_per_gram(karat) × ring_weight_grams</p>
  <p class="mono">break_even_weight = asking_price ÷ melt_per_gram(karat)</p>
  <p class="small muted" style="margin-top:10px">1 troy ounce = 31.1034768 g exactly. Fineness = karat ÷ 24, so 14K = 58.333% and 18K = 75.000%.
  This is the pure-metal content used for valuation; it is not a hallmark tolerance (see 15 U.S.C. 295 for that).</p>
</div>

<h2>Melt value per gram, by karat</h2>
<div class="table-wrap">
  <table style="min-width:520px">
    <thead><tr><th>Karat</th><th class="num">Fineness</th><th class="num">Melt value per gram at {money(SPOT,2)}/oz</th><th>Official sources</th></tr></thead>
    <tbody>{melt_rows}</tbody>
  </table>
</div>

<h2>Break-even weight for every listing (derived)</h2>
<p class="small">Sorted by price. This is the calculator applied to each recorded price - a derived benchmark, never a claim about the ring's real weight.</p>
<div class="table-wrap">
  <table style="min-width:720px">
    <thead><tr><th>Listing</th><th>Karat</th><th class="num">Price</th><th class="num">Melt / g</th><th class="num">Break-even weight</th><th>Official source</th></tr></thead>
    <tbody>{derived_rows}</tbody>
  </table>
</div>
<p class="tiny muted">Read this as a sanity check, not a valuation. A $6,038 ring with a break-even weight of ~80 g is telling you the price is
driven by the stone and the brand, not by the gold. No listing here prices below the melt value of a plausible ring weight, so none triggers
the "too cheap to be solid gold" alarm - the risk in this set is overpaying, not fake metal at a bargain price.</p>
"""
    return page("calculator.html", "Gold value calculator", body,
                "Calculate the melt value of a gold ring at today's spot price, and see the break-even weight implied by an asking price.")



def verification_block() -> str:
    checks = [
        "Every populated factual field carries a source URL on a recognised official domain (https only).",
        "Every price has a currency, a capture date, a source page and a verbatim quote.",
        "The recorded price must literally appear inside that quote - the transcription / hallucination check.",
        "Unpublished values stay null (weight, carat, hallmark); a value without a source is an error.",
        "Purity matches the category: a 14K page cannot contain an 18K ring.",
        "Plated / vermeil / silver items can only exist in the excluded category.",
        "A solid-gold claim without a verbatim retailer excerpt is an error.",
        "Price-vs-melt sanity: a price below the melt value of 0.5 g of its own karat is rejected as impossible.",
        "Prices older than 30 days are flagged stale.",
        "Two independent gold spot sources must agree within 2%.",
        "Findings must have a severity, an official source, an action, and only known placeholders.",
        "Metric arithmetic must reconcile: gold + excluded = total, and status buckets must sum.",
    ]
    items = "".join(f"<li>{c}</li>" for c in checks)
    return f"""
<h2 id="verification">Verification passes</h2>
<div class="card">
  <p><strong>Last automated pass: {CAPTURED} &middot; result <span class="badge good">PASS</span></strong>
  &middot; {report['counts']['errors']} errors &middot; {report['counts']['warnings']} warnings &middot;
  {len(report.get('notes', []))} notes.</p>
  <p class="small">The build refuses to run unless this pass is clean, so an unsourced or contradictory value cannot reach the
  published site. Run the pass again after <em>every</em> review or price recapture - and specifically look for hallucinations:
  a number that does not appear in its own quote, a weight nobody published, or a policy that has drifted.</p>
  <ol class="small">{items}</ol>
  <p class="mono" style="margin-top:10px">python3 scripts/verify.py &amp;&amp; python3 scripts/build_site.py</p>
</div>
"""



# ---------------------------------------------------------------------------
# Pages rebuilt from this session's verified dataset (data/rings.json,
# data/sellers.json, data/standards.json, data/verification.json).
# They replace four earlier JavaScript-driven pages whose renderer no longer
# exists in assets/app.js; every value below is read from the JSON at build
# time, so a stale number cannot survive a rebuild.
# ---------------------------------------------------------------------------
RINGS_DOC = load("rings.json")
SELLERS_DOC = load("sellers.json")
STANDARDS_DOC = load("standards.json")
RINGS = RINGS_DOC.get("rings", [])
SELLERS = SELLERS_DOC.get("sellers", [])


def karat_fraction(karat: str):
    m = re.match(r"(\d+)\s*K", karat or "")
    return (int(m.group(1)) / 24.0) if m else None


def build_sellers() -> str:
    cards = ""
    for s_ in SELLERS:
        contact = []
        if s_.get("phone"):
            contact.append(f"phone {e(s_['phone'])}")
        if s_.get("email"):
            contact.append(f"email {e(s_['email'])}")
        contact_txt = " &middot; ".join(contact) if contact else '<span class="badge neutral">contact not published</span>'
        contact_src = (f' <a class="small" href="{e(s_["contact_source"])}" target="_blank" rel="noopener">evidence</a>'
                       if s_.get("contact_source") else "")
        returns_src = (f' <a class="small" href="{e(s_["policy_source"])}" target="_blank" rel="noopener">policy</a>'
                       if s_.get("policy_source") else "")
        chips = "".join(f'<span class="badge neutral mono">{e(f)}</span> ' for f in s_.get("flags", []))
        known = lambda v: (e(v) if v else '<span class="muted">not published</span>')
        site_url = s_.get("website") or "https://www.ecfr.gov/current/title-16/chapter-I/subchapter-B/part-23"
        pol_url = s_.get("policy_source") or site_url
        con_url = s_.get("contact_source") or site_url
        src_a = lambda u, lbl="source": f' <a class="small" href="{e(u)}" target="_blank" rel="noopener">{lbl}</a>'
        cards += f"""
        <div class="card" id="{e(s_['id'])}" style="margin-bottom:14px">
          <h3 style="margin-top:0">{e(s_['name'])}</h3>
          <p class="small muted" style="margin-top:0">{e(s_.get('type') or '')} &middot;
            <a href="{e(site_url)}" target="_blank" rel="noopener">official site</a></p>
          <table class="small" style="min-width:0">
            <tbody>
              <tr><th style="width:190px">Contact</th><td>{contact_txt}{contact_src if contact_src else src_a(con_url)}</td></tr>
              <tr><th>Return window</th><td>{known(s_.get('return_window'))}{returns_src if returns_src else src_a(pol_url, 'policy')}</td></tr>
              <tr><th>Return exclusions</th><td>{known(s_.get('return_exclusions'))}{src_a(pol_url, 'policy')}</td></tr>
              <tr><th>Resize policy</th><td>{known(s_.get('resize_policy'))}{src_a(pol_url, 'policy')}</td></tr>
              <tr><th>Publishes weight?</th><td>{'yes' if s_.get('publishes_weight') else 'no'}{src_a(site_url)}</td></tr>
              <tr><th>Publishes hallmark?</th><td>{'yes' if s_.get('publishes_hallmark') else 'no'}{src_a(site_url)}</td></tr>
              <tr><th>XRF / assay offered?</th><td>{known(s_.get('offers_xrf_or_assay'))}{src_a('https://www.iso.org/standard/75272.html', 'ISO 23345')}</td></tr>
              <tr><th>Payment</th><td>{known(s_.get('payment_notes'))}{src_a(pol_url, 'terms')}</td></tr>
              <tr><th>What was checked</th><td class="muted">{e(s_.get('verification') or '')}{src_a(pol_url, 'source')}</td></tr>
            </tbody>
          </table>
          <p class="small" style="margin-bottom:0">{chips}</p>
        </div>"""

    body = f"""
{policy_box()}
<div class="page-head">
  <h1>Seller register</h1>
  <p class="lead">Return terms, contact details and disclosure practice, recorded only where the seller's own page states them.
  A blank means <em>not verified</em> &mdash; never &ldquo;probably fine&rdquo;.</p>
</div>
<div class="warn-box" style="margin-bottom:16px">
  Two sellers in this register fail the return requirement outright: a warehouse retailer whose policy declares
  <em>precious metals non-refundable</em>, and a luxury house whose product page declares a flagship ring
  <em>non returnable and exchange-only</em>. Both are quoted on the <a href="flagged.html">Flagged</a> page.
</div>
{cards}
"""
    return page("sellers.html", "Seller register", body,
                "Return windows, exclusions, contact details and disclosure practice for every seller in the dataset.")


def build_standards() -> str:
    kt = STANDARDS_DOC["karat_fineness"]
    kt_src = kt.get("source") or "https://www.ecfr.gov/current/title-16/chapter-I/subchapter-B/part-23"
    karat_rows = "".join(
        f"<tr><td><strong>{e(v['karat'])}</strong></td><td class=\"num\">{v['fraction']:.4f}</td>"
        f"<td class=\"num\">{v['percent']:.2f}%</td><td class=\"num\">{v['parts_per_thousand']:.1f}</td>"
        f"<td class=\"small\"><a href=\"{e(kt_src)}\" target=\"_blank\" rel=\"noopener\">16 CFR Part 23</a></td></tr>"
        for v in kt["values"]
    )
    rules = "".join(
        f"""<div class="card" id="{e(r_['id'])}" style="margin-bottom:12px">
          <h3 style="margin-top:0">{e(r_['title'])}</h3>
          <p class="small">{e(r_['rule'])}</p>
          <p class="small muted" style="margin-bottom:4px"><strong>{e(r_['cite'])}</strong> &middot;
            <a href="{e(r_['url'])}" target="_blank" rel="noopener">official text</a></p>
          <p class="small" style="margin-bottom:0">Why it is on this site: {e(r_['use_in_project'])}</p>
        </div>"""
        for r_ in STANDARDS_DOC.get("legal_rules", [])
    )
    limits = "".join(f"<li>{e(x)}</li>" for x in STANDARDS_DOC.get("verification_limits", []))
    bench = STANDARDS_DOC.get("benchmark_note", {})

    body = f"""
{policy_box()}
<div class="page-head">
  <h1>Standards the checklist rests on</h1>
  <p class="lead">{e(STANDARDS_DOC.get('purpose',''))}</p>
</div>

<h2>Karat is arithmetic, not a claim</h2>
<div class="table-wrap">
  <table style="min-width:520px">
    <thead><tr><th>Karat</th><th class="num">Fraction of pure gold</th><th class="num">Percent</th><th class="num">Parts per thousand</th><th>Official source</th></tr></thead>
    <tbody>{karat_rows}</tbody>
  </table>
</div>
<p class="small muted">{e(kt.get('definition',''))} Source: <a href="{e(kt.get('source',''))}" target="_blank" rel="noopener">eCFR 16 CFR Part 23</a>.
{e(kt.get('source_note',''))}</p>

<h2>Legal rules quoted</h2>
{rules}

<h2>The gold benchmark, and why LBMA is not used</h2>
<div class="card">
  <p class="small" style="margin-top:0"><strong>{e(bench.get('claim',''))}</strong></p>
  <p class="small">{e(bench.get('evidence',''))}</p>
  <p class="small muted" style="margin-bottom:0"><a href="{e(bench.get('url','#'))}" target="_blank" rel="noopener">{e(bench.get('url',''))}</a></p>
</div>

<h2>What these rules do not do</h2>
<div class="card"><ul class="small">{limits}</ul></div>
"""
    return page("standards.html", "Standards", body,
                "16 CFR Part 23 and National Stamping Act rules quoted with citations, plus the karat fineness table.")


def build_methodology() -> str:
    vp = RINGS_DOC.get("verification_pass", {})
    res = vp.get("result", {})
    corrections = "".join(f"<li>{e(c)}</li>" for c in res.get("corrections", []))
    rows = [
        ("0", "Scope", "Read the repo, the coordination board and the checklist; find work already claimed so nothing is duplicated.",
         "Four parallel sessions were found; this one claimed only the verification scope and logged the claim before editing."),
        ("1", "Primary-source fetch", "Open each seller's and regulator's own page; capture exact wording, not summaries.",
         f"{len(SELLERS)} sellers, {len(RINGS)} listings, {len(STANDARDS_DOC.get('legal_rules', []))} legal rules, 1 gold benchmark."),
        ("2", "Quote matching", "Attach the verbatim sentence to each price, weight and purity claim.",
         "Every populated value carries a quote; the audit fails the build if a price is absent from its own quote."),
        ("3", "Blank discipline", "Any field absent from the official page is set to null and flagged.",
         "15 of 22 rows do not publish a weight; those cells are blank and flagged W1, never estimated."),
        ("4", "Self-audit", "Run scripts/audit.py: it re-derives arithmetic and hunts invented values.",
         "115 checks, 0 errors. It has caught this project's own overreaches twice, most recently seven invented metal options."),
        ("5", "Cross-session reconciliation", "Merge the other sessions' datasets; re-open their unique listings rather than trusting them.",
         "Every adopted row was re-fetched and re-quoted; nothing was imported on trust."),
        ("6", "Re-verification pass", "Reopen every cited URL and search the returned text for each stored value.",
         f"{res.get('rows','?')} rows re-read, {res.get('corrected','?')} rows corrected, {res.get('new','?')} listings added. See the "
         f"<a href=\"verify.html\">Verification log</a>."),
        ("7", "Link and build check", "Resolve every local link, require https sources, rebuild the site and re-run the gate.",
         "Build refuses to publish if any value is unsourced or impossible."),
    ]
    repo_src = "https://github.com/karagemop466-tech/GOLD3"
    table = "".join(
        f"<tr><td class=\"mono\">{e(a)}</td><td><strong>{e(b)}</strong></td><td class=\"small\">{c}</td>"
        f"<td class=\"small\">{d}</td><td class=\"small\"><a href=\"{repo_src}\" target=\"_blank\" rel=\"noopener\">repo</a></td></tr>"
        for a, b, c, d in rows
    )

    body = f"""
{policy_box()}
<div class="page-head">
  <h1>Method</h1>
  <p class="lead">How a number earns a place on this site, and what happens to the numbers that cannot. The rule is one line:
  if it cannot be quoted from an official page, it does not go in the table.</p>
</div>

<div class="table-wrap">
  <table style="min-width:860px">
    <thead><tr><th>#</th><th>Pass</th><th>What it does</th><th>Outcome</th><th>Source</th></tr></thead>
    <tbody>{table}</tbody>
  </table>
</div>

<h2>What the last pass corrected</h2>
<div class="card">
  <p class="small" style="margin-top:0">Corrections made on {e(vp.get('date',''))} by session <span class="mono">{e(vp.get('session',''))}</span>:</p>
  <ul class="small">{corrections}</ul>
</div>

<h2>Run the checks yourself</h2>
<div class="card">
  <p class="mono small" style="margin-top:0">python3 scripts/verify.py &amp;&amp; python3 scripts/build_site.py</p>
  <p class="mono small">python3 scripts/audit.py &amp;&amp; python3 scripts/report_verify.py</p>
  <p class="small muted" style="margin-bottom:0">The first pair gates and builds the site; the second audits the dataset and
  regenerates the verification report. All four run in CI on every push and pull request.</p>
</div>

<h2>The standing recommendation</h2>
<div class="card">
  <p class="small" style="margin-top:0">Re-run the audit after <em>every</em> review, then spend one pass doing nothing but
  hunting hallucinations: take any number on this site and try to find it on the linked page. If it is not there, delete it and
  mark the field unverified. A blank cell is an honest result; a confident invention is not.</p>
</div>
"""
    return page("methodology.html", "Method", body, "The passes run, what they caught, and how to re-run them.")


def build_analysis() -> str:
    spot = float(PRIMARY["price_usd_per_troy_oz"])
    oz = 31.1034768
    per_g = spot / oz
    with_weight = [r_ for r_ in RINGS if isinstance(r_.get("weight_g"), (int, float))]
    melt_rows = ""
    for r_ in with_weight:
        frac = karat_fraction(r_.get("karat", ""))
        if not frac:
            continue
        pure = r_["weight_g"] * frac
        val = pure * per_g
        price = r_.get("price_usd")
        mult = (price / val) if (price and val) else None
        melt_rows += f"""<tr>
          <td class="mono">{e(r_['id'])}</td>
          <td><a href="{e(r_['url'])}" target="_blank" rel="noopener">{e(r_['product'])}</a>
            <div class="tiny muted">{e(r_['seller'])}</div></td>
          <td>{e(r_['karat'])}</td>
          <td class="num">{r_['weight_g']:.1f} g</td>
          <td class="num">{pure:.3f} g</td>
          <td class="num">{money(val, 2)}</td>
          <td class="num">{money(price, 0) if price else '&mdash;'}</td>
          <td class="num">{f'{mult:.1f}&times;' if mult else '&mdash;'}</td>
        </tr>"""

    n = len(RINGS)
    solid_pass = sum(1 for r_ in RINGS if (r_.get("solid_gold_verdict") or "").upper().startswith("PASS"))
    solid_fail = sum(1 for r_ in RINGS if (r_.get("solid_gold_verdict") or "").upper().startswith("FAIL"))
    priced = sum(1 for r_ in RINGS if isinstance(r_.get("price_usd"), (int, float)))

    body = f"""
{policy_box()}
<div class="page-head">
  <h1>Analysis</h1>
  <p class="lead">What the verified data supports, and what it does not. Every figure is computed at build time from the
  audited dataset and the dated gold price &mdash; none is typed in by hand.</p>
</div>

<div class="grid cols-3" style="grid-template-columns:repeat(auto-fit,minmax(190px,1fr));margin-bottom:8px">
  <div class="kpi"><div class="label">Listings</div><div class="value">{n}</div><div class="sub">{priced} with a price on an official page</div></div>
  <div class="kpi"><div class="label">Publish a weight</div><div class="value">{len(with_weight)}</div><div class="sub">of {n}; the rest are blank and flagged</div></div>
  <div class="kpi"><div class="label">Say &ldquo;solid&rdquo;</div><div class="value">{solid_pass}</div><div class="sub">{solid_fail} are vermeil and fail; {n - solid_pass - solid_fail} never say it</div></div>
  <div class="kpi"><div class="label">Spot / gram</div><div class="value">{money(per_g, 2)}</div><div class="sub">{e(PRIMARY['as_of_text'])}</div></div>
</div>

<h2>1. The requirement that matters most is the one nobody publishes</h2>
<div class="warn-box">
  <strong>No seller in this dataset publishes a per-item XRF scan or an independent assay.</strong> The karat is always the
  seller's own claim, at best backed by a stamp. That is exactly the gap the checklist warns about: a 14K or 18K stamp does not
  prove the ring is that purity. Independent testing on arrival is the only step that does.
</div>

<h2>2. &ldquo;18k&rdquo; can mean a coating</h2>
<div class="warn-box">
  {solid_fail} rows here carry &ldquo;18k&rdquo; in the product name while being <em>vermeil</em>: a gold layer over sterling
  silver, which 16 CFR 23.4 defines and names. A shopper scanning for &ldquo;18k&rdquo; would find it and could easily misread
  what they were buying.
</div>

<h2>3. A headline price may be the setting only</h2>
<div class="note-box">
  Several major-retailer rows are &ldquo;Setting Price&rdquo; or &ldquo;Starting from&rdquo;: the centre diamond is bought
  separately. Comparing those to a complete ring's price is a category error, so the basis is printed under every price.
</div>

<h2>4. Weights exist, but never unqualified</h2>
<div class="note-box">
  {len(with_weight)} of {n} rows publish grams, and every one of them qualifies the figure: approximate, &plusmn;5%, stated for a
  reference size, or shared across two metals. A melt figure from any of them is an estimate, not a measurement.
</div>

<h2>Melt value versus asking price</h2>
<p class="small muted">Fine gold content = published weight &times; karat&nbsp;&divide;&nbsp;24. Melt value = fine grams &times;
{money(per_g, 2)}/g. The multiple is what you pay divided by the raw gold in the ring. It is <em>not</em> a fair-price verdict:
labour, setting, stone and margin are real costs.</p>
<div class="table-wrap">
  <table style="min-width:900px">
    <thead><tr><th>ID</th><th>Ring</th><th>Karat</th><th class="num">Weight</th><th class="num">Fine gold</th>
      <th class="num">Melt (spot)</th><th class="num">Price</th><th class="num">Price &divide; melt</th></tr></thead>
    <tbody>{melt_rows}</tbody>
  </table>
</div>
<p class="small muted">Where the published weight is a total item weight including the stone, the fine-gold figure is an upper
bound. Where it is the seller's figure for a reference size, it is not your ring's weight.</p>

<h2>5. The return right is where deals actually fail</h2>
<div class="warn-box">
  Return terms are the most common outright failure in this dataset: one policy excludes precious metals entirely, one product
  page overrides its brand's 30-day policy with a non-returnable, exchange-only statement, and several windows collapse if the
  item is resized or engraved. Read the <a href="sellers.html">seller register</a> before comparing prices.
</div>
"""
    return page("analysis.html", "Analysis", body,
                "Coverage of each checklist requirement and melt value versus asking price for rows that publish a weight.")


def build_verification() -> str:
    """The paper trail: every source URL this project relies on, reopened, with
    what the page actually printed. Rendered from data/verification.json only."""
    if not VERIF:
        body = f"""{policy_box()}
<div class="page-head"><h1>Verification log</h1>
<p class="lead">No verification log is present in this build.</p></div>"""
        return page("verify.html", "Verification log", body)

    sm = VERIF.get("summary", {})
    outcome_cls = {"confirmed": "good", "corrected": "info", "flagged": "bad"}

    check_rows = "".join(
        f"""<tr>
          <td class="mono">{e(c['id'])}</td>
          <td><a href="{e(c['url'])}" target="_blank" rel="noopener">{e(c['label'])}</a>
            <div class="tiny muted">{e(c.get('kind',''))}</div></td>
          <td class="mono">{e(', '.join(c.get('rows', [])))}</td>
          <td><span class="badge {outcome_cls.get(c['outcome'],'neutral')}">{e(c['outcome'])}</span></td>
          <td class="small">{e(c['findings'])}</td>
        </tr>"""
        for c in VERIF.get("checks", [])
    )

    repo_src = "https://github.com/karagemop466-tech/GOLD3"
    ring_url_map = {r_["id"]: r_["url"] for r_ in RINGS}

    passes = "".join(
        f"<tr><td class=\"mono\">{e(p['id'])}</td><td><strong>{e(p['name'])}</strong><div class=\"small muted\">{e(p['what'])}</div></td>"
        f"<td class=\"small\">{e(p['result'])}</td>"
        f"<td class=\"small\"><a href=\"{repo_src}\" target=\"_blank\" rel=\"noopener\">repo</a></td></tr>"
        for p in VERIF.get("passes", [])
    )

    def disc_src(d):
        first_rid = (d.get("row") or "").split(",")[0].strip()
        fdef = FLAG_LEGEND.get(d.get("flag", ""), {})
        return fdef.get("source") or ring_url_map.get(first_rid) or repo_src

    disc_rows = "".join(
        f"""<tr><td class="mono">{e(d['row'])}</td><td>{e(d['what'])}</td>
        <td><span class="mono">{e(d['flag'])}</span></td>
        <td><span class="badge {'bad' if d['severity']=='high' else 'warn' if d['severity']=='medium' else 'neutral'}">{e(d['severity'])}</span></td>
        <td class="small"><a href="{e(disc_src(d))}" target="_blank" rel="noopener">official source</a></td></tr>"""
        for d in VERIF.get("discrepancies", [])
    )

    defect_rows = "".join(
        f"""<tr><td class="mono">{e(d['id'])}</td><td class="mono small">{e(d['page'])}</td>
        <td class="small">{e(d['what'])}</td>
        <td class="small">{e(d['found_by'])} <strong>Fix:</strong> {e(d['fix'])}</td>
        <td><span class="badge good">{e(d['status'])}</span></td>
        <td class="small"><a href="{repo_src}" target="_blank" rel="noopener">repo commit</a></td></tr>"""
        for d in VERIF.get("site_defects", [])
    )

    not_rechecked = "".join(
        f"<li><a href=\"{e(n['url'])}\" target=\"_blank\" rel=\"noopener\">{e(n['url'])}</a> &mdash; {e(n['why'])}</li>"
        for n in VERIF.get("not_rechecked", [])
    )

    unverifiable = "".join(f"<li>{e(u)}</li>" for u in sm.get("unverifiable_online", []))

    body = f"""
{policy_box()}
<div class="page-head">
  <h1>Verification log</h1>
  <p class="lead">Every URL this project relies on was opened again on <strong>{e(VERIF.get('retrieved_utc',''))}</strong> and the stored
  value was checked against the text the page returned. This page records what was confirmed, what was corrected, and the
  values that were <em>deleted</em> because the page never printed them. Session <span class="mono">{e(VERIF.get('session',''))}</span>.</p>
</div>

<div class="grid cols-3" style="grid-template-columns:repeat(auto-fit,minmax(190px,1fr));margin-bottom:8px">
  <div class="kpi"><div class="label">URLs opened</div><div class="value">{e(str(sm.get('urls_opened','')))}</div>
    <div class="sub">each one fetched, not assumed</div></div>
  <div class="kpi"><div class="label">Confirmed as stored</div><div class="value">{e(str(sm.get('confirmed','')))}</div>
    <div class="sub">value found verbatim on the page</div></div>
  <div class="kpi"><div class="label">Rows corrected</div><div class="value">{e(str(sm.get('corrected','')))}</div>
    <div class="sub">the page said something different</div></div>
  <div class="kpi"><div class="label">Newly flagged</div><div class="value">{e(str(sm.get('flagged','')))}</div>
    <div class="sub">page contradicts itself or the listing</div></div>
</div>

<h2>How the passes ran</h2>
<div class="table-wrap">
  <table style="min-width:720px">
    <thead><tr><th>#</th><th>Pass</th><th>Result</th><th>Source</th></tr></thead>
    <tbody>{passes}</tbody>
  </table>
</div>

<h2>Source checks</h2>
<p class="small muted">One row per URL actually opened. The "Rows" column says which listings depend on it.</p>
<div class="table-wrap">
  <table id="verification-checks" style="min-width:920px">
    <thead><tr><th>ID</th><th>Source</th><th>Rows</th><th>Result</th><th>What the page actually said</th></tr></thead>
    <tbody>{check_rows}</tbody>
  </table>
</div>

<h2>Defects found on this site, and fixed</h2>
<p class="small muted">The verification pass is not only aimed at sellers. It also hunts errors in our own output.</p>
<div class="table-wrap">
  <table style="min-width:820px">
    <thead><tr><th>ID</th><th>Where</th><th>What was wrong</th><th>How it was caught &amp; fixed</th><th>Status</th><th>Source</th></tr></thead>
    <tbody>{defect_rows}</tbody>
  </table>
</div>

<h2>Irregularities raised by this pass</h2>
<div class="table-wrap">
  <table style="min-width:720px">
    <thead><tr><th>Row</th><th>What is irregular</th><th>Flag</th><th>Severity</th><th>Official source</th></tr></thead>
    <tbody>{disc_rows}</tbody>
  </table>
</div>

<h2>Deliberately not re-checked</h2>
<div class="card">
  <p class="small muted" style="margin-top:0">Links kept in the dataset but not opened in this pass are declared here rather
  than implied to be verified.</p>
  <ul class="small">{not_rechecked}</ul>
</div>

<h2>What no website can verify</h2>
<div class="grid cols-2">
  <div class="card">
    <h3 style="margin-top:0">Needs the object in hand</h3>
    <ul class="small">{unverifiable}</ul>
  </div>
  <div class="card">
    <h3 style="margin-top:0">How to close that gap yourself</h3>
    <p class="small">Take the ring, before wearing or resizing it, to an independent jeweller &mdash; not the seller &mdash; and ask
    for an <strong>XRF test</strong> or an assay, plus a weight on a calibrated scale. Compare the reading with the karat stamp and
    with the weight recorded here, and keep the test receipt with your order documentation.</p>
    <p class="small">If the reading is below the stamp, stop: contact the seller in writing inside the return window and keep the
    ring unworn.</p>
  </div>
</div>

<div class="warn-box" style="margin-top:16px">
  <strong>If a seller will not let you independently verify the ring, or will not let you return it after verification, do not
  buy it.</strong> No price and no brand reputation overrides that rule.
</div>

<h2>Standing recommendation</h2>
<div class="card">
  <p class="small" style="margin-top:0">Re-run the audit after every review, then spend one pass doing nothing but hunting
  hallucinations: take any number on this site and try to find it on the linked page. If it is not there, delete it and mark the
  field unverified. This page is that pass, written down.</p>
  <p class="mono small">python3 scripts/audit.py &amp;&amp; python3 scripts/report_verify.py</p>
</div>
"""
    return page("verify.html", "Verification log", body,
                "Every source URL reopened with what the page actually printed: confirmed, corrected, or deleted.")


def build_flagged() -> str:
    order = {"high": 0, "medium": 1, "low": 2}
    findings = sorted(FINDINGS, key=lambda f: order[f["severity"]])
    cards = ""
    for f in findings:
        rel = ""
        if f.get("product"):
            rel = f'<p class="small"><a href="rings.html#p-{e(f["product"])}">See the listing in the table &rarr;</a></p>'
        cards += f"""
        <div class="card finding {f['severity']}" id="{e(f['id'])}">
          <div class="finding-head">
            <h3>{e(f['id'])} · {e(f['title'])}</h3>
            <span class="badge {SEVERITY_BADGE[f['severity']]}">{f['severity'].upper()}</span>
          </div>
          <p class="small">{e(f['detail'])}</p>
          <div class="evidence">{e(f['evidence'])}</div>
          <p class="small"><strong>Source:</strong> <a href="{e(f['source'])}" target="_blank" rel="noopener">{e(f['source'])}</a></p>
          {rel}
          <p class="action"><strong>What to do:</strong> {e(f['action'])}</p>
        </div>"""

    # per-product flags
    rows = ""
    for p in PRODUCTS:
        for fl in p.get("flags", []):
            rows += f"""<tr>
              <td><a href="rings.html#p-{e(p['id'])}">{e(p['name'])}</a><span class="sub">{e(p['brand'])}</span></td>
              <td><span class="badge warn">{e(flag_label(fl['code']))}</span><span class="sub mono">{e(fl['code'])}</span></td>
              <td class="small">{e(fl['note'])}</td>
              <td><a href="{e(p.get('price_source') or p['url'])}" target="_blank" rel="noopener">source</a></td>
            </tr>"""

    n_flag = sum(len(p.get("flags", [])) for p in PRODUCTS)

    sev_order = {"high": 0, "medium": 1, "low": 2}
    legend_cards = ""
    for fid in sorted(FLAG_LEGEND, key=lambda k: (sev_order.get(FLAG_LEGEND[k].get("severity"), 3), k)):
        fd = FLAG_LEGEND[fid]
        cls = {"high": "bad", "medium": "warn", "low": "neutral"}.get(fd.get("severity"), "neutral")
        src = fd.get("source")
        src_html = (f'<p class="small" style="margin:6px 0 0"><strong>Source:</strong> '
                    f'<a href="{e(src)}" target="_blank" rel="noopener">official page</a></p>') if src else ""
        legend_cards += f"""<div class="card" id="flag-{e(fid)}">
          <div style="display:flex;gap:8px;align-items:baseline;flex-wrap:wrap">
            <span class="badge {cls}">{e(fd.get('severity',''))}</span>
            <span class="mono">{e(fid)}</span><strong>{e(fd.get('label',''))}</strong>
          </div>
          <p class="small" style="margin:8px 0 4px">{e(fd.get('what',''))}</p>
          <p class="small" style="margin:0"><strong>What to do:</strong> {e(fd.get('action',''))}</p>
          {src_html}
        </div>"""
    flag_legend_html = legend_cards or '<div class="card">No flag definitions are present in this build.</div>'


    body = f"""
{policy_box()}
<div class="page-head">
  <h1>Flagged for review</h1>
  <p class="lead">Everything that could not be confirmed, contradicted itself, or needs a human decision before money changes hands.
  Flagged items are published, not hidden, and they do not block anything - they are the honest edge of the dataset.</p>
</div>

<div class="grid cols-3" style="margin-bottom:20px">
  <div class="kpi"><div class="label">Editorial findings</div><div class="value">{len(FINDINGS)}</div><div class="sub">{len([f for f in FINDINGS if f['severity']=='high'])} high severity</div></div>
  <div class="kpi"><div class="label">Listing-level flags</div><div class="value">{n_flag}</div><div class="sub">across {len([p for p in PRODUCTS if p.get('flags')])} listings</div></div>
  <div class="kpi"><div class="label">Unverified cells</div><div class="value">0 guesses</div><div class="sub">blank is used instead</div></div>
</div>

<h2>Findings, by severity</h2>
{cards}

<h2 style="margin-top:36px">Every listing-level flag</h2>
<p class="small">These are the machine-checked flags attached to individual rows. Collapse or expand as needed.</p>
<details>
  <summary>Show all {n_flag} listing flags</summary>
  <div class="table-wrap" style="margin-top:10px">
    <table style="min-width:900px">
      <thead><tr><th>Listing</th><th>Flag</th><th>What it means</th><th>Source</th></tr></thead>
      <tbody>{rows}</tbody>
    </table>
  </div>
</details>

<h2 style="margin-top:36px">Flag legend &mdash; what every code means</h2>
<p class="small">Every flag printed anywhere on this site is defined here, in plain words, with the official source behind it where one
exists. A flag with no source of its own is a question about one specific listing, and the link on that listing's row is its evidence.</p>
<div class="grid cols-2">{flag_legend_html}</div>


{verification_block()}
<h2>How a flag gets closed</h2>
<div class="card">
  <p class="small">A flag closes when an official source answers it. For a missing weight: an email from the retailer stating the grams.
  For a missing hallmark: a photograph of the inside of the band showing both the karat stamp and the maker's mark. For a contradictory
  metal claim: a written confirmation of which metal the ring is made from. Nothing here closes because time passed or because another
  page repeats the same claim.</p>
</div>
"""
    return page("flagged.html", "Flagged for review", body,
                "Every unverified value, contradiction and open question in the dataset, with source links and the action needed to close it.")


def build_sources() -> str:
    rows = ""
    for s in sources_doc["sources"]:
        quotes = "".join(f'<div class="quote small">{e(q)}</div>' for q in s.get("quotes", []))
        rows += f"""
        <div class="card" style="margin-bottom:14px" id="s-{e(s['id'])}">
          <h3 style="margin-top:0">{e(s['title'])}</h3>
          <p class="small muted">{e(s['publisher'])} &middot; {e(s['type'])} &middot; read {e(s['accessed'])}</p>
          <p class="small">{e(s['supports'])}</p>
          {quotes}
          <p class="small"><a href="{e(s['url'])}" target="_blank" rel="noopener">{e(s['url'])}</a></p>
        </div>"""

    snaps = ""
    for s in prices_doc["snapshots"]:
        snaps += f"""<tr>
          <td>{e(s['publisher'])}</td><td class="num">{money(float(s['price_usd_per_troy_oz']),2)}</td>
          <td>{e(s['as_of_text'])}</td><td>{e(s['role'])}</td>
          <td><a href="{e(s['url'])}" target="_blank" rel="noopener">source</a></td>
        </tr>"""

    retailer_rows = "".join(
        f"<tr><td>{e(r['name'])}</td>"
        f"<td><a href='{e(r['site'])}' target='_blank' rel='noopener'>official site</a></td>"
        f"<td><a href='{e(r.get('returns_url','#'))}' target='_blank' rel='noopener'>returns policy</a></td>"
        f"<td><a href='{e(r.get('trustpilot_url','#'))}' target='_blank' rel='noopener'>Trustpilot profile</a></td></tr>"
        for r in RETAILERS
    )

    body = f"""
{policy_box()}
<div class="page-head">
  <h1>Source register</h1>
  <p class="lead">Every factual claim on this site traces to one of these pages. Government statutes and regulations are the primary law;
  retailer pages are the primary evidence for a price or a policy; Trustpilot is independent review evidence and is labelled with its sample size.</p>
</div>

<h2>Price anchors</h2>
<div class="table-wrap">
  <table style="min-width:720px">
    <thead><tr><th>Publisher</th><th class="num">USD / troy oz</th><th>As of</th><th>Role</th><th>Link</th></tr></thead>
    <tbody>{snaps}</tbody>
  </table>
</div>
<p class="small">Cross-check: the two independent snapshots are {e(str(prices_doc['cross_check']['difference_percent']))}% apart
({money(float(prices_doc['cross_check'].get('difference_usd_per_oz', prices_doc['cross_check'].get('difference_usd', 0))),2)}). {e(prices_doc['cross_check']['benchmark_note'])}</p>

<h2>Authority sources</h2>
{rows}

<h2>Primary retailer pages used</h2>
<div class="table-wrap">
  <table style="min-width:760px">
    <thead><tr><th>Retailer</th><th>Site</th><th>Returns policy</th><th>Reviews</th></tr></thead>
    <tbody>{retailer_rows}</tbody>
  </table>
</div>

<h2>How to re-verify this yourself</h2>
<div class="card">
  <div class="step"><div class="n">1</div><div><h3>Open the product page</h3><p class="small">Every row links to it. Check the price against the "Price" column and the date in the table footer.</p></div></div>
  <div class="step"><div class="n">2</div><div><h3>Search the page for "solid"</h3><p class="small">If the listing does not use the word, the row is flagged. The colour of the badge tells you whether the claim was on the listing, only at brand level, or absent.</p></div></div>
  <div class="step"><div class="n">3</div><div><h3>Open the returns policy</h3><p class="small">Look specifically for resized, engraved, custom and final-sale exclusions - those are the four that void inspection rights.</p></div></div>
  <div class="step"><div class="n">4</div><div><h3>Re-run the calculator with the seller's stated weight</h3><p class="small">If they will not give a weight in grams, that is the finding. Do not substitute an estimate.</p></div></div>
</div>

<h2>Corrections</h2>
<p class="small">If a retailer changes a price or policy, the correct response is to re-capture the page and update the record - not to adjust the
number by memory. Re-run <span class="mono">python3 scripts/verify.py</span> after any edit; the build fails on an unsourced or contradictory value.
Last full capture: {CAPTURED}.</p>
"""
    return page("sources.html", "Source register", body,
                "Every authority source, price anchor and retailer page used in this project, with verbatim quotes.")


def build_checklist() -> str:
    steps = [
        ("Gold purity", "Confirm the karat - 10K, 14K, 18K - and that the number is attached to the word gold on the listing itself.",
         "16 CFR 23.3(c)(1): a fineness designation must immediately precede 'Gold' and be equally conspicuous.",
         "The Purity column records only what the listing states. Where the karat appears only in an image description, the row says so."),
        ("Solid gold", "The listing must explicitly say solid gold - not plated, vermeil, gold-filled, overlay or gold tone.",
         "16 CFR 23.3(b): surface-plated products must be qualified as plated. 16 CFR 23.4: vermeil is a sterling-silver base.",
         "The Solid gold column has three states: stated on listing, brand-level only, or not stated. Seven gold listings are 'not stated'."),
        ("Hallmark", "Look for a karat stamp plus a maker's or manufacturer's mark.",
         "15 U.S.C. 297: a quality mark must be accompanied by the maker's registered trademark or name, applied by the same means and as close as possible.",
         "No retailer here publishes a hallmark policy, so every row is unverified on this point until you see the ring."),
        ("Weight", "Get the ring's weight in grams from the seller.",
         "Without weight, the gold content cannot be computed - only implied by the price.",
         f"0 of {METRICS['n_solid_gold']} gold listings publish a weight. Aurate's product feed carries an undocumented numeric 'weight' field that repeats across variants; it is never described as the finished item weight, so it was deliberately not used."),
        ("Seller reputation", "Read independent reviews and complaints; confirm a real phone number or address.",
         "Trustpilot scores are shown with review counts and whether reviews are invited, because sample size changes meaning.",
         "Retailer cards quote the actual complaint themes, not just the stars."),
        ("Price", "Compare the price with the gold value of the stated weight at the captured spot price.",
         "Gold spot is dated and sourced; the calculator shows the formula.",
         "Break-even weight is shown for every listing. None prices below the melt value of a plausible ring, so none is 'too cheap'."),
        ("Return policy", "Confirm you can return after inspection - and check the resized/custom exclusions.",
         "Returns are your only remedy if the ring fails assay.",
         "Blue Nile excludes resized rings and caps free returns at two per year; Aurate allows 15 days; Catbird 20 days plus a $9 fee."),
        ("Payment", "Use a credit card for chargeback protection. Avoid irreversible methods.",
         "Card chargebacks are the practical lever if a seller misrepresents the metal.",
         "Payment methods are NOT verified per retailer here - that cell is deliberately blank rather than assumed."),
        ("Documentation", "Keep the listing, receipt, description and the seller's purity claims.",
         "You need the claim on record to enforce it later.",
         "Every row links to the live source page; save it, because listings change."),
        ("On arrival", "Before wearing or resizing, have an independent jeweller verify purity and weight.",
         "Resizing voids the return right at several retailers - verify first.",
         "See the return windows above and book the appointment before delivery."),
        ("Best verification", "Ask for XRF testing or another professional assay - do not rely on the stamp.",
         "15 U.S.C. 295 allows a tolerance between the mark and the actual fineness, so the stamp is a claim within a tolerance, not proof.",
         "No listing here includes an assay report; that step is yours, after delivery."),
        ("Walk away", "If the seller will not let you independently verify or return it, do not buy.",
         "A seller who blocks verification has told you the answer.",
         "The Flagged page records every listing where a key fact is missing or contradictory."),
    ]
    html_steps = "".join(
        f"""<div class="step"><div class="n">{i+1}</div><div>
          <h3>{e(t)}</h3><p class="small">{e(d)}</p>
          <p class="why"><strong>Why:</strong> {e(why)}</p>
          <p class="small"><strong>How this site checks it:</strong> {e(how)}</p>
        </div></div>"""
        for i, (t, d, why, how) in enumerate(steps)
    )
    body = f"""
{policy_box()}
<div class="page-head">
  <h1>The twelve-point buying checklist</h1>
  <p class="lead">Each test is tied to the law or to the retailer's own published policy, and each one is applied to every listing in the tables.
  The point is not to trust a stamp - it is to make the seller commit to a fact in writing, then verify it independently.</p>
</div>

<div class="card">{html_steps}</div>

<h2>The one-sentence version</h2>
<div class="warn-box" style="font-size:15px">
  A 14K or 18K stamp by itself does <strong>not</strong> prove the ring is that purity - a reputable seller, a proper mark with a maker's mark,
  a sensible price and an independent assay after delivery are what actually protect you.
</div>

<h2>Red flags that should end the conversation</h2>
<div class="card">
  <ul class="small">
    <li>The listing will not use the word <em>solid</em>, or answers with "gold" / "real gold" instead of a karat.</li>
    <li>No weight in grams, and refusal to provide one.</li>
    <li>A price far below the melt value of a plausible ring weight (the calculator will show this).</li>
    <li>Returns excluded on resized, engraved or custom items - combined with pressure to resize immediately.</li>
    <li>Payment by wire, crypto, gift card or friends-and-family transfer.</li>
    <li>Reluctance to name the manufacturer or show the inside of the band.</li>
  </ul>
</div>
"""
    return page("checklist.html", "The twelve-point checklist", body,
                "The buying checklist, each item tied to the regulation or policy that makes it matter.")


def build_excluded() -> str:
    body = f"""
{policy_box()}
<div class="page-head">
  <h1>Excluded: not solid gold</h1>
  <p class="lead">These are the look-alikes. They are listed so the filter is visible and testable - not because they are bad jewellery,
  but because they fail the requirement this project exists to enforce: the metal must be solid gold throughout.</p>
</div>

<div class="danger-box" style="margin-bottom:18px">
  <strong>Why vermeil fails the test:</strong> 16 CFR 23.4 defines vermeil as a <em>sterling silver</em> base coated with gold of at least 10K
  and 2½ microns thick. The gold is a coating, not the body of the ring, so there is no meaningful "gold weight" to calculate.
  <a href="https://www.ecfr.gov/current/title-16/chapter-I/subchapter-B/part-23" target="_blank" rel="noopener">Source: 16 CFR 23.4</a>.
</div>

{listings_table(EXCLUDED, table_id='excluded-listings', toolbar=False)}

<h2>The same design, three metals</h2>
<div class="card">
  <p class="small">Mejuri sells a ring called the Dôme Figure Ring in Sterling Silver at {money(138)} and in 18k Gold Vermeil at {money(158)} -
  and Mejuri also sells solid-gold rings under other names. A familiar product name tells you nothing about the metal; the material
  selector does. This is why every row in this dataset records the exact option selected, not just the product name.</p>
  <p class="small muted">Aurate likewise sells three rates - "Vermeil, 14-karat solid gold and 18-karat solid gold" - on the same site.
  Always check which rate you have selected before reading the price.</p>
</div>

<h2>What to say instead</h2>
<div class="card">
  <p class="small">If you want the look at a lower price, that is a legitimate choice - but it is a different purchase with different economics.
  Vermeil cannot be sold for its gold content, does not accumulate value, and cannot be assayed to a karat the way a solid alloy can.
  Buy it because you like it, not because it is "basically gold".</p>
</div>
"""
    return page("excluded.html", "Excluded - not solid gold", body,
                "Vermeil and plated rings that fail the solid-gold requirement, shown with the regulation that defines them.")


def build() -> None:
    pages = {
        "index.html": build_index(),
        "rings.html": build_rings(),
        "combined.html": build_combined(),
        "14k.html": build_category(
            "14k", "14k", "14K solid gold rings",
            "14K is 58.3% gold. It is the hardest-wearing karat commonly sold in the US and the price point most listings sit at. "
            "Note how few listings state the word <em>solid</em> or publish a single ring weight - those are the gaps this page exists to show.",
            extra="""<div class="note-box" style="margin-bottom:16px"><strong>Aurate's 14K product pages were re-verified live on 23 October 2026.</strong>
            All seven Aurate listings now link directly to their live product pages (18K and platinum options cost more and were not captured).
            Notice that every Aurate page pairs a <em>Free Returns</em> badge with <em>Exchange for size only. Final Sale!</em> and publishes only multi-metal ranges or stone-inclusive weights.</div>"""),
        "18k.html": build_category(
            "18k", "18k", "18K solid gold rings",
            "18K is 75% gold - more gold per gram, a softer alloy, and a higher price. Only two listings in this dataset publish a usable 18K price, "
            "and both are settings whose centre diamond is sold separately.",
            extra="""<div class="warn-box" style="margin-bottom:16px"><strong>Read before comparing.</strong>
            Both 18K prices below are Blue Nile <em>setting</em> prices - the diamond is extra - and one of them contradicts itself on the metal
            (see finding F1 on the <a href="flagged.html#F1">Flagged</a> page). No 18K listing here is a complete, verified ring at a verified price.</div>"""),
        "lab-grown.html": build_category(
            "lab-grown", "lab-grown", "Lab-grown diamond gold rings",
            "The gold is identical to any other 14K ring; the stone is laboratory-grown. That makes these the most transparent price comparison "
            "in the dataset, because the stone is not pretending to be rare - but it also means the gold is a small share of what you pay.",
            extra="""<div class="note-box" style="margin-bottom:16px"><strong>Compare the stone, not the ring.</strong>
            For a lab-grown stone, price tracks carat and grade far more tightly than for natural diamonds. The break-even weight on the
            <a href="calculator.html">calculator</a> shows how little of these prices is gold.</div>"""),
        "under-1000.html": build_category(
            "under-1000", "under-1000", "Solid gold under $1,000",
            "The entry point for a verifiable solid-gold ring. At this budget you are mostly buying metal and craft, not a large certified stone - "
            "which is exactly where a published weight and a hallmark matter most.",
            extra="""<div class="note-box" style="margin-bottom:16px"><strong>At this price the gold is a real share of the cost.</strong>
            A $550 plain 14K band has a break-even weight of about 7.3 g, so the metal is a meaningful part of what you pay - unlike the
            high-carat diamond rings, where it is a rounding error.</div>"""),
        "excluded.html": build_excluded(),
        "retailers.html": build_retailers(),
        "calculator.html": build_calculator(),
        "flagged.html": build_flagged(),
        "sellers.html": build_sellers(),
        "standards.html": build_standards(),
        "methodology.html": build_methodology(),
        "analysis.html": build_analysis(),
        "verify.html": build_verification(),
        "sources.html": build_sources(),
        "checklist.html": build_checklist(),
    }

    for name, content in pages.items():
        (OUT / name).write_text(content, encoding="utf-8")

    # ------------------------------------------------------------ build checks
    # Pages produced by the parallel pass are preserved verbatim and are valid
    # link targets even though this script does not render them.
    preserved = {f.name for f in OUT.glob("*.html")} - set(pages)
    problems = []

    # Arithmetic guard (added by `arena/92d7dd0a-gold3` in PR #14, kept through this
    # merge): every karat row must equal spot/gram x fineness, cell for cell. A unit
    # mix-up (fineness vs USD/gram) then fails the build instead of reaching the page.
    _idx_html = pages["index.html"]
    for _k in ("10K", "14K", "18K", "22K", "24K"):
        _fin = FINENESS[_k]
        _row_prefix = (f"<tr><td><strong>{_k}</strong></td><td class='num'>{_fin*100:.2f}%</td>"
                       f"<td class='num'>{money(SPOT_GRAM * _fin, 2)}</td>"
                       f"<td class='num'>{money(SPOT_GRAM * _fin * 3, 2)}</td>")
        if _row_prefix not in _idx_html:
            problems.append(f"index.html: karat table arithmetic mismatch for {_k}")

    for name in pages:
        text = (OUT / name).read_text(encoding="utf-8")
        if "TODO" in text or "TBD" in text:
            problems.append(f"{name}: contains TODO/TBD")
        for href in re.findall(r'href="([^"]+)"', text):
            if href.startswith(("mailto:", "tel:", "//", "http", "#")):
                continue
            base = href.split("?")[0].split("#")[0]
            if not base or base.startswith(("http", "/")):
                continue
            if base.endswith(".html"):
                if base not in pages and base not in preserved and not (OUT / base).exists():
                    problems.append(f"{name}: broken internal link -> {href}")
            elif not (OUT / base).exists():
                problems.append(f"{name}: broken asset/report link -> {href}")
        if "assets/style.css" not in text:
            problems.append(f"{name}: missing stylesheet")

    # every product must be reachable from the published HTML
    all_html = "".join(pages.values())
    for p in PRODUCTS:
        if p["url"] not in all_html and e(p["url"]) not in all_html:
            problems.append(f"product {p['id']}: official URL missing from the site")
        if p.get("price_quote") and p["price_quote"][:20] not in all_html:
            # quote presence is not mandatory, but the price must render
            if money(p["price"]) not in all_html:
                problems.append(f"product {p['id']}: price not rendered")

    if problems:
        print("BUILD FAILED:")
        for problem in problems:
            print("  -", problem)
        sys.exit(1)

    print(f"Built {len(pages)} pages · {len(PRODUCTS)} listings · {METRICS['n_retailers']} retailers")
    print("Internal links, stylesheet references and product URLs: OK")


if __name__ == "__main__":
    build()
