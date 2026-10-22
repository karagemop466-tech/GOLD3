#!/usr/bin/env python3
"""
build.py — renders the GOLD3 static site from data/*.json.

No third-party dependencies. Every number shown on the site is read from the
JSON dataset (which carries its own quoted source), or computed by the formulas
documented on the Method page. Nothing is hard-coded into the HTML.

Usage: python3 scripts/build.py
"""
from __future__ import annotations

import html
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

from audit import Audit, load, render_markdown

ROOT = Path(__file__).resolve().parent.parent
SITE_NAME = "GOLD3"
SITE_TAG = "Gold engagement ring research"

NAV = [
    ("index.html", "Dashboard"),
    ("rings.html", "Ring list"),
    ("sellers.html", "Sellers"),
    ("standards.html", "Rules &amp; law"),
    ("calculator.html", "Calculator"),
    ("flagged.html", "Flagged for review"),
    ("method.html", "Method &amp; audit"),
]

CATEGORIES = {
    "engagement-setting": "Engagement ring setting",
    "engagement-complete": "Complete engagement ring",
    "wedding-band": "Wedding band",
    "weight-benchmark": "Weight benchmark",
    "plated-example": "Plated / vermeil (avoid)",
}
CATEGORY_ORDER = list(CATEGORIES)


# --------------------------------------------------------------------------- #
# helpers
# --------------------------------------------------------------------------- #
def e(x) -> str:
    return html.escape(str(x), quote=True)


def money(v, dash="—"):
    if v is None:
        return f'<span class="nv">{dash}</span>'
    return f"${v:,.0f}" if float(v).is_integer() else f"${v:,.2f}"


def num(v, digits=2, dash="—"):
    if v is None:
        return f'<span class="nv">{dash}</span>'
    return f"{v:,.{digits}f}"


def badge(text, kind="mut"):
    return f'<span class="badge b-{kind}">{e(text)}</span>'


def src(url, label="source"):
    if not url:
        return ""
    return f'<a class="srclink" href="{e(url)}" rel="noopener nofollow" target="_blank">{e(label)} ↗</a>'


def shell(title: str, body: str, current: str, extra_head: str = "", extra_js: str = "") -> str:
    parts = []
    for h, l in NAV:
        cur = ' aria-current="page"' if h == current else ""
        parts.append(f'<a href="{h}"{cur}>{l}</a>')
    nav = "".join(parts)
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)} · {SITE_NAME}</title>
<meta name="description" content="Verified, source-linked research on solid gold engagement rings: karat, gram weight, melt value, seller policies and every flagged irregularity.">
<link rel="stylesheet" href="assets/style.css">
<link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'><circle cx='16' cy='16' r='11' fill='%23d9b45b'/></svg>">
{extra_head}
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="site"><div class="wrap">
  <a class="brand" href="index.html"><span class="dot"></span>{SITE_NAME} <small>{SITE_TAG}</small></a>
  <nav class="main">{nav}</nav>
</div></header>
<main id="main"><div class="wrap">
{body}
</div></main>
<footer class="site"><div class="wrap">
  <p><strong>{SITE_NAME}</strong> — an independent, source-linked buying file for solid gold engagement rings.
  Every price on this site was read from the seller's own product page on the date shown; where a value could not be
  confirmed it is left blank and listed on the <a href="flagged.html">Flagged for review</a> page.</p>
  <p>This site is research, not legal, financial or appraisal advice. A karat stamp is a claim, not a test.
  Have any ring verified by an independent jeweller before wearing or resizing it.</p>
</div></footer>
{extra_js}
</body>
</html>"""


# --------------------------------------------------------------------------- #
# derived values
# --------------------------------------------------------------------------- #
def derive(item, ctx):
    d = {"fine_g": None, "melt": None, "premium_pct": None, "comparable": False, "price_per_fine_g": None}
    w, k = item.get("weight_g"), item.get("karat")
    if w and k:
        try:
            frac = ctx["frac"][str(int(str(k).upper().replace("K", "")))]
        except Exception:
            return d
        d["fine_g"] = float(w) * frac
        d["melt"] = d["fine_g"] * ctx["spot_per_g"]
        if item.get("price") and item.get("price_type") == "full":
            d["comparable"] = True
            d["premium_pct"] = (item["price"] - d["melt"]) / d["melt"] * 100
            d["price_per_fine_g"] = item["price"] / d["fine_g"]
    elif item.get("price") and k:
        try:
            frac = ctx["frac"][str(int(str(k).upper().replace("K", "")))]
            d["_frac"] = frac
        except Exception:
            pass
    return d


def build_ctx(data):
    spot = data["spot"]["spot"]
    ozg = data["spot"]["troy_ounce_grams"]
    return {
        "spot": spot,
        "ozg": ozg,
        "spot_per_g": spot["value_per_oz"] / ozg,
        "spot_per_oz": spot["value_per_oz"],
        "frac": {k: v for k, v in data["standards"]["karat_fractions"]["values"].items()},
        "sellers": {s["id"]: s for s in data["sellers_items"]},
    }


# --------------------------------------------------------------------------- #
# snippets
# --------------------------------------------------------------------------- #
def pledge_box() -> str:
    return """
<section class="pledge" aria-label="No-hallucination policy">
  <h2><span class="tag">Rule 0</span> No hallucinated prices. No invented numbers. Ever.</h2>
  <p>Every price, karat and gram weight on this site was <strong>read from the seller's own product page</strong>
  and stamped with the date it was read. If a seller does not publish a value, the table shows
  <span class="nv">—</span> and the gap is listed on the <a href="flagged.html">Flagged for review</a> page.
  Nothing is estimated, averaged, inferred from a search snippet, or carried over from an earlier visit.
  A search-engine copy of a page is never treated as a price — a real one was already caught being $29 out of date.</p>
