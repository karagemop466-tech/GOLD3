#!/usr/bin/env node

/**
 * Source and no-hallucination gate for the GOLD3 static research site.
 * This checks data provenance and local site integrity; it does not test a
 * physical ring, verify a seller's claims, or make third-party sites truthful.
 */
import fs from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const approvedHosts = new Set([
  'bluenile.com', 'www.bluenile.com',
  'bbb.org', 'www.bbb.org',
  'trustpilot.com', 'www.trustpilot.com',
  'ecfr.gov', 'www.ecfr.gov',
  'govinfo.gov', 'www.govinfo.gov',
  'consumerfinance.gov', 'www.consumerfinance.gov',
  'nist.gov', 'www.nist.gov',
  'lbma.org.uk', 'www.lbma.org.uk',
  'assayofficelondon.co.uk', 'www.assayofficelondon.co.uk'
]);

const errors = [];
const warnings = [];
const fail = (message) => errors.push(message);
const warn = (message) => warnings.push(message);
const say = (message) => console.log(message);

async function readJson(relativePath) {
  try {
    return JSON.parse(await fs.readFile(path.join(root, relativePath), 'utf8'));
  } catch (error) {
    fail(`${relativePath}: could not parse JSON (${error.message})`);
    return null;
  }
}

async function walk(directory) {
  const entries = await fs.readdir(directory, { withFileTypes: true });
  const files = [];
  for (const entry of entries) {
    if (entry.name === '.git' || entry.name === 'node_modules' || entry.name === 'dist') continue;
    const absolute = path.join(directory, entry.name);
    if (entry.isDirectory()) files.push(...await walk(absolute));
    else files.push(absolute);
  }
  return files;
}

function validateHttps(urlValue, where) {
  if (typeof urlValue !== 'string' || !urlValue.trim()) {
    fail(`${where}: missing source URL`);
    return null;
  }
  try {
    const url = new URL(urlValue);
    if (url.protocol !== 'https:') fail(`${where}: external source must use HTTPS (${urlValue})`);
    if (!approvedHosts.has(url.hostname.toLowerCase())) fail(`${where}: source host is not in the reviewed allowlist (${url.hostname})`);
    return url;
  } catch {
    fail(`${where}: invalid URL (${urlValue})`);
    return null;
  }
}

const sourcesData = await readJson('data/sources.json');
const ringsData = await readJson('data/rings.json');
const findingsData = await readJson('data/findings.json');
const checklistData = await readJson('data/checklist.json');
const merchantsData = await readJson('data/merchants.json');
const marketData = await readJson('data/market.json');

if (![sourcesData, ringsData, findingsData, checklistData, merchantsData, marketData].every(Boolean)) {
  console.error('\nSource/no-hallucination audit: FAIL');
  process.exit(1);
}

for (const [name, data] of Object.entries({ ringsData, findingsData, checklistData, merchantsData, marketData })) {
  if (data.reviewedOn !== sourcesData.reviewedOn) fail(`${name}: review date does not match the source register`);
}

const sourceById = new Map();
for (const source of sourcesData.sources ?? []) {
  if (!source.id || sourceById.has(source.id)) fail(`Duplicate or missing source id: ${source.id ?? '(blank)'}`);
  sourceById.set(source.id, source);
  validateHttps(source.url, `source ${source.id}`);
  if (source.checkedOn !== sourcesData.reviewedOn) fail(`source ${source.id}: checkedOn must match the source-register review date`);
  if (!source.title || !source.publisher || !source.kind || !source.caveat) {
    fail(`source ${source.id}: title, publisher, kind, and caveat are required`);
  }
  if (!Array.isArray(source.supports) || source.supports.length === 0) {
    fail(`source ${source.id}: at least one supported claim must be documented`);
  }
}

function requireSource(sourceId, where) {
  if (!sourceById.has(sourceId)) fail(`${where}: unknown source id ${String(sourceId)}`);
}

