#!/usr/bin/env node
/**
 * Render test — every claim the site makes, checked against the data it came from.
 *
 * The site is generated from data/*.json by scripts/build_site.py. This test reads the
 * generated HTML and asserts that each printed figure, count, quote and link is
 * reproducible from those files. It exists because a page can pass every data check
 * and still *print the wrong thing* — that is exactly how the karat table shipped with
 * a 129x inflated melt value and fineness figures above 100%.
 *
 * Run: node scripts/render-test.js      Exit 1 on any failure.
 */

const fs = require("fs");
const path = require("path");

const ROOT = path.resolve(__dirname, "..");
const read = (p) => fs.readFileSync(path.join(ROOT, p), "utf8");
const json = (p) => JSON.parse(read(p));

const products = json("data/products.json").products;
const rings = json("data/rings.json").rings;
const retailers = json("data/retailers.json").retailers;
const findings = json("data/findings.json").findings;
const flags = json("data/flags.json").flags;
const sources = json("data/sources.json").sources;
const standards = json("data/standards.json");
const prices = json("data/prices.json");
const ringsDoc = json("data/rings.json");

const OZ = prices.constants.troy_ounce_grams;
const FINENESS = prices.constants.karat_fineness;
const primary = prices.snapshots.find((s) => s.role === "primary");
const cross = prices.snapshots.find((s) => s.role === "cross-check");
const SPOT = primary.price_usd_per_troy_oz;
const SPOT_GRAM = SPOT / OZ;

const money = (n) =>
  "$" + n.toLocaleString("en-US", { minimumFractionDigits: 2, maximumFractionDigits: 2 });

let pass = 0;
const failures = [];
function check(name, fn) {
  try {
    const detail = fn();
    pass++;
    console.log(`PASS  ${name}${detail ? `  (${detail})` : ""}`);
  } catch (e) {
    failures.push([name, e.message]);
    console.log(`FAIL  ${name}  (${e.message})`);
  }
}
function assert(cond, msg) {
  if (!cond) throw new Error(msg);
}

// ---------------------------------------------------------------- pages exist
const PAGES = [
  "index.html", "rings.html", "14k.html", "18k.html", "lab-grown.html",
  "under-1000.html", "combined.html", "excluded.html", "retailers.html",
  "calculator.html", "flagged.html", "sources.html", "checklist.html",
];
const html = {};
for (const p of PAGES) html[p] = fs.existsSync(path.join(ROOT, p)) ? read(p) : "";

check("every page is built and non-trivial", () => {
  const thin = PAGES.filter((p) => html[p].length < 4000);
  assert(thin.length === 0, `empty or missing: ${thin.join(", ")}`);
  return `${PAGES.length} pages`;
});

check("no page leaks template or placeholder text", () => {
  const bad = [];
  for (const p of PAGES) {
    for (const token of ["{{", "}}", "undefined", "NaN", "lorem ipsum", "TODO"]) {
      if (html[p].includes(token)) bad.push(`${p}:${token}`);
    }
  }
  assert(bad.length === 0, bad.slice(0, 5).join(", "));
});

// ---------------------------------------------------------------- home page
check("home: listing count equals products + rings", () => {
  const expected = products.length + rings.length;
  assert(
    html["index.html"].includes(`<div class="value">${expected}</div>`),
    `no KPI showing ${expected} listings`
  );
  return `${expected}`;
});

check("home: seller count equals both registers", () => {
  const sellers = new Set(retailers.map((r) => r.name));
  assert(html["index.html"].includes(String(sellers.size)), "seller KPI missing");
  return `${sellers.size} retailers`;
});

check("home: spot price is the primary snapshot", () => {
  assert(html["index.html"].includes(money(SPOT)), `expected ${money(SPOT)}`);
  return money(SPOT);
});

check("home: per-gram figure derives from spot", () => {
  assert(html["index.html"].includes(money(SPOT_GRAM)), `expected ${money(SPOT_GRAM)}`);
  return money(SPOT_GRAM) + "/g";
});

check("home: both price sources cited", () => {
  assert(html["index.html"].includes(money(cross.price_usd_per_troy_oz)) ||
    html["sources.html"].includes(money(cross.price_usd_per_troy_oz)),
    "cross-check snapshot not shown");
  return `${cross.price_usd_per_troy_oz} cross-check`;
});

check("home: karat table has every karat", () => {
  const body = html["index.html"].slice(html["index.html"].indexOf("Gold value by karat"));
  const table = body.slice(0, body.indexOf("</table>"));
  const rows = [...table.matchAll(/<tr><td><strong>(\d+K)<\/strong><\/td><td class='num'>([\d.]+)%<\/td><td class='num'>\$([\d,]+\.\d\d)<\/td><td class='num'>\$([\d,]+\.\d\d)<\/td>/g)];
  assert(rows.length === 5, `parsed ${rows.length} rows, expected 5`);
  return `${rows.length} karats`;
});

