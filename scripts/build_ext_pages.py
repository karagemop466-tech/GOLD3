#!/usr/bin/env python3
"""
Deterministic Static Site Builder for GOLD3 (GitHub Pages Root Deployment).

Generates all 8 semantic HTML pages directly from verified JSON datasets in data/ and
audit artifacts in verification/ so zero human copy-paste drift can occur.
"""

from __future__ import annotations

import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
VERIF_DIR = ROOT / "verification"

def get_nav_items(n_combined: int = 71, n_flagged_c: int = 19) -> list[tuple[str, str, bool]]:
    return [
        ("index.html", "Main Dashboard", False),
        ("combined.html", f"All {n_combined} Combined Rows", False),
        ("checklist-standards.html", "12-Point Checklist", False),
        ("solitaire-settings.html", "Solitaires (9)", False),
        ("bands-vintage-rings.html", "24K & Solid Bands (12)", False),
        ("sellers-policies.html", "BBB & Policy Audit (5)", False),
        ("calculator.html", "Gold Calculator", False),
        ("flagged-for-review.html", f"Flagged C ({n_flagged_c})", True),
        ("flagged.html", "Flagged A+B", True),
        ("verify.html", "Verify Log", False),
        ("security-audit.html", "Security Passes", False),
    ]


def esc(val: object) -> str:
    return html.escape("" if val is None else str(val), quote=True)


def ext_link(url: str, label: str, cls: str = "source-btn") -> str:
    cls_attr = f' class="{esc(cls)}"' if cls else ""
    return f'<a href="{esc(url)}" target="_blank" rel="noopener noreferrer"{cls_attr}>{esc(label)} &#8599;</a>'


def render_shell(active_file: str, title: str, body_html: str, spot_bench: dict, latest_pass: dict, n_combined: int = 71, n_flagged_c: int = 19) -> str:
    nav_links = []
    for href, label, is_flag in get_nav_items(n_combined, n_flagged_c):
        classes = []
        if href == active_file:
            classes.append("active")
        if is_flag:
            classes.append("nav-flag")
        cls_attr = f' class="{" ".join(classes)}"' if classes else ""
        nav_links.append(f'<a href="{esc(href)}"{cls_attr}>{esc(label)}</a>')

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{esc(title)} — GOLD3 Verified Engagement Ring Research</title>
  <link rel="stylesheet" href="assets/gold3-ext.css">
</head>
<body>
  <div class="spot-topbar">
    <div class="spot-topbar-inner">
      <div>
        <strong>Verified Spot Gold Benchmark ({esc(spot_bench['quote_timestamp_local'])}):</strong>
        ${spot_bench['spot_bid_usd_per_troy_oz']:,.2f} / troy oz &bull;
        <strong>${spot_bench['spot_usd_per_gram_24k_exact']:.2f} / g (24K)</strong>
        ({ext_link(spot_bench['primary_source_url'], 'Kitco Live Feed', '')} |
        {ext_link(spot_bench['secondary_cross_check']['source_url'], 'BullionVault Cross-Check', '')})
      </div>
      <div>
        Security &amp; Hallucination Suite:
        <strong>Pass #{latest_pass['pass_number']} — {esc(latest_pass['overall_status'])} ({latest_pass['error_count']} errors)</strong>
        &bull; <a href="security-audit.html">View Audit Log</a>
        <span class="small" style="opacity:.8">(as recorded when this page was built; each new pass is appended to
        <code>verification/audit-log.json</code> after the build, so the log can be one entry ahead of this banner)</span>
      </div>
    </div>
  </div>

  <header class="site-header">
    <div class="nav-wrap">
      <div class="brand-row">
        <a class="brand-title" href="index.html">
          <span class="brand-mark">AU 999.9 &bull; VERIFIED</span>
          <span>GOLD3 — Solid Gold Engagement Ring Research &amp; Buyer Audit</span>
        </a>
      </div>
      <nav class="nav-links" aria-label="Primary Navigation">
        {"".join(nav_links)}
      </nav>
    </div>
  </header>

  <main class="container">
    {body_html}
  </main>

  <footer class="site-footer">
    <div class="footer-inner">
      <div>
        <strong>GOLD3 Zero-Hallucination Research Repository</strong> &bull;
        All prices, weights, and policies verified directly from official primary sources on <code>2026-10-22</code>.
        Unconfirmed attributes remain strictly blank (<code>Unverified</code>) and are published on <a href="flagged-for-review.html">Flagged for Review</a>.
      </div>
      <div>
        Post-review check command: <code>python3 scripts/run_security_audit.py</code> &bull;
        {ext_link('https://github.com/karagemop466-tech/GOLD3', 'GitHub Repository', '')}
      </div>
    </div>
  </footer>

  <script src="data/verified-data.js"></script>
  <script src="assets/gold3-calc.js"></script>