function scanSourceReferences(value, where = 'data') {
  if (Array.isArray(value)) {
    value.forEach((item, index) => scanSourceReferences(item, `${where}[${index}]`));
    return;
  }
  if (!value || typeof value !== 'object') return;
  if (Object.hasOwn(value, 'value') && value.value !== null && !value.sourceId) {
    fail(`${where}: populated claim value has no sourceId`);
  }
  if (Object.hasOwn(value, 'amount') && value.amount !== null && !value.sourceId) {
    fail(`${where}: populated numeric amount has no sourceId`);
  }
  if (Object.hasOwn(value, 'value') && value.value === null && value.status !== 'unverified') {
    fail(`${where}: blank claim value must be explicitly marked unverified`);
  }
  for (const [key, child] of Object.entries(value)) {
    if (key === 'sourceId' || key === 'primarySourceId' || key === 'returnPolicySourceId') {
      requireSource(child, `${where}.${key}`);
    } else if (key === 'sourceIds' && Array.isArray(child)) {
      child.forEach((id) => requireSource(id, `${where}.${key}`));
    } else {
      scanSourceReferences(child, `${where}.${key}`);
    }
  }
}
scanSourceReferences(ringsData, 'rings');
scanSourceReferences(findingsData, 'findings');
scanSourceReferences(checklistData, 'checklist');
scanSourceReferences(merchantsData, 'merchants');
scanSourceReferences(marketData, 'market');

const findingById = new Map((findingsData.findings ?? []).map((finding) => [finding.id, finding]));
const candidateById = new Map((ringsData.candidates ?? []).map((candidate) => [candidate.id, candidate]));
if (candidateById.size !== (ringsData.candidates ?? []).length) fail('Product candidate ids are not unique.');

for (const candidate of ringsData.candidates ?? []) {
  const where = `candidate ${candidate.id}`;
  const productUrl = validateHttps(candidate.productUrl, `${where}.productUrl`);
  const source = sourceById.get(candidate.primarySourceId);
  if (!source) continue;
  if (source.url !== candidate.productUrl) fail(`${where}: primary source URL does not match the product page URL`);
  if (!candidate.name || !candidate.stockNumber) fail(`${where}: name and seller stock number are required`);
  if (candidate.price?.sourceId !== candidate.primarySourceId) fail(`${where}: price must cite the product's first-party page`);
  if (!Number.isFinite(candidate.price?.amount) || candidate.price.amount <= 0) fail(`${where}: price must be a positive, explicitly sourced number`);
  if (candidate.price?.currency !== 'USD') fail(`${where}: currency must be explicitly recorded`);
  if (candidate.price?.checkedOn !== ringsData.reviewedOn) fail(`${where}: price snapshot date must match the dataset review date`);
  if (!candidate.price?.scope) fail(`${where}: price scope (what the price includes) must be stated`);
  if (!productUrl) continue;

  const fieldChecks = [
    ['solid-gold statement', candidate.metal?.explicitSolidGoldStatement],
    ['plating exclusion', candidate.metal?.platingExcluded],
    ['gold-only weight', candidate.metal?.weightGrams],
    ['physical karat stamp', candidate.metal?.karatStamp],
    ['maker mark', candidate.metal?.makerMark],
    ['independent-test permission', candidate.independentTestPermission],
    ['credit-card payment verification', candidate.sellerPaymentCreditCard]
  ];
  for (const [label, field] of fieldChecks) {
    if (!field || !field.sourceId) {
      fail(`${where}: ${label} needs a linked evidence record, even when the result is blank`);
      continue;
    }
    requireSource(field.sourceId, `${where}.${label}`);
    if (field.value === null) {
      if (field.status !== 'unverified') fail(`${where}: blank ${label} must be labeled unverified`);
      if (!field.flagId || !findingById.has(field.flagId)) fail(`${where}: blank ${label} must link to a published review finding`);
    } else if (field.status !== 'verified') {
      fail(`${where}: populated ${label} must be marked verified and source-linked`);
    }
  }

  for (const flagId of candidate.flagIds ?? []) {
    if (!findingById.has(flagId)) fail(`${where}: unknown flagged-finding id ${flagId}`);
  }

  if (candidate.qualified === true || candidate.qualificationStatus === 'qualified') {
    const required = fieldChecks.map(([, field]) => field);
    if (required.some((field) => !field || field.status !== 'verified' || field.value === null)) {
      fail(`${where}: candidate cannot be qualified while a required evidence field is unverified`);
    }
    if ((candidate.flagIds ?? []).length > 0) fail(`${where}: qualified candidate cannot retain unresolved flags`);
  }
}