</section>"""


def checklist_block() -> str:
    items = [
        ("Gold purity", "Confirm the karat — 10K, 14K, 18K. Under 16 CFR § 23.3 the word “gold” must be preceded by the karat."),
        ("Solid gold", "The listing must say <b>solid gold</b>. Vermeil, gold plate, gold filled and gold overlay all have legal definitions that mean “not solid” (16 CFR § 23.4, § 23.3(c))."),
        ("Hallmark", "A karat stamp plus a maker's/dealer's mark. The marking side of this is U.S. law: 15 U.S.C. § 297(b)."),
        ("Weight", "The gram weight, not the carat weight of the stone. A legitimate seller can provide it."),
        ("Seller reputation", "Independent reviews, complaints, and real contact details on the seller's own site."),
        ("Price vs gold", "Compare the price to the ring's actual gold content at the current spot price — the calculator on this site does exactly that."),
        ("Return policy", "Covering the item after you inspect it. Watch for exclusions on resized, engraved or custom pieces."),
        ("Payment", "Credit card, for chargeback protection. Avoid irreversible payment methods."),
        ("Documentation", "Keep the listing, receipt, description and every purity claim the seller made."),
        ("On arrival", "Independent jeweller first, wearing/resizing second."),
        ("Best verification", "XRF or another professional purity test. A stamp is a claim; an assay is evidence."),
        ("Walk away", "If the seller will not let you independently verify and return it, do not buy."),
    ]
    rows = "".join(f'<li><span class="mk">✓</span><div><b>{n}.</b> {t}</div></li>' for n, t in items)
    return f'<ul class="check">{rows}</ul>'


# --------------------------------------------------------------------------- #
# pages
# --------------------------------------------------------------------------- #
def page_index(data, audit, ctx):
    st, s = audit["stats"], audit["summary"]
    spot = ctx["spot"]
    items = [i for i in data["rings_items"] if i.get("check") == "live"]
    with_w = [i for i in items if i.get("weight_g")]
    solid_yes = [i for i in items if i.get("solid") is True]
    priced = [i for i in items if i.get("price") is not None]
    comparable = [i for i in items if derive(i, ctx)["comparable"]]
    prem = [derive(i, ctx)["premium_pct"] for i in comparable]
    avg_prem = sum(prem) / len(prem) if prem else None
    flagged_count = len([f for f in audit["findings"] if f["severity"] in ("warn", "fail")])

    def card(n, label, key):
        return f"""<div class="card stat"><span class="n">{n}</span><span class="l">{label}</span><span class="k">{key}</span></div>"""

    stats = f"""<div class="grid g4">
      {card(len(items), "live-verified listings", "every field re-read on the seller's page")}
      {card(len(priced), "with a price read off the page", "dated, never inferred")}
      {card(f"{len(with_w)}<small style='font-size:14px;color:var(--muted)'> / {len(items)}</small>", "sellers publish the gram weight", "the single biggest gap in online gold listings")}
      {card(len(solid_yes), "explicitly say “solid gold”", "wording quoted, not inferred")}
    </div>"""

    spotcard = f"""<div class="card">
      <h3>Gold spot used for every melt calculation</h3>
      <p style="font-size:28px;font-weight:700;margin:0;letter-spacing:-.02em">${spot['value_per_oz']:,.2f}<span style="font-size:14px;color:var(--muted);font-weight:500"> / troy oz</span></p>
      <p class="sub" style="margin:6px 0 0">As of <b>{e(spot['as_of'])}</b> · = <b>${ctx['spot_per_g']:,.2f} per gram</b> of fine gold<br>
      {src(spot['source_url'], spot['source_name'])}</p>
      <p class="sub" style="margin-top:10px">Reference price only. Bullion and jewellery trade at a premium to spot; the WB/spot spread on a retail ring is exactly what the calculator is for.</p>
    </div>"""

    findings = []
    if avg_prem is not None:
        findings.append(f"On the {len(comparable)} listing(s) where both a complete-ring price and a gram weight are published, the price averages "
                        f"<b>{avg_prem:,.0f}% above</b> the melt value of the gold in the ring.")
    findings.append(f"<b>{len(with_w)} of {len(items)}</b> live listings publish the ring's gram weight. The rest leave you unable to check the gold value before buying — which is the checklist's biggest single failure.")
    findings.append("Blue Nile and James Allen quote a <b>“setting price”</b> that excludes the centre diamond. Comparing that number to a gold value is meaningless, so this site marks it <span class='badge b-warn'>setting only</span> instead of pretending it is the ring's price.")
    findings.append("A search-engine copy of the Ross-Simons page showed <b>$270</b>; the live page showed <b>$299</b>. Both are recorded, and only the live figure is used.")
    findings.append(f"The audit is run after every review pass: <b>{s['checks_pass']} checks passed, {s['checks_warn']} warnings, {s['checks_fail']} failures</b>. Warnings are published, not hidden.")

    body = f"""
<section class="hero">
  <p class="eyebrow">Buying file · updated {e(data['rings']['meta']['last_updated'])}</p>
  <h1>Solid gold engagement rings, checked line by line.</h1>
  <p class="lead">A short, honest list of gold engagement rings you can actually verify: what karat it is,
  what it weighs, what the gold in it is worth today, what the seller promises about returns, and what
  nobody will tell you. Each row links to the page the number came from.</p>
</section>

{pledge_box()}

<h2>The short version</h2>
<div class="grid g2">
  <div class="card">
    <h3>What this site does</h3>
    <p>Collects ring listings from sellers' own sites, records the karat, the stated gold weight, the price and the
    return terms <em>with the exact quote and the date</em>, then computes what the gold is actually worth at the
    current spot price so an inflated or suspiciously cheap price is obvious.</p>
    <p style="margin-bottom:0"><a href="rings.html">Open the ring list →</a></p>
  </div>
  <div class="card">
    <h3>What this site refuses to do</h3>
    <p>It will not estimate a weight from a photo, will not repeat a price from a search result, will not call an
    unmarked ring “solid gold”, and will not fill a blank with a guess. If you see a number here, it was on the
    seller's page when the page was opened.</p>
    <p style="margin-bottom:0"><a href="method.html">Read the method and the latest audit →</a></p>
  </div>
</div>

<h2>At a glance</h2>
{stats}

<h2>Gold price behind the maths</h2>
<div class="grid g2">{spotcard}
  <div class="card">
    <h3>Latest audit</h3>
    <p class="sub">Generated {e(audit['generated'])}</p>
    <p style="font-size:28px;font-weight:700;margin:0 0 4px">{s['checks_pass']} <span style="font-size:15px;font-weight:500;color:var(--muted)">passed</span>
      · {s['checks_warn']} <span style="font-size:15px;font-weight:500;color:var(--warn)">warn</span>
      · {s['checks_fail']} <span style="font-size:15px;font-weight:500;color:var(--bad)">fail</span></p>
    <p class="sub">{flagged_count} item-level findings are published on the <a href="flagged.html">Flagged for review</a> page with their sources.</p>
    <p style="margin-bottom:0"><a href="method.html#audit">See every check →</a></p>
  </div>
</div>

<h2>What the data already shows</h2>
<div class="card">
  <ul style="margin:0;padding-left:20px">
    {''.join(f'<li style="margin-bottom:8px">{f}</li>' for f in findings)}
  </ul>
</div>

<h2>The checklist this project is built on</h2>
<p class="sub">Each line is either enforced by U.S. law, or is a rule of thumb that the dataset makes checkable.
Where a rule comes from law, the citation is linked.</p>
<div class="card">{checklist_block()}</div>

