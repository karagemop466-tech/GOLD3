#!/usr/bin/env node
/**
 * Page check - every claim on the built pages, traced back to the data it came from.
 *
 * scripts/render-test.js proves the tables render. This proves the *numbers on the page*
 * are the numbers in data/*.json: counts, spot price, per-karat melt arithmetic, prices,
 * row-to-source mapping, published flag definitions and exclusions.
 *
 * It exists because the karat table shipped with melt values 129x too high and fineness
 * above 100% while every data-level check passed. A page can be wrong while the data is
 * right, and that is the failure this file is for.
 *
 * Run: node scripts/page-check.js      Exit 1 on any failure.
 */

const fs = require("fs");
const path = require("path");

const ROOT = path.resolve(__dirname, "..");
const read = (p) => fs.readFileSync(path.join(ROOT, p), "utf8");
const json = (p) => JSON.parse(read(p));

const products = json("data/products.json").products;
const ringsDoc = json("data/rings.json");
const rings = ringsDoc.rings;
const retailers = json("data/retailers.json").retailers;
const findings = json("data/findings.json").findings;
const flags = json("data/flags.json").flags;
const sources = json("data/sources.json").sources;
const standards = json("data/standards.json");
const prices = json("data/prices.json");

const OZ = prices.constants.troy_ounce_grams;
const FINENESS = prices.constants.karat_fineness;
const primary = prices.snapshots.find((s) => s.role === "primary");
const cross = prices.snapshots.find((s) => s.role === "cross-check");
const SPOT = primary.price_usd_per_troy_oz;
const SPOT_GRAM = SPOT / OZ;

const money = (n) =>
  "$" + n.toLocaleString("en-US", { minimumFractionDigits: 2, maximumFractionDigits: 2 });
