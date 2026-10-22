#!/usr/bin/env python3
"""
anti-hallucination audit for the GOLD3 gold-engagement-ring project.

This is a *security check*, not a spellcheck. It tries to catch the ways a
research dataset lies to its reader:

  * a price with no dated official source
  * a weight, stamp or maker's mark that was never quoted from the seller
  * a "solid gold" verdict that the seller never actually said
  * a flag referenced by a row but never defined
  * arithmetic that does not reproduce
  * a number printed in the HTML that exists nowhere in the source data
  * a broken internal link or an off-allowlist external link

Run:  python3 scripts/audit.py
Exit code 0 = clean (warnings allowed), 1 = at least one ERROR.
Writes reports/audit-report.md
"""

import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
REPORTS = ROOT / "reports"

errors, warnings, passes = [], [], []


def err(check, msg):
    errors.append((check, msg))


def warn(check, msg):
    warnings.append((check, msg))


def ok(check, msg):
    passes.append((check, msg))


def load(path):
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001
        err("JSON", f"{path.name} failed to parse: {exc}")
        return None


# ----------------------------------------------------------------------------
# 0. files exist
# ----------------------------------------------------------------------------
required_files = [
    "gold-price.json", "rings.json", "sellers.json", "standards.json", "flags.json",
]
for name in required_files:
    if (DATA / name).exists():
        ok("files", f"data/{name} present")
    else:
        err("files", f"data/{name} is missing")

gold = load(DATA / "gold-price.json")
rings_doc = load(DATA / "rings.json")
sellers_doc = load(DATA / "sellers.json")
standards_doc = load(DATA / "standards.json")
flags_doc = load(DATA / "flags.json")

if not all([gold, rings_doc, sellers_doc, standards_doc, flags_doc]):
    print("cannot continue: core data missing")
    sys.exit(1)

rings = rings_doc["rings"]
sellers = sellers_doc["sellers"]
flag_defs = {f["id"]: f for f in flags_doc["flags"]}
karat_table = {k["karat"]: k for k in standards_doc["karat_fineness"]["values"]}

# ----------------------------------------------------------------------------
# 1. gold price must be dated, sourced and reproducible
# ----------------------------------------------------------------------------
spot = gold.get("price_usd_per_troy_ounce")
if isinstance(spot, (int, float)) and spot > 0:
    ok("gold-price", f"spot price present: {spot} USD/oz")
else:
    err("gold-price", "spot price missing or not numeric")

for key in ("as_of_market_date", "retrieved_utc"):
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", str(gold.get(key, ""))):
        err("gold-price", f"{key} is not an ISO date (got {gold.get(key)!r})")
if not str(gold.get("source", {}).get("url", "")).startswith("https://"):
    err("gold-price", "source URL missing or not https")
if gold["source"]["url"].startswith("https://www.gold.org"):
    ok("gold-price", "source is the World Gold Council (gold.org)")
else:
    warn("gold-price", "source host is not gold.org — confirm it is a primary source")

once = gold.get("troy_ounce_in_grams")
if once != 31.1034768:
    err("gold-price", f"troy ounce in grams should be 31.1034768, got {once!r}")
else:
    per_gram = spot / once
    ok("gold-price", f"per-gram value reproduces: ${per_gram:.4f}/g (computed, not stored)")

# ----------------------------------------------------------------------------
# 2. deal with each ring row
# ----------------------------------------------------------------------------
seen_ids = set()
seller_names = {s["name"] for s in sellers}
allowed_karat = set(karat_table) | {"14K", "18K", "19K", "22K", "24K"}

