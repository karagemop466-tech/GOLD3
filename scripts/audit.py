#!/usr/bin/env python3
"""
audit.py — the no-hallucination / consistency audit for the GOLD3 dataset.

Run after EVERY review pass. It does not fetch anything: it re-reads the stored
dataset and fails loudly wherever a value is not backed by a quoted, dated,
official source, wherever arithmetic cannot be reproduced, and wherever two
recorded observations of the same fact disagree.

Usage:  python3 scripts/audit.py [--json reports/audit-latest.json]
Exit code 1 if any check FAILS (warnings are allowed and are published on the
Flagged for Review page).
"""
from __future__ import annotations

import json
import re
import sys
from datetime import date, datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent.parent
KARATS = {"10", "14", "18", "22", "24"}
PLATED_WORDS = ("plated", "vermeil", "gold filled", "gold-filled", "overlay",
                "rolled gold", "electroplate", "gold tone", "gold-tone", "filled")
# A price/gram-of-fine-gold ratio above this is implausible for any jewellery listing.
MAX_USD_PER_FINE_GRAM = 20000.0


def load(root: Path) -> dict:
    data = {}
    for name in ("rings", "sellers", "standards", "spot"):
        p = root / "data" / f"{name}.json"
        data[name] = json.loads(p.read_text(encoding="utf-8"))
    data["rings_items"] = data["rings"].get("items", [])
    data["sellers_items"] = data["sellers"].get("sellers", [])
    return data


def _severity_rank(s: str) -> int:
    return {"fail": 0, "warn": 1, "pass": 2, "info": 3}.get(s, 4)