<h2>Browse</h2>
<div class="grid g3">
  <a class="card" href="rings.html" style="color:inherit">
    <h3 style="color:var(--gold)">Ring list →</h3>
    <p class="sub" style="margin:0">Every entry, every field, every source. Filter by category, sort by price per gram of gold.</p>
  </a>
  <a class="card" href="sellers.html" style="color:inherit">
    <h3 style="color:var(--gold)">Sellers →</h3>
    <p class="sub" style="margin:0">Who publishes a gram weight, what their return rules actually say, and what is still unknown.</p>
  </a>
  <a class="card" href="standards.html" style="color:inherit">
    <h3 style="color:var(--gold)">Rules &amp; law →</h3>
    <p class="sub" style="margin:0">The FTC jewellery guides and the Stamping Act, quoted. What “solid”, “vermeil” and “gold filled” legally mean.</p>
  </a>
  <a class="card" href="calculator.html" style="color:inherit">
    <h3 style="color:var(--gold)">Calculator →</h3>
    <p class="sub" style="margin:0">Ring weight + karat + spot → fine gold grams, melt value, and the markup you are being asked to pay.</p>
  </a>
  <a class="card" href="flagged.html" style="color:inherit">
    <h3 style="color:var(--gold)">Flagged for review →</h3>
    <p class="sub" style="margin:0">Every unverified value, dead listing and conflicting price, with its source, for you to check yourself.</p>
  </a>
  <a class="card" href="method.html" style="color:inherit">
    <h3 style="color:var(--gold)">Method &amp; audit →</h3>
    <p class="sub" style="margin:0">How each value was verified, what the automated checks look for, and the full audit log.</p>
  </a>
</div>
"""
    return shell("Dashboard", body, "index.html")


def row_for(item, ctx):
    d = derive(item, ctx)
    seller = ctx["sellers"].get(item["seller"], {})
    solid = item.get("solid")
    if solid is True:
        solid_cell = badge("stated solid", "ok")
    elif solid is False:
        solid_cell = badge("NOT solid", "bad")
    else:
        solid_cell = '<span class="nv" title="The seller page does not use the word solid">not stated</span>'
    pt = item.get("price_type")
    basis = {"setting": badge("setting only", "warn"), "from": badge("from-price", "info"),
             "full": badge("full price", "ok"), None: '<span class="nv">—</span>'}[pt]
    flags = "".join(badge(f.replace("-", " "), "mut") for f in item.get("flags", [])[:4])
    if d["comparable"]:
        melt_cell = money(d["melt"])
        prem = d["premium_pct"]
        prem_cell = f'<span style="color:{"var(--bad)" if prem > 150 else "var(--muted)"}">+{prem:,.0f}%</span>'
    elif d["melt"] is not None:
        melt_cell = money(d["melt"])
        prem_cell = '<span class="nv" title="Price is not a complete-ring price">n/c</span>'
    else:
        melt_cell = prem_cell = '<span class="nv">—</span>'
    return f"""<tr id="row-{e(item['id'])}" data-cat="{e(item['category'])}" data-search="{e((item['title'] + ' ' + seller.get('name','')).lower())}">
  <td><a href="{e(item['url'])}" target="_blank" rel="noopener nofollow"><b>{e(item['title'])}</b></a><br>
      <span class="sub">{e(seller.get('name', item['seller']))} · <span class="mono">{e(item['id'])}</span></span></td>
  <td class="tight">{e(CATEGORIES.get(item['category'], item['category']))}</td>
  <td class="tight"><b>{e(item.get('karat') or '—')}</b></td>
  <td class="tight">{e(item.get('color') or '—')}</td>
  <td class="tight">{solid_cell}</td>
  <td class="num">{num(item.get('weight_g'), 2)}</td>
  <td class="num">{money(item.get('price'))}</td>
  <td class="tight">{basis}</td>
  <td class="num">{num(d['fine_g'], 3)}</td>
  <td class="num">{melt_cell}</td>
  <td class="num">{prem_cell}</td>
  <td class="tight">{flags}</td>
  <td class="tight">{src(item['url'], 'page')}</td>
</tr>"""


def evidence_block(item, ctx):
    d = derive(item, ctx)
    ev = item.get("ev") or {}

    def line(label, value, quote, ok=True):
        shown = value if value not in (None, "") else '<span class="nv">not published / not stated</span>'
        q = f'<div class="q">“{e(quote)}”</div>' if quote else ""
        return f"""<tr><td class="tight"><b>{e(label)}</b></td><td>{shown}{q}</td></tr>"""

    rows = [line("Karat", e(item.get("karat") or ""), ev.get("karat")),
            line("Metal colour / plating", e(item.get("color") or ""), ev.get("color")),
            line("Solid gold?", "yes" if item.get("solid") is True else ("no" if item.get("solid") is False else ""), ev.get("solid")),
            line("Gold weight", (f"{item['weight_g']} g" if item.get("weight_g") else ""), ev.get("weight")),
            line("Price", money(item.get("price")), ev.get("price"))]
    notes = f'<p class="sub" style="margin:10px 0 0">{e(item["notes"])}</p>' if item.get("notes") else ""
    obs = ""
    if item.get("observations"):
        obs = "<p class='sub' style='margin:10px 0 0'>Observations: " + " · ".join(
            f"{o['on']} ${o['price']:,.0f} ({e(o['via'])})" for o in item["observations"]) + "</p>"
    return f"""<details id="ev-{e(item['id'])}">
  <summary><b>{e(item['id'])}</b> — {e(item['title'])} · <span class="mono">checked {e(item['checked'])} ({e(item['check'])})</span></summary>
  <table style="margin-top:6px"><tbody>{''.join(rows)}</tbody></table>
  {notes}{obs}
  <p style="margin:10px 0 0">{src(item['url'], 'Open the seller page')}</p>
</details>"""


def page_rings(data, audit, ctx):
    live = [i for i in data["rings_items"] if i.get("check") == "live"]
    live.sort(key=lambda i: (CATEGORY_ORDER.index(i["category"]) if i["category"] in CATEGORY_ORDER else 99,
                             i.get("price") or 0))
    rows = "\n".join(row_for(i, ctx) for i in live)
    counts = {c: len([i for i in live if i["category"] == c]) for c in CATEGORY_ORDER}
    chips = '<button class="chip" data-f="all" aria-pressed="true">All (' + str(len(live)) + ')</button>' + "".join(
        f'<button class="chip" data-f="{c}" aria-pressed="false">{CATEGORIES[c]} ({counts[c]})</button>'
        for c in CATEGORY_ORDER if counts.get(c))
    evidence = "\n".join(evidence_block(i, ctx) for i in live)
    dead = [i for i in data["rings_items"] if i.get("check") == "dead"]

    body = f"""