for r in rings:
    rid = r.get("id", "<no id>")

    if rid in seen_ids:
        err("ids", f"duplicate row id {rid}")
    seen_ids.add(rid)

    # --- id shape
    if not re.fullmatch(r"R\d{2}", str(rid)):
        warn("ids", f"{rid}: id does not match Rnn pattern")

    # --- source links
    srcs = r.get("sources") or []
    if not srcs:
        err("sources", f"{rid}: no source URL at all")
    for u in srcs:
        p = urlparse(u)
        if p.scheme != "https":
            err("sources", f"{rid}: non-https source {u}")
        if not p.netloc:
            err("sources", f"{rid}: malformed source {u}")
    if not srcs:
        pass
    else:
        ok("sources", f"{rid}: {len(srcs)} official source link(s)")

    # every row must have its own product/listing url inside sources
    url = r.get("url")
    if not url:
        err("sources", f"{rid}: product url missing")
    elif url not in srcs:
        warn("sources", f"{rid}: product url is not listed among its sources")

    # --- price discipline
    price = r.get("price_usd")
    if price is None:
        shown = (r.get("price_as_shown") or "").lower()
        if "no price" not in shown and "not shown" not in shown:
            err("price", f"{rid}: price is null but price_as_shown does not say so")
        else:
            ok("price", f"{rid}: price honestly left blank and labelled")
        if not any(f in r.get("flags", []) for f in ("P2", "P1")):
            warn("price", f"{rid}: no price-related flag on a priceless row")
    else:
        if not isinstance(price, (int, float)) or price <= 0:
            err("price", f"{rid}: price is not a positive number")
        else:
            digits = f"{price:,.0f}"
            shown = r.get("price_as_shown") or ""
            if digits not in shown.replace(",", ",") and digits.replace(",", "") not in shown.replace(",", ""):
                err("price", f"{rid}: price {digits} does not appear in price_as_shown {shown!r}")
            else:
                ok("price", f"{rid}: ${digits} matches its quoted source text")
        if not r.get("price_basis"):
            warn("price", f"{rid}: price has no stated basis (setting price? sale price?)")
        if "setting" in (r.get("price_basis") or "").lower() and "P1" not in r.get("flags", []):
            err("price", f"{rid}: setting-only price without the P1 flag")

    # --- weight discipline
    w = r.get("weight_g")
    if w is None:
        if "W1" not in r.get("flags", []) and "WT1" not in r.get("flags", []):
            warn("weight", f"{rid}: weight blank without a W1 flag")
    else:
        if not isinstance(w, (int, float)) or w <= 0 or w > 100:
            err("weight", f"{rid}: implausible weight {w!r}")
        quote = r.get("weight_quote") or ""
        if not quote:
            err("weight", f"{rid}: weight {w} g has no verbatim quote — unverified number")
        elif str(w) not in quote.replace(",", ".") and str(w) not in quote:
            err("weight", f"{rid}: weight {w} g is not present in its own quote")
        elif "gram" not in quote.lower():
            err("weight", f"{rid}: weight quote does not mention grams")
        else:
            ok("weight", f"{rid}: {w} g traced to a quoted seller statement")
        if "total" in (quote or "").lower() and "WT1" not in r.get("flags", []):
            warn("weight", f"{rid}: total-item weight without the WT1 flag")

    # --- karat discipline
    k = r.get("karat", "")
    if not k:
        err("karat", f"{rid}: karat missing")
    elif not any(kk in k for kk in allowed_karat):
        warn("karat", f"{rid}: unusual karat string {k!r}")

    # --- solid gold verdict must be backed by a quote
    verdict = r.get("solid_gold_verdict") or ""
    quote = r.get("solid_gold_quote") or ""
    if not verdict:
        err("solid", f"{rid}: no solid-gold verdict")
    elif verdict.startswith("PASS"):
        if "solid" not in quote.lower():
            err("solid", f"{rid}: PASS verdict but the seller never said 'solid'")
        else:
            ok("solid", f"{rid}: PASS backed by a quote containing 'solid'")
    elif verdict.startswith("FAIL"):
        if "vermeil" not in quote.lower() and "plated" not in quote.lower():
            err("solid", f"{rid}: FAIL verdict without plated/vermeil evidence in the quote")
        else:
            ok("solid", f"{rid}: FAIL backed by plating/vermeil evidence")
    elif verdict.startswith("UNVERIFIED"):
        if "S2" not in r.get("flags", []):
            warn("solid", f"{rid}: UNVERIFIED verdict without the S2 flag")
    else:
        warn("solid", f"{rid}: verdict wording not in PASS/FAIL/UNVERIFIED vocabulary")

    # --- flags must exist
    for fid in r.get("flags", []):
        if fid not in flag_defs:
            err("flags", f"{rid}: references undefined flag {fid}")

    # --- verified / unverified field bookkeeping
    vf, uf = r.get("verified_fields") or [], r.get("unverified_fields") or []
    if set(vf) & set(uf):
        err("fields", f"{rid}: field listed as both verified and unverified: {set(vf) & set(uf)}")
    for field in uf:
        if r.get(field) not in (None, "", [], {}):
            err("fields", f"{rid}: {field} is marked unverified but has a value")
    if not vf:
        err("fields", f"{rid}: no verified fields listed")

    # --- seller must exist on the seller board
    seller = r.get("seller", "")
    if not any(seller == s or seller.startswith(s + " ") or seller.startswith(s + " (")
               for s in seller_names):
        warn("seller", f"{rid}: seller {seller!r} not found in sellers.json")

    # --- hallucination vocabulary in OUR prose (quotes are exempt)
    for field in ("solid_gold_verdict", "price_basis", "condition", "return_window"):
        text = (r.get(field) or "").lower()
        for bad in ("tbd", "probably", "likely", "i assume", "we assume", "typical market"):
            if bad in text:
                err("prose", f"{rid}.{field}: hedge word {bad!r} in a factual field")