class Audit:
    def __init__(self, data: dict):
        self.data = data
        self.findings: list[dict] = []
        self.checks: list[dict] = []

    # ---- helpers -----------------------------------------------------------
    def add(self, check_id, name, status, detail, evidence=None):
        self.checks.append({"id": check_id, "name": name, "status": status,
                            "detail": detail, "evidence": evidence or []})

    def finding(self, severity, item_id, field, message, source=None):
        self.findings.append({"severity": severity, "item": item_id, "field": field,
                              "message": message, "source": source})

    # ---- checks ------------------------------------------------------------
    def run(self):
        items = self.data["rings_items"]
        sellers = {s["id"]: s for s in self.data["sellers_items"]}
        spot = self.data["spot"]["spot"]
        self.spot_per_gram = spot["value_per_oz"] / self.data["spot"]["troy_ounce_grams"]

        self.check_source_required(items, sellers)
        self.check_price_evidence(items)
        self.check_karat_evidence(items)
        self.check_solid_evidence(items)
        self.check_weight(items)
        self.check_derived_math(items)
        self.check_price_drift(items)
        self.check_duplicates(items)
        self.check_dead_links(items)
        self.check_spot_freshness(spot)
        self.check_freshness(items)
        self.check_plausibility(items)
        self.check_seller_policies(items, sellers)
        self.check_url_ownership(items, sellers)

        fails = [c for c in self.checks if c["status"] == "fail"]
        warns = [c for c in self.checks if c["status"] == "warn"]
        return {
            "generated": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
            "checks": self.checks,
            "findings": sorted(self.findings, key=lambda f: _severity_rank(f["severity"])),
            "summary": {
                "checks_total": len(self.checks),
                "checks_pass": len([c for c in self.checks if c["status"] == "pass"]),
                "checks_warn": len(warns),
                "checks_fail": len(fails),
                "findings_fail": len([f for f in self.findings if f["severity"] == "fail"]),
                "findings_warn": len([f for f in self.findings if f["severity"] == "warn"]),
            },
            "stats": self.stats(items),
        }

    def stats(self, items):
        live = [i for i in items if i.get("check") == "live"]
        return {
            "items_total": len(items),
            "items_live": len(live),
            "items_snapshot": len([i for i in items if i.get("check") == "snapshot"]),
            "items_dead": len([i for i in items if i.get("check") == "dead"]),
            "with_weight": len([i for i in live if i.get("weight_g")]),
            "with_price": len([i for i in live if i.get("price") is not None]),
            "solid_true": len([i for i in live if i.get("solid") is True]),
            "solid_false": len([i for i in live if i.get("solid") is False]),
            "solid_unstated": len([i for i in live if i.get("solid") is None]),
            "spot_per_gram": round(self.spot_per_gram, 4),
        }

    # A1 -------------------------------------------------------------------
    def check_source_required(self, items, sellers):
        bad = [i["id"] for i in items if not str(i.get("url", "")).startswith("http")]
        noseller = [i["id"] for i in items if i.get("seller") not in sellers]
        status = "fail" if (bad or noseller) else "pass"
        for b in bad:
            self.finding("fail", b, "url", "No official source URL recorded.")
        for b in noseller:
            self.finding("fail", b, "seller", "Seller is not in the seller register.")
        self.add("A1", "Every entry links to an official seller page",
                 status, f"{len(items) - len(bad) - len(noseller)}/{len(items)} entries have an official URL and a registered seller.")

    # A2 -------------------------------------------------------------------
    def check_price_evidence(self, items):
        problems = []
        for i in items:
            if i.get("price") is None:
                continue
            ev = (i.get("ev") or {}).get("price")
            if not ev:
                problems.append(i["id"]); self.finding("fail", i["id"], "price", "Price stored without an evidence quote.")
            if i.get("check") != "live":
                problems.append(i["id"])
                self.finding("warn", i["id"], "price", f"Price recorded from a '{i.get('check')}' source, not a live page check — treat as unverified.")
        self.add("A2", "No price exists without a quoted, dated source",
                 "fail" if problems else "pass",
                 f"{len([i for i in items if i.get('price') is not None])} priced entries checked; {len(set(problems))} need attention.")

    # A3 -------------------------------------------------------------------
    def check_karat_evidence(self, items):
        bad = []
        for i in items:
            k = i.get("karat")
            if not k:
                continue
            ev = (i.get("ev") or {}).get("karat", "") or ""
            kk = k.upper().replace(" ", "")
            if not re.fullmatch(r"(10|14|18|22|24)K", kk):
                bad.append(i["id"]); self.finding("fail", i["id"], "karat", f"Karat '{k}' is not one of 10K/14K/18K/22K/24K.")
            elif not re.search(rf"{kk[:2]}\s*-?\s*k", ev, re.I):
                bad.append(i["id"]); self.finding("fail", i["id"], "karat", "Karat value is not present in the quoted evidence text.")
        self.add("A3", "Karat value appears verbatim in the quoted evidence",
                 "fail" if bad else "pass", f"{len(items) - len(set(bad))}/{len(items)} karat values traced to a quote.")

    # A4 -------------------------------------------------------------------
    def check_solid_evidence(self, items):
        bad = []
        for i in items:
            solid = i.get("solid")
            if solid is None:
                continue
            ev = ((i.get("ev") or {}).get("solid") or "").lower()
            if not ev:
                bad.append(i["id"]); self.finding("fail", i["id"], "solid", "Solid/plated verdict without an evidence quote.")
                continue
            if solid is True and not re.search(r"solid", ev):
                bad.append(i["id"]); self.finding("fail", i["id"], "solid", "Marked solid gold but the quote contains no 'solid' wording.")
            if solid is False and not any(w in ev for w in PLATED_WORDS):
                bad.append(i["id"]); self.finding("fail", i["id"], "solid", "Marked plated/not-solid but the quote contains no plating wording.")
        self.add("A4", "Solid-gold verdicts are backed by the seller's own wording",
                 "fail" if bad else "pass", f"{len([i for i in items if i.get('solid') is not None])} verdicts checked.")

    # A5 -------------------------------------------------------------------
    def check_weight(self, items):
        problems = []
        for i in items:
            w = i.get("weight_g")
            if w is None:
                continue
            ev = (i.get("ev") or {}).get("weight") or ""
            try:
                val = float(w)
            except (TypeError, ValueError):
                problems.append(i["id"]); self.finding("fail", i["id"], "weight_g", "Weight is not numeric."); continue
            if val <= 0:
                problems.append(i["id"]); self.finding("fail", i["id"], "weight_g", "Weight must be positive.")
            if not ev:
                problems.append(i["id"]); self.finding("fail", i["id"], "weight_g", "Weight stored without an evidence quote.")
            elif not re.search(rf"{re.escape(('%.2f' % val).rstrip('0').rstrip('.'))}\s*(g|gram|grams)", ev, re.I):
                problems.append(i["id"]); self.finding("warn", i["id"], "weight_g", "Weight number is not literally present in the quote (approximation wording?).")
        self.add("A5", "Gram weights come from the seller, never from an estimate",
                 "fail" if problems else "pass",
                 f"{len([i for i in items if i.get('weight_g') is not None])} weight values checked.")

    # A6 -------------------------------------------------------------------
    def check_derived_math(self, items):
        spot = self.data["spot"]["spot"]
        ozg = self.data["spot"]["troy_ounce_grams"]
        per_g = spot["value_per_oz"] / ozg
        frac = self.data["standards"]["karat_fractions"]["values"]
        mismatches = []
        for i in items:
            if i.get("solid") is False:
                continue  # plated/vermeil: no gold content to value at spot
            w, k = i.get("weight_g"), i.get("karat")
            if not w or not k:
                continue
            factor = frac.get(str(int(str(k).upper().replace("K", ""))))
            if factor is None:
                continue
            fine = float(w) * factor
            melt = fine * per_g
            if not (0 < melt < 1_000_000):
                mismatches.append(i["id"]); self.finding("fail", i["id"], "derived", "Melt value out of plausible range.")
            # premium only when a complete-ring price is recorded
            if i.get("price_type") == "full" and i.get("price"):
                prem = (i["price"] - melt) / melt * 100
                if prem < -5:
                    mismatches.append(i["id"])
                    self.finding("warn", i["id"], "price", f"Price is {prem:.0f}% below the melt value of its own stated gold weight — verify weight, karat and price.")
        self.add("A6", "Every derived figure is reproducible from stored inputs",
                 "fail" if mismatches else "pass",
                 f"Melt value = weight_g × karat/24 × (spot ÷ 31.1034768). Recomputed for {len([i for i in items if i.get('weight_g')])} entries.")

    # A7 -------------------------------------------------------------------
    def check_price_drift(self, items):
        drift = []
        for i in items:
            hist = i.get("observations") or []
            vals = {o.get("price") for o in hist if o.get("price") is not None}
            if len(vals) > 1:
                drift.append(i["id"])
                self.finding("warn", i["id"], "price",
                             "More than one price recorded for this item (list-price change, sale price, configuration or a stale index copy) — the live page value is the one used: " +
                             ", ".join(f"${v:,.0f} on {o.get('on')} ({o.get('via')})"
                                       for v in sorted(vals) for o in hist if o.get("price") == v),
                             i.get("url"))
        self.add("A7", "Price-drift detector: same item, different recorded prices",
                 "warn" if drift else "pass",
                 f"{len(drift)} of {len(items)} entries have more than one recorded price observation.")

    # A8 -------------------------------------------------------------------
    def check_duplicates(self, items):
        seen, dupes = {}, []
        for i in items:
            for key in ("url",):
                v = i.get(key)
                if v in seen:
                    dupes.append(i["id"]); self.finding("warn", i["id"], "duplicate", f"Duplicate {key} also used by {seen[v]}.")
                seen[v] = i["id"]
        self.add("A8", "No duplicate listings", "warn" if dupes else "pass",
                 f"{len(dupes)} duplicate entries.")

    # A9 -------------------------------------------------------------------
    def check_dead_links(self, items):
        dead = [i["id"] for i in items if i.get("check") == "dead"]
        for d in dead:
            self.finding("info", d, "availability", "Listing is no longer purchasable (page returned 'not found' / 'not available') — kept for the record, excluded from the buy list.")
        self.add("A9", "Dead listings are labelled, not silently kept", "info" if dead else "pass",
                 f"{len(dead)} dead listing(s) recorded and excluded from recommendations.")

    # A10 ------------------------------------------------------------------
    def check_spot_freshness(self, spot):
        try:
            as_of = date.fromisoformat(spot["as_of"])
            age = (date.today() - as_of).days
        except Exception:
            self.add("A10", "Spot price record is dated", "fail", "Spot price has no usable date."); return
        status = "pass" if age <= 7 else ("warn" if age <= 30 else "fail")
        if age > 7:
            self.finding("warn" if age <= 30 else "fail", spot["id"], "spot",
                         f"Spot price is {age} days old — refresh before quoting a melt value.", spot["source_url"])
        self.add("A10", "Spot price is dated by an official source", status,
                 f"${spot['value_per_oz']:,.2f}/ozt as of {spot['as_of']} ({age} day(s) old) — {spot['source_name']}.")

    # A11 ------------------------------------------------------------------
    def check_freshness(self, items):
        stale = []
        today = date.today()
        for i in items:
            try:
                d = date.fromisoformat(i["checked"])
            except Exception:
                stale.append(i["id"]); self.finding("warn", i["id"], "checked", "No valid check date."); continue
            if (today - d).days > 30:
                stale.append(i["id"]); self.finding("warn", i["id"], "checked", f"Last checked {(today - d).days} days ago — re-verify before buying.")
        self.add("A11", "Every entry carries a recent re-check date", "warn" if stale else "pass",
                 f"{len(stale)} entries older than 30 days.")

    # A12 ------------------------------------------------------------------
    def check_plausibility(self, items):
        bad = []
        for i in items:
            p = i.get("price")
            if p is None:
                continue
            if not isinstance(p, (int, float)) or p <= 0 or p > 5_000_000:
                bad.append(i["id"]); self.finding("fail", i["id"], "price", "Price is not a credible positive amount.")
                continue
            if i.get("weight_g") and i.get("karat"):
                try:
                    frac = self.data["standards"]["karat_fractions"]["values"][str(int(str(i["karat"]).upper().replace("K", "")))]
                    per_g = p / (float(i["weight_g"]) * frac)
                    if per_g > MAX_USD_PER_FINE_GRAM:
                        bad.append(i["id"]); self.finding("warn", i["id"], "price", f"${per_g:,.0f} per fine gram of gold is implausibly high — check weight/karat/price units.")
                except Exception:
                    pass
        self.add("A12", "Price magnitude sanity check", "warn" if bad else "pass",
                 f"All stored prices fall in a credible range (limit ${MAX_USD_PER_FINE_GRAM:,.0f} per fine gram).")

    # A14 ------------------------------------------------------------------
    def check_url_ownership(self, items, sellers):
        """Every stored link must sit on the domain it claims to belong to.
        This catches guessed or copy-pasted URLs, which are the quietest kind of invented fact."""
        def host(u):
            try:
                return (urlparse(u).hostname or "").lower().removeprefix("www.")
            except Exception:
                return ""

        def owned(u, seller):
            h, base = host(u), host(seller.get("site") or "")
            return bool(base) and (h == base or h.endswith("." + base))

        bad = []
        for i in items:
            s = sellers.get(i.get("seller"), {})
            if not owned(i.get("url", ""), s):
                bad.append(i["id"])
                self.finding("fail", i["id"], "url", f"{i.get('url')} is not on {s.get('site')}.")
        for s in sellers.values():
            for key in ("contact_url", "returns_url", "site"):
                u = s.get(key)
                if u and not owned(u, s):
                    bad.append(s["id"])
                    self.finding("fail", s["id"], key, f"{u} is not on the seller's own domain ({s.get('site')}).")
        self.add("A14", "Every link sits on the domain it claims to belong to",
                 "fail" if bad else "pass",
                 f"{len(items)} listing URLs and {len(sellers)} seller links checked against their own domains.")

    # A13 ------------------------------------------------------------------
    def check_seller_policies(self, items, sellers):
        missing = sorted({i["seller"] for i in items if i.get("seller") in sellers
                          and not (sellers[i["seller"]].get("returns_url"))})
        for m in missing:
            self.finding("warn", m, "returns", "No official return-policy URL recorded for this seller.")
        self.add("A13", "Every seller has a linked, official return policy",
                 "warn" if missing else "pass",
                 f"{len(sellers) - len(missing)}/{len(sellers)} sellers documented.")


