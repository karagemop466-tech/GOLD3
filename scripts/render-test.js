#!/usr/bin/env node
/* Render test: executes assets/app.js against the real data/*.json inside a tiny
   DOM shim, so we can prove every page's table actually renders and that the
   values shown are the audited ones. No browser required.

   Run: node scripts/render-test.js
*/
const fs = require("fs");
const path = require("path");
const vm = require("vm");

const ROOT = path.resolve(__dirname, "..");

function makeEl(id) {
  return {
    id,
    _html: "",
    get innerHTML() { return this._html; },
    set innerHTML(v) { this._html = String(v); },
    textContent: "",
    value: "",
    addEventListener() {},
    setAttribute() {},
    getAttribute() { return null; },
  };
}

function runPage(page, appSource) {
  const els = new Map();
  const getEl = (id) => {
    if (!els.has(id)) els.set(id, makeEl(id));
    return els.get(id);
  };

  let bootFn = null;
  const document = {
    body: { dataset: { page } },
    getElementById: getEl,
    querySelectorAll: () => [],
    // "#id tbody" is the only selector the app uses; map it onto a shim element
    querySelector: (sel) => {
      const m = /^#([\w-]+)\s+tbody$/.exec(String(sel));
      return m ? getEl(m[1] + "-body") : null;
    },
    addEventListener: (_evt, fn) => { bootFn = fn; },
  };

  const fetchImpl = async (p) => {
    const file = path.join(ROOT, p);
    if (!fs.existsSync(file)) return { ok: false, status: 404, json: async () => ({}) };
    const text = fs.readFileSync(file, "utf8");
    return { ok: true, status: 200, json: async () => JSON.parse(text) };
  };

  const sandbox = {
    document,
    fetch: fetchImpl,
    location: { pathname: page === "home" ? "/index.html" : `/${page}.html` },
    console,
    Promise,
    Number,
    Object,
    Math,
    parseInt,
    parseFloat,
    String,
    setTimeout,
  };
  sandbox.globalThis = sandbox;

  vm.createContext(sandbox);
  vm.runInContext(appSource, sandbox, { filename: "app.js" });

  return (async () => {
    if (!bootFn) throw new Error("app.js never registered a DOMContentLoaded handler");
    await bootFn();
    // boot() is async and awaits loadAll(); give its microtasks a turn
    await new Promise((r) => setTimeout(r, 50));
    return getEl;
  })();
}

const checks = [];
function check(name, cond, detail = "") {
  checks.push({ name, ok: !!cond, detail });
}

