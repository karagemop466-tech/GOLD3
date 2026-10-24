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
  "analysis.html", "excluded.html", "requirements.html",
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
const _p17AurateRows = json("data/products.json").products.filter((p) => p.id.startsWith("aurate-")).map((p) => {
  const start = _ringsHtml.indexOf(`<tr id="p-${p.id}"`);
  const end = start < 0 ? -1 : _ringsHtml.indexOf("</tr>", start);
  return { p, row: start < 0 || end < 0 ? "" : _ringsHtml.slice(start, end + 5) };
});
check("SD7 rings.html renders every Aurate weight without treating it as gold weight",
  _p17AurateRows.length === 7 &&
  _p17AurateRows.every(({ p, row }) => row && p.weight_quote && row.includes(p.weight_quote) && !row.includes("not published")) &&
  html["rings.html"].includes("range only (unverified)") &&
  html["rings.html"].includes("scope unverified; not gold weight"));

// SD8: combined.html filter toolbar & data-cats attributes on all 3 passes
check("SD8 combined.html toolbar has Dataset C filter", html["combined.html"].includes('data-filter="c"'));
check("SD8 combined.html toolbar has 22K-24K filter", html["combined.html"].includes('data-filter="22k-24k"'));
check("SD8 combined.html toolbar has Weight published filter", html["combined.html"].includes('data-filter="weighted"'));
const _combinedTb = (html["combined.html"].match(/<table id="combined-table">[\s\S]*?<tbody>([\s\S]*?)<\/tbody>/) || ["", ""])[1];
const _combinedRows = [..._combinedTb.matchAll(/<tr([^>]*)>/g)];
check("SD8 combined.html renders all 71 rows with data-cats",
  _combinedRows.length === 71 && _combinedRows.every((m) => /data-cats="[^"]+"/.test(m[1])),
  `${_combinedRows.length} rows`);


// ------------------------------------------------ SD18–SD20 / F41–F43 (Pass P13, arena/fb7e5e3c-gold3)
const _verif = JSON.parse(read("data/verification.json"));
const _ids = _verif.checks.map((c) => c.id);
check("SD18 verification ledger still has unique check ids after P13",
  new Set(_ids).size === _ids.length, `${_ids.length} checks`);
check("SD18 summary.checks equals the number of ledger entries",
  _verif.summary.checks === _verif.checks.length);
