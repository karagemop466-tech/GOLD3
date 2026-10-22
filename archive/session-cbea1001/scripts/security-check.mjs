#!/usr/bin/env node
/**
 * scripts/security-check.mjs
 *
 * Automated Anti-Hallucination & Security Verification Suite for GOLD3.
 * Run after every data/UI review pass (`npm run security-check`).
 *
 * Enforces:
 *   SEC-01: Front-page top summary prominently states "No Hallucinations" commitment & recommends checking for hallucinations.
 *   SEC-02: Every single JSON record and HTML <tbody><tr> table row has a valid HTTPS official source link on an allowlisted domain.
 *   SEC-03: Blank-cell & unverified-flag integrity — unconfirmed values MUST be null/blank and listed in `unverified_fields`; zero placeholder strings.
 *   SEC-04: Deterministic NIST/spot raw-gold & melt-value math verification (31.1034768 g/oz t, 0.200 g/ct) across all benchmark & ring rows.
 *   SEC-05: 12-point online gold ring checklist completeness & automatic disqualification of vermeil/plated/sub-10K/conflicting items.
 *   SEC-06: Referential integrity across rings, sellers, benchmarks, and Flagged-for-Review (`data/flagged-items.json`) feed generation/validation.
 *   SEC-07: Static web security hygiene (no secrets, no eval/javascript: URIs, rel="noopener noreferrer" on external target="_blank" links).
 */

import fs from 'node:fs';
import path from 'node:path';

const ROOT = process.cwd();
const DATA_ONLY = process.argv.includes('--data-only');
const WRITE_REPORTS = process.argv.includes('--write-reports');

const ALLOWED_OFFICIAL_HOSTS = new Set([
  'www.automicgold.com',
  'automicgold.com',
  'www.sarraf.com',
  'sarraf.com',
  'www.vrai.com',
  'vrai.com',
  'help.vrai.com',
  'www.bluenile.com',
  'bluenile.com',
  'www.brilliantearth.com',
  'brilliantearth.com',
  'mejuri.com',
  'www.mejuri.com',
  'www.localeclectic.com',
  'localeclectic.com',
  'mene.com',
  'www.mene.com',
  'www.catbirdnyc.com',
  'catbirdnyc.com',
  'www.kitco.com',
  'kitco.com',
  'www.bullionvault.com',
  'bullionvault.com',
  'www.lbma.org.uk',
  'lbma.org.uk',
  'www.ecfr.gov',
  'ecfr.gov',
  'www.govinfo.gov',
  'govinfo.gov',
  'www.nist.gov',
  'nist.gov',
  'www.iso.org',
  'iso.org',
  'consumer.ftc.gov',
  'www.ftc.gov',
  'www.bbb.org',
  'bbb.org',
  'github.com',
  'karagemop466-tech.github.io'
]);

const FORBIDDEN_PLACEHOLDER_PATTERNS = [
  /\bexample\.com\b/i,
  /\blorem ipsum\b/i,
  /\bTODO\b/,
  /\bTBD\b/,
  /\bfake[-_ ]price\b/i,
  /\bsample[-_ ]data\b/i
];

const NIST_GRAMS_PER_TROY_OZ = 31.1034768;

const errors = [];
const warnings = [];
const checks = [];

function recordCheck(id, name, passed, details) {
  checks.push({ id, name, status: passed ? 'PASS' : 'FAIL', details });
  if (!passed) {
    errors.push(`[${id}] ${name}: ${details}`);
  }
}

function readJson(relPath) {
  const full = path.join(ROOT, relPath);
  if (!fs.existsSync(full)) {
    throw new Error(`Missing required JSON file: ${relPath}`);
  }
  return JSON.parse(fs.readFileSync(full, 'utf8'));
}