const countedQualified = (ringsData.candidates ?? []).filter((candidate) => candidate.qualified === true).length;
if (ringsData.qualifyingCandidateCount !== countedQualified) fail('qualifyingCandidateCount does not match the candidate data.');

for (const finding of findingsData.findings ?? []) {
  if (!finding.id || !finding.title || !finding.finding || !finding.action) fail(`finding ${finding.id ?? '(blank)'} is missing required explanation/action`);
  if (!Array.isArray(finding.sourceIds) || finding.sourceIds.length === 0) fail(`finding ${finding.id}: every finding must link to a source`);
  if (!Array.isArray(finding.candidateIds) || finding.candidateIds.some((id) => !candidateById.has(id))) {
    fail(`finding ${finding.id}: candidate references must point to listed candidates`);
  }
  if (finding.recommendLookingForHallucinations !== true) warn(`finding ${finding.id}: add the review reminder to look for hallucinations`);
}

for (const check of checklistData.checks ?? []) {
  if (!check.requirement || !check.status || !check.currentEvidence || !check.nextStep) fail(`checklist row ${check.id} is incomplete`);
  if (!Array.isArray(check.sourceIds) || check.sourceIds.length === 0) fail(`checklist row ${check.id}: every row must have a source link`);
}

for (const merchant of merchantsData.merchants ?? []) {
  validateHttps(merchant.officialSite, `merchant ${merchant.id}.officialSite`);
  if (!merchant.contact?.sourceId) fail(`merchant ${merchant.id}: contact data needs a source`);
  if (!Array.isArray(merchant.reputationSignals) || merchant.reputationSignals.length === 0) {
    fail(`merchant ${merchant.id}: reputation data needs linked independent sources or an explicit unresolved flag`);
  }
  for (const signal of merchant.reputationSignals ?? []) {
    requireSource(signal.sourceId, `merchant ${merchant.id} reputation signal`);
    if (signal.metrics && signal.metrics.checkedOn !== merchantsData.reviewedOn) {
      fail(`merchant ${merchant.id} reputation metric is missing the current review date`);
    }
    for (const [metric, value] of Object.entries(signal.metrics ?? {})) {
      if (metric === 'checkedOn') continue;
      if (typeof value === 'number' && (!Number.isFinite(value) || value < 0)) {
        fail(`merchant ${merchant.id} reputation metric ${metric} must be a non-negative finite value`);
      }
    }
  }
}

const quote = marketData.goldSpotQuote;
if (quote?.amount !== null || quote?.quoteDateTime !== null || quote?.unit !== null) {
  fail('Market quote must remain blank unless a dated value and its primary source have been verified and explicitly entered.');
}
if (quote?.status !== 'not populated') fail('Blank market quote must be clearly marked not populated.');

const htmlFiles = (await walk(root)).filter((file) => file.endsWith('.html'));
const htmlByPath = new Map();
for (const file of htmlFiles) htmlByPath.set(file, await fs.readFile(file, 'utf8'));