(async () => {
  const appSource = fs.readFileSync(path.join(ROOT, "assets/app.js"), "utf8");
  const rings = JSON.parse(fs.readFileSync(path.join(ROOT, "data/rings.json"), "utf8")).rings;
  const gold = JSON.parse(fs.readFileSync(path.join(ROOT, "data/gold-price.json"), "utf8"));

  // ---- home
  let el = await runPage("home", appSource);
  const stats = el("stats").innerHTML;
  check("home: stat cards render", stats.includes(String(rings.length)), stats.slice(0, 80));
  check("home: benchmark renders with source",
    el("spot").innerHTML.includes("gold.org") && el("spot").innerHTML.includes(gold.as_of_market_date));
  const homeTbl = el("home-table").innerHTML;
  check("home: table renders rows", (homeTbl.match(/<tr>/g) || []).length >= rings.length,
    `${(homeTbl.match(/<tr>/g) || []).length} <tr>`);

  // a published weight must appear as quoted
  check("home: published weights appear", homeTbl.includes("6.1 g"), "R11 weight 6.1 g");
  // an unpublished weight must be labelled, not zero-filled
  check("home: unpublished weights marked unverified",
    homeTbl.includes("unverified"), "unverified badge present");

  // ---- rings
  el = await runPage("rings", appSource);
  const ringsTbl = el("rings-table").innerHTML;
  check("rings: table renders", ringsTbl.includes("R11") && ringsTbl.includes("R01"));
  check("rings: count label set", /\d+ of \d+ rows/.test(el("f-count").textContent),
    el("f-count").textContent);
  check("rings: every row has a source link",
    rings.every((r) => ringsTbl.includes(r.sources[0])));

  // ---- sellers
  el = await runPage("sellers", appSource);
  const sellersHtml = el("sellers-list").innerHTML;
  check("sellers: cards render", sellersHtml.includes("Blue Nile") && sellersHtml.includes("Wilson"));
  check("sellers: precious-metals exclusion surfaced",
    sellersHtml.includes("Precious metals are non-refundable"));
  check("sellers: blank contact stays blank",
    sellersHtml.includes("unverified"), "Mejuri phone/email unverified");

  // ---- flagged
  el = await runPage("flagged", appSource);
  const flagsHtml = el("flags-list").innerHTML;
  check("flagged: flags render", flagsHtml.includes("RET1") && flagsHtml.includes("S1"));
  check("flagged: high severity first", flagsHtml.indexOf("high") < flagsHtml.indexOf("low"));

  // ---- analysis
  el = await runPage("analysis", appSource);
  const melt = el("melt-body").innerHTML;
  check("analysis: melt table renders", melt.includes("R11"));
  const expected = ((6.1 * (14 / 24)) * (gold.price_usd_per_troy_ounce / gold.troy_ounce_in_grams));
  const shown = /R11[\s\S]*?\$\s?([\d,]+\.\d{2})/.exec(melt);
  check("analysis: R11 melt value reproduces arithmetic",
    shown && Math.abs(parseFloat(shown[1].replace(/,/g, "")) - expected) < 1,
    `expected ~${expected.toFixed(2)}, page shows ${shown ? shown[1] : "n/a"}`);
  check("analysis: coverage computed", el("coverage").innerHTML.includes(`/ ${rings.length}`));

  // ---- calculator
  el = await runPage("calculator", appSource);
  check("calculator: karat options come from standards",
    el("c-karat").innerHTML.includes("14K") && el("c-karat").innerHTML.includes("58.33%"));
  check("calculator: refuses to compute without a weight",
    el("c-out").innerHTML.includes("Enter the ring") || el("c-out").innerHTML.includes("weight"),
    "no default weight");

  // ---- standards
  el = await runPage("standards", appSource);
  check("standards: karat table renders", el("karat-body").innerHTML.includes("58.33"));
  check("standards: legal rules render", el("rules-list").innerHTML.includes("16 CFR 23.4"));

  // ---- verification log
  el = await runPage("verify", appSource);
  const verif = JSON.parse(fs.readFileSync(path.join(ROOT, "data/verification.json"), "utf8"));
  const vTbl = el("verify-table-body").innerHTML;
  check("verify: every check renders", vTbl.includes(verif.checks[0].id) &&
    vTbl.includes(verif.checks[verif.checks.length - 1].id),
    `${verif.checks.length} checks`);
  check("verify: stats come from the log",
    el("vstats").innerHTML.includes(String(verif.summary.urls_opened)));
  check("verify: discrepancies listed",
    verif.discrepancies.every((d) => el("disc-table-body").innerHTML.includes(d.flag)));
  check("verify: declared gaps are printed, not hidden",
    (verif.not_rechecked || []).every((n) => el("notrechecked").innerHTML.includes(n.url)));

  // ---- report
  let failed = 0;
  console.log("render test\n" + "=".repeat(60));
  for (const c of checks) {
    console.log(`${c.ok ? "PASS" : "FAIL"}  ${c.name}${c.detail ? `  (${c.detail})` : ""}`);
    if (!c.ok) failed++;
  }
  console.log("=".repeat(60));
  console.log(`${checks.length - failed}/${checks.length} checks passed`);
  process.exit(failed ? 1 : 0);
})().catch((e) => {
  console.error("render test crashed:", e);
  process.exit(1);
});