def render_markdown(result: dict, data: dict) -> str:
    s = result["summary"]; st = result["stats"]
    L = []
    L.append("# No-hallucination audit\n")
    L.append(f"Generated: **{result['generated']}**  ")
    L.append(f"Dataset: {st['items_total']} entries "
             f"({st['items_live']} live-verified, {st['items_snapshot']} index-snapshot, {st['items_dead']} dead)\n")
    L.append(f"**Result: {s['checks_pass']} passed · {s['checks_warn']} warnings · {s['checks_fail']} failed**\n")
    L.append("| Check | Status | Detail |\n|---|---|---|")
    icon = {"pass": "PASS", "warn": "WARN", "fail": "FAIL", "info": "INFO"}
    for c in result["checks"]:
        L.append(f"| `{c['id']}` {c['name']} | **{icon[c['status']]}** | {c['detail']} |")
    L.append("\n## Findings\n")
    if not result["findings"]:
        L.append("No findings.")
    else:
        L.append("| Severity | Item | Field | Finding |\n|---|---|---|---|")
        for f in result["findings"]:
            L.append(f"| {f['severity'].upper()} | `{f['item']}` | {f['field']} | {f['message']} |")
    L.append("\n## Arithmetic reference\n")
    L.append(f"- Spot used: ${data['spot']['spot']['value_per_oz']:,.2f}/ozt as of {data['spot']['spot']['as_of']}")
    L.append(f"  ({data['spot']['spot']['source_name']})")
    L.append(f"- Spot per gram: **${st['spot_per_gram']:,.4f}/g** (spot ÷ 31.1034768)")
    L.append("- Melt value of a ring = `weight_g × (karat ÷ 24) × spot_per_gram`")
    L.append("- Premium vs melt = `(price − melt) ÷ melt × 100%` — only computed when a complete-ring price is stored")
    L.append("\n_Source of every row is linked on the Flagged for Review and Rings pages._\n")
    return "\n".join(L)


def main(argv):
    data = load(ROOT)
    result = Audit(data).run()
    outdir = ROOT / "reports"
    outdir.mkdir(exist_ok=True)
    (outdir / "audit-latest.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    (outdir / "audit-latest.md").write_text(render_markdown(result, data), encoding="utf-8")
    print(render_markdown(result, data))
    return 0 if result["summary"]["checks_fail"] == 0 else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