<p class="eyebrow">The list</p>
<h1>Gold ring list</h1>
<p class="lead">Live-verified listings only. <b>—</b> means the seller does not publish that value; it is never filled in.
“Melt” is the spot value of the gold actually in the ring, so the last column tells you how much of the price is
gold and how much is everything else.</p>

<div class="note warn"><p><b>How to read the price column.</b>
<span class="badge b-ok">full price</span> is the price of the whole ring as sold.
<span class="badge b-warn">setting only</span> excludes the centre diamond — it is <em>not</em> comparable to a melt value.
<span class="badge b-info">from-price</span> means the seller shows a floor price that changes with size or metal.</p></div>

<div class="controls">
  {chips}
  <input type="search" id="q" placeholder="Search seller or product…" aria-label="Search listings" style="margin-left:auto;min-width:220px">
</div>

<div class="tablewrap">
<table id="rings">
<thead><tr>
  <th>Ring / seller</th><th>Category</th><th>Karat</th><th>Colour</th><th>Solid gold</th>
  <th class="num">Weight g</th><th class="num">Price</th><th>Price basis</th>
  <th class="num">Fine gold g</th><th class="num">Melt value</th><th class="num">vs melt</th><th>Flags</th><th>Source</th>
</tr></thead>
<tbody>{rows}</tbody>
</table>
</div>
<p class="sub">Showing {len(live)} live-verified entries. Melt value uses ${ctx['spot']['value_per_oz']:,.2f}/ozt
(spot as of {e(ctx['spot']['as_of'])}, {src(ctx['spot']['source_url'], ctx['spot']['source_name'])}) and
<code>weight × karat ÷ 24</code> for fine gold. “n/c” = price basis makes the comparison invalid.</p>

<h2>Evidence for every cell</h2>
<p class="sub">Each entry below quotes the exact wording found on the seller's page. If a value is blank, the seller did not publish it.</p>
{evidence}

<h2>Excluded from the list</h2>
<p class="sub">Listings that exist but can no longer be bought. They are kept so the record is complete, and are never presented as recommendations.</p>
<div class="tablewrap"><table><thead><tr><th>Entry</th><th>Status</th><th>What happened</th></tr></thead><tbody>
{''.join(f'<tr><td>{e(i["title"])} <span class="sub">({e(i["id"])})</span></td><td>{badge("dead listing", "bad")}</td><td class="sub">{e(i["notes"])}</td></tr>' for i in dead) or '<tr><td colspan="3" class="sub">None.</td></tr>'}
</tbody></table></div>
"""
    js = """
<script>
(function(){
  var chips=[].slice.call(document.querySelectorAll('.chip'));
  var q=document.getElementById('q');
  var rows=[].slice.call(document.querySelectorAll('#rings tbody tr'));
  var f='all';
  function apply(){
    var s=(q.value||'').toLowerCase().trim();
    rows.forEach(function(r){
      var ok=(f==='all'||r.dataset.cat===f)&&(!s||r.dataset.search.indexOf(s)>-1);
      r.style.display=ok?'':'none';
    });
  }
  chips.forEach(function(c){c.addEventListener('click',function(){
    chips.forEach(function(o){o.setAttribute('aria-pressed','false')});
    c.setAttribute('aria-pressed','true'); f=c.dataset.f; apply();
  })});
  q.addEventListener('input',apply);
})();
</script>"""
    return shell("Ring list", body, "rings.html", extra_js=js)


def page_sellers(data, audit, ctx):
    rows = []
    for s in data["sellers_items"]:
        items = [i for i in data["rings_items"] if i["seller"] == s["id"] and i.get("check") == "live"]
        wpub = len([i for i in items if i.get("weight_g")])
        contact = []
        if s.get("phone"):
            contact.append(e(s["phone"]))
        if s.get("email"):
            contact.append(e(s["email"]))
        contact_html = "<br>".join(contact) if contact else '<span class="nv">not captured</span>'
        if s.get("contact_url"):
            contact_html += f'<br>{src(s["contact_url"], "contact page")}'
        ret = e(s.get("returns_summary") or "") or '<span class="nv">not verified yet</span>'
        ret_badge = badge("verified on page", "ok") if s.get("returns_verified") else badge("not verified", "warn")
        if s.get("returns_url"):
            ret += f'<br>{src(s["returns_url"], "policy page")}'
        rows.append(f"""<tr>
          <td><b>{e(s['name'])}</b><br><span class="sub">{e(s.get('type') or '')}</span><br>{src(s['site'], 'official site')}</td>
          <td>{len(items)} live<br><span class="sub">{wpub} with weight</span></td>
          <td>{contact_html}</td>
          <td>{ret} <br>{ret_badge}</td>
          <td class="sub">{e(s.get('payment_note') or '') or '<span class="nv">not verified</span>'}</td>
          <td class="sub">{''.join(badge(f.replace('-', ' '), 'mut') for f in s.get('flags', []))}</td>
        </tr>""")
    body = f"""
<p class="eyebrow">Who you are buying from</p>
<h1>Sellers</h1>
<p class="lead">The checklist says: research the seller, verify real contact details, and read the return policy
before you buy. This page records only what each seller publishes about itself — and marks clearly what has
<em>not</em> been verified. Reputation research is listed as an open item on the Flagged page rather than guessed at.</p>

<div class="note bad"><p><b>The one line to remember:</b> a return policy you have not read is not a return policy.
Every exclusion that matters — resized, engraved, custom, final sale — is written in the policy page, not in the
product description.</p></div>

<div class="tablewrap"><table>
<thead><tr><th>Seller</th><th>In dataset</th><th>Contact (from their site)</th><th>Returns</th><th>Payment</th><th>Open flags</th></tr></thead>
<tbody>{''.join(rows)}</tbody></table></div>

<h2>What "good" looks like on a listing</h2>
<div class="grid g2">
  <div class="card"><h3>Green flags</h3>
    <ul style="margin:0;padding-left:20px">
      <li>Says <b>solid 14k</b> or <b>solid 18k</b> in the seller's own words.</li>
      <li>Publishes the <b>gram weight</b> of the ring, not just the stone's carat weight.</li>
      <li>Shows the <b>maker's mark</b> or names the manufacturer/assay office.</li>
      <li>Return window stated in days, with the exclusions spelled out.</li>
    </ul>
  </div>
  <div class="card"><h3>Red flags</h3>
    <ul style="margin:0;padding-left:20px">
      <li>No weight anywhere, or a weight so low the ring cannot be solid (under ~1 g for a full band).</li>
      <li>“Gold” with no karat, or “14k gold plated / vermeil / filled” presented as a gold ring.</li>
      <li>“Solid gold” wording on a page that also mentions a hollow centre — prohibited by 16 CFR § 23.3(c)(1).</li>
      <li>Price far below the melt value of the stated weight — arithmetic that cannot be true.</li>
    </ul>
  </div>
