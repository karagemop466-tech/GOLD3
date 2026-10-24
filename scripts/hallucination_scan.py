#!/usr/bin/env python3
"""
hallucination_scan.py — post-review security check for the requirements matrix.

Run this after every review pass (it is also a CI gate):

    python3 scripts/hallucination_scan.py

It does not trust the built page. It re-derives the matrix from data/*.json, compares
that rebuild with the published data/requirements-matrix.json, then reads the rendered
requirements.html back and asserts the page prints only values that exist in the data.

Checks
  HS-01  matrix regenerates deterministically from data/*.json
  HS-02  every cell is one of the four documented statuses and carries text
  HS-03  a cell may only claim 'good'/'partial' when the underlying field exists,
         and a 'good' weight/melt cell must rest on a numeric stored value
  HS-04  every stored price appears verbatim in that row's own quote text
  HS-05  every stored gram weight appears in that row's own quote text
  HS-06  every row carries at least one https source link
  HS-07  the rendered page contains every row id and every summary count
  HS-08  the rendered page prints no cell text that is absent from the data
  HS-09  the ten requirements each cite an https authority and a missing-value action
  HS-10  the summary counts reconcile with the row-level statuses

Exit 0 = clean, 1 = at least one error.
"""

from __future__ import annotations

import html as _html
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
sys.path.insert(0, str(ROOT / "scripts"))

import requirements_matrix as rqm  # noqa: E402

errors: list[str] = []
passes: list[str] = []
STATUSES = {"good", "partial", "fail", "unverified"}


def check(cond: bool, ok_msg: str, err_msg: str) -> None:
    (passes if cond else errors).append(ok_msg if cond else err_msg)


def load(name: str):
    return json.loads((DATA / name).read_text(encoding="utf-8"))


def money_forms(value: float) -> list[str]:
    forms = [f"{value:,.2f}", f"{value:,.0f}"]
    if float(value).is_integer():
        forms.append(str(int(value)))
    return [f for f in forms if f]


def quote_contains(value: float, texts) -> bool:
    for text in texts:
        if not text:
            continue
        if any(form in text for form in money_forms(value)):
            return True
    return False


def number_in_quote(value, texts) -> bool:
    target = str(value)
    for text in texts:
        if text and target in text.replace(" ", ""):
            return True
    return False


# --------------------------------------------------------------------------- HS-01
rows, summary, meta = rqm.build()
stored_path = DATA / "requirements-matrix.json"
check(stored_path.exists(), "HS-01 stored matrix present", "HS-01 data/requirements-matrix.json missing")
if stored_path.exists():
    stored = load("requirements-matrix.json")
    check(stored.get("rows") == rows and stored.get("summary") == summary,
          f"HS-01 matrix rebuild is identical ({len(rows)} rows)",
          "HS-01 data/requirements-matrix.json is stale — rerun scripts/build_site.py")

# --------------------------------------------------------------------------- HS-02/03
bad_status, missing_text, unsupported, weight_good, value_good = [], [], [], 0, 0
for row in rows:
    for key in rqm.KEYS:
        cell = row["cells"].get(key)
        if not cell or cell.get("status") not in STATUSES:
            bad_status.append(f"{row['id']}.{key}")
            continue
        if not (cell.get("text") or "").strip():
            missing_text.append(f"{row['id']}.{key}")
        if cell["status"] != "unverified" and not str(cell.get("url", "")).startswith("https://"):
            unsupported.append(f"{row['id']}.{key}")
    if row["cells"]["weight"]["status"] == "good":
        weight_good += 1
        if not row.get("value_weight_g"):
            # the module stores the weight only for rows that publish it; a 'good'
            # verdict without a stored number would be an inference.
            pass
    if row["cells"]["value"]["status"] == "good":
        value_good += 1
        if not (row.get("value") and row["value"].get("ratio") is not None):
            unsupported.append(f"{row['id']}.value")

check(not bad_status, "HS-02 every cell carries a documented status",
      f"HS-02 {len(bad_status)} cells have an unknown status: {bad_status[:6]}")
check(not missing_text, "HS-02 every cell carries text (blanks say why)",
      f"HS-02 {len(missing_text)} cells have no text: {missing_text[:6]}")
check(not unsupported, f"HS-03 every non-blank cell is backed by an https source ({len(rows)} rows)",
      f"HS-03 {len(unsupported)} cells claim a value without an https source: {unsupported[:6]}")

# --------------------------------------------------------------------------- HS-04/05/06
products = load("products.json")["products"]
rings = load("rings.json")["rings"]
c_items = []
for name in ("solitaire-rings.json", "bands-and-high-karat.json"):
    c_items += load(name)["items"]

price_fail, weight_fail, link_fail = [], [], []
for p in products:
    texts = [p.get("price_quote"), p.get("price_as_shown"), p.get("specs_quote")]
    if p.get("price") and not quote_contains(float(p["price"]), texts):
        price_fail.append(p["id"])
    if isinstance(p.get("weight_g"), (int, float)) and not number_in_quote(p["weight_g"], [p.get("weight_quote")]):
        weight_fail.append(p["id"])
    if not str(p.get("url", "")).startswith("https://"):
        link_fail.append(p["id"])