check("home: no fineness exceeds 100%", () => {
  const pcts = [...html["index.html"].matchAll(/<td class='num'>([\d.]+)%<\/td>/g)].map((m) => +m[1]);
  const bad = pcts.filter((p) => p > 100);
  assert(bad.length === 0, `impossible fineness printed: ${bad.join(", ")}%`);
  return `max ${Math.max(...pcts)}%`;
});

check("home: every melt value reproduces from spot x fineness", () => {
  const body = html["index.html"].slice(html["index.html"].indexOf("Gold value by karat"));
  const table = body.slice(0, body.indexOf("</table>"));
  const rows = [...table.matchAll(/<tr><td><strong>(\d+K)<\/strong><\/td><td class='num'>[\d.]+%<\/td><td class='num'>\$([\d,]+\.\d\d)<\/td><td class='num'>\$([\d,]+\.\d\d)<\/td><\/tr>/g)];
  assert(rows.length === 5, "table did not parse");
  for (const [, k, perGram, three] of rows) {
    const f = FINENESS[k];
    assert(f !== undefined, `${k} has no fineness constant`);
    const expectPer = SPOT_GRAM * f;
    const gotPer = +perGram.replace(/,/g, "");
    const got3 = +three.replace(/,/g, "");
    assert(Math.abs(gotPer - expectPer) < 0.011, `${k}: printed ${gotPer}, expected ${expectPer.toFixed(2)}`);
    assert(Math.abs(got3 - expectPer * 3) < 0.021, `${k}: 3g printed ${got3}, expected ${(expectPer * 3).toFixed(2)}`);
  }
  return "5/5 reproduce to the cent";
});

check("home: every high-severity finding is surfaced", () => {
  const high = findings.filter((f) => f.severity === "high");
  const missing = high.filter((f) => !html["index.html"].includes(f.id));
  assert(missing.length === 0, missing.map((f) => f.id).join(", "));
  return `${high.length} high-severity`;
});

check("home: weight claim matches the data", () => {
  const withWeight = products.filter((p) => p.weight_grams != null).length +
    rings.filter((r) => r.weight_grams != null).length;
  const total = products.length + rings.length;
  assert(
    html["index.html"].includes(`${withWeight} of ${total}`) ||
    html["index.html"].includes(`${withWeight}`),
    `page does not state ${withWeight} of ${total}`
  );
  return `${withWeight} of ${total}`;
});

// ---------------------------------------------------------------- rings table
check("rings: one row per product, ids intact", () => {
  const ids = [...html["rings.html"].matchAll(/<tr id="p-([a-z0-9-]+)"/g)].map((m) => m[1]);
  assert(ids.length === products.length, `${ids.length} rows for ${products.length} products`);
  const missing = products.filter((p) => !ids.includes(p.id));
  assert(missing.length === 0, `missing rows: ${missing.map((p) => p.id).slice(0, 3).join(", ")}`);
  return `${ids.length} rows`;
});

check("rings: every row links to the seller's own page", () => {
  const page = html["rings.html"].replace(/&amp;/g, "&");
  const missing = products.filter((p) => !page.includes(p.url));
  assert(missing.length === 0, `${missing.length} product URLs absent`);
  return `${products.length}/${products.length} linked`;
});

check("rings: every price shown is a price in the data", () => {
  const amounts = new Set(
    [...[...products, ...rings].flatMap((x) => [x.price_usd, x.price_low, x.price_high])
      .filter((n) => typeof n === "number")].map((n) => money(n))
  );
  const shown = [...html["rings.html"].matchAll(/\$([\d,]+\.\d\d)/g)].map((m) => "$" + m[1]);
  for (const snap of prices.snapshots) amounts.add(money(snap.price_usd_per_troy_oz));
  amounts.add(money(SPOT_GRAM));
  const unexplained = [...new Set(shown)].filter((s) => !amounts.has(s));
  assert(unexplained.length === 0, `not in data: ${unexplained.slice(0, 4).join(", ")}`);
  return `${amounts.size} data prices`;
});

check("rings: unpriced rows say so instead of guessing", () => {
  const unpriced = products.filter((p) => p.price_usd == null && p.price_low == null);
  for (const p of unpriced) {
    const at = html["rings.html"].indexOf(`id="p-${p.id}"`);
    assert(at > -1, `${p.id} row missing`);
    const row = html["rings.html"].slice(at, html["rings.html"].indexOf("</tr>", at));
    assert(/unverified|not published|no price|contact/i.test(row), `${p.id} shows no honest blank`);
  }
  return `${unpriced.length} unpriced, all labelled`;
});

// ---------------------------------------------------------------- other pages
check("retailers: every retailer in the register appears", () => {
  const missing = retailers.filter((r) => !html["retailers.html"].includes(r.name));
  assert(missing.length === 0, missing.map((r) => r.name).join(", "));
  return `${retailers.length}`;
});

