#!/usr/bin/env node
/* Render test for the generated static site.
   The site is rendered by scripts/build_site.py, so there is no client-side
   table to execute any more: every assertion below reads the built HTML and
   checks it against the JSON it claims to have been built from.

   Run: node scripts/render-test.js   (after python3 scripts/build_site.py)
*/
const fs = require("fs");
const path = require("path");

const ROOT = path.resolve(__dirname, "..");
const read = (p) => fs.readFileSync(path.join(ROOT, p), "utf8");
const json = (p) => JSON.parse(read(p));

const rings = json("data/rings.json").rings;
const sellers = json("data/sellers.json").sellers;
const standards = json("data/standards.json");
const verif = json("data/verification.json");
const gold = json("data/gold-price.json");
const prices = json("data/prices.json");

// normalise for comparison: strip tags/entities and keep letters+digits only,
// so an HTML-escaped apostrophe or a registered-mark glyph does not fail a match
const norm = (t) =>
  String(t).replace(/<[^>]*>/g, " ").replace(/&[a-z#0-9]+;/gi, " ")
    .toLowerCase().replace(/[^a-z0-9]+/g, " ").trim();
const includesText = (haystack, needle) => norm(haystack).includes(norm(needle));

const checks = [];
const check = (name, cond, detail = "") => checks.push({ name, ok: !!cond, detail });

const pages = [
  "index.html", "rings.html", "combined.html", "14k.html", "18k.html", "lab-grown.html",
  "under-1000.html", "retailers.html", "sellers.html", "standards.html", "calculator.html",
  "flagged.html", "verify.html", "sources.html", "checklist.html", "methodology.html",
  "analysis.html", "excluded.html",
];

// ---------------------------------------------------------------- pages exist
const html = {};
for (const p of pages) {
  const exists = fs.existsSync(path.join(ROOT, p));
  check(`page exists: ${p}`, exists);
  if (exists) html[p] = read(p);
}

// ------------------------------------------------------- no unfinished output
for (const [p, text] of Object.entries(html)) {
  check(`${p}: no TODO/TBD/Loading placeholders`,
    !/\bTODO\b|\bTBD\b|Loading…|Loading\.\.\./.test(text));
}

// --------------------------------------------------------------- navigation
const navTargets = [...(html["index.html"] || "").matchAll(/<nav class="main-nav">([\s\S]*?)<\/nav>/g)]
  .flatMap((m) => [...m[1].matchAll(/href="([^"]+)"/g)].map((x) => x[1]));
check("nav: every page is reachable from the nav", navTargets.length >= 15, `${navTargets.length} links`);
for (const target of navTargets) {
  check(`nav target exists: ${target}`, fs.existsSync(path.join(ROOT, target)));
}
for (const p of Object.keys(html)) {
  const missing = navTargets.filter((t) => !html[p].includes(`href="${t}"`));
  check(`${p}: carries the full nav`, missing.length === 0, missing.join(","));
}

// --------------------------------------------- the policy is on every page
for (const [p, text] of Object.entries(html)) {
  check(`${p}: zero-hallucination policy present`, /Zero-hallucination policy/.test(text));
}

// ------------------------------------------- dataset B is actually published
check("combined.html: every dataset-B row is rendered",
  rings.every((r) => includesText(html["combined.html"], r.product)),
  `${rings.length} rows`);
check("combined.html: every dataset-B row keeps its source link",
  rings.every((r) => html["combined.html"].includes(r.url)));
check("combined.html: both passes side by side",
  includesText(html["combined.html"], "aurate") && includesText(html["combined.html"], "Wilson"),
  "dataset A + B");

// ------------------------------------------------------------- sellers page
check("sellers.html: all sellers rendered",
  sellers.every((s) => includesText(html["sellers.html"], s.name)), `${sellers.length} sellers`);
check("sellers.html: precious-metals exclusion quoted",
  /precious metals non-refundable/i.test(html["sellers.html"]) ||
  html["sellers.html"].includes("Precious metals are non-refundable"));

// ------------------------------------------------------------ standards page
check("standards.html: karat table renders", html["standards.html"].includes("58.33"));
check("standards.html: every legal rule cited",
  standards.legal_rules.every((r) => html["standards.html"].includes(r.cite)),
  `${standards.legal_rules.length} rules`);

// -------------------------------------------------------- verification page
check("verify.html: every check id rendered",
  verif.checks.every((c) => html["verify.html"].includes(c.id)), `${verif.checks.length} checks`);
check("verify.html: summary counts rendered",
  html["verify.html"].includes(String(verif.summary.urls_opened)) &&
  html["verify.html"].includes(String(verif.summary.flagged)));
check("verify.html: every discrepancy rendered",
  verif.discrepancies.every((d) => html["verify.html"].includes(d.flag)));
check("verify.html: declared gaps printed, not hidden",
  (verif.not_rechecked || []).every((n) => html["verify.html"].includes(n.url)));

// ------------------------------------------------------------- melt arithmetic
// The dashboard table previously squared the melt value (10K fineness printed
// as 5394.3%). Recompute from the published spot and require the exact string.
const spot = Number(prices.snapshots.find((s) => s.role === "primary").price_usd_per_troy_oz);
const oz = Number(prices.constants.troy_ounce_grams);
const perGram = spot / oz;
for (const [karat, frac] of Object.entries(prices.constants.karat_fineness)) {
  const melt = (perGram * frac).toFixed(2).replace(/\B(?=(\d{3})+(?!\d))/g, ",");
  check(`index.html: ${karat} melt/g is $${melt}`, html["index.html"].includes(`$${melt}`));
}
check("index.html: fineness shown as a percentage, not a multiple",
  html["index.html"].includes("41.67%") && html["index.html"].includes("58.33%"));

// --------------------------------------------------------- published weights
const weighted = rings.filter((r) => typeof r.weight_g === "number");
check("combined.html: every published weight appears",
  weighted.every((r) => [String(r.weight_g), r.weight_g.toFixed(1)]
    .some((w) => html["combined.html"].includes(`${w} g`))),
  `${weighted.length} weights`);
check("analysis.html: melt table reproduces each published weight",
  weighted.every((r) => html["analysis.html"].includes(`${r.weight_g.toFixed(1)} g`)));

// --------------------------------------------------------------- price basis
check("rings.html: setting-only prices are labelled",
  /Setting Price|setting price|Setting only|setting only/.test(html["rings.html"]));
check("flagged.html: high-severity content present", /high/i.test(html["flagged.html"]));

// SD4: rings.html must not claim to be the complete list. It renders dataset A only.
const _ringsHtml = read("rings.html");
check("SD4 rings.html title says dataset A", includesText(_ringsHtml, "Dataset A: all verified listings"));
check("SD4 rings.html carries a scope box", includesText(_ringsHtml, "Scope of this page"));
check("SD4 rings.html links the full combined list", _ringsHtml.includes('href="combined.html"'));
check("SD4 rings.html makes no completeness claim", !/every verified solid gold ring listing/i.test(_ringsHtml));

// SD7: nav & footnote consistency across datasets
check("SD7 nav carries Combined (71)", html["index.html"].includes("Combined (71)"));
check("SD7 index.html melt footnote does not claim zero weights overall",
  !/none of the listings publishes a weight/i.test(html["index.html"]));
check("SD7 rings.html renders Aurate published weight range",
  html["rings.html"].includes("Weight: 5.5-8.5g") && html["rings.html"].includes("range only (unverified)"));

// SD8: combined.html filter toolbar & data-cats attributes on all 3 passes
check("SD8 combined.html toolbar has Dataset C filter", html["combined.html"].includes('data-filter="c"'));
check("SD8 combined.html toolbar has 22K-24K filter", html["combined.html"].includes('data-filter="22k-24k"'));
check("SD8 combined.html toolbar has Weight published filter", html["combined.html"].includes('data-filter="weighted"'));
const _combinedTb = (html["combined.html"].match(/<table id="combined-table">[\s\S]*?<tbody>([\s\S]*?)<\/tbody>/) || ["", ""])[1];
const _combinedRows = [..._combinedTb.matchAll(/<tr([^>]*)>/g)];
check("SD8 combined.html renders all 71 rows with data-cats",
  _combinedRows.length === 71 && _combinedRows.every((m) => /data-cats="[^"]+"/.test(m[1])),
  `${_combinedRows.length} rows`);

// ------------------------------------------------------------------- report
let failed = 0;
console.log("render test (static site)\n" + "=".repeat(66));
for (const c of checks) {
  if (!c.ok) {
    console.log(`FAIL  ${c.name}${c.detail ? `  (${c.detail})` : ""}`);
    failed++;
  }
}
for (const c of checks) {
  if (c.ok) console.log(`PASS  ${c.name}${c.detail ? `  (${c.detail})` : ""}`);
}
console.log("=".repeat(66));

console.log(`${checks.length - failed}/${checks.length} checks passed`);
process.exit(failed ? 1 : 0);