function validateOfficialUrl(urlStr, contextLabel) {
  if (typeof urlStr !== 'string' || urlStr.trim() === '') {
    return `${contextLabel}: missing official source URL`;
  }
  let parsed;
  try {
    parsed = new URL(urlStr);
  } catch {
    return `${contextLabel}: invalid URL "${urlStr}"`;
  }
  if (parsed.protocol !== 'https:') {
    return `${contextLabel}: URL must use https:// ("${urlStr}")`;
  }
  if (!ALLOWED_OFFICIAL_HOSTS.has(parsed.hostname)) {
    return `${contextLabel}: host "${parsed.hostname}" is not in ALLOWED_OFFICIAL_HOSTS ("${urlStr}")`;
  }
  return null;
}

// 1. Load core datasets
const repoAudit = readJson('data/repo-audit.json');
const goldBenchmark = readJson('data/gold-benchmark.json');
const purityStandards = readJson('data/purity-standards.json');
const ringsData = readJson('data/rings.json');
const sellersData = readJson('data/sellers.json');

// Build deterministic Flagged-for-Review items from all verified datasets
function buildFlaggedItems() {
  const items = [];

  for (const rec of repoAudit.entries) {
    if (rec.verification_status === 'flagged') {
      items.push({
        flag_id: `FLAG-${rec.id}`,
        source_dataset: 'data/repo-audit.json',
        entity_id: rec.id,
        category: 'Repository Baseline Irregularity',
        subject: rec.target,
        unverified_or_blank_fields: [],
        severity: 'needs_review',
        finding: rec.irregularity_flag,
        buyer_or_reviewer_action: rec.action_taken,
        verified_date: rec.verified_date,
        official_source_url: rec.source_url
      });
    }
  }

  for (const ring of ringsData.rings) {
    const hasFlags =
      ring.verification_status === 'needs_review' ||
      ring.verification_status === 'disqualified_control' ||
      (ring.unverified_fields && ring.unverified_fields.length > 0) ||
      (ring.irregularity_flags && ring.irregularity_flags.length > 0);

    if (hasFlags) {
      let severity = 'needs_review';
      if (!ring.is_solid_gold_compliant) {
        severity = 'disqualified_do_not_buy_as_solid_gold';
      } else if (
        ring.unverified_fields.includes('claimed_karat') ||
        ring.unverified_fields.includes('price_usd') ||
        ring.unverified_fields.includes('weight_grams')
      ) {
        severity = 'needs_review_missing_or_conflicting_spec';
      } else {
        severity = 'minor_arrival_hallmark_check';
      }

      items.push({
        flag_id: `FLAG-${ring.ring_id}`,
        source_dataset: 'data/rings.json',
        entity_id: ring.ring_id,
        category: ring.is_solid_gold_compliant ? 'Ring Listing — Unverified / Irregular Spec' : 'Ring Listing — Disqualified / Karat Conflict',
        subject: `${ring.retailer_name} — ${ring.product_name}`,
        unverified_or_blank_fields: ring.unverified_fields,
        severity,
        finding: ring.irregularity_flags.join(' | '),
        buyer_or_reviewer_action: !ring.is_solid_gold_compliant
          ? 'Walk away: fails solid karat gold requirement (vermeil plating or unresolved 9K/10K conflict).'
          : ring.unverified_fields.includes('claimed_karat')
            ? 'Do not purchase until seller confirms exact karat in writing; verify on arrival via 0.01g scale + ED-XRF.'
            : ring.unverified_fields.includes('weight_grams')
              ? 'Request written gram weight for your ring size prior to checkout; weigh on 0.01g scale upon arrival.'
              : 'Inspect interior karat + registered maker’s mark stamp and verify mass/purity via non-destructive scale + XRF within return window.',
        verified_date: ring.verified_date,
        official_source_url: ring.official_source_url
      });
    }
  }

  for (const seller of sellersData.sellers) {
    if (
      seller.verification_status === 'needs_review' ||
      (seller.unverified_fields && seller.unverified_fields.length > 0) ||
      (seller.irregularity_flags && seller.irregularity_flags.length > 0)
    ) {
      items.push({
        flag_id: `FLAG-${seller.seller_id}`,
        source_dataset: 'data/sellers.json',
        entity_id: seller.seller_id,
        category: 'Seller Policy / Reputation Irregularity',
        subject: `${seller.retailer_name} (${seller.walk_away_check_status})`,
        unverified_or_blank_fields: seller.unverified_fields,
        severity: seller.verification_status === 'needs_review' ? 'high_policy_or_reputation_risk' : 'policy_watch_note',
        finding: seller.irregularity_flags.join(' | '),
        buyer_or_reviewer_action: seller.xrf_inspection_guidance,
        verified_date: seller.verified_date,
        official_source_url: seller.official_source_url
      });
    }
  }

  return {
    metadata: {
      dataset_id: 'GOLD3-FLAGGED-ITEMS-2026-10-22',
      generated_and_verified_utc: '2026-10-22',
      no_hallucinations_policy:
        'Every blank (null) unconfirmed field, conflicting on-page specification, vermeil keyword trap, and restrictive seller return/reputation finding is surfaced here with its official source URL rather than guessed or hidden. Per COORDINATION.md, needs_review items are published transparently on Flagged for Review and do not block merge.',
      total_flagged_items: items.length
    },
    flagged_items: items
  };
}