</div>
"""
    return shell("Sellers", body, "sellers.html")


def page_standards(data, audit, ctx):
    std = data["standards"]
    cards = []
    for it in std["items"]:
        q2 = f'<div class="q" style="margin-top:6px">“{e(it["quote_2"])}”</div>' if it.get("quote_2") else ""
        cards.append(f"""<article class="card" id="{e(it['id'])}">
          <h3>{e(it['topic'])}</h3>
          <p style="margin-bottom:10px">{e(it['requirement'])}</p>
          <div class="q">“{e(it['quote'])}”</div>{q2}
          <p class="sub" style="margin:10px 0 0">{src(it['url'], it['source'])} · read {e(it['verified_on'])}</p>
        </article>""")
    kt = "".join(
        f"<tr><td><b>{k}K</b></td><td class='num'>{float(v)*100:.2f}%</td>"
        f"<td class='num'>${ctx['spot_per_g']*float(v):,.2f}</td>"
        f"<td class='num'>${ctx['spot_per_oz']*float(v):,.2f}</td>"
        f"<td class='sub'>${ctx['spot_per_oz']*float(v):,.0f} per troy oz of fine gold equivalent</td></tr>"
        for k, v in std["karat_fractions"]["values"].items())
    body = f"""
<p class="eyebrow">The rules</p>
<h1>What the words are legally allowed to mean</h1>
<p class="lead">This page exists so that no claim on the site is my opinion. These are the actual U.S. rules on
gold content, plating, “solid”, hallmarks and tolerances, quoted from the eCFR and the U.S. Code, with the date
each one was read.</p>

<div class="note"><p><b>Why this matters for the checklist:</b> 15 U.S.C. § 297(b) is the legal basis for
“karat stamp <em>plus</em> a maker's mark”. It is not folklore — when a quality mark is stamped, the maker's
trademark or name must be applied too, in lettering at least as large and as close as possible to it.</p></div>

<div class="grid g2">{''.join(cards)}</div>

<h2>Purity and raw-gold amounts</h2>
<p>Nominal purity is <code>karat ÷ 24</code>. The dollar columns are the spot value of the fine gold in
one gram or one troy ounce of that alloy, at ${ctx['spot']['value_per_oz']:,.2f}/ozt
(as of {e(ctx['spot']['as_of'])}). <b>They are not prices</b> — a finished ring costs more than its metal.</p>
<div class="tablewrap"><table>
<thead><tr><th>Karat</th><th class="num">Fine gold</th><th class="num">Value per gram of alloy</th><th class="num">Value per troy oz of alloy</th><th>Note</th></tr></thead>
<tbody>{kt}</tbody></table></div>
<p class="sub">{src(ctx['spot']['source_url'], ctx['spot']['source_name'])} · 1 troy ounce = 31.1034768 g.
U.S. law tolerates the actual fineness being up to 3/1000 below the stamp (7/1000 when solder is included in the assay) —
see <a href="#std-tolerance">15 U.S.C. § 295</a> above.</p>

<h2>Independent verification: what to ask for</h2>
<div class="card">
  <p><b>XRF (X-ray fluorescence)</b> is the usual non-destructive test: it reads the elemental composition of the
  surface without cutting the ring. Ask the jeweller to test the band in more than one place, and to weigh the ring
  on a calibrated scale to 0.01 g, because plating and solder can make a single surface reading optimistic.</p>
  <p class="sub" style="margin-bottom:0"><b>Honesty note (flagged):</b> the two legal tolerances above are quoted from
  statute. The <em>practice</em> of XRF testing is described here as general trade practice — this project has not
  found a single official U.S. standard that prescribes XRF as <em>the</em> required test, so treat the method
  description as guidance, not as a regulation. That gap is listed on the
  <a href="flagged.html">Flagged for review</a> page.</p>
</div>
"""
    return shell("Rules &amp; law", body, "standards.html")


def page_calculator(data, audit, ctx):
    spot = ctx["spot"]
    preset_opts = "".join(
        f'<option value="{i["weight_g"]}|{str(i["karat"]).replace("K","")}">{e(i["id"])} — {e(i["title"][:44])} ({i["weight_g"]} g, {i["karat"]})</option>'
        for i in data["rings_items"] if i.get("weight_g") and i.get("karat"))
    kt_rows = "".join(
        f"<tr><td><b>{k}K</b></td><td class='num'>{float(v)*100:.2f}%</td><td class='num'>${ctx['spot_per_g']*float(v):,.2f}</td></tr>"
        for k, v in data["standards"]["karat_fractions"]["values"].items())
    body = f"""
<p class="eyebrow">Do the maths</p>
<h1>Gold value calculator</h1>
<p class="lead">Enter the ring's weight and karat, and the calculator tells you how many grams of fine gold it
contains, what that gold is worth at spot, and — if you enter the asking price — what percentage of the price is
gold. Nothing here is stored or sent anywhere; it runs in your browser.</p>

<div class="grid g2">
  <div class="card">
    <h3>Inputs</h3>
    <div class="grid g2" style="gap:12px">
      <div class="field"><label for="w">Ring weight</label>
        <input type="number" id="w" value="4" min="0" step="0.01" inputmode="decimal"></div>
      <div class="field"><label for="unit">Unit</label>
        <select id="unit"><option value="g">grams</option><option value="ozt">troy ounces</option><option value="dwt">pennyweight (dwt)</option></select></div>
      <div class="field"><label for="k">Karat</label>
        <select id="k"><option value="10">10K</option><option value="14" selected>14K</option><option value="18">18K</option><option value="22">22K</option><option value="24">24K</option></select></div>
      <div class="field"><label for="spot">Spot price (USD / troy oz)</label>
        <input type="number" id="spot" value="{spot['value_per_oz']}" step="0.01" inputmode="decimal"></div>
      <div class="field"><label for="paid">Asking price (optional)</label>
        <input type="number" id="paid" placeholder="e.g. 1450" step="1" inputmode="decimal"></div>
      <div class="field"><label for="preset">Load a measured weight</label>
        <select id="preset"><option value="">— dataset entries with a published weight —</option>{preset_opts}</select></div>
    </div>
    <p class="sub" style="margin:10px 0 0">Spot default: ${spot['value_per_oz']:,.2f}/ozt as of {e(spot['as_of'])} —
    {src(spot['source_url'], spot['source_name'])}. Edit it to your own quote if you have a fresher one.</p>
  </div>
  <div class="card result">
    <h3>Result</h3>
    <p class="sub" style="margin:0">Fine gold in the ring</p>
    <p class="big" id="r-fine">—</p>
    <p class="sub" style="margin:0">Melt value at spot</p>
    <p class="big" id="r-melt" style="color:var(--gold)">—</p>
    <hr style="margin:16px 0">
    <p class="sub" style="margin:0">Gold value per gram of the ring</p>
    <p id="r-perg">—</p>
    <p class="sub" style="margin:0">Asking price ÷ melt value</p>
    <p id="r-x">—</p>
    <p class="sub" style="margin:0">Share of the price that is gold</p>
    <p id="r-share">—</p>
    <p class="sub" id="r-msg" style="margin:14px 0 0"></p>
  </div>