const decode = (t) =>
  t.replace(/&amp;/g, "&").replace(/&#39;|&#x27;/g, "'").replace(/&quot;|&#34;/g, '"');

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
const assert = (cond, msg) => {
  if (!cond) throw new Error(msg);
};

const PAGES = [
  "index.html", "rings.html", "14k.html", "18k.html", "lab-grown.html",
  "under-1000.html", "combined.html", "excluded.html", "retailers.html",
  "calculator.html", "flagged.html", "sources.html", "checklist.html",
];
const html = {};
for (const p of PAGES) html[p] = fs.existsSync(path.join(ROOT, p)) ? read(p) : "";

// ------------------------------------------------------------------ build sanity
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

check("no stale page exists outside the builder's output", () => {
  const built = new Set(PAGES);
  const archived = new Set(["analysis.html", "standards.html", "sellers.html", "methodology.html"]);
  const extra = fs
    .readdirSync(ROOT)
    .filter((f) => f.endsWith(".html") && !built.has(f) && !archived.has(f));
  assert(extra.length === 0, `not generated and not archived: ${extra.join(", ")}`);
  for (const p of archived) {
    assert(read(p).includes("Archived snapshot - superseded"), `${p} lacks its archived banner`);
  }
  return `${archived.size} archived pages bannered`;
});

// ------------------------------------------------------------------ home page
check("home: listing count equals both datasets", () => {
  const expected = products.length + rings.length;
  assert(html["index.html"].includes(`<div class="value">${expected}</div>`),
    `no KPI showing ${expected}`);
  return `${expected}`;
});

check("home: spot price is the primary snapshot", () => {
  assert(html["index.html"].includes(money(SPOT)), `expected ${money(SPOT)}`);
  return money(SPOT);
});

check("home: per-gram figure derives from spot", () => {
  assert(html["index.html"].includes(money(SPOT_GRAM)), `expected ${money(SPOT_GRAM)}`);
  return money(SPOT_GRAM) + "/g";
});

check("home: cross-check snapshot is cited", () => {
  const shown = html["index.html"].includes(money(cross.price_usd_per_troy_oz)) ||
    html["sources.html"].includes(money(cross.price_usd_per_troy_oz));
  assert(shown, `${money(cross.price_usd_per_troy_oz)} not cited anywhere`);
  return `${money(cross.price_usd_per_troy_oz)}`;
});

check("home: karat table has every karat", () => {
  const i = html["index.html"].indexOf("Gold value by karat");
  assert(i > -1, "karat table missing");
  const table = html["index.html"].slice(i, html["index.html"].indexOf("</table>", i));
  const rows = [...table.matchAll(/<tr><td><strong>(\d+K)<\/strong><\/td>/g)];
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
  const i = html["index.html"].indexOf("Gold value by karat");
  const table = html["index.html"].slice(i, html["index.html"].indexOf("</table>", i));
  const rows = [...table.matchAll(
    /<tr><td><strong>(\d+K)<\/strong><\/td><td class='num'>[\d.]+%<\/td><td class='num'>\$([\d,]+\.\d\d)<\/td><td class='num'>\$([\d,]+\.\d\d)<\/td><\/tr>/g
  )];
  assert(rows.length === 5, `table did not parse (${rows.length} rows)`);
  for (const [, k, perGram, three] of rows) {
    const f = FINENESS[k];
    assert(f !== undefined, `${k} has no fineness constant`);
    const expect = SPOT_GRAM * f;
    const gotPer = +perGram.replace(/,/g, "");
    const got3 = +three.replace(/,/g, "");
    assert(Math.abs(gotPer - expect) < 0.011, `${k}: printed ${gotPer}, expected ${expect.toFixed(2)}`);
    assert(Math.abs(got3 - expect * 3) < 0.021, `${k}: 3 g printed ${got3}, expected ${(expect * 3).toFixed(2)}`);
  }
  return "5/5 reproduce to the cent";
});

check("home: every high-severity finding is surfaced", () => {
  const high = findings.filter((f) => f.severity === "high");
  const missing = high.filter((f) => !html["index.html"].includes(f.id));
  assert(missing.length === 0, missing.map((f) => f.id).join(", "));
  return `${high.length} high severity`;
});

// ------------------------------------------------------------------ ring tables
check("rings: one row per product, ids intact", () => {
  const ids = [...html["rings.html"].matchAll(/<tr id="p-([a-z0-9-]+)"/g)].map((m) => m[1]);
  assert(ids.length === products.length, `${ids.length} rows for ${products.length} products`);
  const missing = products.filter((p) => !ids.includes(p.id));
  assert(missing.length === 0, `missing: ${missing.map((p) => p.id).slice(0, 3).join(", ")}`);
  return `${ids.length} rows`;
});

check("rings: every row links to the seller's own page", () => {
  const page = decode(html["rings.html"]);
  const missing = products.filter((p) => !page.includes(p.url));
  assert(missing.length === 0, `${missing.length} product URLs absent`);
  return `${products.length}/${products.length} linked`;
});

check("rings: every price shown exists in the data", () => {
  const amounts = new Set(
    [...products, ...rings]
      .flatMap((x) => [x.price, x.price_usd, x.price_low, x.price_high])
      .filter((n) => typeof n === "number")
      .map((n) => money(n))
  );
  for (const snap of prices.snapshots) amounts.add(money(snap.price_usd_per_troy_oz));
  amounts.add(money(SPOT_GRAM));
  const shown = [...html["rings.html"].matchAll(/\$([\d,]+\.\d\d)/g)].map((m) => "$" + m[1]);
  const unexplained = [...new Set(shown)].filter((s) => !amounts.has(s));
  assert(unexplained.length === 0, `not in data: ${unexplained.slice(0, 4).join(", ")}`);
  return `${amounts.size} data prices`;
});

check("rings: unpriced rows say so instead of guessing", () => {
  const unpriced = products.filter((p) => p.price == null && p.price_low == null);
  for (const p of unpriced) {
    const at = html["rings.html"].indexOf(`id="p-${p.id}"`);
    assert(at > -1, `${p.id} row missing`);
    const row = html["rings.html"].slice(at, html["rings.html"].indexOf("</tr>", at));
    assert(/unverified|not published|no price|contact/i.test(row), `${p.id} has no honest blank`);
  }
  return `${unpriced.length} unpriced, all labelled`;
});

// ------------------------------------------------------------------ registers
check("retailers: every retailer in the register appears", () => {
  const missing = retailers.filter((r) => !html["retailers.html"].includes(r.name));
  assert(missing.length === 0, missing.map((r) => r.name).join(", "));
  return `${retailers.length}`;
});

check("retailers: policy links resolve, or say they cannot", () => {
  const missing = retailers.filter(
    (r) => r.returns_url && !html["retailers.html"].includes(r.returns_url)
  );
  assert(missing.length === 0, missing.map((r) => r.id).join(", "));
  const none = retailers.filter((r) => !r.returns_url);
  if (none.length) {
    assert(html["retailers.html"].includes("policy page not retrievable"),
      `${none.map((r) => r.id).join(", ")}: no URL and no honest replacement`);
  }
  return `${retailers.length - none.length} linked, ${none.length} marked unretrievable`;
});

check("flagged: every finding appears with its evidence link", () => {
  const clean = decode(html["flagged.html"]);
  const missing = findings.filter(
    (f) => !html["flagged.html"].includes(`id="${f.id}"`) || (f.source && !clean.includes(f.source))
  );
  assert(missing.length === 0, missing.map((f) => f.id).join(", "));
  return `${findings.length} findings`;
});

check("flagged: the flag dictionary publishes every definition", () => {
  const page = decode(html["flagged.html"]);
  const missing = flags.filter((f) => !page.includes(`#${f.id}"`) || !page.includes(f.label));
  assert(missing.length === 0, missing.map((f) => f.id).join(", "));
  return `${flags.length} flags`;
});

check("combined: both passes and the exclusions are represented", () => {
  const t = html["combined.html"];
  assert(t.includes(String(products.length)) && t.includes(String(rings.length)),
    "combined page does not state both pass counts");
  assert(t.includes(String(ringsDoc.excluded_listings.length)), "excluded count absent");
  return `${products.length} + ${rings.length}`;
});

check("excluded: every rejected listing is listed", () => {
  const text = decode(html["excluded.html"]).toLowerCase();
  const all = ringsDoc.excluded_listings
    .map((x) => x.product)
    .concat(["9330"]);
  const missing = ringsDoc.excluded_listings.filter(
    (x) => !text.includes(x.product.toLowerCase().slice(0, 22))
  );
  assert(missing.length === 0, `${missing.length} of ${all.length - 1} excluded items absent`);
  return `${ringsDoc.excluded_listings.length} exclusions`;
});

// ------------------------------------------------------------------ tools & law
check("calculator: karat options come from the standards file", () => {
  for (const k of Object.keys(FINENESS)) assert(html["calculator.html"].includes(k), `${k} not offered`);
  assert(/melt/i.test(html["calculator.html"]), "no melt explanation");
  return `${Object.keys(FINENESS).length} karats`;
});

check("calculator: no weight is pre-filled", () => {
  const tags = [...html["calculator.html"].matchAll(/<input[^>]*id="calc-grams"[^>]*>/g)];
  assert(tags.length > 0, "no weight input found");
  for (const t of tags) assert(!/value="[0-9]/.test(t[0]), "weight input ships with a default");
  return "blank by default";
});

check("standards: every legal rule is cited somewhere", () => {
  const all = Object.values(html).join("");
  const base = (cite) => `${cite}`.match(/(16 CFR|15 U\.S\.C\.)\s*[\d.]+/g) || [];
  const missing = standards.legal_rules.filter((r) => {
    const refs = base(r.cite);
    return refs.length === 0 || !refs.some((ref) => all.includes(ref));
  });
  assert(missing.length === 0, missing.map((r) => r.cite).join(", "));
  return `${standards.legal_rules.length} rules`;
});

check("sources: every source is https and printed", () => {
  const bad = sources.filter((s) => !/^https:\/\//.test(s.url) || !html["sources.html"].includes(s.url));
  assert(bad.length === 0, bad.map((s) => s.id).join(", "));
  return `${sources.length} sources`;
});

check("every local link resolves", () => {
  const broken = [];
  for (const p of PAGES) {
    for (const m of html[p].matchAll(/href="([^"#:]+\.(?:html|css))"/g)) {
      if (!fs.existsSync(path.join(ROOT, m[1]))) broken.push(`${p} -> ${m[1]}`);
    }
  }
  assert(broken.length === 0, broken.slice(0, 4).join(", "));
  return "all resolve";
});

console.log("\n" + "=".repeat(60));
console.log(`${pass}/${pass + failures.length} checks passed`);
if (failures.length) {
  console.log("\nFailures:");
  for (const [n, m] of failures) console.log(`  - ${n}: ${m}`);
  process.exit(1);
}