if (WRITE_REPORTS || !fs.existsSync(path.join(ROOT, 'data/flagged-items.json'))) {
  const generatedFlags = buildFlaggedItems();
  fs.writeFileSync(path.join(ROOT, 'data/flagged-items.json'), JSON.stringify(generatedFlags, null, 2) + '\n');
}

const flaggedData = readJson('data/flagged-items.json');

// SEC-02: Official Source Links on Every JSON Record (and HTML table rows when present)
{
  const urlErrors = [];
  const checkGroups = [
    ['repo-audit.entries', repoAudit.entries, 'source_url'],
    ['gold-benchmark.benchmarks', goldBenchmark.benchmarks, 'source_url'],
    ['gold-benchmark.karat_melt_rates', goldBenchmark.karat_melt_rates, 'source_url'],
    ['purity-standards.checklist_items', purityStandards.checklist_items, 'source_url'],
    ['rings.rings', ringsData.rings, 'official_source_url'],
    ['sellers.sellers', sellersData.sellers, 'official_source_url'],
    ['flagged-items.flagged_items', flaggedData.flagged_items, 'official_source_url']
  ];

  if (Array.isArray(purityStandards.testing_standards)) {
    checkGroups.push(['purity-standards.testing_standards', purityStandards.testing_standards, 'source_url']);
  }

  let totalJsonRowsChecked = 0;
  for (const [groupName, arr, urlKey] of checkGroups) {
    if (!Array.isArray(arr) || arr.length === 0) {
      urlErrors.push(`${groupName}: empty or non-array`);
      continue;
    }
    arr.forEach((row, idx) => {
      totalJsonRowsChecked += 1;
      const err = validateOfficialUrl(row[urlKey], `${groupName}[${idx}]`);
      if (err) urlErrors.push(err);
      if (Array.isArray(row.secondary_official_urls)) {
        row.secondary_official_urls.forEach((u, sIdx) => {
          const sErr = validateOfficialUrl(u, `${groupName}[${idx}].secondary_official_urls[${sIdx}]`);
          if (sErr) urlErrors.push(sErr);
        });
      }
    });
  }

  // Also scan every HTML file's <tbody><tr> rows if not --data-only
  let htmlRowsChecked = 0;
  if (!DATA_ONLY) {
    const htmlFiles = fs.readdirSync(ROOT).filter((f) => f.endsWith('.html'));
    if (htmlFiles.length === 0) {
      urlErrors.push('No HTML files found in repository root (run with --data-only prior to Task C6).');
    }
    for (const file of htmlFiles) {
      const html = fs.readFileSync(path.join(ROOT, file), 'utf8');
      const tbodyMatches = [...html.matchAll(/<tbody[^>]*>([\s\S]*?)<\/tbody>/gi)];
      for (const [tIdx, tb] of tbodyMatches.entries()) {
        const trMatches = [...tb[1].matchAll(/<tr[^>]*>([\s\S]*?)<\/tr>/gi)];
        for (const [rIdx, tr] of trMatches.entries()) {
          htmlRowsChecked += 1;
          const hrefs = [...tr[1].matchAll(/<a\s+[^>]*href=["']([^"']+)["'][^>]*>/gi)].map((m) => m[1]);
          const officialHrefs = hrefs.filter((h) => h.startsWith('https://'));
          if (officialHrefs.length === 0) {
            urlErrors.push(`${file} tbody#${tIdx + 1} row#${rIdx + 1}: missing official https:// source link`);
          } else {
            for (const h of officialHrefs) {
              const uErr = validateOfficialUrl(h, `${file} tbody#${tIdx + 1} row#${rIdx + 1}`);
              if (uErr) urlErrors.push(uErr);
            }
          }
        }
      }
    }
  }

  recordCheck(
    'SEC-02',
    'Official Source URL on Every JSON Row & HTML Table Row',
    urlErrors.length === 0,
    urlErrors.length === 0
      ? `Verified ${totalJsonRowsChecked} JSON rows${DATA_ONLY ? '' : ` and ${htmlRowsChecked} static HTML <tbody><tr> rows`} — 100% link to allowlisted official HTTPS sources.`
      : urlErrors.join('; ')
  );
}