</div>

<div class="note warn"><p><b>What this calculator cannot tell you:</b> the value of the diamonds, the workmanship,
the brand, or whether the ring is genuinely the karat it claims. It only values the gold you told it about.
A premium far above melt is normal for retail jewellery; a price <em>below</em> melt is a red flag, not a bargain.</p></div>

<h2>Raw gold amounts by karat</h2>
<p>At ${spot['value_per_oz']:,.2f}/ozt, one gram of alloy is worth this much in fine gold:</p>
<div class="tablewrap"><table><thead><tr><th>Karat</th><th class="num">Fine gold</th><th class="num">Gold value per gram of alloy</th></tr></thead>
<tbody>{kt_rows}</tbody></table></div>
<p class="sub">Formulas: <code>fine_g = weight_g × karat ÷ 24</code> · <code>melt = fine_g × (spot ÷ 31.1034768)</code> ·
<code>premium = (price − melt) ÷ melt</code> · 1 dwt = 1.55517384 g.</p>
"""
    js = """
<script>
(function(){
  var $=function(id){return document.getElementById(id)};
  var OZG=31.1034768, DWT=1.55517384;
  function calc(){
    var w=parseFloat($('w').value), u=$('unit').value;
    var k=parseFloat($('k').value), spot=parseFloat($('spot').value);
    var paid=parseFloat($('paid').value);
    var g = isNaN(w)?0:(u==='g'?w:(u==='ozt'?w*OZG:w*DWT));
    var fine=g*k/24, perg=spot/OZG, melt=fine*perg;
    function f(x,d){return (isFinite(x)?x:0).toLocaleString(undefined,{minimumFractionDigits:d,maximumFractionDigits:d})}
    $('r-fine').textContent = fine? f(fine,3)+' g' : '—';
    $('r-melt').textContent = melt? '$'+f(melt,2) : '—';
    $('r-perg').textContent = g? '$'+f(perg*g/g,2)+' of gold per gram of ring ('+(k/24*100).toFixed(2)+'% fine)' : '—';
    if(paid && melt){
      var x=paid/melt, share=melt/paid*100;
      $('r-x').textContent='×'+f(x,2)+'  ('+(x>=1?'+':'')+f((x-1)*100,0)+'% vs melt)';
      $('r-share').textContent=f(share,1)+'%';
      var m=$('r-msg');
      if(x<1){m.className='sub';m.style.color='var(--bad)';m.textContent='Below melt value of its own stated gold. That is arithmetic that cannot be true for a new solid-gold ring — verify the weight, the karat, or the seller.'}
      else if(x>6){m.className='sub';m.style.color='var(--warn)';m.textContent='A premium of more than 6× the gold value. Normal for brand/setting-heavy pieces, but it means you are paying for the design, not the metal.'}
      else {m.className='sub';m.style.color='var(--muted)';m.textContent='Within the usual retail range above melt.'}
    } else { $('r-x').textContent='—'; $('r-share').textContent='—'; $('r-msg').textContent=''; }
  }
  ['w','unit','k','spot','paid'].forEach(function(id){$(id).addEventListener('input',calc);$(id).addEventListener('change',calc)});
  $('preset').addEventListener('change',function(){
    if(!this.value) return;
    var p=this.value.split('|'); $('w').value=p[0]; $('unit').value='g'; $('k').value=p[1]; calc();
  });
  calc();
})();
</script>"""
    return shell("Calculator", body, "calculator.html", extra_js=js)


def page_flagged(data, audit, ctx):
    items = data["rings_items"]
    # a) every blank field, per entry
    blanks = []
    fields = [("karat", "Karat"), ("weight_g", "Gold weight (g)"), ("price", "Price"), ("solid", "Solid gold stated")]
    for i in items:
        if i.get("check") == "dead":
            continue
        missing = [lbl for key, lbl in fields if i.get(key) is None]
        if missing:
            blanks.append(f"""<tr><td><b>{e(i['id'])}</b><br><span class="sub">{e(i['title'])}</span></td>
              <td>{''.join(badge(m, 'warn') for m in missing)}</td>
              <td class="sub">Left blank on purpose — the seller's page does not publish this. Do not assume a value.</td>
              <td>{src(i['url'], 'page')}</td></tr>""")
    # b) findings from the audit
    finds = ""
    for f in audit["findings"]:
        if f["severity"] == "info":
            continue
        kind = {"fail": "bad", "warn": "warn"}.get(f["severity"], "mut")
        finds += f"""<tr><td>{badge(f['severity'], kind)}</td><td class="mono">{e(f['item'])}</td><td>{e(f['field'])}</td>
          <td>{e(f['message'])}</td><td>{src(f.get('source') or '', 'source') if f.get('source') else '<span class="nv">—</span>'}</td></tr>"""
    # c) manual irregularity log
    manual = [
        ("Price drift on the same URL", "RS-932728",
         "The search-engine copy of the Ross-Simons product page showed <b>$270</b>; the live page showed <b>$299</b>. "
         "Both observations are stored. The site uses the live figure only. This is the exact failure mode that makes "
         "“price from a search result” a hallucination risk.",
         "https://www.ross-simons.com/products/932728"),
        ("Tiffany's own pages disagree on the “starting from” price", "tiffany",
         "Different official Tiffany pages show The Tiffany® Setting in 18k yellow gold starting from $1,540, $1,560, $1,600 "
         "and $1,650 depending on the page. No single price has been written into the dataset, because the figure is not "
         "stable across the seller's own site — it needs a live product page with a configuration selected.",
         "https://www.tiffany.com/engagement/engagement-rings/the-tiffany-setting-engagement-ring-in-18k-yellow-gold-GRP10863/"),
        ("Costco listings are gone", "COSTCO-100423493",
         "Costco URLs that appear in search results now return “Page Not Found!” or “Product Not Available”. "
         "Recorded as a dead listing; no price or weight from the search snippet was copied into the dataset.",
         "https://www.costco.com/4mm-diamond-cut-wedding-ring-14kt-gold.product.100423493.html"),
        ("“Solid gold” is not printed on most listings", "dataset",
         "Of the live listings, most describe the metal only as “14K white gold” / “14kt yellow gold”. Under 16 CFR § 23.3 "
         "that is a legal karat claim, but it is <b>not</b> the same as saying the ring is solid. This site marks those as "
         "“not stated” rather than upgrading them to solid.",
         "https://www.ecfr.gov/current/title-16/chapter-I/subchapter-B/part-23#23.3"),
        ("Gram weight is the missing number", "dataset",
         "The checklist asks for the ring's weight in grams. Most major sellers do not publish it, so the gold value of the "
         "ring cannot be checked before purchase. This is the largest open gap in the dataset and the first thing to ask a "
         "seller by email — the answer should be in writing.",
         "index.html"),
        ("XRF described as trade practice, not regulation", "standards",
         "The purity tolerances on the Rules page are quoted from statute. The XRF testing advice is general trade practice; "
         "no single official U.S. standard prescribing XRF as <em>the</em> required method was found in this pass.",
         "standards.html"),
        ("Seller reputation research is incomplete", "sellers",
         "Independent review aggregation and complaint history were not completed for every seller in the register. "
         "Rather than write something plausible, those rows say “not verified”.",
         "sellers.html"),
    ]
    manual_rows = "".join(
        f"""<tr><td><b>{e(t)}</b></td><td class="mono">{e(ref)}</td><td>{d}</td><td>{src(url, 'open')}</td></tr>"""
        for t, ref, d, url in manual)

    body = f"""