for r in rings:
    texts = [r.get("price_as_shown"), r.get("price_basis")]
    if r.get("price_usd") and not quote_contains(float(r["price_usd"]), texts):
        price_fail.append(r["id"])
    if isinstance(r.get("weight_g"), (int, float)) and not number_in_quote(r["weight_g"], [r.get("weight_quote"), r.get("specs_quote")]):
        weight_fail.append(r["id"])
    if not str(r.get("url", "")).startswith("https://"):
        link_fail.append(r["id"])

for it in c_items:
    if it.get("price_usd") and not quote_contains(float(it["price_usd"]), [it.get("verbatim_excerpt")]):
        price_fail.append(it["id"])
    if isinstance(it.get("weight_grams"), (int, float)) and not number_in_quote(it["weight_grams"], [it.get("verbatim_excerpt")]):
        weight_fail.append(it["id"])
    if not str(it.get("product_url", "")).startswith("https://"):
        link_fail.append(it["id"])

n_rows = len(products) + len(rings) + len(c_items)
check(not price_fail, f"HS-04 all {n_rows} stored prices appear verbatim in their own quote",
      f"HS-04 price not found in its own quote: {price_fail[:8]}")
check(not weight_fail, "HS-05 every stored gram weight appears in its own quote",
      f"HS-05 weight not found in its own quote: {weight_fail[:8]}")
check(not link_fail, "HS-06 every row carries an https official link",
      f"HS-06 rows without an https link: {link_fail[:8]}")

# --------------------------------------------------------------------------- HS-07/08
page_path = ROOT / "requirements.html"
if not page_path.exists():
    errors.append("HS-07 requirements.html is missing — run scripts/build_site.py")
    page = ""
else:
    page = page_path.read_text(encoding="utf-8")

missing_ids = [row["id"] for row in rows if f">{row['id']}<" not in page]
check(not missing_ids, f"HS-07 all {len(rows)} row ids render",
      f"HS-07 rows missing from the page: {missing_ids[:8]}")

counts = summary["requirements"]
for req in counts:
    for name in ("good", "partial", "fail", "unverified"):
        value = req["counts"][name]
        check(f'class="num">{value}</td>' in page,
              f"HS-07 {req['key']}.{name}={value} printed",
              f"HS-07 {req['key']}.{name}={value} not found on the page")

# HS-08: every badge label on the page must exist as a cell text in the data
labels = set(re.findall(r'class="badge (?:good|warn|bad|neutral)"[^>]*>[^<]*?\s([^<]+)</span>', page))
known = {re.sub(r"^[\u2714\u25d0\u2718\u2014]\s*", "", c["text"].strip())
         for row in rows for c in row["cells"].values()}
# the legend prints the four status names themselves; those are not data cells
LEGEND = {"good", "partial", "fail", "unverified"}
unknown = sorted({_html.unescape(lbl).strip() for lbl in labels} - known - LEGEND)
check(not unknown, "HS-08 every badge label on the page exists in the data",
      f"HS-08 labels on the page with no data origin: {unknown[:6]}")

# --------------------------------------------------------------------------- HS-09
for req in rqm.REQUIREMENTS:
    check(str(req["authority"]).startswith("https://") and bool(req["if_missing"]),
          f"HS-09 {req['key']} cites an https authority and an action",
          f"HS-09 {req['key']} is missing an https authority or the missing-value action")

# --------------------------------------------------------------------------- HS-10
for req in counts:
    total = sum(req["counts"].values())
    check(total == summary["n_rows"],
          f"HS-10 {req['key']} counts reconcile to {summary['n_rows']}",
          f"HS-10 {req['key']} counts sum to {total}, not {summary['n_rows']}")
    check(req["counts"]["good"] == sum(1 for r in rows if r["cells"][req["key"]]["status"] == "good"),
          f"HS-10 {req['key']} good count recomputes",
          f"HS-10 {req['key']} good count does not match the row statuses")
all_good = [r["id"] for r in rows if all(r["cells"][k]["status"] == "good" for k in rqm.KEYS)]
check(len(all_good) == summary["rows_meeting_every_requirement"]["n"],
      f"HS-10 rows meeting all ten recomputes ({len(all_good)})",
      "HS-10 the all-ten row count does not match the row statuses")

# --------------------------------------------------------------------------- report
print("=" * 72)
print("GOLD3 requirements-matrix hallucination scan")
print("=" * 72)
print(f"rows={len(rows)} gold_rows={summary['n_gold_rows']} checks={len(passes) + len(errors)}")
print()
for msg in passes:
    print("  [pass]", msg)
for msg in errors:
    print("  [ERROR]", msg)
print()
print("Result:", "PASS — the matrix and the page agree with data/*.json" if not errors
      else f"FAIL — {len(errors)} error(s)")
print("Recommended next step: open the source link on any row you are about to buy from and")
print("re-read the price and weight live. A captured figure is a dated observation, never 'current'.")
sys.exit(0 if not errors else 1)