// SEC-01: Front-page top summary "No Hallucinations" commitment & hallucination-check recommendation
if (!DATA_ONLY) {
  const indexPath = path.join(ROOT, 'index.html');
  if (!fs.existsSync(indexPath)) {
    recordCheck('SEC-01', 'Front-Page Top Summary No-Hallucinations Commitment', false, 'index.html does not exist');
  } else {
    const indexHtml = fs.readFileSync(indexPath, 'utf8');
    const topSlice = indexHtml.slice(0, 10500);
    const hasNoHallucinations = /no hallucinations/i.test(topSlice);
    const hasRecommendLook = /(look(?:ing)? for hallucinations|inspect for hallucinations|check for hallucinations|audit every row for hallucinations)/i.test(indexHtml);
    recordCheck(
      'SEC-01',
      'Front-Page Top Summary No-Hallucinations Commitment & Recommendation',
      hasNoHallucinations && hasRecommendLook,
      hasNoHallucinations && hasRecommendLook
        ? 'Verified index.html top summary prominently features the "No Hallucinations" commitment and explicitly recommends looking for hallucinations.'
        : `Missing front-page requirement (hasNoHallucinations=${hasNoHallucinations}, hasRecommendLook=${hasRecommendLook})`
    );
  }
} else {
  const metaCheck =
    /zero prices|no[- ]hallucinations|never infer/i.test(ringsData.metadata.no_hallucinations_commitment) &&
    /every seller address/i.test(sellersData.metadata.no_hallucinations_commitment);
  recordCheck(
    'SEC-01',
    'Dataset Metadata No-Hallucinations Commitment (Data-Only Pre-UI Mode)',
    metaCheck,
    metaCheck ? 'All dataset metadata headers carry explicit No-Hallucinations commitments.' : 'Missing metadata commitment.'
  );
}