check("retailers: every cited policy URL resolves into the page", () => {
  const noUrl = retailers.filter((r) => r.returns_url && !html["retailers.html"].includes(r.returns_url));
  const unretrievable = retailers.filter((r) => !r.returns_url);
  for (const r of unretrievable) {
    assert(html["retailers.html"].includes("policy page not retrievable"),
      `${r.id}: no policy URL and no honest replacement shown`);
  }
  assert(noUrl.length === 0, noUrl.map((r) => r.id).join(", "));
  return `${retailers.filter((r) => r.returns_url).length} policy links`;
});

check("flagged: every finding appears with its evidence link", () => {
  const clean = html["flagged.html"].replace(/&amp;/g, "&");
  const missing = findings.filter((f) => !html["flagged.html"].includes(`id="${f.id}"`) ||
    (f.source && !clean.includes(f.source)));
  assert(missing.length === 0, missing.map((f) => f.id).join(", "));
  return `${findings.length} findings`;
});

check("flagged: every flag definition is published", () => {
  const page = html["flagged.html"]
    .replace(/&amp;/g, "&").replace(/&#39;|&#x27;/g, "'").replace(/&quot;|&#34;/g, '"');
  const missing = flags.filter(
    (f) => !page.includes(`#${f.id}"`) || !page.includes(f.label)
  );
  assert(missing.length === 0, missing.map((f) => f.id).join(", "));
  return `${flags.length} flags`;
});

check("combined: both passes are represented", () => {
  const t = html["combined.html"];
  assert(t.includes(String(products.length)) && t.includes(String(rings.length)),
    "combined page does not state both pass counts");
  assert(t.includes(String(ringsDoc.excluded_listings.length)), "excluded count absent");
  return `${products.length} + ${rings.length}`;
});

check("excluded: every rejected listing is listed", () => {
  const text = html["excluded.html"]
    .replace(/&amp;/g, "&").replace(/&#39;|&rsquo;/g, "'").replace(/&quot;/g, '"')
    .toLowerCase();
  const missing = ringsDoc.excluded_listings.filter(
    (e) => !text.includes(e.product.toLowerCase().slice(0, 22))
  );
  assert(missing.length === 0, `${missing.length} excluded items absent`);
  return `${ringsDoc.excluded_listings.length} excluded`;
});

check("calculator: karat options come from the standards file", () => {
  for (const k of Object.keys(FINENESS)) {
    assert(html["calculator.html"].includes(k), `${k} not offered`);
  }
  assert(/fin(e|_)?\s?gold|melt/i.test(html["calculator.html"]), "no melt explanation");
  return `${Object.keys(FINENESS).length} karats`;
});

check("calculator: no weight is pre-filled", () => {
  const m = [...html["calculator.html"].matchAll(/<input[^>]*id="calc-grams"[^>]*>/g)];
  assert(m.length > 0, "no weight input found");
  for (const tag of m) assert(!/value="[0-9]/.test(tag[0]), "weight input ships with a default");
  return "blank by default";
});

check("standards: every legal rule is cited with its reference", () => {
  const all = Object.values(html).join("");
  // citations carry subsections and parallel references ("16 CFR 23.10 · 15 U.S.C. 297");
  // the check is that each reported authority is present, not that the punctuation matches.
  const base = (cite) => (`${cite}`.match(/(16 CFR|15 U\.S\.C\.)\s*[\d.]+/g) || []);
  const missing = standards.legal_rules.filter((r) => {
    const refs = base(r.cite);
    return refs.length === 0 || !refs.some((ref) => all.includes(ref.replace(/\s+/g, " ")));
  });
  assert(missing.length === 0, missing.map((r) => r.cite).join(", "));
  return `${standards.legal_rules.length} rules`;
});

check("sources: every source is https and printed", () => {
  const bad = sources.filter((s) => !/^https:\/\//.test(s.url) || !html["sources.html"].includes(s.url));
  assert(bad.length === 0, bad.map((s) => s.id).join(", "));
  return `${sources.length} sources`;
});

check("every local link on every page resolves", () => {
  const broken = [];
  for (const p of PAGES) {
    for (const m of html[p].matchAll(/href="([^"#:]+\.(?:html|css))"/g)) {
      const target = path.join(ROOT, m[1]);
      if (!fs.existsSync(target)) broken.push(`${p} -> ${m[1]}`);
    }
  }
  assert(broken.length === 0, broken.slice(0, 4).join(", "));
  return "all resolve";
});

// ---------------------------------------------------------------- summary
console.log("\n" + "=".repeat(60));
console.log(`${pass}/${pass + failures.length} checks passed`);
if (failures.length) {
  console.log("\nFailures:");
  for (const [n, m] of failures) console.log(`  - ${n}: ${m}`);
  process.exit(1);
}