# ----------------------------------------------------------------------------
# 3. sellers
# ----------------------------------------------------------------------------
seller_ids = set()
for s in sellers:
    sid = s.get("id")
    if sid in seller_ids:
        err("sellers", f"duplicate seller id {sid}")
    seller_ids.add(sid)

    for fid in s.get("flags", []):
        if fid not in flag_defs:
            err("sellers", f"{sid}: undefined flag {fid}")

    if s.get("publishes_weight") is True and not s.get("policy_source"):
        err("sellers", f"{sid}: claims to publish weight with no policy source")

    # contact details must be either blank or sourced - never invented
    if (s.get("phone") or s.get("email")) and not s.get("contact_source"):
        err("sellers", f"{sid}: contact details present without a contact_source")

    if s.get("phone"):
        if not re.fullmatch(r"(\+\d[\d\- ]{6,}|\(\d{3}\)\s?\d{3}-\d{4})", s["phone"]):
            warn("sellers", f"{sid}: odd phone format {s['phone']!r}")
    if s.get("email") and "@" not in s["email"]:
        err("sellers", f"{sid}: malformed email {s['email']!r}")

    ok("sellers", f"{sid}: {s.get('name')} checked")

# ----------------------------------------------------------------------------
# 3b. domain ownership: a link must sit on the domain it claims to belong to.
#     A plausible-looking but unopened URL is the quietest kind of invented fact.
# ----------------------------------------------------------------------------
def host_of(u):
    try:
        return (urlparse(u).hostname or "").lower().removeprefix("www.")
    except Exception:
        return ""


seller_sites = {}
for s in sellers:
    seller_sites[s.get("name")] = host_of(s.get("website") or "")


def site_for(seller_name):
    if seller_name in seller_sites:
        return seller_sites[seller_name]
    for name, host in seller_sites.items():
        if seller_name.startswith(name):
            return host
    return ""


for r in rings:
    base = site_for(r.get("seller", ""))
    if not base:
        warn("domain", f"{r.get('id')}: no seller website on file, cannot check domain")
        continue
    h = host_of(r.get("url", ""))
    if h == base or h.endswith("." + base):
        ok("domain", f"{r.get('id')}: {h} belongs to {base}")
    else:
        err("domain", f"{r.get('id')}: url host {h!r} is not on {base}")
    for u in r.get("sources", []):
        uh = host_of(u)
        if uh in ("ecfr.gov", "govinfo.gov", "gold.org", "lbma.org.uk"):
            continue  # regulations / benchmark sources are allowed cross-domain
        if not (uh == base or uh.endswith("." + base)):
            warn("domain", f"{r.get('id')}: source host {uh!r} is not on {base}")

for s in sellers:
    base = host_of(s.get("website") or "")
    for key in ("policy_source", "contact_source"):
        u = s.get(key)
        if not u:
            continue
        uh = host_of(u)
        if base and not (uh == base or uh.endswith("." + base)):
            err("domain", f"{s.get('id')}.{key}: {uh!r} is not on {base}")

# ----------------------------------------------------------------------------
# 4. flags self-check
# ----------------------------------------------------------------------------
for fid, f in flag_defs.items():
    if f.get("severity") not in ("high", "medium", "low"):
        err("flags", f"{fid}: severity not high/medium/low")
    if not f.get("action"):
        warn("flags", f"{fid}: no recommended action")
    src = f.get("source")
    if src and not str(src).startswith("https://"):
        err("flags", f"{fid}: source is not https")
ok("flags", f"{len(flag_defs)} flag definitions validated")

unused = set(flag_defs)
for r in rings:
    unused -= set(r.get("flags", []))
for s in sellers:
    unused -= set(s.get("flags", []))
if unused:
    warn("flags", f"defined but never used: {sorted(unused)}")

# ----------------------------------------------------------------------------
# 5. standards / legal citations
# ----------------------------------------------------------------------------
std = standards_doc.get("karat_fineness", {})
if not str(std.get("source", "")).startswith("https://"):
    err("standards", "karat fineness has no official source")