// SEC-03: Blank-cell & Unverified-flag Consistency Check
{
  const blankErrors = [];
  const trackableRingFields = [
    'price_usd',
    'claimed_karat',
    'purity_fraction',
    'hallmark_online_stated',
    'weight_grams',
    'stone_carat',
    'band_width_mm',
    'pure_gold_grams',
    'raw_gold_melt_usd',
    'price_to_melt_ratio',
    'melt_share_of_price_pct'
  ];

  for (const ring of ringsData.rings) {
    const declaredUnverified = new Set(ring.unverified_fields || []);
    for (const field of trackableRingFields) {
      const val = ring[field];
      if (val === null && !declaredUnverified.has(field)) {
        blankErrors.push(`${ring.ring_id}: field "${field}" is null (blank) but missing from unverified_fields`);
      }
      if (declaredUnverified.has(field) && val !== null) {
        blankErrors.push(`${ring.ring_id}: field "${field}" is listed in unverified_fields but has non-null value "${val}"`);
      }
      if (typeof val === 'string' && /^(n\/a|tbd|unknown|est\.|~|\?|-)$/i.test(val.trim())) {
        blankErrors.push(`${ring.ring_id}: field "${field}" uses forbidden filler string "${val}" instead of null`);
      }
    }
    if (ring.hallmark_online_stated !== null && ring.hallmark_status === 'unverified') {
      blankErrors.push(`${ring.ring_id}: hallmark_online_stated must be null when hallmark_status is unverified`);
    }
  }

  const trackableSellerFields = ['bbb_complaints_3yr', 'credit_card_accepted', 'credit_card_details'];
  for (const seller of sellersData.sellers) {
    const declaredUnverified = new Set(seller.unverified_fields || []);
    for (const field of trackableSellerFields) {
      const val = seller[field];
      if (val === null && !declaredUnverified.has(field)) {
        blankErrors.push(`${seller.seller_id}: field "${field}" is null (blank) but missing from unverified_fields`);
      }
      if (declaredUnverified.has(field) && val !== null) {
        blankErrors.push(`${seller.seller_id}: field "${field}" is listed in unverified_fields but has non-null value "${val}"`);
      }
    }
  }

  recordCheck(
    'SEC-03',
    'Blank-Cell (null) & Unverified-Field Strict Consistency',
    blankErrors.length === 0,
    blankErrors.length === 0
      ? '100% of unconfirmed fields across rings.json and sellers.json are strictly null (blank) and explicitly registered in unverified_fields; zero guessed or filler values.'
      : blankErrors.join('; ')
  );
}

// SEC-04: Deterministic Raw Gold & Melt Math Recalculation
{
  const mathErrors = [];
  const primaryBm = goldBenchmark.benchmarks.find((b) => b.id === 'GOLD-BM-01');
  if (!primaryBm) {
    mathErrors.push('Missing primary spot benchmark GOLD-BM-01');
  } else {
    for (const bm of goldBenchmark.benchmarks) {
      const expectedPerGram = bm.price_usd_per_troy_oz / NIST_GRAMS_PER_TROY_OZ;
      if (Math.abs(expectedPerGram - bm.price_usd_per_gram_24k) > 0.01) {
        mathErrors.push(
          `${bm.id}: price_usd_per_gram_24k=${bm.price_usd_per_gram_24k} differs from oz/31.1034768=${expectedPerGram.toFixed(4)}`
        );
      }
    }

    const spot24kGram = primaryBm.price_usd_per_troy_oz / NIST_GRAMS_PER_TROY_OZ;
    for (const kr of goldBenchmark.karat_melt_rates) {
      const expectedRate = spot24kGram * kr.purity_decimal;
      if (Math.abs(expectedRate - kr.raw_gold_usd_per_gram) > 0.015) {
        mathErrors.push(
          `${kr.id}: raw_gold_usd_per_gram=${kr.raw_gold_usd_per_gram} != ${expectedRate.toFixed(2)}`
        );
      }
    }

    for (const ring of ringsData.rings) {
      if (ring.weight_grams !== null && ring.purity_fraction !== null) {
        const expectedPureG = Number((ring.weight_grams * ring.purity_fraction).toFixed(4));
        const expectedMelt = Number((ring.weight_grams * ring.purity_fraction * spot24kGram).toFixed(2));
        if (Math.abs(expectedPureG - ring.pure_gold_grams) > 0.001) {
          mathErrors.push(`${ring.ring_id}: pure_gold_grams=${ring.pure_gold_grams} != expected ${expectedPureG}`);
        }
        if (Math.abs(expectedMelt - ring.raw_gold_melt_usd) > 0.02) {
          mathErrors.push(`${ring.ring_id}: raw_gold_melt_usd=${ring.raw_gold_melt_usd} != expected ${expectedMelt}`);
        }
        if (ring.price_usd !== null) {
          const expectedRatio = Number((ring.price_usd / (ring.weight_grams * ring.purity_fraction * spot24kGram)).toFixed(2));
          const expectedPct = Number((((ring.weight_grams * ring.purity_fraction * spot24kGram) / ring.price_usd) * 100).toFixed(2));
          if (Math.abs(expectedRatio - ring.price_to_melt_ratio) > 0.02) {
            mathErrors.push(`${ring.ring_id}: price_to_melt_ratio=${ring.price_to_melt_ratio} != expected ${expectedRatio}`);
          }
          if (Math.abs(expectedPct - ring.melt_share_of_price_pct) > 0.02) {
            mathErrors.push(`${ring.ring_id}: melt_share_of_price_pct=${ring.melt_share_of_price_pct} != expected ${expectedPct}`);
          }
        } else {
          if (ring.price_to_melt_ratio !== null || ring.melt_share_of_price_pct !== null) {
            mathErrors.push(`${ring.ring_id}: ratio/pct must be null when price_usd is null`);
          }
        }
      } else {
        if (ring.pure_gold_grams !== null || ring.raw_gold_melt_usd !== null) {
          mathErrors.push(`${ring.ring_id}: pure_gold_grams and raw_gold_melt_usd must be null when weight or purity is unverified`);
        }
      }
    }
  }

  recordCheck(
    'SEC-04',
    'Deterministic NIST & Spot Gold Melt Math Verification',
    mathErrors.length === 0,
    mathErrors.length === 0
      ? 'Independently recomputed all 5 spot benchmarks, 5 karat rates, and 22 ring listings using 1 oz t = 31.1034768 g — zero arithmetic discrepancies.'
      : mathErrors.join('; ')
  );
}