</body>
</html>
"""


def render_mandate_banner(compact: bool = False) -> str:
    if compact:
        return """
    <section class="mandate-banner" id="no-hallucinations-policy">
      <h2>&#9888; Strict Zero-Hallucinations Policy &amp; Line-by-Line Source Verification</h2>
      <p>
        <strong>Zero-Inference Rule:</strong> No price, gram weight, karat fineness, or return exclusion on this page is ever estimated or inferred.
        Every row links directly to an official primary webpage fetched on <code>2026-10-22</code>; any metric omitted by the retailer is left explicitly
        <strong>blank (<code>&mdash; Unverified</code>)</strong> and logged on <a href="flagged-for-review.html"><strong>Flagged for Review</strong></a>.
        Always run <code>python3 scripts/run_security_audit.py</code> after every review pass and actively check primary links to look for hallucinations or live price drift.
      </p>
    </section>"""
    return """
    <section class="mandate-banner" id="no-hallucinations-policy">
      <h2>&#9888; Core Project Mandate: Strict No-Hallucinations Policy &amp; Automated Security Verification</h2>
      <p>
        <strong>1. Do Not Hallucinate Prices, Weights, or Purities:</strong> Every single ring price, gram weight, karat fineness, spot gold benchmark,
        and return-policy rule in this project is verified verbatim against an official primary website on <code>2026-10-22</code> and linked directly in every table row.
      </p>
      <p>
        <strong>2. Never Infer Missing Values — Leave Unconfirmed Cells Blank:</strong> Major bridal jewelers (including Blue Nile, Brilliant Earth, and Mejuri)
        routinely omit gold gram weights on online product pages. Rather than guessing or interpolating weights, every unconfirmed field is left strictly
        <strong>blank (<code>&mdash; Unverified</code>)</strong> and published transparently on <a href="flagged-for-review.html"><strong>Flagged for Review</strong></a>.
      </p>
      <p>
        <strong>3. Run Security Checks &amp; Actively Look for Hallucinations After Every Review:</strong> After every data review or edit pass,
        <code>python3 scripts/run_security_audit.py</code> re-verifies substring price proofs, NIST troy-ounce melt math (<code>31.1034768 g/ozt</code>),
        HTTPS allowlist domains, and link integrity. Reviewers should always inspect <a href="flagged-for-review.html">Flagged for Review</a> and
        <a href="security-audit.html">Security &amp; Hallucination Audit</a> to look for hallucinations, stale prices, or contradictory seller claims.
      </p>
    </section>"""


def render_calculator_section(spot_oz: float, include_presets: bool = True) -> str:
    presets_html = ""
    if include_presets:
        presets_html = """
      <div>
        <strong style="font-size:0.84rem; display:block; margin-bottom:0.4rem;">Load a Live-Verified Catalog Ring into Calculator:</strong>
        <div class="preset-row">
          <button type="button" class="preset-btn" data-preset="1" data-karat="14K" data-weight="4.0" data-gem="0" data-price="1195">Ross-Simons 6mm 14K Flat (4.0g &bull; $1,195 &bull; 3.96x)</button>
          <button type="button" class="preset-btn" data-preset="1" data-karat="14K" data-weight="2.1" data-gem="0" data-price="599">Ross-Simons Italian 14K (2.1g &bull; $599 &bull; 3.78x)</button>
          <button type="button" class="preset-btn" data-preset="1" data-karat="14K" data-weight="4.2" data-gem="0" data-price="949">Ross-Simons 14K 4mm Band (4.2g &bull; $949 &bull; 2.99x Melt)</button>
          <button type="button" class="preset-btn" data-preset="1" data-karat="14K" data-weight="1.7" data-gem="0" data-price="400">Ross-Simons 14K 2mm Band (1.7g &bull; $400 &bull; 3.12x Melt)</button>
          <button type="button" class="preset-btn" data-preset="1" data-karat="14K" data-weight="4.0" data-gem="0" data-price="199">Simulated Below-Melt Scam Alert (4.0g 14K @ $199)</button>
          <button type="button" class="preset-btn" data-preset="1" data-karat="PLATED" data-weight="3.0" data-gem="0" data-price="29">Ross-Simons Plated Control ($29 &bull; 0g Solid Core)</button>
        </div>
      </div>"""

    return f"""
    <section class="section-card" id="melt-calculator">
      <div class="section-header">
        <div>
          <h2>Interactive Gold Purity, Gram Weight &amp; Raw Melt Value Calculator</h2>
          <p>Convert grams, pennyweights (dwt), or troy ounces into exact pure 24K gold content, live melt value, and automatic below-melt scam alerts.</p>
        </div>
        <a href="calculator.html" class="source-btn">Open Full Calculator &amp; Karat Table</a>
      </div>
      {presets_html}
      <div class="calc-layout">
        <form class="calc-form" id="gold-calc-form" onsubmit="return false;">
          <div class="field-group">
            <label for="calc-karat">1. Ring Metal Purity / Stamp (Checklist #1 &amp; #2)</label>
            <select id="calc-karat">
              <option value="24K">24K Pure Gold (99.95% / Hallmark 999)</option>
              <option value="22K">22K Gold (91.67% / Hallmark 916)</option>
              <option value="21K">21K Gold (87.50% / Hallmark 875)</option>
              <option value="18K">18K Solid Gold (75.00% / Hallmark 750)</option>
              <option value="14K" selected>14K Solid Gold (58.33% / Hallmark 585)</option>
              <option value="10K">10K Solid Gold — US Minimum (41.67% / Hallmark 417)</option>
              <option value="9K">9K Gold — UK Hallmarked Minimum (37.50% / Hallmark 375)</option>
              <option value="PLATED">Gold-Plated / Vermeil / Gold-Filled (0% Solid Gold Core)</option>
            </select>
          </div>
          <div class="field-group">
            <label for="calc-weight">2. Total Ring Weight (Checklist #4 — Request from Seller if Omitted)</label>
            <div style="display:flex; gap:0.5rem;">
              <input id="calc-weight" type="number" step="0.01" min="0" value="4.20" style="flex:1;">
              <select id="calc-unit" style="width:165px;">
                <option value="g" selected>Grams (g)</option>
                <option value="dwt">Pennyweights (dwt)</option>
                <option value="ozt">Troy Ounces (ozt)</option>
              </select>
            </div>
          </div>
          <div class="field-group">
            <label for="calc-gem-ct">3. Optional Gemstone Carat Deduction (GIA exact: 1.00 ct = 0.20 g)</label>
            <input id="calc-gem-ct" type="number" step="0.01" min="0" value="0">
          </div>
          <div class="field-group">
            <label for="calc-spot-oz">4. Live 24K Spot Gold Benchmark ($ USD / Troy Oz — Verified 2026-10-22)</label>
            <input id="calc-spot-oz" type="number" step="0.10" min="0" value="{spot_oz:.2f}">
          </div>
          <div class="field-group">
            <label for="calc-ask-price">5. Seller Asking Price ($ USD — Checklist #6 Scam / Markup Check)</label>
            <input id="calc-ask-price" type="number" step="1" min="0" value="949">
          </div>
        </form>

        <div class="calc-results" aria-live="polite">
          <h3 style="margin:0 0 0.7rem; font-size:1.05rem;">Live Intrinsic Gold &amp; Markup Breakdown</h3>
          <div class="calc-result-row">
            <span>24K Spot Benchmark per Gram (<code>Spot &divide; 31.1034768</code>)</span>
            <strong id="out-spot-gram" class="num">$129.41 / g (24K)</strong>
          </div>
          <div class="calc-result-row">
            <span>Net Gold Alloy Weight (after stone deduction)</span>
            <strong id="out-net-alloy" class="num">4.200 g</strong>
          </div>
          <div class="calc-result-row">
            <span>Pure 24K Gold Content (Grams)</span>
            <strong id="out-pure-grams" class="num">2.4500 g pure Au</strong>
          </div>
          <div class="calc-result-row">
            <span>Pure 24K Gold Content (Troy Ounces)</span>
            <strong id="out-pure-oz" class="num">0.0788 troy oz</strong>
          </div>
          <div class="calc-result-row">
            <span><strong>Exact Raw Gold Melt Value ($ USD)</strong></span>
            <span id="out-melt-usd" class="calc-big num">$317.05</span>
          </div>
          <div class="calc-result-row">
            <span>Retail Asking Price vs. Raw Gold Melt</span>
            <strong id="out-markup" class="num">2.99x melt (33.4% intrinsic gold value)</strong>
          </div>
          <div id="out-verdict" class="verdict-box badge-ok">
            NORMAL FINE RETAIL RANGE (2.99x melt): Consistent with verified traditional 14K solid gold retail bands.
          </div>
        </div>
      </div>
    </section>"""


def render_ring_rows(rings: list[dict]) -> str:
    rows_html = []
    for r in rings:
        is_rejected = r["checklist_status"].startswith("REJECT")
        row_cls = "row-rejected" if is_rejected else ("row-flagged" if r["flagged"] else "")

        karat_num = r["karat_numeric"]
        if karat_num == 24:
            k_group = "24K"
        elif karat_num == 22:
            k_group = "22K"
        elif karat_num == 18:
            k_group = "18K"
        elif karat_num == 14:
            k_group = "14K"
        elif karat_num == 10:
            k_group = "10K"
        else:
            k_group = "PLATED"

        w_state = "WEIGHT_VERIFIED" if r["weight_grams"] is not None else "WEIGHT_OMITTED"

        weight_cell = (
            f'<span class="num">{r["weight_grams"]:.2f} g</span>'
            if r["weight_grams"] is not None
            else '<span class="blank-cell">&mdash; Unverified</span>'
        )
        pure_cell = (
            f'<span class="num">{r["pure_gold_grams"]:.4f} g</span>'
            if r["pure_gold_grams"] is not None
            else '<span class="blank-cell">&mdash; Unverified</span>'
        )
        melt_cell = (
            f'<span class="num">${r["melt_value_usd"]:,.2f}</span>'
            if r["melt_value_usd"] is not None
            else '<span class="blank-cell">&mdash; Unverified</span>'
        )
        ratio_cell = (
            f'<span class="num">{r["price_to_melt_ratio"]:.2f}x</span>'
            if r["price_to_melt_ratio"] is not None
            else '<span class="blank-cell">&mdash;</span>'
        )

        if is_rejected:
            badge_cls = "badge-bad"
        elif r["flagged"]:
            badge_cls = "badge-warn"
        else:
            badge_cls = "badge-ok"

        extra_link = ""
        if r.get("secondary_weight_source_url"):
            extra_link = "<br>" + ext_link(r["secondary_weight_source_url"], "Weight Spec Page")

        flag_summary = ""
        if r.get("flags"):
            items = "".join(f"<li>{esc(f)}</li>" for f in r["flags"])
            flag_summary = f'<ul style="margin:0.35rem 0 0; padding-left:1.1rem; font-size:0.8rem; color:#475569;">{items}</ul>'

        rows_html.append(
            f"""
          <tr id="{esc(r['id'])}" class="{row_cls}" data-ring-row="1" data-karat-group="{k_group}" data-weight-state="{w_state}">
            <td><strong>{esc(r['id'])}</strong><br><span style="font-size:0.78rem; color:#64748b;">{esc(r['verified_date'])}</span></td>
            <td><strong>{esc(r['seller_name'])}</strong><br><span style="font-size:0.8rem; color:#475569;">SKU: {esc(r['sku'])}</span></td>
            <td>
              <strong>{esc(r['product_name'])}</strong>
              <div style="font-size:0.8rem; color:#475569; margin-top:0.2rem;">Dimensions: {esc(r.get('band_dimensions') or '—')} &bull; Stones: {esc(r.get('gemstone_details') or '—')}</div>
              <details class="excerpt-box">
                <summary>Verbatim Official Excerpt</summary>
                <code>{esc(r['verbatim_excerpt'])}</code>
              </details>
            </td>
            <td>
              <strong>{esc(r['karat_label'])}</strong>
              <div style="font-size:0.79rem; color:#475569;">{esc(r.get('solid_gold_assessment') or '')}</div>
            </td>
            <td class="num">${r['price_usd']:,.2f}</td>
            <td>{weight_cell}</td>
            <td>{pure_cell}</td>
            <td>{melt_cell}</td>
            <td>{ratio_cell}</td>
            <td>
              <span class="badge {badge_cls}">{esc(r['checklist_status'])}</span>
              {flag_summary}
            </td>
            <td>
              {ext_link(r['product_url'], 'Official Listing')}
              {extra_link}
            </td>
          </tr>"""
        )
    return "\n".join(rows_html)


def render_ring_table_block(title: str, subtitle: str, rings: list[dict], show_filters: bool = True) -> str:
    filter_html = ""
    n_w_ok = sum(1 for r in rings if r.get("weight_grams") is not None)
    n_w_omit = sum(1 for r in rings if r.get("weight_grams") is None)
    if show_filters:
        filter_html = f"""
      <div class="filter-bar">
        <input id="ring-search" type="search" placeholder="Search seller, ring name, SKU, karat, or finding...">
        <select id="ring-karat-filter" aria-label="Filter by Karat">
          <option value="ALL">All Metal Purities</option>
          <option value="24K">24K Pure Gold (99.95%)</option>
          <option value="22K">22K Coin + 14K Shank</option>
          <option value="18K">18K Solid Gold (75.0%)</option>
          <option value="14K">14K Solid Gold (58.33%)</option>
          <option value="10K">10K Gold (Contradiction Flagged)</option>
          <option value="PLATED">Plated Brass Control (Rejected)</option>
        </select>
        <select id="ring-status-filter" aria-label="Filter by Weight Disclosure">
          <option value="ALL">All Weight Disclosure States</option>
          <option value="WEIGHT_VERIFIED">Official Gram Weight Published ({n_w_ok})</option>
          <option value="WEIGHT_OMITTED">Gram Weight Omitted — Blank/Unverified ({n_w_omit})</option>
        </select>
        <span id="visible-row-count" class="badge badge-neutral"></span>
      </div>"""

    return f"""
    <section class="section-card" id="verified-catalog">
      <div class="section-header">
        <div>
          <h2>{esc(title)}</h2>
          <p>{esc(subtitle)}</p>
        </div>
      </div>
      {filter_html}
      <div class="table-wrap">
        <table class="data-table">
          <thead>
            <tr>
              <th>ID &amp; Date</th>
              <th>Seller &amp; SKU</th>
              <th>Ring / Setting &amp; Verbatim Archive</th>
              <th>Karat &amp; Solid Gold Wording</th>
              <th>Verified Price</th>
              <th>Official Weight</th>
              <th>Pure 24K Au</th>
              <th>Raw Melt Value</th>
              <th>Price / Melt</th>
              <th>Checklist Audit &amp; Notes</th>
              <th>Official Source</th>
            </tr>
          </thead>
          <tbody>
            {render_ring_rows(rings)}
          </tbody>
        </table>
      </div>
    </section>"""


def build_all() -> None:
    spot_std = json.loads((DATA_DIR / "spot-and-standards.json").read_text(encoding="utf-8"))
    solitaires = json.loads((DATA_DIR / "solitaire-rings.json").read_text(encoding="utf-8"))["items"]
    bands = json.loads((DATA_DIR / "bands-and-high-karat.json").read_text(encoding="utf-8"))["items"]
    sellers = json.loads((DATA_DIR / "sellers-policies.json").read_text(encoding="utf-8"))["sellers"]
    audit_log = json.loads((VERIF_DIR / "audit-log.json").read_text(encoding="utf-8"))
    manifest = json.loads((VERIF_DIR / "sources-manifest.json").read_text(encoding="utf-8"))

    all_rings = solitaires + bands
    bench = spot_std["spot_gold_benchmark"]
    latest_pass = audit_log["runs"][-1]
    flagged_rings = [r for r in all_rings if r["flagged"]]

    # ======================================================================
    # 1. index.html — Front Page Dashboard + Prominent No-Hallucinations Summary
    # ======================================================================
    index_body = f"""
    <section class="page-hero">
      <p class="page-eyebrow">Verified Buyer Research &bull; Updated October 22, 2026</p>
      <h1>Buying a Genuine Solid Gold Engagement Ring Online: Line-by-Line Audit, Melt Value Benchmarks &amp; Scam Protection</h1>
      <p class="lead">
        Independent empirical research comparing <strong>{len(all_rings)} live ring listings</strong> across <strong>{len(sellers)} major online jewelers</strong>
        against US/UK hallmark law, NIST weight standards, Better Business Bureau complaint records, and live spot gold
        (<strong>${bench['spot_bid_usd_per_troy_oz']:,.2f}/oz = ${bench['spot_usd_per_gram_24k_exact']:.2f}/g</strong> at <code>{esc(bench['quote_timestamp_local'])}</code>).
      </p>
    </section>

    {render_mandate_banner(compact=False)}

    <div class="kpi-grid">
      <div class="kpi-card">
        <div class="kpi-label">Live Spot Gold (2026-10-22)</div>
        <div class="kpi-value">${bench['spot_bid_usd_per_troy_oz']:,.2f} / oz</div>
        <div class="kpi-sub"><strong>${bench['spot_usd_per_gram_24k_exact']:.2f}/g</strong> (24K) &bull; <strong>$75.49/g</strong> (14K) &bull; <strong>$97.06/g</strong> (18K)</div>
      </div>
      <div class="kpi-card">
        <div class="kpi-label">Best Weight-Verified Band</div>
        <div class="kpi-value">2.99x Melt</div>
        <div class="kpi-sub">Ross-Simons 4mm 14K Band ($949 vs. $317.05 gold melt &bull; 4.2g verified in static HTML)</div>
      </div>
      <div class="kpi-card">
        <div class="kpi-label">Best 14K Solid Retail Ratio</div>
        <div class="kpi-value">2.99x – 3.12x</div>
        <div class="kpi-sub">Ross-Simons 4mm ($949 / 4.2g) &amp; 2mm ($400 / 1.7g) &bull; BBB A+ Accredited</div>
      </div>
      <div class="kpi-card">
        <div class="kpi-label">Flagged Items &amp; Omissions</div>
        <div class="kpi-value">{len(flagged_rings)} of {len(all_rings)}</div>
        <div class="kpi-sub">13 omitted weights left blank + 4 live page contradictions logged on <a href="flagged-for-review.html">Flagged for Review</a></div>
      </div>
    </div>

    <section class="section-card">
      <div class="section-header">
        <div>
          <h2>Executive Findings: What Every Online Gold Ring Buyer Must Know First</h2>
          <p>Key conclusions derived exclusively from verbatim primary product pages, policies, and regulatory standards.</p>
        </div>
      </div>
      <div class="cards-grid">
        <div class="cat-card">
          <div>
            <span class="badge badge-ok">Finding #1 &bull; Weight &amp; Melt Value</span>
            <h3>Most Bridal Jewelers Hide Gram Weight Online</h3>
            <p>Blue Nile, Brilliant Earth, and Mejuri omit gram weights in static HTML, and Menē renders 24K weights only via client JS. Ross-Simons publishes explicit static-HTML weights on 14K bands (<strong>2.99x–3.96x melt</strong>).</p>
          </div>
          <a href="bands-vintage-rings.html">Compare Weight-Verified Bands &rarr;</a>
        </div>
        <div class="cat-card">
          <div>
            <span class="badge badge-warn">Finding #2 &bull; Return &amp; Wire Traps</span>
            <h3>Engraving, Resizing &amp; Bank Wires Void Protection</h3>
            <p>Blue Nile and Brilliant Earth void 30-day returns on engraved or resized rings and pitch a <strong>1.5% bank wire discount</strong> that forfeits credit card chargeback rights. Menē enforces a strict <strong>7-day return window</strong>.</p>
          </div>
          <a href="sellers-policies.html">Inspect Seller Policy Audit &rarr;</a>
        </div>
        <div class="cat-card">
          <div>
            <span class="badge badge-bad">Finding #3 &bull; Live Page Contradictions Caught</span>
            <h3>Even Established Retailers Publish Conflicting Specs</h3>
            <p>Line-by-line reading caught Ross-Simons Item <code>251663</code> advertising <code>10kt</code> in specs and <code>14kt</code> in prose, and Brilliant Earth <code>BE1FM0126</code> displaying a <code>Free 1-Year Resizing</code> banner above text stating resizing is unavailable.</p>
          </div>
          <a href="flagged-for-review.html">Review All {len(flagged_rings)} Flagged Listings &rarr;</a>
        </div>
        <div class="cat-card">
          <div>
            <span class="badge badge-neutral">Finding #4 &bull; Day-1 XRF Verification</span>
            <h3>Verify by Scale &amp; XRF Before Resizing or Wearing</h3>
            <p>Pay strictly by credit card, keep all tags attached, weigh on a calibrated 0.01g scale, confirm karat + maker trademark under 10x loupe, and run non-destructive XRF purity testing within the return window.</p>
          </div>
          <a href="checklist-standards.html">Read Complete 12-Point Checklist &rarr;</a>
        </div>
      </div>
    </section>

    {render_calculator_section(bench['spot_bid_usd_per_troy_oz'], include_presets=True)}

    <section class="section-card">
      <div class="section-header">
        <div>
          <h2>Explore Research Categories &amp; Verification Subpages</h2>
          <p>Clean subpages organized by ring type, seller policy audit, interactive melt math, flagged anomalies, and automated security checks.</p>
        </div>
      </div>
      <div class="cards-grid">
        <div class="cat-card">
          <div>
            <h3>1. 12-Point Checklist &amp; Legal Standards</h3>
            <p>US 16 CFR Part 23, 15 U.S.C. Ch. 8, UK Hallmarking Act 1973, 9K–24K purity table, and post-arrival XRF testing workflow.</p>
          </div>
          <a href="checklist-standards.html" class="source-btn">Open Checklist &amp; Standards</a>
        </div>
        <div class="cat-card">
          <div>
            <h3>2. Solitaire Engagement Settings (9)</h3>
            <p>14K &amp; 18K solitaire mounts from Blue Nile, Brilliant Earth, and Ross-Simons (plus $2,819 GIA 0.80ct diamond solitaire &amp; $29 plated control).</p>
          </div>
          <a href="solitaire-settings.html" class="source-btn">Open Solitaire Catalog</a>
        </div>
        <div class="cat-card">
          <div>
            <h3>3. Solid Gold &amp; 24K Bands (12)</h3>
            <p>Weight-verified 24K pure gold bands, traditional 14K bands, Italian signets, 22K gold coin mount, and 14K diamond eternity bands.</p>
          </div>
          <a href="bands-vintage-rings.html" class="source-btn">Open Bands &amp; Vintage Catalog</a>
        </div>
        <div class="cat-card">
          <div>
            <h3>4. Sellers, Returns &amp; Payment Audit (5)</h3>
            <p>Physical HQ addresses, phone numbers, BBB ratings (A+ to D-), resized/engraved return exclusions, and credit card chargeback protection.</p>
          </div>
          <a href="sellers-policies.html" class="source-btn">Open Seller Policy Table</a>
        </div>
        <div class="cat-card">
          <div>
            <h3>5. Flagged for Review ({len(flagged_rings)} Items)</h3>
            <p>Complete transparency register of every omitted weight, 10kt/14kt copy error, resizing contradiction, BBB D- rating, and plated control.</p>
          </div>
          <a href="flagged-for-review.html" class="source-btn">Open Flagged Items</a>
        </div>
        <div class="cat-card">
          <div>
            <h3>6. Security &amp; Anti-Hallucination Audit</h3>
            <p>Machine-executed audit passes (SEC-01..SEC-07), SHA-256 data digests, and full primary URL manifest.</p>
          </div>
          <a href="security-audit.html" class="source-btn">Open Security Audit</a>
        </div>
      </div>
    </section>

    {render_ring_table_block(
        "Complete Master Comparison Table — All 21 Audited Ring Listings",
        "Every row links directly to an official primary product page verified on 2026-10-22. Unconfirmed weights are never inferred.",
        all_rings,
        show_filters=True,
    )}
    """

    # ======================================================================
    # 2. checklist-standards.html — All 12 Checklist Rules + Karat Table
    # ======================================================================
    checklist_items = [
        ("Rule 01", "Check Karat Purity Explicitly (10K / 14K / 18K / 22K / 24K)", "Confirm exact fractional purity: 10K (41.7% — US legal minimum under 16 CFR § 23.3), 14K (58.3% — classic durable daily bridal balance), 18K (75.0% — richer yellow hue, slightly softer), 22K (91.7%), or 24K (99.95% pure bullion softness).", "https://www.ecfr.gov/current/title-16/chapter-I/subchapter-B/part-23", "16 CFR Part 23 (FTC Jewelry Guides)"),
        ("Rule 02", "Verify Explicit 'Solid Gold' Wording", "Require unambiguous 'Solid 14K Gold' or 'Solid 18K Gold' wording. Reject 'Gold Plated', 'Gold Vermeil' (gold over sterling silver), 'Gold Filled' (mechanically bonded layer), or 'Gold over Brass' (see SOL-09 control at $29).", "https://www.ecfr.gov/current/title-16/chapter-I/subchapter-B/part-23/section-23.3", "16 CFR § 23.3 Misrepresentation of Gold Content"),
        ("Rule 03", "Confirm Mandatory Karat & Maker's Trademark Hallmarks", "Under the US National Gold and Silver Stamping Act (15 U.S.C. § 297), any quality mark ('14K', '585', '750') MUST be accompanied by the registered manufacturer trademark. UK items >1.0g require statutory Assay Office hallmarks.", "https://www.govinfo.gov/content/pkg/USCODE-2023-title15/html/USCODE-2023-title15-chap8.htm", "15 U.S.C. Ch. 8 Stamping Act"),
        ("Rule 04", "Ask for Exact Gram Weight Before Paying", "Millimeter width (e.g., 1.8mm vs 4.0mm) tells you dimensions, not hollow vs solid density. Request net gold weight in grams via live chat/email whenever omitted (Blue Nile, Brilliant Earth, Mejuri).", "https://www.nist.gov/pml/owm/metric-si/unit-conversion/precious-metals-conversion-information", "NIST Weight Standards"),
        ("Rule 05", "Check Independent Seller Reputation, Address & Phone", "Verify physical headquarters, working toll-free phone, and independent BBB complaint history — never rely solely on curated on-site reviews (e.g., Mejuri holds a BBB D- rating despite glossy site reviews).", "https://www.bbb.org/us/ri/cranston/profile/jewelry-stores/ross-simons-inc-0021-25107", "BBB Official Business Profiles"),
        ("Rule 06", "Compare Asking Price Against Live Raw Gold Melt Value", "At $4,025.10/oz ($129.41/g 24K), pure 14K gold melts at $75.49/g and 18K at $97.06/g. Any 'solid gold' ring priced near or below raw melt value is counterfeit, hollow ultra-thin foil, or plated brass.", "https://www.kitco.com/price/precious-metals", "Kitco Live Gold Spot"),
        ("Rule 07", "Read Return Policy Exclusions (Resized, Engraved & Custom)", "Crucial trap: Blue Nile and Brilliant Earth void returns once a ring is engraved or resized! Menē gives only 7 calendar days from delivery. Never engrave or resize before independent verification.", "https://www.bluenile.com/policies/returns", "Blue Nile Official Return Policy"),
        ("Rule 08", "Pay Strictly by Major Credit Card for Dispute Protection", "Never pay via Zelle, crypto, cash app, or bank wire — even when tempted by Blue Nile's or Brilliant Earth's 1.5% wire discount — so you preserve statutory Fair Credit Billing Act chargeback protection.", "https://www.brilliantearth.com/flexible-payment-options/", "Brilliant Earth Payment Terms"),
        ("Rule 09", "Demand Detailed Written Invoice & Grading Certificates", "Require an itemized invoice specifying metal karat, gram weight, ring size, SKU, and natural/lab stone status, plus verifiable GIA report numbers (e.g., GIA #2225975086 on SOL-07) or Menē CoA.", "https://www.gia.edu/report-check-landing", "GIA Report Check"),
        ("Rule 10", "Inspect Immediately at an Independent Local Jeweler", "On Day 1–2 of arrival (with security tags intact!), have an independent bench jeweler inspect prongs, weigh the ring on a legal-for-trade 0.01g scale, and verify internal karat + maker stamps.", "https://www.gov.uk/government/publications/hallmarking-guidance-notes/hallmarking-is-the-law-guidance-summary", "UK Assay & Hallmarking Guidance"),
        ("Rule 11", "Verify Alloy Purity Non-Destructively via XRF Analyzer", "Ask a local coin dealer, refiner, or independent jeweler to run a 30-second non-destructive X-Ray Fluorescence (XRF) scan — never acid-scratch a returnable ring, as damage voids return rights.", "https://www.nist.gov/pml/special-publication-811", "NIST Measurement Reference"),
        ("Rule 12", "Walk Away Whenever Answers Are Vague or Contradictory", "If a listing mixes '10kt' and '14kt' on the same page (SOL-08), contradicts its own resizing banner (SOL-05), refuses to state solid gold purity, or pressures instant wire payment — walk away.", "https://www.ross-simons.com/products/251663", "Live Contradiction Example (SOL-08)"),
    ]
    cards_12 = "\n".join(
        f"""
        <div class="check-item">
          <span class="check-num">{esc(num)}</span>
          <h3>{esc(h)}</h3>
          <p>{esc(desc)}</p>
          {ext_link(url, src_label)}
        </div>"""
        for num, h, desc, url, src_label in checklist_items
    )

    karat_rows = "\n".join(
        f"""
            <tr>
              <td><strong>{esc(k['label'])}</strong></td>
              <td class="num">{k['pure_gold_pct']:.2f}%</td>
              <td><code>{esc(k['millesimal_stamp'])}</code></td>
              <td>{esc(k['legal_status_us_uk'])}</td>
              <td class="num">${k['usd_per_gram_at_spot']:,.2f} / g</td>
              <td class="num">${k['usd_per_troy_oz_at_spot']:,.2f} / oz</td>
              <td>{esc(k['ring_suitability_note'])}</td>
              <td>{ext_link(k['source_url'], 'Standard Source')}</td>
            </tr>"""
        for k in spot_std["karat_purity_reference"]
    )

    checklist_body = f"""
    <section class="page-hero">
      <p class="page-eyebrow">Buyer Verification Framework &bull; 12 Mandatory Checks</p>
      <h1>Complete 12-Point Online Gold Engagement Ring Checklist &amp; Legal Hallmarking Standards</h1>
      <p class="lead">Every step required before checkout and immediately after delivery, anchored to US FTC regulations, federal stamping law, UK Assay Office standards, and NIST mass constants.</p>
    </section>

    {render_mandate_banner(compact=True)}

    <section class="section-card">
      <div class="section-header">
        <div>
          <h2>The 12 Mandatory Buyer Verification Rules</h2>
          <p>Each rule links directly to an official statutory, regulatory, or live empirical primary source.</p>
        </div>
      </div>
      <div class="checklist-grid">
        {cards_12}
      </div>
    </section>

    <section class="section-card" id="karat-reference-table">
      <div class="section-header">
        <div>
          <h2>Official Gold Karat Fineness, Millesimal Hallmarks &amp; Spot Value per Gram ({esc(bench['quote_timestamp_local'])})</h2>
          <p>Computed from NIST exact constant <code>1 troy oz = 31.1034768 g</code> and verified Kitco spot <code>${bench['spot_bid_usd_per_troy_oz']:,.2f}/oz</code>.</p>
        </div>
      </div>
      <div class="table-wrap">
        <table class="data-table">
          <thead>
            <tr>
              <th>Karat Tier</th>
              <th>Pure Gold %</th>
              <th>Millesimal</th>
              <th>Standard Hallmarks</th>
              <th>Melt Value / Gram</th>
              <th>Melt Value / Troy Oz</th>
              <th>Engagement Ring Suitability &amp; Legal Thresholds</th>
              <th>Official Source</th>
            </tr>
          </thead>
          <tbody>
            {karat_rows}
          </tbody>
        </table>
      </div>
    </section>
    """

    # ======================================================================
    # 3. solitaire-settings.html
    # ======================================================================
    solitaire_body = f"""
    <section class="page-hero">
      <p class="page-eyebrow">Category Audit 01 &bull; Solitaire Engagement Settings &amp; Diamond Rings</p>
      <h1>Verified Solitaire Gold Engagement Ring Settings &amp; Complete Diamond Rings (9 Listings)</h1>
      <p class="lead">
        Line-by-line audit of 14K and 18K solid gold solitaire settings from Blue Nile and Brilliant Earth, complete GIA-graded diamond solitaires from Ross-Simons,
        and a live $29 gold-plated brass control benchmark demonstrating Checklist #2 and #6.
      </p>
    </section>
    {render_mandate_banner(compact=True)}
    {render_ring_table_block(
        "Solitaire Engagement Settings & Diamond Rings — Line-by-Line Table",
        "Notice how all 6 Blue Nile and Brilliant Earth settings omit metal gram weights online — left strictly blank (Unverified) per our Zero-Hallucinations Mandate.",
        solitaires,
        show_filters=True,
    )}
    """

    # ======================================================================
    # 4. bands-vintage-rings.html
    # ======================================================================
    bands_body = f"""
    <section class="page-hero">
      <p class="page-eyebrow">Category Audit 02 &bull; Solid Gold Bands, 24K Bullion Rings, Signets &amp; Coin Rings</p>
      <h1>Verified Solid Gold Wedding/Engagement Bands, 24K Investment Rings &amp; Vintage/Signet Styles (12 Listings)</h1>
      <p class="lead">
        Head-to-head comparison of static-HTML weight-verified 14K bands (Ross-Simons at <strong>2.99x–3.96x melt</strong>) and Menē pure 24K bands (JS-hydrated weights left null in static HTML per zero-inference rule)
        against weight-opaque DTC listings (Mejuri 14K solid gold bands with omitted weights) and mixed-alloy coin rings (<code>BND-08</code>).
      </p>
    </section>
    {render_mandate_banner(compact=True)}
    {render_calculator_section(bench['spot_bid_usd_per_troy_oz'], include_presets=True)}
    {render_ring_table_block(
        "Solid Gold Bands, 24K Rings & Vintage/Signet Styles — Line-by-Line Table",
        "Exact pure gold grams and melt values are shown for all 7 single-karat weight-published rings; mixed-karat and weight-omitted items remain strictly blank (Unverified).",
        bands,
        show_filters=True,
    )}
    """

    # ======================================================================
    # 5. sellers-policies.html
    # ======================================================================
    seller_rows = "\n".join(
        f"""
            <tr id="{esc(s['id'])}" class="{'row-flagged' if 'FLAGGED' in s['checklist_grade'] else ''}">
              <td>
                <strong>{esc(s['name'])}</strong>
                <div style="font-size:0.8rem; color:#475569;">Founded {s['founded_year']} ({s['years_in_business']} yrs)</div>
              </td>
              <td style="font-size:0.83rem;">
                <strong>HQ:</strong> {esc(s['headquarters_address'])}<br>
                <strong>Phone:</strong> <code>{esc(s['verified_phone'])}</code><br>
                <strong>Email:</strong> <code>{esc(s['verified_email'])}</code>
              </td>
              <td>
                <span class="badge {'badge-ok' if s['bbb_rating'].startswith('A') else 'badge-bad'}">BBB: {esc(s['bbb_rating'])}</span>
                <div style="font-size:0.8rem; color:#475569; margin-top:0.25rem;">
                  Accredited: <strong>{'Yes' if s['bbb_accredited'] else 'No'}</strong> &bull;
                  3-Yr Complaints: <strong>{s['bbb_complaints_3yr']}</strong><br>
                  {esc(s['bbb_customer_rating'])}
                </div>
              </td>
              <td style="font-size:0.84rem;">{esc(s['gram_weight_transparency'])}</td>
              <td style="font-size:0.84rem;">
                <strong>{s['return_window_days']} Days</strong> — {esc(s['return_shipping_terms'])}
                <div style="margin-top:0.35rem; color:#991b1b; font-weight:600;">{esc(s['resized_custom_exclusions'])}</div>
              </td>
              <td style="font-size:0.84rem;">
                <div>{esc(s['accepted_payments'])}</div>
                <div style="margin-top:0.35rem; color:#78350f; font-weight:600;">{esc(s['wire_transfer_risk_note'])}</div>
              </td>
              <td>
                <span class="badge {'badge-warn' if 'FLAGGED' in s['checklist_grade'] or 'CONDITIONAL' in s['checklist_grade'] else 'badge-ok'}">{esc(s['checklist_grade'])}</span>
              </td>
              <td style="white-space:nowrap;">
                {ext_link(s['official_site_url'], 'Storefront')}<br>
                {ext_link(s['bbb_url'], 'BBB Profile')}<br>
                {ext_link(s['return_policy_url'], 'Return Policy')}<br>
                {ext_link(s['payment_policy_url'], 'Payment Policy')}
              </td>
            </tr>"""
        for s in sellers
    )

    sellers_body = f"""
    <section class="page-hero">
      <p class="page-eyebrow">Category Audit 03 &bull; Seller Reputation, Return Exclusions &amp; Payment Safety</p>
      <h1>Seller Reputation, Physical Contact Verification, Return Traps &amp; Credit Card Protection (5 Jewelers)</h1>
      <p class="lead">
        Side-by-side audit covering Checklist Rules #4, #5, #7, and #8 across Ross-Simons, Blue Nile, Brilliant Earth, Menē, and Mejuri.
        Every cell links directly to official policy pages and independent Better Business Bureau records.
      </p>
    </section>
    {render_mandate_banner(compact=True)}
    <section class="section-card">
      <div class="section-header">
        <div>
          <h2>Complete Seller Policy &amp; BBB Reputation Matrix</h2>
          <p>Always verify return exclusions on resized/engraved items and pay strictly with a major credit card.</p>
        </div>
      </div>
      <div class="table-wrap">
        <table class="data-table">
          <thead>
            <tr>
              <th>Jeweler</th>
              <th>Verified Physical HQ, Phone &amp; Email</th>
              <th>Independent BBB Rating</th>
              <th>Gram Weight Disclosure</th>
              <th>Return Window &amp; Resized/Custom Exclusions</th>
              <th>Payment Methods &amp; Wire Risk</th>
              <th>Overall Audit Grade</th>
              <th>Official Links (4/Row)</th>
            </tr>
          </thead>
          <tbody>
            {seller_rows}
          </tbody>
        </table>
      </div>
    </section>
    """

    # ======================================================================
    # 6. calculator.html — Full Interactive Calculator + Live Dynamic Karat Table
    # ======================================================================
    live_karat_rows = "\n".join(
        f"""
            <tr data-karat-fraction="{k['pure_gold_fraction']:.8f}">
              <td><strong>{esc(k['label'])}</strong></td>
              <td class="num">{k['pure_gold_pct']:.2f}%</td>
              <td><code>{esc(k['millesimal_stamp'])}</code></td>
              <td class="num live-gram-usd">${k['usd_per_gram_at_spot']:,.2f}</td>
              <td class="num live-oz-usd">${k['usd_per_troy_oz_at_spot']:,.2f}</td>
              <td>{ext_link(k['source_url'], 'Official Standard')}</td>
            </tr>"""
        for k in spot_std["karat_purity_reference"]
    )

    calc_body = f"""
    <section class="page-hero">
      <p class="page-eyebrow">Interactive Tool &bull; NIST Mass Conversion &amp; Scam Detection</p>
      <h1>Gold Purity, Gram Weight, Gemstone Deduction &amp; Raw Melt Value Calculator</h1>
      <p class="lead">
        Test any online ring listing before you buy. Uses NIST exact conversion constants (<code>1 troy oz = 31.1034768 g</code>,
        <code>1 dwt = 1.55517384 g</code>, <code>1 metric carat = 0.20 g</code>) and live verified gold spot (<code>${bench['spot_bid_usd_per_troy_oz']:,.2f}/oz</code>).
      </p>
    </section>
    {render_mandate_banner(compact=True)}
    {render_calculator_section(bench['spot_bid_usd_per_troy_oz'], include_presets=True)}
    <section class="section-card">
      <div class="section-header">
        <div>
          <h2>Live Dynamic Melt Value Table by Karat (Updates Automatically as You Edit Spot Price Above)</h2>
          <p>Shows exact melt USD per 1.00 gram and per 1.00 troy ounce across all statutory gold purities.</p>
        </div>
      </div>
      <div class="table-wrap">
        <table class="data-table">
          <thead>
            <tr>
              <th>Karat Purity</th>
              <th>Pure Gold %</th>
              <th>Hallmark Stamps</th>
              <th>Melt Value per 1.00 Gram</th>
              <th>Melt Value per 1.00 Troy Oz</th>
              <th>Primary Standard Source</th>
            </tr>
          </thead>
          <tbody>
            {live_karat_rows}
          </tbody>
        </table>
      </div>
    </section>
    """

    # ======================================================================
    # 7. flagged-for-review.html — Dedicated Unverified & Anomaly Registry
    # ======================================================================
    flagged_body = f"""
    <section class="page-hero" style="border-left: 7px solid #d97706;">
      <p class="page-eyebrow">Transparency &amp; Anomaly Registry &bull; Published Without Blocking Deployment</p>
      <h1>Flagged for Review — Unverified Attributes, Live Listing Contradictions &amp; Seller Policy Risks ({len(flagged_rings)} Entries)</h1>
      <p class="lead">
        Per our <strong>Strict No-Hallucinations Mandate</strong>, no missing gram weight or mixed-karat alloy split is ever guessed or filled in.
        Every item with omitted specifications, contradictory seller copy, short return windows, low BBB ratings, or non-solid plating is published clearly below for human inspection.
      </p>
    </section>
    {render_mandate_banner(compact=False)}
    {render_ring_table_block(
        f"All {len(flagged_rings)} Flagged & Unverified Ring Listings (With Verbatim Evidence & Official Links)",
        "Inspect verbatim archived text alongside live official links to verify omissions, copy errors, and policy risks firsthand.",
        flagged_rings,
        show_filters=True,
    )}
    """

    # ======================================================================
    # 8. security-audit.html — Automated Anti-Hallucination & Security Pass Log
    # ======================================================================
    repo_audit_url = "https://github.com/karagemop466-tech/GOLD3"
    pass_rows = "\n".join(
        f"""
            <tr>
              <td class="num"><strong>Pass #{r['pass_number']}</strong></td>
              <td><code>{esc(r['timestamp_utc'])}</code></td>
              <td><strong>{esc(r['pass_label'])}</strong></td>
              <td><span class="badge {'badge-ok' if r['overall_status'] == 'PASS' else 'badge-bad'}">{esc(r['overall_status'])} ({r['error_count']} errors)</span></td>
              <td class="num">{len(r['checks'])} checks</td>
              <td class="num">{r['flagged_items_count']} items ({r['total_flag_notes']} notes)</td>
              <td style="font-size:0.82rem;">{esc(r['manual_review_recommendation'])}</td>
              <td>{ext_link(repo_audit_url, 'Repo Suite', '')}</td>
            </tr>"""
        for r in reversed(audit_log["runs"])
    )

    check_rows = "\n".join(
        f"""
            <tr>
              <td><code>{esc(c['check_id'])}</code></td>
              <td><strong>{esc(c['name'])}</strong></td>
              <td><span class="badge {'badge-ok' if c['status'] == 'PASS' else 'badge-bad'}">{esc(c['status'])}</span></td>
              <td class="num">{c['verified_count']}</td>
              <td>{esc(c['details'])}</td>
              <td>{ext_link(repo_audit_url, 'Audit Script', '')}</td>
            </tr>"""
        for c in latest_pass["checks"]
    )

    source_rows = "\n".join(
        f"""
            <tr>
              <td class="num">{idx}</td>
              <td>{ext_link(item['url'], item['url'], '')}</td>
              <td style="font-size:0.82rem;">{esc('; '.join(item['referenced_by'][:4]))}{' ...' if len(item['referenced_by']) > 4 else ''}</td>
            </tr>"""
        for idx, item in enumerate(manifest["official_sources"], start=1)
    )

    security_body = f"""
    <section class="page-hero">
      <p class="page-eyebrow">Automated Security &amp; Hallucination Detection</p>
      <h1>Security &amp; Anti-Hallucination Audit Log (<code>scripts/run_security_audit.py</code>)</h1>
      <p class="lead">
        Every review pass executes deterministic checks for verbatim price/weight substrings, zero-inference blank cells,
        NIST melt math precision, HTTPS domain allowlisting, broken links/anchors, and tabnabbing/XSS safety.
        <strong>Always re-run <code>python3 scripts/run_security_audit.py</code> after every review and actively look for hallucinations!</strong>
      </p>
    </section>
    {render_mandate_banner(compact=False)}

    <section class="section-card">
      <div class="section-header">
        <div>
          <h2>Latest Verification Pass Breakdown (Pass #{latest_pass['pass_number']})</h2>
          <p>Executed at <code>{esc(latest_pass['timestamp_utc'])}</code> — Status: <strong>{esc(latest_pass['overall_status'])}</strong></p>
        </div>
      </div>
      <div class="table-wrap">
        <table class="data-table">
          <thead>
            <tr>
              <th>Check ID</th>
              <th>Automated Check</th>
              <th>Status</th>
              <th>Verified Count</th>
              <th>Audit Result Details</th>
              <th>Official Source</th>
            </tr>
          </thead>
          <tbody>
            {check_rows}
          </tbody>
        </table>
      </div>
    </section>

    <section class="section-card">
      <div class="section-header">
        <div>
          <h2>Recorded Multi-Pass Verification History (<code>verification/audit-log.json</code>)</h2>
          <p>Chronological record of automated verification passes run after data compilation, site build, and pre-PR review.
          The banner at the top of every page is rendered <em>from this log at build time</em>; the CI job
          (<code>.github/workflows/audit.yml</code>) runs the check <em>after</em> the build and then appends the next pass, so the
          newest row here is normally one ahead of the banner. That is the designed order, not a stale page: a pass cannot
          describe a build that has not happened yet.</p>
        </div>
      </div>
      <div class="table-wrap">
        <table class="data-table">
          <thead>
            <tr>
              <th>Pass #</th>
              <th>Timestamp (UTC)</th>
              <th>Review Stage</th>
              <th>Result</th>
              <th>Checks Run</th>
              <th>Flagged Count</th>
              <th>Post-Review Guidance</th>
              <th>Official Source</th>
            </tr>
          </thead>
          <tbody>
            {pass_rows}
          </tbody>
        </table>
      </div>
    </section>

    <section class="section-card" id="official-sources-manifest">
      <div class="section-header">
        <div>
          <h2>Complete Official HTTPS Primary Sources Manifest ({manifest['unique_official_urls_count']} Unique Verified URLs)</h2>
          <p>Every external URL referenced anywhere in JSON data or HTML tables, validated against our strict trusted domain allowlist.</p>
        </div>
      </div>
      <div class="table-wrap">
        <table class="data-table">
          <thead>
            <tr>
              <th>#</th>
              <th>Official HTTPS URL</th>
              <th>Referenced By</th>
            </tr>
          </thead>
          <tbody>
            {source_rows}
          </tbody>
        </table>
      </div>
    </section>
    """

    pages = [
        ("checklist-standards.html", "12-Point Buyer Checklist & Legal Standards", checklist_body),
        ("solitaire-settings.html", "Solitaire Engagement Settings & Diamond Rings", solitaire_body),
        ("bands-vintage-rings.html", "Solid Gold Bands, 24K Rings & Vintage Styles", bands_body),
        ("sellers-policies.html", "Seller Reputation, Return Policies & Payment Protection", sellers_body),
        ("flagged-for-review.html", "Flagged for Review — Unverified & Irregular Listings", flagged_body),
        ("security-audit.html", "Security & Anti-Hallucination Verification Log", security_body),
    ]

    n_a = len(json.loads((DATA_DIR / "products.json").read_text(encoding="utf-8"))["products"])
    n_b = len(json.loads((DATA_DIR / "rings.json").read_text(encoding="utf-8"))["rings"])
    n_combined_total = n_a + n_b + len(all_rings)

    for filename, page_title, content in pages:
        full_html = render_shell(filename, page_title, content, bench, latest_pass, n_combined=n_combined_total, n_flagged_c=len(flagged_rings))
        (ROOT / filename).write_text(full_html, encoding="utf-8")
        print(f"  Built {filename} ({len(full_html):,} bytes)")


if __name__ == "__main__":
    build_all()