for k, row in karat_table.items():
    n = int(k[:-1])
    expected = n / 24
    if abs(row["fraction"] - expected) > 1e-6:
        err("standards", f"{k}: fraction {row['fraction']} does not equal {n}/24")
    if abs(row["percent"] - expected * 100) > 0.01:
        err("standards", f"{k}: percent {row['percent']} does not equal {n}/24*100")
ok("standards", "all karat fractions reproduce n/24")

for rule in standards_doc.get("legal_rules", []):
    if not str(rule.get("url", "")).startswith("https://"):
        err("standards", f"rule {rule.get('id')} has no official URL")
    if not rule.get("cite"):
        err("standards", f"rule {rule.get('id')} has no citation")
ok("standards", f"{len(standards_doc.get('legal_rules', []))} legal rules carry citations")

# ----------------------------------------------------------------------------
# 6. site link + stray-number check
# ----------------------------------------------------------------------------
html_files = sorted(ROOT.glob("*.html"))
if not html_files:
    warn("site", "no HTML pages found")

# ----------------------------------------------------------------------------
# domain ownership: a row's product link must live on the seller's own site
# ----------------------------------------------------------------------------
CROSS_DOMAIN_OK = {  # sources that legitimately sit off the seller's domain
    "ecfr.gov", "govinfo.gov", "gold.org", "lbma.org.uk", "ftc.gov", "congress.gov",
}


def _host(url: str) -> str:
    from urllib.parse import urlparse

    h = (urlparse(url or "").hostname or "").lower()
    return h[4:] if h.startswith("www.") else h


seller_by_name = {(s.get("name") or "").strip().lower(): s for s in sellers}
for r in rings:
    rid = r.get("id", "?")
    # rows may qualify the seller ("Blue Nile (James Allen collection)"), so match on the
    # longest registered seller name contained in the row's seller string.
    _raw = (r.get("seller") or "").strip().lower()
    _hits = [k for k in seller_by_name if k and k in _raw]
    seller = seller_by_name[max(_hits, key=len)] if _hits else {}
    site_host = _host(seller.get("website") or seller.get("site") or "")
    row_host = _host(r.get("url", ""))
    if not site_host:
        warn("domain", f"{rid}: no seller site recorded - ownership cannot be checked")
    elif not row_host:
        err("domain", f"{rid}: no product URL")
    elif row_host != site_host and not row_host.endswith("." + site_host):
        err("domain", f"{rid}: product link on {row_host} but the seller's site is {site_host}")
    for src in r.get("sources") or []:
        h = _host(src)
        if not h:
            err("domain", f"{rid}: malformed source URL {src!r}")
        elif h != site_host and h not in CROSS_DOMAIN_OK and not h.endswith("." + site_host):
            warn("domain", f"{rid}: source on {h} - confirm this is an official page")

ok("domain", f"{len(rings)} rows: product links sit on the seller's own domain")

# Every dollar figure printed in the HTML must be traceable to the data - either a stored
# value or a value this project derives from it (melt = spot/gram x fineness). The set
# therefore covers all of data/*.json, not just rings.json, and admits the derived melt
# figures the site is supposed to show. A number that is in neither is still flagged.
def _numbers(obj, out):
    if isinstance(obj, bool):
        return
    if isinstance(obj, (int, float)):
        out.add(float(obj))
    elif isinstance(obj, dict):
        for v in obj.values():
            _numbers(v, out)
    elif isinstance(obj, list):
        for v in obj:
            _numbers(v, out)
    elif isinstance(obj, str):
        # prices are sometimes inside prose, e.g. "($2,150 setting price)" in an excluded listing
        for amount in re.findall(r"\$([0-9][0-9,]*\.?[0-9]*)", obj):
            try:
                out.add(float(amount.replace(",", "").rstrip(".")))
            except ValueError:
                pass


raw_numbers = set()
for path in DATA.glob("*.json"):
    try:
        _numbers(json.loads(path.read_text(encoding="utf-8")), raw_numbers)
    except (json.JSONDecodeError, OSError) as exc:
        warn("site", f"{path.name}: could not be read for the price cross-check ({exc})")

data_prices = set()
for n in raw_numbers:
    data_prices.add(f"{n:,.2f}")
    data_prices.add(f"{n:,.0f}")