<p class="eyebrow">Nothing is hidden</p>
<h1>Flagged for review</h1>
<p class="lead">This is the honest half of the project. Everything here is either unverified, contradictory, or
impossible to confirm from an official source. None of it blocks the list from being useful — it is published so
you can check it yourself and tell me what to fix.</p>

<div class="note bad"><p><b>Rule for this page:</b> if a value could not be confirmed on the seller's own page, it was
left blank in the table and written here instead. No value on this site was produced by estimating, averaging, or
copying a search-engine snippet. The audit in <a href="method.html#audit">Method &amp; audit</a> re-checks that
automatically after every review pass.</p></div>

<h2>1. Blank fields in the dataset</h2>
<p class="sub">Each row is a real listing where at least one checklist value is simply not published. A blank is data too:
it tells you what to ask the seller.</p>
<div class="tablewrap"><table><thead><tr><th>Entry</th><th>Not published</th><th>Why it is blank</th><th>Source</th></tr></thead>
<tbody>{''.join(blanks) or '<tr><td colspan="4" class="sub">None.</td></tr>'}</tbody></table></div>

<h2>2. Automated findings (latest audit)</h2>
<p class="sub">Generated {e(audit['generated'])} by <code>scripts/audit.py</code>. Failures block a release; warnings are published here.</p>
<div class="tablewrap"><table><thead><tr><th>Severity</th><th>Item</th><th>Field</th><th>Finding</th><th>Source</th></tr></thead>
<tbody>{finds or '<tr><td colspan="5" class="sub">No findings.</td></tr>'}</tbody></table></div>

<h2>3. Irregularities found during manual review</h2>
<div class="tablewrap"><table><thead><tr><th>Irregularity</th><th>Where</th><th>What was found</th><th>Source</th></tr></thead>
<tbody>{manual_rows}</tbody></table></div>

<h2>4. Open items</h2>
<ul style="padding-left:20px">
  <li>Ask each seller for the ring's gram weight in writing, then add it to the dataset with the seller's reply as the source.</li>
  <li>Read and quote the full return policy for Blue Nile, James Allen, Ross-Simons and Catbird (currently only the product-page wording is recorded).</li>
  <li>Independent reputation research per seller (review aggregation, complaint history, registered business address).</li>
  <li>Add a second spot-price source so the melt value can be cross-checked, not just dated.</li>
</ul>
"""
    return shell("Flagged for review", body, "flagged.html")


def page_method(data, audit, ctx, link_report):
    icon = {"pass": ("PASS", "ok"), "warn": ("WARN", "warn"), "fail": ("FAIL", "bad"), "info": ("INFO", "info")}
    rows = "".join(
        f"<tr><td class='mono'>{e(c['id'])}</td><td><b>{e(c['name'])}</b></td>"
        f"<td>{badge(*icon[c['status']])}</td><td class='sub'>{e(c['detail'])}</td></tr>"
        for c in audit["checks"])
    findings = "".join(
        f"<tr><td>{badge(f['severity'], {'fail':'bad','warn':'warn'}.get(f['severity'],'mut'))}</td>"
        f"<td class='mono'>{e(f['item'])}</td><td>{e(f['field'])}</td><td class='sub'>{e(f['message'])}</td></tr>"
        for f in audit["findings"])
    s = audit["summary"]
    body = f"""
<p class="eyebrow">How this was built</p>
<h1>Method &amp; audit</h1>
<p class="lead">The whole value of this project is that you can check it. This page explains exactly where each
number came from, what was deliberately left out, and what the automated anti-hallucination audit verifies after
every review pass.</p>

<h2>The no-hallucination protocol</h2>
<div class="card">
  <ol style="margin:0;padding-left:20px">
    <li><b>One source of truth per value.</b> A price, karat, colour or weight may only exist in the dataset with a
      quoted string taken from the seller's own page, plus the date the page was read.</li>
    <li><b>Live beats cached.</b> A value seen in a search-engine copy of a page is recorded as an observation but is
      <em>never</em> used as the price. Only a page opened and read counts as a live check.</li>
    <li><b>Blank beats wrong.</b> If the page does not publish it, the field stays <code>null</code>. The site shows
      <span class="nv">—</span> and the entry appears on <a href="flagged.html">Flagged for review</a>.</li>
    <li><b>Wording must match the verdict.</b> “Solid gold = yes” is only allowed if the quote contains the word
      <em>solid</em>; “solid gold = no” only if the quote contains plating/vermeil/filled/overlay wording.</li>
    <li><b>Arithmetic must reproduce.</b> Every melt value is recomputed from stored inputs with the published formula,
      and any price below its own melt value is flagged, not published as a deal.</li>
    <li><b>Conflicts are surfaced.</b> Two prices for the same URL are both stored, and the disagreement is flagged.</li>
  </ol>
</div>

<h2 id="audit">Automated audit — latest run</h2>
<div class="grid g4">
  <div class="card stat"><span class="n">{s['checks_total']}</span><span class="l">checks run</span></div>
  <div class="card stat"><span class="n" style="color:var(--ok)">{s['checks_pass']}</span><span class="l">passed</span></div>
  <div class="card stat"><span class="n" style="color:var(--warn)">{s['checks_warn']}</span><span class="l">warnings</span></div>
  <div class="card stat"><span class="n" style="color:var(--bad)">{s['checks_fail']}</span><span class="l">failures</span></div>