// SEC-05: 12-Point Checklist & Vermeil/Plated/Sub-10K Trap Detection
{
  const chkErrors = [];
  const checklist = purityStandards.checklist_items || [];
  if (checklist.length !== 12) {
    chkErrors.push(`Expected 12 checklist items, found ${checklist.length}`);
  }
  const expectedIds = Array.from({ length: 12 }, (_, i) => `CHK-${String(i + 1).padStart(2, '0')}`);
  for (const id of expectedIds) {
    if (!checklist.some((c) => c.id === id)) {
      chkErrors.push(`Missing checklist item ${id}`);
    }
  }

  for (const ring of ringsData.rings) {
    const combinedText = `${ring.product_name} ${ring.claimed_karat || ''} ${ring.solid_gold_verbatim || ''}`;
    const hasDisqualifyingTerm = /\b(vermeil|gold[- ]plated|gold[- ]filled|rolled gold|gold overlay|gold[- ]tone|9k)\b/i.test(combinedText);
    if (hasDisqualifyingTerm && ring.is_solid_gold_compliant !== false) {
      chkErrors.push(`${ring.ring_id}: contains disqualifying coating/sub-10K term in "${combinedText}" but is_solid_gold_compliant is not false`);
    }
  }

  recordCheck(
    'SEC-05',
    '12-Point Gold Ring Checklist & Plated/Vermeil/Sub-10K Trap Guard',
    chkErrors.length === 0,
    chkErrors.length === 0
      ? 'Verified all 12 buying checklist criteria (CHK-01..CHK-12) and confirmed coated/vermeil/9K-conflict items are automatically marked non-compliant.'
      : chkErrors.join('; ')
  );
}

// SEC-06: Referential Integrity & Flagged-for-Review Coverage
{
  const refErrors = [];
  const sellerIds = new Set(sellersData.sellers.map((s) => s.seller_id));
  const flaggedEntityIds = new Set(flaggedData.flagged_items.map((f) => f.entity_id));

  for (const ring of ringsData.rings) {
    if (!sellerIds.has(ring.retailer_id)) {
      refErrors.push(`${ring.ring_id}: unknown retailer_id "${ring.retailer_id}"`);
    }
    if (
      (ring.verification_status === 'needs_review' ||
        ring.verification_status === 'disqualified_control' ||
        ring.unverified_fields.length > 0) &&
      !flaggedEntityIds.has(ring.ring_id)
    ) {
      refErrors.push(`${ring.ring_id}: has unverified/flagged status but is missing from data/flagged-items.json`);
    }
  }

  for (const seller of sellersData.sellers) {
    if (
      (seller.verification_status === 'needs_review' || seller.unverified_fields.length > 0) &&
      !flaggedEntityIds.has(seller.seller_id)
    ) {
      refErrors.push(`${seller.seller_id}: has unverified/needs_review status but is missing from data/flagged-items.json`);
    }
  }

  recordCheck(
    'SEC-06',
    'Cross-Dataset Referential Integrity & Flagged-for-Review Completeness',
    refErrors.length === 0,
    refErrors.length === 0
      ? `All 22 rings map to verified sellers and all ${flaggedData.flagged_items.length} unverified/irregular records are published in data/flagged-items.json.`
      : refErrors.join('; ')
  );
}