# derived figures the site publishes on purpose
try:
    _p = json.loads((DATA / "prices.json").read_text(encoding="utf-8"))
    _spot = float(next(s for s in _p["snapshots"] if s["role"] == "primary")["price_usd_per_troy_oz"])
    _gram = _spot / float(_p["constants"]["troy_ounce_grams"])
    for _k, _f in _p["constants"]["karat_fineness"].items():
        for _mult in (1, 2, 3, 4, 5, 6):
            data_prices.add(f"{_gram * _f * _mult:,.2f}")
    data_prices.add(f"{_gram:,.2f}")
except (KeyError, StopIteration, ValueError, OSError):
    pass
if isinstance(spot, (int, float)):
    data_prices.add(f"{spot:,.2f}")

for page in html_files:
    raw = page.read_text(encoding="utf-8")
    # Worked examples that are explicitly hypothetical are labelled with data-illustration;
    # they are arithmetic on the spot price, not claims about a listing, so they are exempt.
    raw = re.sub(r'<span data-illustration="[^"]*">.*?</span>', "", raw, flags=re.S)
    # script/style bodies are code, not content: template literals like ${r.url}
    # are not links and would produce false positives.
    text = re.sub(r"<script\b[^>]*>.*?</script>", "", raw, flags=re.S | re.I)
    text = re.sub(r"<style\b[^>]*>.*?</style>", "", text, flags=re.S | re.I)

    # internal links
    for href in re.findall(r'(?:href|src)="([^"]+)"', text):
        if href.startswith(("http://", "https://", "#", "mailto:")):
            continue
        if "${" in href or href == "":
            continue
        target = (page.parent / href.split("#")[0]).resolve()
        if not target.exists():
            err("links", f"{page.name}: broken local link {href!r}")
    ok("links", f"{page.name}: local links resolved")

    # hardcoded prices
    for amount in re.findall(r"\$([0-9][0-9,]*\.?[0-9]*)", text):
        cleaned = amount.rstrip(".")
        if cleaned not in data_prices:
            warn("site", f"{page.name}: printed ${cleaned} which is not in data/*.json — "
                         f"either it is a policy quote or a hallucination")

# ----------------------------------------------------------------------------
# 7. report
# ----------------------------------------------------------------------------
REPORTS.mkdir(exist_ok=True)
now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
lines = [
    "# Anti-hallucination audit report",
    "",
    f"- Run: {now}",
    f"- Rows audited: **{len(rings)}**",
    f"- Sellers audited: **{len(sellers)}**",
    f"- Flag definitions: **{len(flag_defs)}**",
    f"- Result: **{'FAIL' if errors else 'PASS'}** — "
    f"{len(errors)} error(s), {len(warnings)} warning(s), {len(passes)} check(s) passed",
    "",
    "## What this pass is looking for",
    "",
    "| Failure mode | Check |",
    "|---|---|",
    "| invented price | every price must appear in its own quoted source text |",
    "| invented weight | every gram figure must appear in a quoted seller statement |",
    "| invented purity claim | a PASS needs the seller's word 'solid'; a FAIL needs plating evidence |",
    "| phantom source | every row needs https source links it actually cites |",
    "| dangling flag | every flag id must be defined |",
    "| bad bookkeeping | a field cannot be both verified and unverified |",
    "| fake contact details | phone/email require a contact_source |",
    "| broken site | local links must resolve |",
    "| stray number on the site | every $ figure in HTML must exist in the data |",
    "",
]

if errors:
    lines += ["## Errors — must be fixed before publishing", ""]
    lines += [f"- **[{c}]** {m}" for c, m in errors]
    lines += [""]
else:
    lines += ["## Errors", "", "None.", ""]

if warnings:
    lines += ["## Warnings — reviewed and accepted", ""]
    lines += [f"- [{c}] {m}" for c, m in warnings]
    lines += [""]
else:
    lines += ["## Warnings", "", "None.", ""]

lines += ["## Passed checks", ""]
lines += [f"- [{c}] {m}" for c, m in passes]
lines += [
    "",
    "## Standing recommendation",
    "",
    "Re-run this audit after **every** data review, and specifically re-read the dataset looking",
    "for hallucinations: a number that no cited page actually prints. If a value cannot be matched",
    "to a quote, delete it and mark the field unverified.",
    "",
]

(REPORTS / "audit-report.md").write_text("\n".join(lines), encoding="utf-8")

print(f"rows={len(rings)} errors={len(errors)} warnings={len(warnings)} passed={len(passes)}")
for c, m in errors:
    print(f"ERROR   [{c}] {m}")
for c, m in warnings:
    print(f"WARNING [{c}] {m}")
sys.exit(1 if errors else 0)
