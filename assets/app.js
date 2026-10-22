/* GOLD3 dashboard logic.
   Rule: this file contains NO factual values of its own.
   Every price, weight, karat and quote is read from data/*.json at runtime,
   so the site cannot drift from the audited dataset. */

const GOLD = (() => {
  const state = { gold: null, rings: [], sellers: [], flags: [], standards: null };
  let flagIndex = {};

  const fmtMoney = (n, dec = 0) =>
    n === null || n === undefined
      ? "—"
      : "$" + n.toLocaleString("en-US", { minimumFractionDigits: dec, maximumFractionDigits: dec });

  const fmtNum = (n, dec = 2) =>
    n === null || n === undefined
      ? "—"
      : n.toLocaleString("en-US", { minimumFractionDigits: dec, maximumFractionDigits: dec });

  const esc = (s) =>
    String(s === null || s === undefined ? "" : s).replace(/[&<>"']/g, (c) =>
      ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c])
    );

  const unverified = () => '<span class="badge b-neutral" title="Not stated on the seller\'s official page. Left blank rather than guessed.">unverified</span>';

  function verdictBadge(v) {
    const t = (v || "").toUpperCase();
    if (t.startsWith("PASS")) return `<span class="badge b-ok">${esc(v)}</span>`;
    if (t.startsWith("FAIL")) return `<span class="badge b-bad">${esc(v)}</span>`;
    if (t.startsWith("UNVERIFIED")) return `<span class="badge b-warn">${esc(v)}</span>`;
    return `<span class="badge b-neutral">${esc(v || "—")}</span>`;
  }

  function weightBadge(r) {
    if (r.weight_g === null || r.weight_g === undefined) {
      return `${unverified()}`;
    }
    return `<span class="badge b-gold">${fmtNum(r.weight_g, 1)} g</span>`;
  }

  function flagChips(ids) {
    if (!ids || !ids.length) return '<span class="na">none</span>';
    return ids
      .map((id) => {
        const f = flagIndex[id];
        const sev = f ? f.severity : "low";
        const label = f ? f.label : "undefined flag";
        return `<span class="flagchip ${sev}" title="${esc(label)}">${esc(id)}</span>`;
      })
      .join("");
  }

  /* ---- economics, computed live from the audited spot price ---- */
  function spotPerGram() {
    if (!state.gold) return null;
    return state.gold.price_usd_per_troy_ounce / state.gold.troy_ounce_in_grams;
  }

  function goldValue(weightG, karatStr) {
    const m = /(\d+)\s*K/i.exec(karatStr || "");
    if (!m || weightG === null || weightG === undefined) return null;
    const karat = Number(m[1]);
    const pure = weightG * (karat / 24);
    return { pure, value: pure * spotPerGram(), karat };
  }

  /* ---- data loading ---- */
  async function loadAll() {
    const get = async (p) => {
      const res = await fetch(p, { cache: "no-cache" });
      if (!res.ok) throw new Error(`${p} → HTTP ${res.status}`);
      return res.json();
    };
    const [gold, rings, sellers, flags, standards] = await Promise.all([
      get("data/gold-price.json"),
      get("data/rings.json"),
      get("data/sellers.json"),
      get("data/flags.json"),
      get("data/standards.json"),
    ]);
    state.gold = gold;
    state.rings = rings.rings;
    state.sellers = sellers.sellers;
    state.flags = flags.flags;
    state.standards = standards;
    flagIndex = Object.fromEntries(state.flags.map((f) => [f.id, f]));
    return state;
  }

  function showError(el, err) {
    if (!el) return;
    el.innerHTML = `<div class="loaderr"><strong>Could not load the verified dataset.</strong><br>
      ${esc(err.message)}<br>
      This page reads <code>data/*.json</code> over HTTP. Serve the site from a web server
      (GitHub Pages, or <code>python3 -m http.server</code>) rather than opening the file directly.</div>`;
  }

  /* ---- navigation highlight ---- */
  function markNav() {
    const here = location.pathname.split("/").pop() || "index.html";
    document.querySelectorAll("nav.main a").forEach((a) => {
      const href = a.getAttribute("href");
      if (href === here) a.setAttribute("aria-current", "page");
    });
  }

  /* ---- index ---- */
  function renderHome() {
    const withWeight = state.rings.filter((r) => r.weight_g !== null).length;
    const notSolid = state.rings.filter((r) => (r.solid_gold_verdict || "").toUpperCase().startsWith("FAIL")).length;
    const passSolid = state.rings.filter((r) => (r.solid_gold_verdict || "").toUpperCase().startsWith("PASS")).length;
    const priced = state.rings.filter((r) => r.price_usd !== null).length;
    const el = document.getElementById("stats");
    if (!el) return;

    el.innerHTML = `
      <div class="card stat g"><span class="n">${state.rings.length}</span>
        <span class="k">listings verified</span>
        <span class="sub">${priced} with a price printed on an official page</span></div>
      <div class="card stat b"><span class="n">${state.sellers.length}</span>
        <span class="k">sellers checked</span>
        <span class="sub">return policy + contact read from the seller</span></div>
      <div class="card stat a"><span class="n">${withWeight}/${state.rings.length}</span>
        <span class="k">publish a gram weight</span>
        <span class="sub">the rest are blank and flagged</span></div>
      <div class="card stat r"><span class="n">${state.flags.length}</span>
        <span class="k">flags for review</span>
        <span class="sub">${notSolid} non-solid · ${passSolid} confirmed solid</span></div>`;

    const spotEl = document.getElementById("spot");
    if (spotEl && state.gold) {
      spotEl.innerHTML = `
        <div class="kv"><span class="k">Spot price (USD / troy oz)</span>
          <span class="v">${fmtMoney(state.gold.price_usd_per_troy_ounce, 2)}</span></div>
        <div class="kv"><span class="k">Spot price (USD / gram)</span>
          <span class="v">${fmtMoney(spotPerGram(), 2)}</span></div>
        <div class="kv"><span class="k">Market date</span>
          <span class="v">${esc(state.gold.as_of_market_date)}</span></div>
        <div class="kv"><span class="k">Retrieved</span>
          <span class="v">${esc(state.gold.retrieved_utc)}</span></div>
        <div class="kv"><span class="k">Source</span>
          <span class="v"><a href="${esc(state.gold.source.url)}" rel="noopener">${esc(state.gold.source.publisher)}</a></span></div>`;
    }

    const tbl = document.getElementById("home-table");
    if (tbl) tbl.innerHTML = ringsTable(state.rings, { compact: true });
  }

  /* ---- rings table ---- */
  function ringsTable(rows, opts = {}) {
    if (!rows.length) return '<div class="empty">No rows match.</div>';
    const head = `
      <thead><tr>
        <th>ID</th><th>Seller</th><th>Ring</th><th>Karat</th><th>Price</th>
        <th>Weight</th><th>Solid gold?</th><th>Stamp / maker</th><th>Returns</th><th>Flags</th><th>Source</th>
      </tr></thead>`;

    const body = rows
      .map((r) => {
        const priceCell =
          r.price_usd === null || r.price_usd === undefined
            ? unverified()
            : `<span class="mono">${fmtMoney(r.price_usd)}</span>`;
        const basis = r.price_basis ? `<span class="sub">${esc(r.price_basis)}</span>` : "";
        const stamp = [r.hallmark_reported, r.maker_mark_reported].filter(Boolean);
        const stampCell = stamp.length
          ? stamp.map((s) => esc(s)).join("<br>")
          : unverified();
        const srcLinks = r.sources
          .slice(0, 2)
          .map((u, i) => `<a href="${esc(u)}" rel="noopener" title="${esc(u)}">source ${i + 1}</a>`)
          .join("<br>");
        return `
        <tr>
          <td class="num">${esc(r.id)}</td>
          <td>${esc(r.seller)}</td>
          <td class="name"><a href="${esc(r.url)}" rel="noopener">${esc(r.product)}</a>
            <span class="sub">${esc(r.metal_color || "")}</span></td>
          <td class="num">${esc(r.karat)}</td>
          <td class="num">${priceCell}${basis}</td>
          <td class="num">${weightBadge(r)}</td>
          <td>${verdictBadge(r.solid_gold_verdict)}</td>
          <td>${stampCell}</td>
          <td>${esc(r.return_window || "—")}</td>
          <td>${flagChips(r.flags)}</td>
          <td class="src">${srcLinks}</td>
        </tr>`;
      })
      .join("");

    return head + "<tbody>" + body + "</tbody>";
  }

  function initRingsPage() {
    const table = document.getElementById("rings-table");
    if (!table) return;
    const search = document.getElementById("f-search");
    const sellerSel = document.getElementById("f-seller");
    const solidSel = document.getElementById("f-solid");
    const weightSel = document.getElementById("f-weight");
    const count = document.getElementById("f-count");

    const sellers = [...new Set(state.rings.map((r) => r.seller))].sort();
    sellerSel.innerHTML =
      '<option value="">All sellers</option>' +
      sellers.map((s) => `<option value="${esc(s)}">${esc(s)}</option>`).join("");

    const apply = () => {
      const q = (search.value || "").trim().toLowerCase();
      const sv = sellerSel.value;
      const sol = solidSel.value;
      const wt = weightSel.value;

      let rows = state.rings.filter((r) => {
        const hay = `${r.id} ${r.seller} ${r.product} ${r.karat} ${r.metal_color}`.toLowerCase();
        if (q && !hay.includes(q)) return false;
        if (sv && r.seller !== sv) return false;
        if (sol) {
          const v = (r.solid_gold_verdict || "").toUpperCase();
          if (sol === "pass" && !v.startsWith("PASS")) return false;
          if (sol === "fail" && !v.startsWith("FAIL")) return false;
          if (sol === "unverified" && !v.startsWith("UNVERIFIED")) return false;
        }
        if (wt === "yes" && (r.weight_g === null || r.weight_g === undefined)) return false;
        if (wt === "no" && r.weight_g !== null && r.weight_g !== undefined) return false;
        return true;
      });

      table.innerHTML = ringsTable(rows);
      if (count) count.textContent = `${rows.length} of ${state.rings.length} rows`;
    };

    [search, sellerSel, solidSel, weightSel].forEach((el) => {
      el.addEventListener("input", apply);
      el.addEventListener("change", apply);
    });
    apply();
  }

  /* ---- sellers ---- */
  function initSellers() {
    const el = document.getElementById("sellers-list");
    if (!el) return;
    el.innerHTML = state.sellers
      .map((s) => {
        const rows = [
          ["Type", esc(s.type)],
          ["Phone", s.phone ? esc(s.phone) : unverified()],
          ["Email", s.email ? esc(s.email) : unverified()],
          ["Return window", esc(s.return_window)],
          ["Return exclusions", esc(s.return_exclusions)],
          ["Resize policy", s.resize_policy ? esc(s.resize_policy) : unverified()],
          ["Payment notes", s.payment_notes ? esc(s.payment_notes) : unverified()],
          ["Publishes gram weight", s.publishes_weight ? '<span class="badge b-ok">yes</span>' : '<span class="badge b-bad">no</span>'],
          ["Publishes hallmark / maker's mark", s.publishes_hallmark ? '<span class="badge b-ok">yes</span>' : '<span class="badge b-bad">no</span>'],
          ["Independent assay / XRF per item", esc(s.offers_xrf_or_assay || "—")],
          ["Price display", esc(s.price_display || "—")],
          ["Flags", flagChips(s.flags)],
        ];
        return `<div class="card" style="margin-bottom:14px">
          <h3><a href="${esc(s.website)}" rel="noopener">${esc(s.name)}</a>
            <span class="sub" style="display:inline">${esc(s.type)}</span></h3>
          ${rows.map(([k, v]) => `<div class="kv"><span class="k">${k}</span><span class="v" style="text-align:right;max-width:66%">${v}</span></div>`).join("")}
          <p class="hint" style="margin-top:10px">Policy source:
            <a href="${esc(s.policy_source)}" rel="noopener">${esc(s.policy_source)}</a></p>
          <p class="hint">${esc(s.verification)}</p>
        </div>`;
      })
      .join("");
  }

  /* ---- flagged ---- */
  function initFlagged() {
    const el = document.getElementById("flags-list");
    if (!el) return;
    const usage = {};
    state.rings.forEach((r) => (r.flags || []).forEach((f) => (usage[f] = usage[f] || []).push(r.id)));
    state.sellers.forEach((s) => (s.flags || []).forEach((f) => (usage[f] = usage[f] || []).push(s.name)));

    const order = { high: 0, medium: 1, low: 2 };
    const sorted = [...state.flags].sort((a, b) => order[a.severity] - order[b.severity]);

    el.innerHTML = sorted
      .map((f) => {
        const used = usage[f.id] || [];
        return `<div class="flagcard ${esc(f.severity)}">
          <h3><span class="id">${esc(f.id)}</span> ${esc(f.label)}
            <span class="badge ${f.severity === "high" ? "b-bad" : f.severity === "medium" ? "b-warn" : "b-neutral"}">${esc(f.severity)}</span></h3>
          <dl style="margin:0">
            <dt>What was found</dt><dd>${esc(f.what)}</dd>
            <dt>Why it matters</dt><dd>${esc(f.why_it_matters)}</dd>
            <dt>What to do</dt><dd>${esc(f.action)}</dd>
            <dt>Applies to</dt><dd>${used.length ? used.map(esc).join(", ") : "general"}</dd>
            ${f.source ? `<dt>Source</dt><dd><a href="${esc(f.source)}" rel="noopener">${esc(f.source)}</a></dd>` : ""}
          </dl>
        </div>`;
      })
      .join("");
  }

  /* ---- analysis ---- */
  function initAnalysis() {
    const melt = document.getElementById("melt-body");
    if (melt) {
      const rows = state.rings.filter((r) => r.weight_g !== null && r.price_usd !== null);
      melt.innerHTML = rows
        .map((r) => {
          const gv = goldValue(r.weight_g, r.karat);
          if (!gv) return "";
          const pct = (gv.value / r.price_usd) * 100;
          const perPure = r.price_usd / gv.pure;
          return `<tr>
            <td class="num">${esc(r.id)}</td>
            <td class="name">${esc(r.seller)}<span class="sub">${esc(r.product)}</span></td>
            <td class="num">${esc(r.karat)}</td>
            <td class="num">${fmtNum(r.weight_g, 1)}</td>
            <td class="num">${fmtNum(gv.pure, 2)}</td>
            <td class="num">${fmtMoney(gv.value, 2)}</td>
            <td class="num">${fmtMoney(r.price_usd)}</td>
            <td class="num">${fmtNum(pct, 1)}%</td>
            <td class="num">${fmtMoney(perPure, 2)}</td>
          </tr>`;
        })
        .join("");
    }

    const cov = document.getElementById("coverage");
    if (cov) {
      const n = state.rings.length;
      const w = state.rings.filter((r) => r.weight_g !== null).length;
      const h = state.rings.filter((r) => r.hallmark_reported).length;
      const m = state.rings.filter((r) => r.maker_mark_reported).length;
      const solid = state.rings.filter((r) => (r.solid_gold_verdict || "").toUpperCase().startsWith("PASS")).length;
      const pct = (a) => `${Math.round((a / n) * 100)}%`;
      cov.innerHTML = `
        <div class="kv"><span class="k">Stated a weight in grams</span><span class="v">${w} / ${n} — ${pct(w)}</span></div>
        <div class="kv"><span class="k">Described the hallmark/stamp</span><span class="v">${h} / ${n} — ${pct(h)}</span></div>
        <div class="kv"><span class="k">Described a maker's mark</span><span class="v">${m} / ${n} — ${pct(m)}</span></div>
        <div class="kv"><span class="k">Explicitly said "solid" gold</span><span class="v">${solid} / ${n} — ${pct(solid)}</span></div>
        <div class="kv"><span class="k">Published a per-item XRF/assay</span><span class="v">0 / ${n} — 0%</span></div>`;
    }
  }

  /* ---- standards ---- */
  function initStandards() {
    const kt = document.getElementById("karat-body");
    if (kt) {
      kt.innerHTML = state.standards.karat_fineness.values
        .map(
          (k) => `<tr>
            <td class="num">${esc(k.karat)}</td>
            <td class="num">${fmtNum(k.percent, 2)}%</td>
            <td class="num">${fmtNum(k.parts_per_thousand, 1)}</td>
            <td class="num">${k.fraction}</td>
          </tr>`
        )
        .join("");
    }
    const rules = document.getElementById("rules-list");
    if (rules) {
      rules.innerHTML = state.standards.legal_rules
        .map(
          (r) => `<div class="card" style="margin-bottom:12px">
            <h3>${esc(r.title)}</h3>
            <p>${esc(r.rule)}</p>
            <p class="hint">Cite: <strong>${esc(r.cite)}</strong> ·
              <a href="${esc(r.url)}" rel="noopener">official text</a></p>
            <p class="hint">Used here to: ${esc(r.use_in_project)}</p>
          </div>`
        )
        .join("");
    }
  }

  /* ---- calculator ---- */
  function initCalc() {
    const form = document.getElementById("calc");
    if (!form || !state.gold) return;
    const wEl = document.getElementById("c-weight");
    const kEl = document.getElementById("c-karat");
    const out = document.getElementById("c-out");
    const note = document.getElementById("c-note");

    kEl.innerHTML = state.standards.karat_fineness.values
      .map((k) => `<option value="${k.karat}">${k.karat} — ${fmtNum(k.percent, 2)}% gold</option>`)
      .join("");
    kEl.value = "14K";

    const compute = () => {
      const w = parseFloat(wEl.value);
      if (!w || w <= 0 || w > 200) {
        out.innerHTML = `<p class="dim">Enter the ring's weight in grams to see its gold content and melt value.</p>`;
        note.textContent = "";
        return;
      }
      const karat = parseInt(kEl.value, 10);
      const pure = w * (karat / 24);
      const val = pure * spotPerGram();
      out.innerHTML = `
        <div class="kv"><span class="k">Fine (pure) gold content</span>
          <span class="v">${fmtNum(pure, 3)} g</span></div>
        <div class="kv"><span class="k">Gold-only melt value at spot</span>
          <span class="v" style="color:var(--gold);font-size:17px">${fmtMoney(val, 2)}</span></div>
        <div class="kv"><span class="k">Spot used</span>
          <span class="v">${fmtMoney(state.gold.price_usd_per_troy_ounce, 2)}/oz · ${fmtMoney(spotPerGram(), 2)}/g</span></div>
        <div class="kv"><span class="k">Market date</span><span class="v">${esc(state.gold.as_of_market_date)}</span></div>`;
      note.innerHTML = `This is the <strong>raw gold content</strong> of ${fmtNum(w, 2)} g of ${karat}K.
        It is not a price for the ring: it ignores the diamond, the setting work, the brand and any retail margin.
        If the weight you typed is the <em>total</em> item weight, this figure is an <strong>upper bound</strong>,
        because stones weigh something but contain no gold.`;
    };

    wEl.addEventListener("input", compute);
    kEl.addEventListener("change", compute);
    compute();
  }

  /* ---- boot ---- */
  async function boot() {
    markNav();
    try {
      await loadAll();
    } catch (e) {
      ["stats", "rings-table", "sellers-list", "flags-list", "c-out"].forEach((id) =>
        showError(document.getElementById(id), e)
      );
      return;
    }
    const page = document.body.dataset.page;
    if (page === "home") renderHome();
    if (page === "rings") initRingsPage();
    if (page === "sellers") initSellers();
    if (page === "flagged") initFlagged();
    if (page === "analysis") initAnalysis();
    if (page === "standards") initStandards();
    if (page === "calculator") initCalc();
  }

  return { boot, fmtMoney, fmtNum, state };
})();

document.addEventListener("DOMContentLoaded", GOLD.boot);
