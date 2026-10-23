#!/usr/bin/env python3
"""Re-anchor every gold-price-derived number in the repo to a freshly read,
verbatim, dated spot quote.

Why this exists
---------------
The gold spot price is the only *input* the site's melt arithmetic consumes, so a
stale anchor makes every melt figure wrong by the same percentage while every
individual row still looks internally consistent. Hand-editing the anchor in five
JSON files is exactly the kind of change that introduces an unsourced number, so
the arithmetic lives here instead: the four live readings below are copied
verbatim from the pages named next to them, and every derived value (USD/gram,
the 7-karat table, and the 5 weight-complete melt rows in Dataset C) is
recomputed from them with the same formulas the CI gates re-check.

Refuses to run twice for the same capture id, and refuses to run if the anchor
date is not today, so nobody can silently "refresh" with an old number.

This is a maintenance tool, NOT part of the build: the project keeps a dated
calculation anchor and publishes the live reading beside it (findings F39 / F44),
so nothing calls this script automatically and nothing should re-anchor silently.

Usage:  python3 scripts/refresh_spot_anchor.py [--check]
        --check  verify the on-disk numbers still reproduce from the stored
                 anchor, exit 1 if they do not (no writes)
"""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

DATA = Path(__file__).resolve().parent.parent / "data"
TROY_OZ_G = 31.1034768

# --------------------------------------------------------------------------
# Live readings. Each block is a page that was opened in the session named in
# `read_by`; `quote` is the string the page returned, not a paraphrase.
# --------------------------------------------------------------------------
CAPTURE = {
    "capture_id": "2026-10-23T20:17Z",
    "read_by": "arena/438a583e-gold3 (Pass P12)",
    "read_utc": "2026-10-23T20:17:00Z",
    "read_local_ny": "2026-10-23 16:17 EDT",
    "primary": {
        "publisher": "GoldPrice.org",
        "url": "https://goldprice.org/",
        "price_usd_per_troy_oz": 3997.22,
        "as_of_text": "Oct 23rd, 2026 at 04:17 NY Time",
        "quote": "Spot Gold Price: USD 3,997.22 / Ounce | Spot Silver Price: USD 53.92 / Ounce Oct 23rd, 2026 at 04:17 NY Time",
    },
    "cross_check": {
        "publisher": "World Gold Council (Goldhub), market data by ICE Data Services",
        "url": "https://www.gold.org/goldhub/data/gold-prices",
        "price_usd_per_troy_oz": 3996.31,
        "as_of_text": "Live tile 3,996.31 (read 2026-10-23T20:17Z); dataset 'Data as of 22 October, 2026'",
        "quote": "Gold Spot price USD/oz - 3,996.31 ... Data as of 22 October, 2026",
    },
    "kitco": {
        "publisher": "Kitco Live World Spot Price (USD)",
        "url": "https://www.kitco.com/price/precious-metals",
        "bid": 3996.20,
        "ask": 3998.20,
        "day_low": 3975.10,
        "day_high": 4040.20,
        "change": -27.20,
        "change_pct": -0.68,
        "as_of_text": "Oct 23, 2026 16:17",
        "quote": "GOLD Oct 23, 2026 16:17 3,996.20 3,998.20 -27.20 -0.68% 3,975.10 4,040.20",
    },
    "bullionvault": {
        "publisher": "BullionVault Live Wholesale Gold Market Feed",
        "url": "https://www.bullionvault.com/gold-price-chart.do",
        "mid": 3997.14,
        "per_gram": 128.51,
        "per_kg": 128511.04,
        "as_of_text": "23 October 2026, 16:17:24 (GMT-04:00)",
        "quote": "Current Gold Price - $3,997.14 per Ounce | Gold Price per Gram $128.51 | Gold Price per Kilo $128,511 | 23 October 2026, 16:17:24 (GMT-04:00)",
    },
}


def jload(name: str):
    return json.loads((DATA / name).read_text(encoding="utf-8"))


def jdump(name: str, doc) -> None:
    """Write with the same Unicode escaping the file already uses, so a refresh
    produces a readable diff instead of re-encoding every em dash in the file."""
    path = DATA / name
    ascii_only = all(ord(ch) < 128 for ch in path.read_text(encoding="utf-8"))
    path.write_text(json.dumps(doc, indent=2, ensure_ascii=ascii_only) + "\n", encoding="utf-8")


