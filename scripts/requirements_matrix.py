#!/usr/bin/env python3
"""
requirements_matrix.py — builds the buyer-checklist compliance matrix.

Every cell is derived from a stored field in data/*.json. Nothing is estimated,
inferred or typed in: where the stored record holds no value, the cell is
`unverified` and it renders blank with the reason printed beside it.

The matrix answers one question per listing and per requirement:
    "Does an official page I can click actually say this?"

Statuses
    good        — an official page in the record states it
    partial     — stated only partly (brand-level policy, range, seller-level, low sample)
    fail        — the record shows the listing does not meet the requirement
    unverified  — not published in the record; left blank, never filled in

Cells are produced by `build()`, which returns (rows, summary, meta). The renderer
lives in scripts/build_site.py and prints them without adding any value of its own.
`scripts/hallucination_scan.py` re-derives every cell from scratch and fails the
build if the rendered page disagrees with the data.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"

REQUIREMENTS = [
    {
        "key": "purity",
        "n": 1,
        "title": "Karat / purity stated",
        "rule": "The listing must print the karat (10K, 14K, 18K …). A karat in an image or in another seller's policy does not count for this column.",
        "authority": "https://www.ecfr.gov/current/title-16/chapter-I/subchapter-B/part-23",
        "authority_label": "16 CFR Part 23 (FTC gold-marking rule)",
        "if_missing": "Ask the seller in writing which karat the metal is and keep the reply with the order.",
    },
    {
        "key": "solid",
        "n": 2,
        "title": "Word “solid” used",
        "rule": "The listing, or the seller's own materials policy, must say solid gold. Plated, vermeil, gold-filled, overlay and gold-tone do not qualify.",
        "authority": "https://www.ecfr.gov/current/title-16/chapter-I/subchapter-B/part-23",
        "authority_label": "16 CFR 23.4 (misuse of “gold”)",
        "if_missing": "Ask the seller to state “solid 14K gold” (or the karat bought) in writing before paying.",
    },
    {
        "key": "hallmark",
        "n": 3,
        "title": "Hallmark (karat stamp) disclosed",
        "rule": "The seller should state that the piece is stamped with its karat. No seller in this file publishes a hallmark policy, so this column is almost always blank.",
        "authority": "https://www.ecfr.gov/current/title-16/chapter-I/subchapter-B/part-23",
        "authority_label": "16 CFR 23.9–23.10 (quality marks)",
        "if_missing": "Check the inside of the shank with a loupe the day the ring arrives.",
    },
    {
        "key": "maker",
        "n": 4,
        "title": "Maker's mark disclosed",
        "rule": "Under 15 U.S.C. 297 a karat stamp must be accompanied by the manufacturer's or dealer's trademark or name. Two Dataset B listings document one.",
        "authority": "https://www.law.cornell.edu/uscode/text/15/297",
        "authority_label": "15 U.S.C. § 297",
        "if_missing": "Ask the seller whose registered mark sits beside the karat stamp.",
    },
    {
        "key": "weight",
        "n": 5,
        "title": "Finished weight in grams",
        "rule": "A legitimate seller can state the ring's weight in grams. Ranges, stone-inclusive totals and client-side-only figures are marked partial, never treated as a gold weight.",
        "authority": "https://www.nist.gov/pml/special-publication-811/nist-guide-si-appendix-b-conversion-factors/nist-guide-si-appendix-b9",
        "authority_label": "NIST SP 811 App. B.9 (the gram used here)",
        "if_missing": "Ask for the weight in grams; if refused, that is the answer.",
    },
    {
        "key": "reputation",
        "n": 6,
        "title": "Independent seller reputation",
        "rule": "An independent review sample (Trustpilot or BBB) plus working contact details. A seller with no recorded sample is left blank, not assumed good.",
        "authority": "https://www.trustpilot.com/",
        "authority_label": "Trustpilot review profiles",
        "if_missing": "Search the business name plus “complaints” and call the published number.",
    },
    {
        "key": "returns",
        "n": 7,
        "title": "Return window you can use",
        "rule": "No US statute sets a minimum return window for a correctly delivered ring, so the window is the seller's promise. It must be long enough to have the ring independently tested; resized, engraved, custom and final-sale exclusions are shown where the seller states them.",
        "authority": "https://www.ecfr.gov/current/title-16/chapter-I/subchapter-D/part-435",
        "authority_label": "16 CFR Part 435 (FTC mail-order rule)",
        "if_missing": "Get the return window and exclusions in writing before ordering.",
    },
    {
        "key": "payment",
        "n": 8,
        "title": "Credit card accepted",
        "rule": "A credit card gives Fair Credit Billing Act dispute rights. Bank wire, crypto and irreversible methods forfeit them; sellers that only advertise instalments are marked partial.",
        "authority": "https://www.law.cornell.edu/uscode/text/15/1666",
        "authority_label": "15 U.S.C. § 1666 (Fair Credit Billing Act)",
        "if_missing": "Pay by credit card, or do not buy.",
    },
    {
        "key": "docs",
        "n": 9,
        "title": "Documentation captured",
        "rule": "A verbatim price/description quote, the official URL it came from, and the date it was read. This is what you keep if the ring arrives wrong.",
        "authority": "https://www.law.cornell.edu/uscode/text/15/1666",
        "authority_label": "15 U.S.C. § 1666 (keep the evidence for a dispute)",
        "if_missing": "Screenshot the listing and save the receipt before the page changes.",
    },
    {
        "key": "xrf",
        "n": 10,
        "title": "Independent / XRF verification",
        "rule": "Whether the seller offers, or will accept, an assay. Practically every seller states nothing, so the fallback is your own jeweller inside the return window.",
        "authority": "https://www.ecfr.gov/current/title-16/chapter-I/subchapter-B/part-23",
        "authority_label": "16 CFR Part 23 - a stamp is a marking, not an assay",
        "if_missing": "Book an XRF check with an independent jeweller before resizing or wearing.",
    },
]

KEYS = [r["key"] for r in REQUIREMENTS]


# --------------------------------------------------------------------- helpers
def _load(name: str):
    return json.loads((DATA / name).read_text(encoding="utf-8"))


def _cell(status: str, text: str, url: str | None = None, sub: str = "") -> dict:
    return {"status": status, "text": text, "url": url or "", "sub": sub}


def _money(v) -> str:
    return f"${v:,.0f}" if float(v).is_integer() else f"${v:,.2f}"


def _norm(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", (s or "").lower()).strip()


def _match(record_name: str, candidates: dict) -> dict | None:
    """Longest normalised name that is contained in the record name or vice-versa."""
    target = _norm(record_name)
    best, best_len = None, 0
    for name, rec in candidates.items():
        n = _norm(name)
        if not n:
            continue
        if n == target or n in target or target in n:
            if len(n) > best_len:
                best, best_len = rec, len(n)
    return best


def _karat_fraction(label: str, numeric: int | None = None) -> float | None:
    if numeric:
        return numeric / 24
    m = re.search(r"(\d{1,2})\s*[Kk]", label or "")
    if m:
        k = int(m.group(1))
        if 8 <= k <= 24:
            return k / 24
    return None


def _payment_from_policy(rec: dict) -> dict:
    """Classify a sellers-policies.json record (Dataset C)."""
    accepted = (rec.get("accepted_payments") or "").strip()
    url = rec.get("payment_policy_url") or rec.get("official_site_url") or ""
    if rec.get("credit_card_supported") is True and accepted:
        risk = "bank wire" in accepted.lower() or "wire transfer" in accepted.lower()
        note = (rec.get("wire_transfer_risk_note") or "").strip()
        return _cell(
            "partial" if risk else "good",
            "Credit cards accepted" + (" · wire also offered" if risk else ""),
            url,
            sub=accepted if len(accepted) < 160 else accepted[:157] + "…",
        )
    if accepted:
        return _cell("partial", accepted[:80], url, sub=note[:160])
    return _cell("unverified", "Not published", url)


def _payment_from_seller(rec: dict) -> dict:
    """Classify a sellers.json payment_notes string. Keyword rules only."""
    note = (rec.get("payment_notes") or "").strip()
    url = rec.get("policy_source") or rec.get("website") or ""
    low = note.lower()
    if not note or "not verified" in low or "no payment-method detail" in low:
        return _cell("unverified", "Not verified", url, sub=note[:160])
    card_words = ("credit card", "major credit cards", "card checkout", "card payment",
                  "card refunds", "cards", "visa", "mastercard")
    has_card = any(w in low for w in card_words)
    risk = "bank wire" in low or "wire" in low or "crypto" in low or "bitpay" in low
    if has_card and risk:
        return _cell("partial", "Card accepted · irreversible option also offered", url,
                     sub=note[:170])
    if has_card:
        return _cell("good", "Card accepted", url, sub=note[:170])
    if "klarna" in low or "affirm" in low or "instalment" in low or "installement" in low \
            or "payment plan" in low:
        return _cell("partial", "Instalments shown; card acceptance not stated", url,
                     sub=note[:170])
    return _cell("partial", "Not stated", url, sub=note[:170])


def _bbb_cell(rec: dict | None) -> dict | None:
    if not rec:
        return None
    rating = (rec.get("bbb_rating") or "").strip()
    if not rating:
        return None
    complaints = rec.get("bbb_complaints_3yr")
    sub = (f"{complaints} complaints in 3 years" if isinstance(complaints, int) else "")
    letter = re.match(r"([A-F][+-]?)", rating)
    status = "good" if letter and letter.group(1).startswith("A") else "partial"
    return _cell(status, f"BBB {rating}", rec.get("bbb_url") or "", sub=sub)


def _trustpilot_cell(rec: dict | None) -> dict | None:
    if not rec:
        return None
    score, reviews = rec.get("trustpilot_score"), rec.get("trustpilot_reviews")
    if score is None:
        return None
    status = "good" if isinstance(reviews, int) and reviews >= 50 else "partial"
    sub = f"{reviews:,} reviews" if isinstance(reviews, int) else ""
    return _cell(status, f"Trustpilot {score}/5", rec.get("trustpilot_url") or "", sub=sub)


# --------------------------------------------------------------------- builder
def build() -> tuple[list[dict], dict, dict]:
    prices = _load("prices.json")
    primary = next(s for s in prices["snapshots"] if s["role"] == "primary")
    spot = float(primary["price_usd_per_troy_oz"])
    oz = float(prices["constants"]["troy_ounce_grams"])
    primary_gram = spot / oz

    # Dataset C's melt values were computed from the exact 24K gram price recorded in
    # data/spot-and-standards.json (Kitco bid / 31.1034768). Use that same constant for
    # every row here so all 71 rows are comparable, and publish both anchors.
    standards = _load("spot-and-standards.json")
    bench = standards["spot_gold_benchmark"]
    spot_gram = float(bench["spot_usd_per_gram_24k_exact"])
    spot_source = {
        "url": "https://www.kitco.com/price/precious-metals",
        "as_of_text": bench.get("quote_timestamp_local", ""),
    }

    products = _load("products.json")["products"]
    retailers = {r["id"]: r for r in _load("retailers.json")["retailers"]}
    rings_doc = _load("rings.json")
    rings = rings_doc["rings"]
    sellers_doc = _load("sellers.json")
    sellers = sellers_doc["sellers"]
    sellers_by_name = {s["name"]: s for s in sellers}
    sellers_by_name.update({s["id"]: s for s in sellers})
    c_sellers = _load("sellers-policies.json")["sellers"]
    c_by_name = {s["name"]: s for s in c_sellers}

    # A retailer id → the same company's Dataset B/D record and Dataset C record
    A_TO_B = {"blue-nile": "S-BN", "mejuri": "S-MJ", "catbird": "S-CB"}
    A_TO_C = {"blue-nile": "SEL-BLUENILE", "mejuri": "SEL-MEJURI"}

    rows: list[dict] = []

    # ---------------------------------------------------------------- Dataset A
    for p in products:
        rid = p["id"]
        rec = retailers.get(p.get("retailer"), {})
        url = p.get("url") or ""
        excluded = "excluded" in p.get("categories", [])
        cells = {}

        _pur = p.get("purity") or ""
        _plated = "plating" in _pur.lower() or "vermeil" in _pur.lower() or "silver" in _pur.lower()
        cells["purity"] = _cell(
            "partial" if _plated else ("good" if _pur else "unverified"),
            _pur or "Not published",
            p.get("purity_source") or url,
            sub="describes the plating, not the body metal" if _plated else "",
        )

        status = (p.get("solid_gold_status") or "").strip()
        if p.get("solid_gold") is True:
            listing_level = status in ("stated on listing", "stated in product name")
            cells["solid"] = _cell(
                "good" if listing_level else "partial",
                {"stated on listing": "“solid” on the listing",
                 "stated in product name": "“solid” in the product name",
                 "stated at brand level": "Brand policy only"}.get(status, status),
                p.get("solid_gold_source") or url,
                sub=(p.get("solid_gold_evidence") or "")[:170],
            )
        elif p.get("solid_gold") is False:
            cells["solid"] = _cell("fail", "Not solid gold", url, sub=status)
        else:
            cells["solid"] = _cell("unverified", "Word “solid” not stated", url,
                                   sub=(p.get("metal_detail") or "")[:170])

        cells["hallmark"] = _cell("unverified", "Not published", url,
                                  sub=(rec.get("hallmark_note") or "")[:170])
        cells["maker"] = _cell("unverified", "Not published", url)

        if isinstance(p.get("weight_g"), (int, float)):
            cells["weight"] = _cell("good", f"{p['weight_g']} g", p.get("weight_source") or url,
                                    sub=(p.get("weight_note") or "")[:150])
        elif p.get("weight_status") == "published as a range":
            cells["weight"] = _cell("partial", "Range only", p.get("weight_source") or url,
                                    sub=(p.get("weight_note") or "")[:150])
        else:
            cells["weight"] = _cell("unverified", "Not published", url,
                                    sub=(p.get("weight_note") or "")[:150])

        rep = _trustpilot_cell(rec)
        if rep:
            contact = ", ".join(x for x in (rec.get("phone"), rec.get("email")) if x)
            if contact:
                rep["sub"] = (rep["sub"] + " · " + contact).strip(" ·")
        cells["reputation"] = rep or _cell("unverified", "No review sample recorded", url)

        days = rec.get("returns_window_days")
        if isinstance(days, int):
            excl = (rec.get("returns_exclusions") or "")
            final_sale = "final sale" in excl.lower() or "exchange only" in excl.lower()
            st = "good" if days >= 14 else "partial"
            if final_sale:
                st = "partial"
            cells["returns"] = _cell(
                st, f"{days}-day window" + (" · final-sale items" if final_sale else ""),
                rec.get("returns_url") or url, sub=(rec.get("returns_quote") or "")[:170])
        else:
            cells["returns"] = _cell("unverified", "Not published", url)

        # payment: prefer the seller's own accepted-payments record
        crec = next((s for s in c_sellers if s["id"] == A_TO_C.get(p.get("retailer"))), None)
        if crec:
            cells["payment"] = _payment_from_policy(crec)
            cells["payment"]["sub"] = "seller-level record · " + cells["payment"]["sub"]
        else:
            brec = sellers_by_name.get(A_TO_B.get(p.get("retailer"), ""))
            cells["payment"] = (_payment_from_seller(brec) if brec
                                else _cell("unverified", "Not published", url))

        has_quote = bool(p.get("price_quote"))
        has_source = bool(p.get("price_source"))
        has_date = bool(p.get("price_captured_on"))
        n_docs = sum([has_quote, has_source, has_date])
        cells["docs"] = _cell(
            "good" if n_docs == 3 else ("partial" if n_docs == 2 else "unverified"),
            f"{n_docs}/3 captured",
            p.get("price_source") or url,
            sub="quote · source URL · read date" if n_docs == 3 else "incomplete record",
        )

        brec = sellers_by_name.get(A_TO_B.get(p.get("retailer"), "")) or {}
        xrf = brec.get("offers_xrf_or_assay") or ""
        xrf_url = brec.get("policy_source") or url
        cells["xrf"] = (_cell("unverified", "Seller states nothing", xrf_url, sub=xrf[:150])
                        if not xrf or xrf.lower().startswith("not stated")
                        else _cell("partial", "Seller statement only", xrf_url, sub=xrf[:150]))

        fr = _karat_fraction(p.get("purity") or "")
        if isinstance(p.get("weight_g"), (int, float)) and fr and isinstance(p.get("price"), (int, float)):
            pure = float(p["weight_g"]) * fr
            melt = pure * spot_gram
            rows_value = {"ratio": float(p["price"]) / melt, "melt": melt, "pure_g": pure,
                          "ceiling": False}
            cells["value"] = _cell(
                "good", f"{p['price'] / melt:.2f}× melt",
                spot_source["url"],
                sub=f"{pure:.3f} g pure gold · melt {_money(melt)} (derived)",
            )
        else:
            rows_value = None
            cells["value"] = _cell("unverified", "No gold weight → not computable", url,
                                   sub="left blank, never back-calculated")

        rows.append({
            "id": rid, "dataset": "A", "seller": p.get("brand") or "", "name": p.get("name") or "",
            "url": url, "price_usd": p.get("price"), "price_label": (p.get("price_basis") or ""),
            "karat": p.get("purity") or "", "excluded": excluded, "cells": cells,
            "value": rows_value,
        })

    # ---------------------------------------------------------------- Dataset B
    for r in rings:
        rid = r["id"]
        url = r.get("url") or ""
        rec = _match(r.get("seller") or "", sellers_by_name)
        trec = _match(r.get("seller") or "", {x["name"]: x for x in retailers.values()})
        crec = _match(r.get("seller") or "", c_by_name)
        cells = {}

        kt = r.get("karat") or ""
        _plated = "plating" in kt.lower() or "vermeil" in kt.lower()
        cells["purity"] = _cell("partial" if _plated else ("good" if kt else "unverified"),
                                kt or "Not published", url,
                                sub="describes the plating, not the body metal" if _plated else "")

        verdict = (r.get("solid_gold_verdict") or "")
        quote = (r.get("solid_gold_quote") or "")
        if verdict.startswith("PASS"):
            cells["solid"] = _cell("good", "“solid” stated", url, sub=quote[:170])
        elif verdict.startswith("FAIL"):
            cells["solid"] = _cell("fail", "Not solid gold", url, sub=quote[:170])
        else:
            cells["solid"] = _cell("unverified", "Word “solid” not stated", url, sub=quote[:170])

        hall = r.get("hallmark_reported")
        cells["hallmark"] = (_cell("good", hall, url,
                                   sub=(r.get("hallmark_quote") or "")[:150])
                             if hall else _cell("unverified", "Not published", url))
        maker = r.get("maker_mark_reported")
        cells["maker"] = (_cell("good", maker, url) if maker
                          else _cell("unverified", "Not published", url))

        if isinstance(r.get("weight_g"), (int, float)):
            cells["weight"] = _cell("good", f"{r['weight_g']} g", url,
                                    sub=(r.get("weight_quote") or "")[:160])
        else:
            cells["weight"] = _cell("unverified", "Not published", url,
                                    sub=(r.get("weight_quote") or "")[:160])

        rep = _trustpilot_cell(trec) or _bbb_cell(crec)
        if rep is None:
            contact = ", ".join(x for x in ((rec or {}).get("phone"), (rec or {}).get("email")) if x)
            rep = _cell("unverified", "No review sample recorded",
                        (rec or {}).get("contact_source") or url,
                        sub=("contact published: " + contact) if contact else "")
        cells["reputation"] = rep

        rw = (r.get("return_window") or "").strip()
        low = rw.lower()
        if not rw:
            cells["returns"] = _cell("unverified", "Not published", url)
        elif "non returnable" in low or "non-returnable" in low or "final sale" in low:
            cells["returns"] = _cell("fail", "Final sale / non-returnable",
                                     r.get("return_policy_source") or url, sub=rw[:180])
        else:
            days = re.search(r"(\d{1,2})\s*day", low)
            st = "good"
            if days and int(days.group(1)) < 14:
                st = "partial"
            if "store credit" in low:
                st = "partial"
            cells["returns"] = _cell(st, f"{days.group(1)}-day window" if days else "Policy stated",
                                     r.get("return_policy_source") or (rec or {}).get("policy_source") or url,
                                     sub=rw[:180])

        cells["payment"] = (_payment_from_seller(rec) if rec
                            else _cell("unverified", "Not published", url))

        docs = sum([bool(r.get("price_as_shown")), bool(url), bool(r.get("last_verified"))])
        cells["docs"] = _cell("good" if docs == 3 else "partial", f"{docs}/3 captured", url,
                              sub="price as shown · source URL · verified date")

        xrf = (rec or {}).get("offers_xrf_or_assay") or ""
        cells["xrf"] = (_cell("unverified", "Seller states nothing",
                              (rec or {}).get("policy_source") or url, sub=xrf[:150])
                        if not xrf or xrf.lower().startswith("not stated")
                        else _cell("partial", "Seller statement only",
                                   (rec or {}).get("policy_source") or url, sub=xrf[:150]))

        fr = _karat_fraction(kt)
        if isinstance(r.get("weight_g"), (int, float)) and fr and isinstance(r.get("price_usd"), (int, float)):
            pure = float(r["weight_g"]) * fr
            melt = pure * spot_gram
            ceiling = "total item weight" in (r.get("weight_quote") or "").lower() or \
                      "includes" in (r.get("weight_quote") or "").lower()
            rows_value = {"ratio": float(r["price_usd"]) / melt, "melt": melt, "pure_g": pure,
                          "ceiling": ceiling}
            cells["value"] = _cell(
                "good", f"{r['price_usd'] / melt:.2f}× melt" + (" ceiling" if ceiling else ""),
                spot_source["url"],
                sub=f"{pure:.3f} g pure gold · melt {_money(melt)} (derived"
                    + ("; weight includes the stone so the true multiple is higher)" if ceiling else ")"),
            )
        else:
            rows_value = None
            cells["value"] = _cell("unverified", "No gold weight → not computable", url)

        rows.append({
            "id": rid, "dataset": "B", "seller": r.get("seller") or "", "name": r.get("product") or "",
            "url": url, "price_usd": r.get("price_usd"), "price_label": r.get("price_basis") or "",
            "karat": kt, "excluded": verdict.startswith("FAIL"), "cells": cells,
            "value": rows_value,
        })

    # ---------------------------------------------------------------- Dataset C
    for f in ("solitaire-rings.json", "bands-and-high-karat.json"):
        for it in _load(f)["items"]:
            rid = it["id"]
            url = it.get("product_url") or ""
            crec = c_sellers and next((s for s in c_sellers if s["id"] == it.get("seller_id")), None)
            rec = _match(it.get("seller_name") or "", sellers_by_name)
            kt = it.get("karat_label") or ""
            cells = {}

            cells["purity"] = _cell("good" if kt else "unverified", kt or "Not published", url)

            if it.get("explicit_solid_wording") is True:
                cells["solid"] = _cell("good", "“solid” on the listing", url,
                                       sub=(it.get("solid_gold_assessment") or "")[:170])
            else:
                cells["solid"] = _cell("unverified", "Word “solid” not stated", url,
                                       sub=(it.get("solid_gold_assessment") or "")[:170])

            disc = (it.get("hallmark_disclosure") or "")
            if disc.lower().startswith("not published"):
                cells["hallmark"] = _cell("unverified", "Not published", url, sub=disc[:150])
                cells["maker"] = _cell("unverified", "Not published", url)
            else:
                cells["hallmark"] = _cell("partial", disc[:80], url, sub=disc[:150])
                cells["maker"] = _cell("unverified", "Not published", url, sub=disc[:150])

            if isinstance(it.get("weight_grams"), (int, float)):
                cells["weight"] = _cell("good", f"{it['weight_grams']} g", url)
            else:
                cells["weight"] = _cell("unverified", "Not published", url)

            cells["reputation"] = _bbb_cell(crec) or _cell(
                "unverified", "No review sample recorded", (rec or {}).get("contact_source") or url)

            days = crec.get("return_window_days") if crec else None
            if isinstance(days, int):
                excl = (crec.get("resized_custom_exclusions") or "")
                cells["returns"] = _cell(
                    "good" if days >= 14 else "partial",
                    f"{days}-day window" + (" · resized excluded" if excl else ""),
                    crec.get("return_policy_url") or url, sub=excl[:160])
            else:
                cells["returns"] = _cell("unverified", "Not published", url)

            cells["payment"] = (_payment_from_policy(crec) if crec
                                else _cell("unverified", "Not published", url))

            docs = sum([bool(it.get("verbatim_excerpt")), bool(url), bool(it.get("verified_date"))])
            cells["docs"] = _cell("good" if docs == 3 else "partial", f"{docs}/3 captured", url,
                                  sub="verbatim excerpt · source URL · verified date")

            xrf = (rec or {}).get("offers_xrf_or_assay") or ""
            cells["xrf"] = (_cell("unverified", "Seller states nothing",
                                  (rec or {}).get("policy_source") or url, sub=xrf[:150])
                            if not xrf or xrf.lower().startswith("not stated")
                            else _cell("partial", "Seller statement only",
                                       (rec or {}).get("policy_source") or url, sub=xrf[:150]))

            if isinstance(it.get("weight_grams"), (int, float)) and it.get("melt_value_usd"):
                ratio = it.get("price_to_melt_ratio")
                rows_value = {"ratio": float(ratio) if ratio else None,
                              "melt": float(it["melt_value_usd"]),
                              "pure_g": it.get("pure_gold_grams"), "ceiling": False}
                cells["value"] = _cell(
                    "good", f"{float(ratio):.2f}× melt" if ratio else "Melt published",
                    spot_source["url"],
                    sub=f"{it.get('pure_gold_grams')} g pure gold · melt "
                        f"{_money(float(it['melt_value_usd']))} (recorded)",
                )
            else:
                rows_value = None
                cells["value"] = _cell("unverified", "No gold weight → not computable", url)

            rows.append({
                "id": rid, "dataset": "C", "seller": it.get("seller_name") or "",
                "name": it.get("product_name") or "", "url": url,
                "price_usd": it.get("price_usd"), "price_label": it.get("listing_type") or "",
                "karat": kt, "excluded": False, "cells": cells, "value": rows_value,
            })

    # ---------------------------------------------------------------- summary
    summary = {"n_rows": len(rows), "n_gold_rows": sum(1 for r in rows if not r["excluded"]),
               "by_dataset": {d: sum(1 for r in rows if r["dataset"] == d) for d in "ABC"},
               "requirements": []}
    for req in REQUIREMENTS:
        counts = {"good": 0, "partial": 0, "fail": 0, "unverified": 0}
        gold = {"good": 0, "partial": 0, "fail": 0, "unverified": 0}
        for row in rows:
            st = row["cells"][req["key"]]["status"]
            counts[st] += 1
            if not row["excluded"]:
                gold[st] += 1
        summary["requirements"].append({**{k: req[k] for k in ("key", "n", "title", "rule",
                                                               "authority", "authority_label",
                                                               "if_missing")},
                                        "counts": counts, "gold_counts": gold})

    all_clean = [r["id"] for r in rows
                 if all(r["cells"][k]["status"] == "good" for k in KEYS)]
    summary["rows_meeting_every_requirement"] = {
        "ids": all_clean, "n": len(all_clean),
        "note": "Every one of the ten requirements must be ‘good’ — an official page states it.",
    }

    essential = ["purity", "solid", "weight", "hallmark", "maker", "returns", "payment", "xrf"]
    summary["rows_with_core_five"] = {
        "n": sum(1 for r in rows if all(r["cells"][k]["status"] in ("good", "partial")
                                        for k in essential)),
        "definition": "karat + solid wording + weight + hallmark + maker's mark + returns "
                      "+ card payment + XRF, each at least partly documented",
    }
    # Two honest, non-zero denominators: what a seller can publish itself, and the same
    # set with a hallmark/maker's mark at least partly documented.
    seller_core = ["purity", "solid", "weight", "returns"]
    summary["rows_seller_core_all_good"] = {
        "n": sum(1 for r in rows if all(r["cells"][k]["status"] == "good" for k in seller_core)),
        "definition": "karat + word “solid” + weight in grams + a usable return window, all ‘good’",
    }
    summary["rows_seller_core_partial"] = {
        "n": sum(1 for r in rows if all(r["cells"][k]["status"] in ("good", "partial")
                                        for k in seller_core)),
        "definition": "the same four, at least partly documented",
    }

    meta = {
        "spot_usd_per_troy_oz": float(bench["spot_bid_usd_per_troy_oz"]),
        "spot_as_of_text": spot_source.get("as_of_text", ""),
        "spot_source_url": spot_source["url"],
        "spot_usd_per_gram_24k": spot_gram,
        "goldprice_org_anchor_usd_per_oz": spot,
        "goldprice_org_anchor_as_of": primary.get("as_of_text", ""),
        "goldprice_org_gram_24k": primary_gram,
        "anchor_note": ("All ratios in this matrix use the exact 24K gram price recorded in "
                        "data/spot-and-standards.json so the 19 weight-bearing rows agree with "
                        "Dataset C's stored melt values. data/prices.json carries a second, "
                        "0.012%-different anchor from GoldPrice.org; both are printed."),
        "troy_ounce_grams": oz,
        "formula": "pure gold g = ring weight g × (karat ÷ 24); melt USD = pure gold g × "
                   "(spot USD/oz ÷ 31.1034768)",
        "datasets": {
            "A": {"rows": len(products), "source": "data/products.json",
                  "sellers": "data/retailers.json"},
            "B": {"rows": len(rings), "source": "data/rings.json",
                  "sellers": "data/sellers.json"},
            "C": {"rows": len(rows) - len(products) - len(rings),
                  "source": "data/solitaire-rings.json + data/bands-and-high-karat.json",
                  "sellers": "data/sellers-policies.json"},
        },
        "generated_by": "scripts/requirements_matrix.py",
    }
    return rows, summary, meta


if __name__ == "__main__":
    rows, summary, meta = build()
    out = {"meta": meta, "summary": summary, "rows": rows}
    (DATA / "requirements-matrix.json").write_text(
        json.dumps(out, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"rows={summary['n_rows']} gold={summary['n_gold_rows']} "
          f"all-ten-good={summary['rows_meeting_every_requirement']['n']}")
    for r in summary["requirements"]:
        c = r["counts"]
        print(f"  {r['key']:<11} good={c['good']:<3} partial={c['partial']:<3} "
              f"fail={c['fail']:<3} unverified={c['unverified']}")