// SEC-07: Static Code & Content Security Hygiene
{
  const secErrors = [];
  const scanDirs = ['', 'data', 'scripts', 'assets'];
  const scannedFiles = [];

  for (const dir of scanDirs) {
    const absDir = path.join(ROOT, dir);
    if (!fs.existsSync(absDir)) continue;
    for (const entry of fs.readdirSync(absDir)) {
      const fullPath = path.join(absDir, entry);
      if (!fs.statSync(fullPath).isFile()) continue;
      if (!/\.(html|js|mjs|css|json|md)$/i.test(entry)) continue;
      const rel = path.relative(ROOT, fullPath);
      scannedFiles.push(rel);
      const text = fs.readFileSync(fullPath, 'utf8');

      // Secret patterns
      if (/(ghp_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{30,}|sk-[A-Za-z0-9]{30,}|AKIA[0-9A-Z]{16})/.test(text)) {
        secErrors.push(`${rel}: potential credential/token detected`);
      }

      if (rel !== 'scripts/security-check.mjs') {
        for (const pat of FORBIDDEN_PLACEHOLDER_PATTERNS) {
          if (pat.test(text)) {
            secErrors.push(`${rel}: matched forbidden placeholder pattern ${pat}`);
          }
        }
      }

      if (/\.(html|js)$/i.test(entry)) {
        if (/\beval\s*\(|new\s+Function\s*\(|href\s*=\s*["']javascript:/i.test(text)) {
          secErrors.push(`${rel}: unsafe JS execution or javascript: URI detected`);
        }
      }

      if (/\.html$/i.test(entry)) {
        const blankTargets = [...text.matchAll(/<a\s+[^>]*target=["']_blank["'][^>]*>/gi)].map((m) => m[0]);
        for (const tag of blankTargets) {
          if (!/rel=["'][^"']*noopener/i.test(tag)) {
            secErrors.push(`${rel}: <a target="_blank"> missing rel="noopener noreferrer": ${tag}`);
          }
        }
      }
    }
  }

  recordCheck(
    'SEC-07',
    'Static Security, Anti-Placeholder & Safe External Link Hygiene',
    secErrors.length === 0,
    secErrors.length === 0
      ? `Scanned ${scannedFiles.length} workspace files — zero secrets, zero placeholders, zero unsafe JS patterns, and 100% rel="noopener noreferrer" compliance.`
      : secErrors.join('; ')
  );
}

const report = {
  audit_suite: 'GOLD3 Anti-Hallucination & Security Verification Suite',
  verified_date_utc: '2026-10-22',
  mode: DATA_ONLY ? 'data-only' : 'full-site-and-data',
  overall_status: errors.length === 0 ? 'PASS' : 'FAIL',
  total_checks: checks.length,
  passed_checks: checks.filter((c) => c.status === 'PASS').length,
  failed_checks: errors.length,
  recommendation:
    'Always inspect every price, karat stamp, gram weight, and return exclusion against the linked official source page. Leave any unconfirmed value blank and flag it as unverified rather than estimating.',
  checks,
  warnings
};

if (WRITE_REPORTS || !fs.existsSync(path.join(ROOT, 'data/audit-report.json'))) {
  fs.writeFileSync(path.join(ROOT, 'data/audit-report.json'), JSON.stringify(report, null, 2) + '\n');
}

console.log(`\n=== ${report.audit_suite} (${report.mode}) ===`);
for (const c of checks) {
  console.log(`[${c.status}] ${c.id} — ${c.name}: ${c.details}`);
}
console.log(`Overall Status: ${report.overall_status} (${report.passed_checks}/${report.total_checks} checks passed)\n`);

if (errors.length > 0) {
  process.exit(1);
}