for (const [file, html] of htmlByPath) {
  const relativeFile = path.relative(root, file);
  if (!/http-equiv\s*=\s*["']Content-Security-Policy["']/i.test(html)) fail(`${relativeFile}: Content Security Policy meta tag missing`);
  if (/\bon[a-z]+\s*=\s*["']/i.test(html)) fail(`${relativeFile}: inline event handler found`);
  if (/\bstyle\s*=\s*["']/i.test(html)) fail(`${relativeFile}: inline CSS found`);
  if (/javascript:/i.test(html)) fail(`${relativeFile}: javascript: URL found`);
  if (/<script\b[^>]*\bsrc\s*=\s*["']https?:/i.test(html)) fail(`${relativeFile}: remote script source found`);
  if (/<iframe\b|<object\b|<embed\b/i.test(html)) fail(`${relativeFile}: embedded third-party content found`);

  for (const match of html.matchAll(/<a\b[^>]*>/gi)) {
    const tag = match[0];
    if (/\bhref\s*=\s*["']https:/i.test(tag) && /\btarget\s*=\s*["']_blank["']/i.test(tag)) {
      const rel = tag.match(/\brel\s*=\s*["']([^"']*)["']/i)?.[1] ?? '';
      if (!/\bnoopener\b/i.test(rel) || !/\bnoreferrer\b/i.test(rel)) {
        fail(`${relativeFile}: new-tab external link must include rel=noopener noreferrer`);
      }
    }
  }

  const idList = [...html.matchAll(/\bid\s*=\s*["']([^"']+)["']/gi)].map((match) => match[1]);
  const ids = new Set(idList);
  if (ids.size !== idList.length) fail(`${relativeFile}: duplicate HTML id found`);
  for (const match of html.matchAll(/\bhref\s*=\s*["']([^"']+)["']/gi)) {
    const href = match[1].replaceAll('&amp;', '&');
    if (/^(mailto:|tel:)/i.test(href)) continue;
    if (/^https:/i.test(href)) {
      validateHttps(href, `${relativeFile} link`);
      continue;
    }
    if (/^http:/i.test(href)) {
      fail(`${relativeFile}: insecure external link (${href})`);
      continue;
    }
    if (/^(data:|javascript:)/i.test(href)) {
      fail(`${relativeFile}: unsafe link scheme (${href.split(':')[0]})`);
      continue;
    }
    const [pathPart, hashPart = ''] = href.split('#');
    const target = pathPart
      ? path.resolve(path.dirname(file), decodeURIComponent(pathPart))
      : file;
    let targetPath = target;
    try {
      const stat = await fs.stat(target);
      if (stat.isDirectory()) targetPath = path.join(target, 'index.html');
    } catch {
      fail(`${relativeFile}: broken local link (${href})`);
      continue;
    }
    if (hashPart) {
      const targetHtml = htmlByPath.get(targetPath) ?? (await fs.readFile(targetPath, 'utf8').catch(() => ''));
      const targetIds = new Set([...targetHtml.matchAll(/\bid\s*=\s*["']([^"']+)["']/gi)].map((item) => item[1]));
      if (!targetIds.has(decodeURIComponent(hashPart))) fail(`${relativeFile}: missing local anchor (${href})`);
    } else if (!pathPart && !ids.size) {
      fail(`${relativeFile}: empty same-page anchor (${href})`);
    }
  }
}

const jsFiles = (await walk(root)).filter((file) => file.endsWith('.js') || file.endsWith('.mjs'));
for (const file of jsFiles) {
  const relativeFile = path.relative(root, file);
  const code = await fs.readFile(file, 'utf8');
  if (/\beval\s*\(|\bnew\s+Function\s*\(/.test(code)) fail(`${relativeFile}: dynamic code execution found`);
  if (/\b(innerHTML|outerHTML)\s*=/.test(code)) fail(`${relativeFile}: unsafe HTML-string insertion found`);
  if (/https?:\/\//i.test(code)) warn(`${relativeFile}: review any hard-coded remote URL before adding it`);
}

if (errors.length > 0) {
  console.error('\nSource/no-hallucination audit: FAIL');
  for (const error of errors) console.error(`  - ${error}`);
  if (warnings.length) {
    console.error('\nWarnings:');
    for (const warning of warnings) console.error(`  - ${warning}`);
  }
  process.exit(1);
}

say('Source/no-hallucination audit: PASS');
say(`  ${sourceById.size} sourced claims registered; all source links use HTTPS and reviewed hosts.`);
say(`  ${(ringsData.candidates ?? []).length} retail listing snapshots; ${countedQualified} fully qualified rings.`);
say(`  ${(findingsData.findings ?? []).length} flagged findings; blank required values remain explicitly unverified.`);
say(`  ${htmlFiles.length} HTML pages checked for broken local paths, unsafe schemes, and embedded remote content.`);
say(`  ${jsFiles.length} JavaScript files checked for dynamic code execution and unsafe HTML insertion.`);
say('  Gold quote remains blank; no market price or missing ring weight was invented.');
if (warnings.length) {
  console.log('\nWarnings:');
  for (const warning of warnings) console.log(`  - ${warning}`);
}
console.log('\nReview reminder: re-check every live listing and source for changes and hallucinations before purchase.');