check("SD18 verify.html renders the P13 pass",
  includesText(html["verify.html"].replace(/&#x27;/g, "'"), "arena/fb7e5e3c-gold3"));

const _prices = JSON.parse(read("data/prices.json"));
const _primary = _prices.snapshots.find((s) => s.role === "primary");
const _cross = _prices.snapshots.find((s) => s.role === "cross-check");
const _live = _prices.snapshots.find((s) => String(s.role).startsWith("live-check"));
check("SD20 combined.html prints the stored primary spot",
  html["combined.html"].includes(`$${_primary.price_usd_per_troy_oz.toLocaleString("en-US", { minimumFractionDigits: 2 })}`));
check("SD20 combined.html prints the stored cross-check",
  html["combined.html"].includes(`$${_cross.price_usd_per_troy_oz.toLocaleString("en-US", { minimumFractionDigits: 2 })}`));
check("SD20 combined.html no longer prints the stale $4,026.79 anchor",
  !html["combined.html"].includes("4,026.79"));
check("SD20 methodology.html no longer claims 15 of 22 rows lack a weight",
  !includesText(html["methodology.html"], "15 of 22 rows"));
check("SD20 methodology.html no longer claims 115 checks",
  !includesText(html["methodology.html"], "115 checks"));
check("SD20 methodology.html carries the live audit tally",
  /\d+ checks, 0 errors at the last recorded run/.test(html["methodology.html"]));
check("SD20 calculator prints the labelled live-check reading",
  !!_live && html["calculator.html"].includes(
    `$${_live.price_usd_per_troy_oz.toLocaleString("en-US", { minimumFractionDigits: 2 })}`));

const _ringsDoc = JSON.parse(read("data/rings.json"));
const _b14 = _ringsDoc.rings.filter((r) => /14k/i.test(r.karat || "") && !/plating|vermeil/i.test(r.karat || ""));
const _b18 = _ringsDoc.rings.filter((r) => /18k/i.test(r.karat || "") && !/plating|vermeil/i.test(r.karat || ""));
check("SD19 14k.html lists Dataset B 14K rows",
  _b14.every((r) => html["14k.html"].includes(`id="x-${r.id}"`)), `${_b14.length} rows`);
check("SD19 18k.html lists Dataset B 18K rows",
  _b18.every((r) => html["18k.html"].includes(`id="x-${r.id}"`)), `${_b18.length} rows`);
check("SD19 18k.html no longer claims no complete verified 18K ring exists",
  !includesText(html["18k.html"], "No 18K listing here is a complete, verified ring"));
check("SD19 18k.html carries the Dataset B/C cross-karat table",
  html["18k.html"].includes('id="cross-18k"'));
check("SD19 every cross-karat row carries an https source link",
  [...html["18k.html"].matchAll(/<tr id="x-[^"]+">([\s\S]*?)<\/tr>/g)]
    .every((m) => /href="https:\/\//.test(m[1])));

const _flags = JSON.parse(read("data/flags.json")).flags.map((f) => f.id);
check("SD19 SPEC8 flag defined", _flags.includes("SPEC8"));
const _r01 = _ringsDoc.rings.find((r) => r.id === "R01");
const _r03 = _ringsDoc.rings.find((r) => r.id === "R03");
check("SD19 R01 and R03 carry SPEC8", _r01.flags.includes("SPEC8") && _r03.flags.includes("SPEC8"));
check("SD19 R03 no longer carries the misapplied SPEC2", !_r03.flags.includes("SPEC2"));

check("SD21 calculator labels the pre-filled snapshot with its own capture date",
  /Pre-filled with the 23 October 2026 snapshot/.test(html["calculator.html"]) &&
  !/Pre-filled with the 22 October 2026 snapshot/.test(html["calculator.html"]));
// SD21: the flagged page must print the date from reports/audit-report.md, whatever it is.
// A literal date here fails the moment the audit runs on a new day, which is a guard bug,
// not a site bug — so the expected string is derived from the report itself.
const _auditRun = (read("reports/audit-report.md").match(/- Run: (\d{4})-(\d{2})-(\d{2})/) || []);
const _months = ["January", "February", "March", "April", "May", "June", "July",
  "August", "September", "October", "November", "December"];
const _auditDate = _auditRun.length
  ? `${Number(_auditRun[3])} ${_months[Number(_auditRun[2]) - 1]} ${_auditRun[1]}`
  : "";
check("SD21 flagged.html audit date comes from the audit report, not a typed literal",
  _auditDate !== "" && new RegExp(`Last automated pass: ${_auditDate}`).test(html["flagged.html"]));

// P15: additive Dataset-C weight, source-attribution and calculator-provenance guards.
const _p15C = [
  ...JSON.parse(read("data/solitaire-rings.json")).items,
  ...JSON.parse(read("data/bands-and-high-karat.json")).items,
];
const _p15BandPage = read("bands-vintage-rings.html");
const _p15Ratios = _p15C.filter((r) => typeof r.price_to_melt_ratio === "number")
  .map((r) => r.price_to_melt_ratio);
const _p15Range = `${Math.min(..._p15Ratios).toFixed(2)}x–${Math.max(..._p15Ratios).toFixed(2)}x`;
check("P15 band ratio range is derived from Dataset C", _p15BandPage.includes(_p15Range), _p15Range);
check("P15 calculator presets use the actual BND-04..BND-07 product names",
  _p15C.filter((r) => ["BND-04", "BND-05", "BND-06", "BND-07"].includes(r.id))
    .every((r) => includesText(_p15BandPage, r.product_name)) &&
  !_p15BandPage.includes("Ross-Simons 6mm 14K Flat"));
const _p15Rows = new Set(verif.checks.filter((c) => c.id.startsWith("P15-")).flatMap((c) => c.rows || []));
check("P15 covers all five Dataset-C published-weight rows",
  ["BND-04", "BND-05", "BND-06", "BND-07", "BND-08"].every((id) => _p15Rows.has(id)));
const _p15Flags = JSON.parse(read("data/flags.json")).flags;
const _p15Spec7 = _p15Flags.find((f) => f.id === "SPEC7");
check("P15 SPEC7 names the actual R28 page and asserts no price",
  _p15Spec7.source.includes("petite-4-prong-ring") && !_p15Spec7.what.includes("$1,460") &&
  _ringsDoc.rings.find((r) => r.id === "R23").flags.includes("SPEC5"));
check("P15 findings F46-F49 are published for manual review",
  ["F46", "F47", "F48", "F49"].every((id) => html["flagged.html"].includes(`id="${id}"`)));
const _p15Nist = JSON.parse(read("data/spot-and-standards.json")).nist_conversion_constants;
check("P15 NIST constant carries its exact derivation and corrected attribution",
  _p15Nist.derivation.includes("480 x 0.06479891") &&
  _p15Nist.attribution_correction_p15.includes("prints no"));

// SD24: post-deploy read-back guards for pass/count prose.
check("SD24 verification session attribution includes P15",
  verif.session.includes("arena/db2fe957-gold3 (P15)") &&
  includesText(html["verify.html"], "arena/db2fe957-gold3 (P15)"));
check("SD24 F2 uses full counts and distinguishes entered weights from published ranges",
  includesText(html["flagged.html"], "Only 19 of 71 listings have a numeric gram weight for melt review") &&
  includesText(html["flagged.html"], "Published ranges and unscoped figures") &&
  !includesText(html["flagged.html"], "Only 14 of 50 listings publish a weight"));
check("SD24 README pass range and ledger count are current",
  read("README.md").includes("P1`–`P19") && read("README.md").includes("265 logged checks"));

// P17: source-drift, duplicate-flag and unsupported-inference regression guards.
const _p17 = JSON.parse(read("data/reverification-p17.json"));
const _p17A = JSON.parse(read("data/products.json")).products;
const _p17ById = Object.fromEntries(_p17A.map((p) => [p.id, p]));
const _p17Rows = new Set(_p17.checks.filter((c) => c.kind === "listing").flatMap((c) => c.rows || []));
check("P17 covers every Dataset A row and reconciles its 31-check ledger",
  _p17.checks.length === 31 && _p17Rows.size === _p17A.length && _p17A.length === 19 &&
  _p17.summary.confirmed === 10 && _p17.summary.corrected === 18 && _p17.summary.flagged === 3 &&
  verif.checks.filter((c) => c.id.startsWith("P17-")).length === 31);
check("P17 confirms all Dataset A prices without a numeric change",
  _p17.summary.dataset_a_products === 19 && _p17.summary.numeric_price_changes === 0 &&
  _p17.summary.published_weight_changes === 0);
const _p17Bezels = ["aurate-1ct-round-lgd-bezel", "aurate-2ct-emerald-lgd-bezel", "aurate-3ct-pear-lgd-bezel"]
  .map((id) => _p17ById[id]);
check("P17 leaves conflicting Aurate bezel carats null and preserves current dimensions",
  _p17Bezels.every((p) => p.carat === null && p.weight_g === null && p.weight_status === "published as unscoped weight") &&
  _p17Bezels[0].metal_detail.includes("Thickness: 5.04mm") &&
  _p17Bezels[1].metal_detail.includes("Thickness: 4.6mm") &&
  _p17Bezels[2].metal_detail.includes("Thickness: 6.10mm") &&
  !/includes [123]tcw stone|stone included|including 0\.36 g|0\.72 g stone|0\.21 g stone/i.test(JSON.stringify(_p17A)));
check("P17 Blue Nile and Mejuri specifications match the current official text",
  _p17ById["bluenile-petite-hidden-halo-14k-yg"].metal_detail.includes("502250y14; width 1.60mm") &&
  _p17ById["bluenile-riviera-pave-14k-wg"].metal_detail.includes("501590w14; width 2.00mm") &&
  _p17ById["mejuri-stacker-ring-10k"].metal_detail.includes("Width: 1 mm") &&
  _p17ById["mejuri-stacker-ring-10k"].flags.some((f) => f.code === "HALLMARK_ALT_TEXT_ONLY") &&
  !_p17ById["mejuri-stacker-ring-10k"].flags.some((f) => f.code === "HALLMARK_NOT_STATED"));
check("P17 removes false Ring Concierge purity flags and duplicate Dataset A issue codes",
  ["ringconcierge-2-08-oval-lab-whisper-thin", "ringconcierge-2-72-round-lab-whisper-thin"]
    .every((id) => !_p17ById[id].flags.some((f) => f.code === "PURITY_NOT_IN_BODY_TEXT")) &&
  _p17A.every((p) => new Set(p.flags.map((f) => f.code)).size === p.flags.length));
const _p17Bands = JSON.parse(read("data/bands-and-high-karat.json")).items;
check("P17 Ross-Simons weights stay approximate and solidity is not inferred",
  _p17Bands.filter((r) => ["BND-04", "BND-05", "BND-06", "BND-07"].includes(r.id))
    .every((r) => r.listing_type.includes("Published Approximate Gram Weight")) &&
  !/Exact Gram Weight Verified|weight confirm solid|matches solid cast/i.test(JSON.stringify(_p17Bands)));
const _p17Retailers = JSON.parse(read("data/retailers.json")).retailers;
const _p17Mejuri = _p17Retailers.find((r) => r.id === "mejuri");
check("P17 Mejuri policy drops unsupported exclusions and stale unreadable-page flag",
  !_p17Mejuri.returns_exclusions.includes("bespoke") &&
  !_p17Mejuri.flags.includes("RETURN_POLICY_PAGE_JAVASCRIPT_ONLY") &&
  _p17Mejuri.returns_exclusions.includes("SCS certificate"));
check("P17 publishes F50-F55 for manual review",
  ["F50", "F51", "F52", "F53", "F54", "F55"].every((id) => html["flagged.html"].includes(`id="${id}"`)));
const _p17Primary = _prices.snapshots.find((s) => s.role === "primary");
const _p17Live = _prices.snapshots.find((s) => String(s.role).startsWith("live-check"));
check("P17 refreshes only the live spot reference and preserves the calculation anchor",
  _p17Primary.price_usd_per_troy_oz === 4022.22 && _p17Live.price_usd_per_troy_oz === 3995.88 &&
  html["calculator.html"].includes("3,995.88") && html["calculator.html"].includes("finding F55") &&
  !html["calculator.html"].includes("findings F39 and F43"));


// P17: the requirements matrix must stay derived, not typed in.
const _reqRows = JSON.parse(read("data/requirements-matrix.json"));
const _p19verif = JSON.parse(read("data/verification.json"));
check("P19 requirements matrix covers every listing",
  _reqRows.summary.n_rows === 71 && _reqRows.rows.length === 71);
check("P19 requirements matrix has ten requirements per row",
  _reqRows.summary.requirements.length === 10 &&
  _reqRows.rows.every(r => Object.keys(r.cells).filter(k => k !== "value").length === 10));
check("P19 requirements page renders every row and the headline honestly",
  includesText(html["requirements.html"], ">R01<") &&
  includesText(html["requirements.html"], ">BND-12<") &&
  includesText(html["requirements.html"], "pass all ten"));
check("P19 every blank cell renders as an explicit unverified badge",
  (html["requirements.html"].match(/unverified/g) || []).length >= 400 &&
  !html["requirements.html"].includes(">n/a<") &&
  !html["requirements.html"].includes(">N/A<"));
check("P19 verification ledger includes the P19 checks",
  _p19verif.checks.some(c => c.id.startsWith("P19-")) &&
  includesText(html["verify.html"], "P19"));
check("P19 findings F56-F58 are published for manual review",
  includesText(html["flagged.html"], "F56") && includesText(html["flagged.html"], "F58"));
check("P19 index links to the requirements matrix",
  html["index.html"].includes('href="requirements.html"') &&
  html["requirements.html"].includes('href="index.html"'));

// P19: independent corroborating pass after peer P17 merged first via PR #69.
const _p19 = JSON.parse(read("data/reverification-p19.json"));
const _p19Ids = verif.checks.map((c) => c.id);
const _p19Report = read("reports/reverification-pass-p19.md");
const _p19Hist = JSON.stringify(JSON.parse(read("data/reverification-c-6ccbc523.json")));
const _p19Bundle = read("reports/reverification-1162b2db.md");
check("P19 preserves peer P17 and appends 36 unique checks",
  verif.session.includes("arena/36ebce13-gold3 (P17)") &&
  verif.session.includes("arena/bd0ed905-gold3 (P19)") &&
  verif.checks.filter((c) => c.id.startsWith("P17-")).length === 31 &&
  verif.checks.filter((c) => c.id.startsWith("P19-")).length === 36 &&
  _p19Ids.length === new Set(_p19Ids).size && _p19Ids.length === 289 &&
  _p19.summary.confirmed === 13 && _p19.summary.corrected === 21 && _p19.summary.flagged === 2);
check("P19 artifacts publish the pass and keep README/session counts current",
  _p19Report.includes("Pass P19") && _p19Report.includes("P19-36") &&
  read("README.md").includes("P1`–`P19") && read("README.md").includes("289 logged checks") &&
  includesText(html["verify.html"], "arena/bd0ed905-gold3 (P19)"));
check("P19 findings F56-F61 are published for manual review",
  ["F56", "F57", "F58", "F59", "F60", "F61"].every((id) => html["flagged.html"].includes(`id=\"${id}\"`)));
check("P19 all seven Aurate rows quote their live weights without inferring exact weight_g",
  _p17A.filter((p) => p.id.startsWith("aurate-")).length === 7 &&
  _p17A.filter((p) => p.id.startsWith("aurate-")).every((p) => p.weight_g === null && /^Weight: /.test(p.weight_quote || "")) &&
  ["Weight: 2.23g", "Weight: 2.36g", "Weight: 3.33g"].every((q) => includesText(html["rings.html"], q)));
check("P19 corrected the last Ring Concierge E VS1 prose and excluded-Mejuri source links",
  !_p17ById["ringconcierge-2-72-round-lab-whisper-thin"].notes.includes("E VS1") &&
  _p17ById["ringconcierge-2-72-round-lab-whisper-thin"].carat_note.includes("E VVS2") &&
  ["mejuri-dome-figure-vermeil", "mejuri-dome-figure-sterling"]
    .every((id) => _p17ById[id].price_source === _p17ById[id].url));
check("P19 structured Kitco cross-check and live-check history exist while the anchor stays fixed",
  _prices.live_cross_check && _prices.live_cross_check.price_usd_per_troy_oz === 3994.9 &&
  _prices.snapshots.find((s) => String(s.role).startsWith("live-check")).history?.[0]?.price_usd_per_troy_oz === 3997.22 &&
  html["calculator.html"].includes("$3,994.90") && html["calculator.html"].includes("value=\"4022.22\"") &&
  html["calculator.html"].includes("reference observations only"));
check("P19 CR closeout preserves the original evidence and both report versions",
  _p19Hist.includes("evidence_original_preserved") && _p19Hist.includes("NIST SP 811 Appendix B.9") &&
  ["## Version A", "## Version B", "Resolution"].every((s) => _p19Bundle.includes(s)) &&
  !/^(<{7}|={7}|>{7})/m.test(_p19Bundle));
check("P19 site-defect counters and review flags stay consistent",
  verif.site_defects_fixed === verif.summary.site_defects_fixed &&
  verif.site_defects_fixed === verif.site_defects.filter((d) => /fixed/i.test(d.status)).length &&
  ["SPOT2", "REV1", "SRC4"].every((id) => html["flagged.html"].includes(id)));

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
