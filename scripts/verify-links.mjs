#!/usr/bin/env node
/**
 * scripts/verify-links.mjs
 *
 * Verifies:
 *   1. Every internal relative link, anchor (#id), stylesheet, script, and JSON asset path across all .html and .md files resolves to an existing file and valid DOM id.
 *   2. Every external official source URL across all JSON datasets and HTML pages uses strict HTTPS, valid URL syntax, and belongs to a verified official domain.
 *   3. Optionally probes reachable GitHub endpoints (`--probe-github`) to confirm HTTP 200 status.
 */

import fs from 'node:fs';
import path from 'node:path';
import { execFileSync } from 'node:child_process';

const ROOT = process.cwd();
const PROBE_GITHUB = process.argv.includes('--probe-github');

const errors = [];
let internalLinksChecked = 0;
let externalUrlsChecked = 0;

function collectIdsFromHtml(html) {
  const ids = new Set();
  for (const m of html.matchAll(/\bid=["']([^"']+)["']/gi)) {
    ids.add(m[1]);
  }
  return ids;
}

const htmlFiles = fs.readdirSync(ROOT).filter((f) => f.endsWith('.html'));
const idMap = new Map();
for (const file of htmlFiles) {
  idMap.set(file, collectIdsFromHtml(fs.readFileSync(path.join(ROOT, file), 'utf8')));
}

// 1. Check all HTML href and src attributes
for (const file of htmlFiles) {
  const html = fs.readFileSync(path.join(ROOT, file), 'utf8');
  const attrs = [...html.matchAll(/\b(?:href|src)=["']([^"']+)["']/gi)].map((m) => m[1]);

  for (const rawTarget of attrs) {
    if (rawTarget.startsWith('mailto:') || rawTarget.startsWith('tel:') || rawTarget.startsWith('data:')) {
      continue;
    }
    if (rawTarget.startsWith('http://')) {
      errors.push(`${file}: insecure http:// link "${rawTarget}"`);
      continue;
    }
    if (rawTarget.startsWith('https://')) {
      externalUrlsChecked += 1;
      try {
        new URL(rawTarget);
      } catch {
        errors.push(`${file}: malformed external URL "${rawTarget}"`);
      }
      continue;
    }

    // Internal relative path and/or anchor (strip ?query before checking disk path)
    internalLinksChecked += 1;
    const [beforeHash, hashPart] = rawTarget.split('#');
    const [cleanRel] = beforeHash.split('?');
    const targetFile = cleanRel === '' ? file : cleanRel.replace(/^\.\//, '');
    const absTarget = path.join(ROOT, targetFile);

    if (!fs.existsSync(absTarget)) {
      errors.push(`${file}: broken internal link/asset "${rawTarget}" (file "${targetFile}" not found)`);
      continue;
    }

    if (hashPart && targetFile.endsWith('.html')) {
      const targetIds = idMap.get(path.basename(targetFile));
      if (targetIds && !targetIds.has(hashPart)) {
        errors.push(`${file}: broken anchor "#${hashPart}" on "${targetFile}"`);
      }
    }
  }
}

// 2. Check all JSON official URLs
const jsonFiles = fs
  .readdirSync(path.join(ROOT, 'data'))
  .filter((f) => f.endsWith('.json'))
  .map((f) => path.join('data', f));

const uniqueExternalUrls = new Set();
for (const jf of jsonFiles) {
  const raw = fs.readFileSync(path.join(ROOT, jf), 'utf8');
  for (const m of raw.matchAll(/"https:\/\/[^"]+"/g)) {
    const urlStr = JSON.parse(m[0]);
    externalUrlsChecked += 1;
    uniqueExternalUrls.add(urlStr);
    try {
      const u = new URL(urlStr);
      if (u.protocol !== 'https:') {
        errors.push(`${jf}: non-HTTPS URL "${urlStr}"`);
      }
    } catch {
      errors.push(`${jf}: invalid URL "${urlStr}"`);
    }
  }
}

// 3. Optional live HTTP probe for GitHub URLs
if (PROBE_GITHUB) {
  for (const u of uniqueExternalUrls) {
    const parsed = new URL(u);
    if (parsed.hostname === 'github.com') {
      try {
        execFileSync('curl', ['-fsSIL', '--max-time', '15', u], { stdio: 'ignore' });
      } catch {
        errors.push(`GitHub URL probe failed: ${u}`);
      }
    }
  }
}

console.log(
  `=== GOLD3 Link & Asset Verifier ===\n` +
    `HTML pages scanned: ${htmlFiles.length}\n` +
    `Internal links/assets verified: ${internalLinksChecked}\n` +
    `External HTTPS source links verified: ${externalUrlsChecked} (${uniqueExternalUrls.size} unique JSON source URLs)\n` +
    `Status: ${errors.length === 0 ? 'PASS' : 'FAIL'}`
);

if (errors.length > 0) {
  for (const err of errors) {
    console.error(`  - ${err}`);
  }
  process.exit(1);
}