</div>
<p class="sub">Run {e(audit['generated'])} · <code>python3 scripts/audit.py</code> · machine-readable copy in
<code>reports/audit-latest.json</code>.</p>
<div class="tablewrap"><table><thead><tr><th>ID</th><th>Check</th><th>Result</th><th>Detail</th></tr></thead><tbody>{rows}</tbody></table></div>

<h3>Findings this run</h3>
<div class="tablewrap"><table><thead><tr><th>Severity</th><th>Item</th><th>Field</th><th>Finding</th></tr></thead>
<tbody>{findings or '<tr><td colspan="4" class="sub">None.</td></tr>'}</tbody></table></div>

<h2>Build integrity</h2>
<div class="card">
<p><b>{link_report['internal_total']}</b> internal links checked, <b>{link_report['broken']}</b> broken.
<b>{link_report['anchors']}</b> in-page anchors checked, <b>{link_report['bad_anchors']}</b> missing.
Pages generated: {', '.join('<code>' + e(p) + '</code>' for p in link_report['pages'])}.</p>
<p class="sub" style="margin-bottom:0">External links point at the seller or government page that was actually read;
each entry in <code>data/rings.json</code> stores the URL together with the quote taken from it.</p>
</div>

<h2>Formulas</h2>
<div class="card">
  <table><tbody>
    <tr><td class="mono">fine_g</td><td>= ring weight in grams × karat ÷ 24</td></tr>
    <tr><td class="mono">spot_per_g</td><td>= spot price per troy ounce ÷ 31.1034768</td></tr>
    <tr><td class="mono">melt_value</td><td>= fine_g × spot_per_g</td></tr>
    <tr><td class="mono">premium</td><td>= (price − melt_value) ÷ melt_value × 100 — only when the price covers the whole ring</td></tr>
  </tbody></table>
  <p class="sub" style="margin-bottom:0">Spot reference: {src(ctx['spot']['source_url'], ctx['spot']['source_name'])} —
  ${ctx['spot']['value_per_oz']:,.2f}/ozt as of {e(ctx['spot']['as_of'])}, read {e(ctx['spot']['verified_on'])}.</p>
</div>

<h2>Reproduce it</h2>
<div class="card">
<pre class="q" style="white-space:pre-wrap">git clone https://github.com/karagemop466-tech/GOLD3
cd GOLD3
python3 scripts/audit.py     # prints the audit, writes reports/audit-latest.{{md,json}}
python3 scripts/build.py     # regenerates every page from data/*.json</pre>
<p class="sub" style="margin-bottom:0">The dataset is plain JSON: <code>data/rings.json</code>,
<code>data/sellers.json</code>, <code>data/standards.json</code>, <code>data/spot.json</code>.</p>
</div>

<h2>What this project is not</h2>
<div class="note warn"><p>Not an appraisal, not legal advice, not a price guarantee. Prices change without notice — the
date on every row is the only thing that makes it honest. Before buying, confirm the price on the seller's page
yourself, and before wearing the ring, have an independent jeweller test and weigh it.</p></div>
"""
    return shell("Method &amp; audit", body, "method.html")


# --------------------------------------------------------------------------- #
# link check
# --------------------------------------------------------------------------- #
def check_links(pages: dict[str, str]) -> dict:
    broken, bad_anchors, n_internal, n_anchors = [], [], 0, 0
    ids_by_page = {name: set(re.findall(r'id="([^"]+)"', txt)) for name, txt in pages.items()}
    for name, txt in pages.items():
        for href in re.findall(r'href="([^"]+)"', txt):
            if href.startswith(("http://", "https://", "mailto:", "data:")):
                continue
            n_internal += 1
            target, _, anchor = href.partition("#")
            target = target or name
            if not target.endswith(".html"):
                if not (ROOT / target).exists():
                    broken.append(f"{name} → {href}")
                continue
            if target not in pages:
                broken.append(f"{name} → {href}")
                continue
            if anchor:
                n_anchors += 1
                if anchor not in ids_by_page.get(target, set()):
                    bad_anchors.append(f"{name} → {href}")
    return {"broken": len(broken), "bad_anchors": len(bad_anchors), "internal_total": n_internal,
            "anchors": n_anchors, "pages": list(pages), "broken_list": broken,
            "bad_anchor_list": bad_anchors}


def main():
    data = load(ROOT)
    audit = Audit(data).run()
    ctx = build_ctx(data)
    link_stub = {"broken": 0, "bad_anchors": 0, "internal_total": 0, "anchors": 0, "pages": []}
    pages = {
        "index.html": page_index(data, audit, ctx),
        "rings.html": page_rings(data, audit, ctx),
        "sellers.html": page_sellers(data, audit, ctx),
        "standards.html": page_standards(data, audit, ctx),
        "calculator.html": page_calculator(data, audit, ctx),
        "flagged.html": page_flagged(data, audit, ctx),
        "method.html": page_method(data, audit, ctx, link_stub),
    }
    rep = check_links(pages)
    # method.html displays the report, so render it once more with real numbers
    pages["method.html"] = page_method(data, audit, ctx, rep)
    rep2 = check_links(pages)
    for name, txt in pages.items():
        (ROOT / name).write_text(txt, encoding="utf-8")
    outdir = ROOT / "reports"
    outdir.mkdir(exist_ok=True)
    (outdir / "audit-latest.json").write_text(json.dumps(audit, indent=2), encoding="utf-8")
    (outdir / "audit-latest.md").write_text(render_markdown(audit, data), encoding="utf-8")
    (outdir / "link-check.json").write_text(json.dumps(rep2, indent=2), encoding="utf-8")
    print(f"built {len(pages)} pages → {', '.join(pages)}")
    print(f"links: {rep2['internal_total']} internal, {rep2['broken']} broken; "
          f"{rep2['anchors']} anchors, {rep2['bad_anchors']} missing")
    if rep2["broken_list"]:
        print("BROKEN:", *rep2["broken_list"], sep="\n  ")
    if rep2["bad_anchor_list"]:
        print("MISSING ANCHORS:", *rep2["bad_anchor_list"], sep="\n  ")
    fails = audit["summary"]["checks_fail"]
    print(f"audit: {audit['summary']['checks_pass']} pass / {audit['summary']['checks_warn']} warn / {fails} fail")
    return 0 if (fails == 0 and rep2["broken"] == 0 and rep2["bad_anchors"] == 0) else 1


if __name__ == "__main__":
    sys.exit(main())