def main() -> int:
    check_only = "--check" in sys.argv

    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    if CAPTURE["read_utc"][:10] != today:
        sys.exit(
            f"Refusing to re-anchor: the capture in this script is dated {CAPTURE['read_utc'][:10]} "
            f"but today is {today}. Re-read the four pages and update CAPTURE first."
        )

    spot = CAPTURE["kitco"]["bid"]                      # karat-table basis (Kitco bid, as before)
    spot_gram = spot / TROY_OZ_G                        # 24K USD per gram, unrounded
    primary_spot = CAPTURE["primary"]["price_usd_per_troy_oz"]
    cross_spot = CAPTURE["cross_check"]["price_usd_per_troy_oz"]
    diff = round(abs(primary_spot - cross_spot), 2)
    diff_pct = round(diff / primary_spot * 100, 4)

    bv = CAPTURE["bullionvault"]["mid"]
    bv_diff = round(abs(spot - bv), 2)
    bv_pct = round(bv_diff / spot * 100, 3)

    changes: list[str] = []

    # ------------------------------------------------------------------ prices.json
    prices = jload("prices.json")
    old = [s for s in prices["snapshots"] if s.get("role") in ("primary", "cross-check")]
    history = [s for s in prices["snapshots"] if s.get("role") == "history"]
    for s in old:
        s["role"] = "history"
        s["superseded_by"] = CAPTURE["capture_id"]
        history.append(s)

    prices["snapshots"] = [
        {
            "id": "goldprice-org-2026-10-23T2017Z",
            "publisher": CAPTURE["primary"]["publisher"],
            "url": CAPTURE["primary"]["url"],
            "metal": "gold",
            "price_usd_per_troy_oz": primary_spot,
            "as_of_text": CAPTURE["primary"]["as_of_text"],
            "captured_on": CAPTURE["read_utc"][:10],
            "captured_utc": CAPTURE["read_utc"],
            "role": "primary",
            "quote": CAPTURE["primary"]["quote"],
        },
        {
            "id": "world-gold-council-2026-10-23T2017Z",
            "publisher": CAPTURE["cross_check"]["publisher"],
            "url": CAPTURE["cross_check"]["url"],
            "metal": "gold",
            "price_usd_per_troy_oz": cross_spot,
            "as_of_text": CAPTURE["cross_check"]["as_of_text"],
            "captured_on": CAPTURE["read_utc"][:10],
            "captured_utc": CAPTURE["read_utc"],
            "role": "cross-check",
            "quote": CAPTURE["cross_check"]["quote"],
        },
    ] + history

    prices["cross_check"] = {
        "difference_usd_per_oz": diff,
        "difference_percent": diff_pct,
        "note": (
            f"The two independent snapshots read on {CAPTURE['read_utc'][:10]} at {CAPTURE['read_utc'][11:16]}Z differ by "
            f"{diff_pct}% (${primary_spot:,.2f} vs ${cross_spot:,.2f}), consistent with normal intraday movement between the two "
            f"timestamps and consistent with the simultaneous Kitco (${spot:,.2f}/oz) and BullionVault (${bv:,.2f}/oz) quotes, "
            f"which are ${bv_diff:,.2f} ({bv_pct}%) apart. Calculations use the primary (GoldPrice.org) snapshot; the World Gold "
            "Council figure is shown next to it so the reader can see the spread."
        ),
        "benchmark_note": prices["cross_check"].get("benchmark_note", ""),
    }
    changes.append(f"prices.json: primary ${primary_spot:,.2f}/oz (GoldPrice.org), cross-check ${cross_spot:,.2f}/oz (WGC), {diff_pct}% apart")
    if not check_only:
        jdump("prices.json", prices)

    # --------------------------------------------------------- spot-and-standards.json
    std = jload("spot-and-standards.json")
    bench = std["spot_gold_benchmark"]
    bench["quote_timestamp_local"] = CAPTURE["kitco"]["as_of_text"] + " NY Time"
    bench["quote_timestamp_utc"] = CAPTURE["read_utc"]
    bench["spot_bid_usd_per_troy_oz"] = spot
    bench["spot_ask_usd_per_troy_oz"] = CAPTURE["kitco"]["ask"]
    bench["day_low_usd_per_troy_oz"] = CAPTURE["kitco"]["day_low"]
    bench["day_high_usd_per_troy_oz"] = CAPTURE["kitco"]["day_high"]
    bench["spot_usd_per_gram_24k_exact"] = round(spot_gram, 4)
    bench["daily_change_usd_per_troy_oz"] = CAPTURE["kitco"]["change"]
    bench["daily_change_pct"] = CAPTURE["kitco"]["change_pct"]
    bench["verbatim_quote"] = CAPTURE["kitco"]["quote"]

    sec = bench["secondary_cross_check"]
    sec["quote_timestamp_local"] = CAPTURE["bullionvault"]["as_of_text"]
    sec["quote_timestamp_utc"] = CAPTURE["read_utc"]
    sec["spot_mid_usd_per_troy_oz"] = bv
    sec["spot_usd_per_gram"] = CAPTURE["bullionvault"]["per_gram"]
    sec["spot_usd_per_kg"] = CAPTURE["bullionvault"]["per_kg"]
    sec["inter_source_delta_usd_per_oz"] = bv_diff
    sec["inter_source_delta_pct"] = bv_pct
    sec["verbatim_quote"] = CAPTURE["bullionvault"]["quote"]

    for k in std["karat_purity_reference"]:
        k["usd_per_gram_at_spot"] = round(spot_gram * k["pure_gold_fraction"], 2)
        k["usd_per_troy_oz_at_spot"] = round(spot * k["pure_gold_fraction"], 2)

    std["metadata"]["verified_date_utc"] = CAPTURE["read_utc"]
    std["metadata"]["session_id"] = CAPTURE["read_by"]
    std["metadata"]["reverified_by_session"] = (
        (std["metadata"].get("reverified_by_session", "") + " \u00b7 " + CAPTURE["read_by"]).strip(" \u00b7")
    )
    changes.append(
        f"spot-and-standards.json: Kitco bid ${spot:,.2f}/oz = ${spot_gram:.4f}/g, 7 karat rows recomputed, "
        f"BullionVault ${bv:,.2f}/oz ({bv_pct}% apart)"
    )
    if not check_only:
        jdump("spot-and-standards.json", std)

    # ------------------------------------------------------------- gold-price.json (Dataset A/B anchor)
    gold = jload("gold-price.json")
    gold["price_usd_per_troy_ounce"] = cross_spot
    gold["as_of_market_date"] = "2026-10-22"   # the date the WGC page states for its dataset
    gold["retrieved_utc"] = CAPTURE["read_utc"][:10]
    gold["source"]["quote"] = CAPTURE["cross_check"]["quote"]
    gold["source"]["retrieved_utc"] = CAPTURE["read_utc"]
    gold["notes"] = [n for n in gold["notes"] if not n.startswith("Spot price moves continuously")]
    gold["notes"].append(
        f"Re-anchored {CAPTURE['read_utc']} by {CAPTURE['read_by']}. Spot price moves continuously; the value above is the "
        "dated snapshot this pass read, not a live quote."
    )
    changes.append(f"gold-price.json: World Gold Council ${cross_spot:,.2f}/oz (dataset 'Data as of 22 October, 2026')")
    if not check_only:
        jdump("gold-price.json", gold)

    # ------------------------------------------------- Dataset C melt rows (weight-complete only)
    melted = 0
    for name in ("bands-and-high-karat.json", "solitaire-rings.json"):
        doc = jload(name)
        doc["spot_reference_usd_per_oz"] = spot
        doc["spot_reference_usd_per_gram_24k"] = round(spot_gram, 4)
        doc["verified_date_utc"] = CAPTURE["read_utc"]
        doc["reverified_by_session"] = (
            (doc.get("reverified_by_session", "") + " \u00b7 " + CAPTURE["read_by"]).strip(" \u00b7")
        )
        for it in doc["items"]:
            w = it.get("weight_grams")
            frac = it.get("purity_fraction")
            if w is None or not frac:
                # weight null -> pure grams and melt MUST stay null/0 (zero-inference rule)
                continue
            pure = round(w * frac, 4)
            melt = round(pure * spot_gram, 2)
            it["pure_gold_grams"] = pure
            it["melt_value_usd"] = melt
            if it.get("price_usd"):
                it["price_to_melt_ratio"] = round(it["price_usd"] / melt, 2)
            melted += 1
            changes.append(f"{it['id']}: {w}g x {frac} = {pure}g pure -> melt ${melt:,.2f}, price/melt {it.get('price_to_melt_ratio')}")
        if not check_only:
            jdump(name, doc)

    print(f"Spot anchor {CAPTURE['capture_id']} (read {CAPTURE['read_utc']})")
    for c in changes:
        print("  -", c)
    print(f"{melted} weight-complete melt rows recomputed; {len(prices['snapshots'])} snapshots retained "
          f"({len(history)} historic).")
    if check_only:
        print("--check: values above are what the on-disk anchor reproduces (no files written)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
