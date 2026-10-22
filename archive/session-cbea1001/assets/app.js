/* assets/app.js — Interactive Gold Weight & Raw Melt Calculator, Ring Filter & 12-Point Checklist */
(function () {
  'use strict';

  const NIST_GRAMS_PER_TROY_OZ = 31.1034768;
  const NIST_GRAMS_PER_DWT = 1.55517384;
  const NIST_GRAMS_PER_CARAT = 0.2;

  function formatUsd(val) {
    if (!Number.isFinite(val)) return '—';
    return '$' + val.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
  }

  function formatGrams(val, digits = 3) {
    if (!Number.isFinite(val)) return '—';
    return val.toFixed(digits) + ' g';
  }

  // ---------------------------------------------------------------------------
  // 1. Gold Weight, Purity, Melt Value & Post-Arrival XRF Calculator
  // ---------------------------------------------------------------------------
  function initCalculator() {
    const form = document.getElementById('gold-calc-form');
    if (!form) return;

    const presetSelect = document.getElementById('calc-ring-preset');
    const benchmarkSelect = document.getElementById('calc-benchmark');
    const spotOzInput = document.getElementById('calc-spot-oz');
    const karatSelect = document.getElementById('calc-karat');
    const weightInput = document.getElementById('calc-weight');
    const weightUnitSelect = document.getElementById('calc-weight-unit');
    const stoneCaratInput = document.getElementById('calc-stone-ct');
    const priceInput = document.getElementById('calc-price');
    const arrivalWeightInput = document.getElementById('calc-arrival-weight');
    const arrivalXrfInput = document.getElementById('calc-arrival-xrf');
    const hasSolderSelect = document.getElementById('calc-solder');

    const presets = window.GOLD3_RING_PRESETS || [];

    function applyPreset(ringId) {
      const item = presets.find((r) => r.ring_id === ringId);
      if (!item) return;

      if (spotOzInput && benchmarkSelect) {
        benchmarkSelect.value = '4025.10';
        spotOzInput.value = '4025.10';
      }
      if (karatSelect && item.purity_fraction !== null) {
        karatSelect.value = String(item.purity_fraction);
      }
      if (weightUnitSelect) {
        weightUnitSelect.value = 'g';
      }
      if (weightInput) {
        weightInput.value = item.weight_grams !== null ? String(item.weight_grams) : '';
      }
      if (stoneCaratInput) {
        // Note: Automic & Sarraf publish metal weight directly; set stone deduction to 0 by default on metal-weight presets
        stoneCaratInput.value = '0';
      }
      if (priceInput) {
        priceInput.value = item.price_usd !== null ? String(item.price_usd) : '';
      }
      if (arrivalWeightInput) arrivalWeightInput.value = '';
      if (arrivalXrfInput) arrivalXrfInput.value = '';
      recalculate();
    }

    if (benchmarkSelect && spotOzInput) {
      benchmarkSelect.addEventListener('change', function () {
        if (benchmarkSelect.value !== 'custom') {
          spotOzInput.value = benchmarkSelect.value;
        }
        recalculate();
      });
      spotOzInput.addEventListener('input', function () {
        benchmarkSelect.value = 'custom';
        recalculate();
      });
    }

    if (presetSelect) {
      presetSelect.addEventListener('change', function () {
        if (presetSelect.value) {
          applyPreset(presetSelect.value);
        }
      });
    }

    function recalculate() {
      const spotOz = parseFloat(spotOzInput ? spotOzInput.value : '4025.10');
      const purity = parseFloat(karatSelect ? karatSelect.value : '0.583333');
      const rawWeight = parseFloat(weightInput ? weightInput.value : '');
      const unit = weightUnitSelect ? weightUnitSelect.value : 'g';
      const stoneCt = parseFloat(stoneCaratInput ? stoneCaratInput.value : '0') || 0;
      const askPrice = parseFloat(priceInput ? priceInput.value : '');

      const spot24kGram = Number.isFinite(spotOz) && spotOz > 0 ? spotOz / NIST_GRAMS_PER_TROY_OZ : NaN;
      const alloyRatePerGram = Number.isFinite(spot24kGram) && Number.isFinite(purity) ? spot24kGram * purity : NaN;

      let grossGrams = NaN;
      if (Number.isFinite(rawWeight) && rawWeight >= 0) {
        if (unit === 'g') grossGrams = rawWeight;
        else if (unit === 'dwt') grossGrams = rawWeight * NIST_GRAMS_PER_DWT;
        else if (unit === 'ozt') grossGrams = rawWeight * NIST_GRAMS_PER_TROY_OZ;
      }

      const stoneGrams = Math.max(0, stoneCt) * NIST_GRAMS_PER_CARAT;
      const netGoldAlloyGrams = Number.isFinite(grossGrams) ? Math.max(0, grossGrams - stoneGrams) : NaN;
      const pureGoldGrams = Number.isFinite(netGoldAlloyGrams) && Number.isFinite(purity) ? netGoldAlloyGrams * purity : NaN;
      const pureGoldTroyOz = Number.isFinite(pureGoldGrams) ? pureGoldGrams / NIST_GRAMS_PER_TROY_OZ : NaN;
      const meltUsd = Number.isFinite(pureGoldGrams) && Number.isFinite(spot24kGram) ? pureGoldGrams * spot24kGram : NaN;

      const hasPrice = Number.isFinite(askPrice) && askPrice > 0;
      const markupUsd = hasPrice && Number.isFinite(meltUsd) ? askPrice - meltUsd : NaN;
      const ratioMultiple = hasPrice && Number.isFinite(meltUsd) && meltUsd > 0 ? askPrice / meltUsd : NaN;
      const meltSharePct = hasPrice && Number.isFinite(meltUsd) ? (meltUsd / askPrice) * 100 : NaN;

      const setOut = (id, text) => {
        const el = document.getElementById(id);
        if (el) el.textContent = text;
      };

      setOut('out-spot-gram', Number.isFinite(spot24kGram) ? formatUsd(spot24kGram) + ' / g' : '—');
      setOut('out-alloy-gram', Number.isFinite(alloyRatePerGram) ? formatUsd(alloyRatePerGram) + ' / g' : '—');
      setOut('out-net-alloy-g', Number.isFinite(netGoldAlloyGrams) ? formatGrams(netGoldAlloyGrams, 2) : 'Unverified (enter g)');
      setOut(
        'out-pure-gold-g',
        Number.isFinite(pureGoldGrams)
          ? pureGoldGrams.toFixed(4) + ' g (' + pureGoldTroyOz.toFixed(4) + ' oz t)'
          : 'Unverified'
      );
      setOut('out-melt-usd', Number.isFinite(meltUsd) ? formatUsd(meltUsd) : 'Unverified');
      setOut('out-markup-usd', Number.isFinite(markupUsd) ? formatUsd(markupUsd) : 'Enter retail price');
      setOut('out-ratio', Number.isFinite(ratioMultiple) ? ratioMultiple.toFixed(2) + 'x melt' : '—');
      setOut('out-melt-share', Number.isFinite(meltSharePct) ? meltSharePct.toFixed(2) + '% of price' : '—');

      // Update live Karat Reference Matrix on calculator.html if present
      const matrixRows = document.querySelectorAll('[data-karat-rate-row]');
      matrixRows.forEach((row) => {
        const rowPurity = parseFloat(row.getAttribute('data-purity'));
        const rateCell = row.querySelector('[data-cell="rate"]');
        const sampleMeltCell = row.querySelector('[data-cell="sample-melt"]');
        if (rateCell && Number.isFinite(spot24kGram)) {
          rateCell.textContent = formatUsd(spot24kGram * rowPurity) + '/g';
        }
        if (sampleMeltCell) {
          if (Number.isFinite(netGoldAlloyGrams) && Number.isFinite(spot24kGram)) {
            sampleMeltCell.textContent = formatUsd(netGoldAlloyGrams * rowPurity * spot24kGram);
          } else {
            sampleMeltCell.textContent = 'Enter weight';
          }
        }
      });

      // Verdict Banner
      const verdictEl = document.getElementById('calc-verdict-banner');
      if (verdictEl) {
        if (!Number.isFinite(netGoldAlloyGrams) || netGoldAlloyGrams <= 0) {
          verdictEl.className = 'verdict-banner verdict-warn';
          verdictEl.textContent =
            'Checklist CHK-04 Alert: Gram weight is blank/unverified. Never guess ring weight — request exact gram weight for your ring size in writing from the seller before paying.';
        } else if (purity < 0.416) {
          verdictEl.className = 'verdict-banner verdict-fail';
          verdictEl.textContent =
            'Checklist CHK-01 / 16 CFR § 23.3 Warning: Selected alloy is below the 10K (41.67% Au) US karat-gold standard. Walk away from unqualified sub-10K rings.';
        } else if (Number.isFinite(ratioMultiple)) {
          if (ratioMultiple < 1.0) {
            verdictEl.className = 'verdict-banner verdict-fail';
            verdictEl.textContent =
              'CRITICAL COUNTERFEIT / PLATING RED FLAG: Asking price (' +
              formatUsd(askPrice) +
              ') is BELOW raw gold melt value (' +
              formatUsd(meltUsd) +
              '). Legitimate jewelers do not sell new rings below scrap gold melt — high risk of gold-plated brass/silver or hollow core.';
          } else if (ratioMultiple <= 4.5) {
            verdictEl.className = 'verdict-banner verdict-pass';
            verdictEl.textContent =
              'Strong Intrinsic Gold Value: Raw gold melt accounts for ' +
              meltSharePct.toFixed(1) +
              '% of retail price (' +
              ratioMultiple.toFixed(2) +
              'x melt). Still perform post-arrival 0.01g scale + ED-XRF check within return window.';
          } else {
            verdictEl.className = 'verdict-banner verdict-warn';
            verdictEl.textContent =
              'High Design / Gemstone / Brand Markup (' +
              ratioMultiple.toFixed(2) +
              'x raw gold melt; gold is ' +
              meltSharePct.toFixed(1) +
              '% of price). Verify center diamond grading report, solid shank mass, and return policy before purchase.';
          }
        } else {
          verdictEl.className = 'verdict-banner verdict-pass';
          verdictEl.textContent =
            'Raw Gold Melt Value computed: ' +
            formatUsd(meltUsd) +
            ' (' +
            pureGoldGrams.toFixed(3) +
            ' g fine 24K gold). Enter an asking price to evaluate retail markup multiple.';
        }
      }

      // Post-Arrival Scale & XRF Assay Verification (CHK-10 & CHK-11)
      const xrfVerdictEl = document.getElementById('xrf-assay-verdict');
      if (xrfVerdictEl && (arrivalWeightInput || arrivalXrfInput)) {
        const measuredW = parseFloat(arrivalWeightInput ? arrivalWeightInput.value : '');
        const measuredXrfPct = parseFloat(arrivalXrfInput ? arrivalXrfInput.value : '');
        const withSolder = hasSolderSelect ? hasSolderSelect.value === 'yes' : true;
        const toleranceParts = withSolder ? 0.007 : 0.003; // 15 U.S.C. § 295: 7‰ with solder, 3‰ without solder
        const minLegalPct = Math.max(0, (purity - toleranceParts) * 100);

        if (!Number.isFinite(measuredW) && !Number.isFinite(measuredXrfPct)) {
          xrfVerdictEl.className = 'verdict-banner verdict-warn';
          xrfVerdictEl.textContent =
            'Post-Arrival Verification (CHK-10 & CHK-11): Enter independent jeweler 0.01g scale reading and non-destructive ED-XRF Au% reading upon delivery. Legal minimum under 15 U.S.C. § 295 is ' +
            minLegalPct.toFixed(2) +
            '% Au (' +
            (withSolder ? '7‰ solder tolerance' : '3‰ no-solder tolerance') +
            ').';
        } else {
          const issues = [];
          if (Number.isFinite(measuredW) && Number.isFinite(grossGrams) && grossGrams > 0) {
            const diffG = measuredW - grossGrams;
            const diffPct = (Math.abs(diffG) / grossGrams) * 100;
            if (diffG < -0.25 && diffPct > 6) {
              issues.push(
                'Scale shortfall: measured ' +
                  measuredW.toFixed(2) +
                  'g vs stated ' +
                  grossGrams.toFixed(2) +
                  'g (' +
                  diffG.toFixed(2) +
                  'g lighter — check for hollowing or wrong ring size).'
              );
            }
          }
          if (Number.isFinite(measuredXrfPct)) {
            if (measuredXrfPct < minLegalPct) {
              issues.push(
                'XRF FAIL vs 15 U.S.C. § 295: measured ' +
                  measuredXrfPct.toFixed(2) +
                  '% Au is below legal minimum ' +
                  minLegalPct.toFixed(2) +
                  '% Au for claimed karat!'
              );
            }
          }
          if (issues.length > 0) {
            xrfVerdictEl.className = 'verdict-banner verdict-fail';
            xrfVerdictEl.textContent =
              'RETURN IMMEDIATELY / CREDIT CARD DISPUTE ALERT: ' +
              issues.join(' ') +
              ' Keep tags intact, photograph scale & XRF printout, and initiate return within window.';
          } else {
            xrfVerdictEl.className = 'verdict-banner verdict-pass';
            xrfVerdictEl.textContent =
              'POST-ARRIVAL ASSAY PASS: Measured reading meets 15 U.S.C. § 295 statutory fineness floor (>=' +
              minLegalPct.toFixed(2) +
              '% Au) and expected mass tolerance. Retain jeweler receipt & XRF report (CHK-09).';
          }
        }
      }
    }

    form.querySelectorAll('input, select').forEach((el) => {
      el.addEventListener('input', recalculate);
      el.addEventListener('change', recalculate);
    });

    // Check URL query ?ring=RING-XX
    const params = new URLSearchParams(window.location.search);
    const requestedRing = params.get('ring');
    if (requestedRing && presetSelect) {
      presetSelect.value = requestedRing;
      applyPreset(requestedRing);
    } else {
      recalculate();
    }
  }

  // ---------------------------------------------------------------------------
  // 2. Ring Listings Table Filter & Sort (rings.html)
  // ---------------------------------------------------------------------------
  function initRingTableFilters() {
    const table = document.getElementById('rings-master-table');
    if (!table) return;

    const searchInput = document.getElementById('ring-search');
    const karatFilter = document.getElementById('ring-karat-filter');
    const statusFilter = document.getElementById('ring-status-filter');
    const sortSelect = document.getElementById('ring-sort');
    const countBadge = document.getElementById('ring-visible-count');
    const tbody = table.querySelector('tbody');
    const rows = Array.from(tbody.querySelectorAll('tr'));

    function updateTable() {
      const q = (searchInput ? searchInput.value : '').trim().toLowerCase();
      const karat = karatFilter ? karatFilter.value : 'ALL';
      const status = statusFilter ? statusFilter.value : 'ALL';
      const sortBy = sortSelect ? sortSelect.value : 'default';

      let visibleCount = 0;
      rows.forEach((tr) => {
        const rowText = tr.textContent.toLowerCase();
        const rowKarat = tr.getAttribute('data-karat') || 'UNVERIFIED';
        const isCompliant = tr.getAttribute('data-compliant') === 'true';
        const hasWeight = tr.getAttribute('data-has-weight') === 'true';

        let show = true;
        if (q && !rowText.includes(q)) show = false;
        if (karat !== 'ALL' && rowKarat !== karat) show = false;
        if (status === 'COMPLIANT_SOLID' && !isCompliant) show = false;
        if (status === 'VERIFIED_WEIGHT' && (!isCompliant || !hasWeight)) show = false;
        if (status === 'MISSING_WEIGHT' && hasWeight) show = false;
        if (status === 'DISQUALIFIED' && isCompliant) show = false;

        tr.style.display = show ? '' : 'none';
        if (show) visibleCount += 1;
      });

      const sortedRows = [...rows].sort((a, b) => {
        if (sortBy === 'default') {
          return parseInt(a.getAttribute('data-index'), 10) - parseInt(b.getAttribute('data-index'), 10);
        }
        const numAttr = (el, attr, fallback) => {
          const v = parseFloat(el.getAttribute(attr));
          return Number.isFinite(v) ? v : fallback;
        };
        if (sortBy === 'price-asc') return numAttr(a, 'data-price', 1e12) - numAttr(b, 'data-price', 1e12);
        if (sortBy === 'price-desc') return numAttr(b, 'data-price', -1) - numAttr(a, 'data-price', -1);
        if (sortBy === 'weight-desc') return numAttr(b, 'data-weight', -1) - numAttr(a, 'data-weight', -1);
        if (sortBy === 'melt-desc') return numAttr(b, 'data-melt', -1) - numAttr(a, 'data-melt', -1);
        if (sortBy === 'ratio-asc') return numAttr(a, 'data-ratio', 1e12) - numAttr(b, 'data-ratio', 1e12);
        return 0;
      });

      sortedRows.forEach((r) => tbody.appendChild(r));
      if (countBadge) {
        countBadge.textContent = visibleCount + ' of ' + rows.length + ' verified rows shown';
      }
    }

    [searchInput, karatFilter, statusFilter, sortSelect].forEach((el) => {
      if (el) {
        el.addEventListener('input', updateTable);
        el.addEventListener('change', updateTable);
      }
    });
  }

  // ---------------------------------------------------------------------------
  // 3. Flagged-for-Review Filter (flagged.html)
  // ---------------------------------------------------------------------------
  function initFlaggedFilters() {
    const table = document.getElementById('flagged-master-table');
    if (!table) return;

    const searchInput = document.getElementById('flag-search');
    const sevSelect = document.getElementById('flag-severity');
    const dsSelect = document.getElementById('flag-dataset');
    const countEl = document.getElementById('flag-visible-count');
    const rows = Array.from(table.querySelectorAll('tbody tr'));

    function applyFilter() {
      const q = (searchInput ? searchInput.value : '').trim().toLowerCase();
      const sev = sevSelect ? sevSelect.value : 'ALL';
      const ds = dsSelect ? dsSelect.value : 'ALL';
      let shown = 0;

      rows.forEach((tr) => {
        const text = tr.textContent.toLowerCase();
        const rSev = tr.getAttribute('data-severity') || '';
        const rDs = tr.getAttribute('data-dataset') || '';
        let ok = true;
        if (q && !text.includes(q)) ok = false;
        if (sev !== 'ALL' && rSev !== sev) ok = false;
        if (ds !== 'ALL' && rDs !== ds) ok = false;
        tr.style.display = ok ? '' : 'none';
        if (ok) shown += 1;
      });

      if (countEl) {
        countEl.textContent = shown + ' of ' + rows.length + ' flagged items shown';
      }
    }

    [searchInput, sevSelect, dsSelect].forEach((el) => {
      if (el) {
        el.addEventListener('input', applyFilter);
        el.addEventListener('change', applyFilter);
      }
    });
  }

  // ---------------------------------------------------------------------------
  // 4. Interactive 12-Point Buying Checklist Scorecard (checklist.html)
  // ---------------------------------------------------------------------------
  function initChecklistScorecard() {
    const container = document.getElementById('interactive-checklist-box');
    if (!container) return;

    const checkboxes = Array.from(container.querySelectorAll('input[type="checkbox"][data-chk-id]'));
    const statusEl = document.getElementById('checklist-score-banner');
    const resetBtn = document.getElementById('checklist-reset-btn');
    const STORAGE_KEY = 'gold3_buyer_checklist_v1';

    let saved = {};
    try {
      saved = JSON.parse(localStorage.getItem(STORAGE_KEY) || '{}');
    } catch {
      saved = {};
    }

    checkboxes.forEach((cb) => {
      const id = cb.getAttribute('data-chk-id');
      if (saved[id]) cb.checked = true;
      cb.addEventListener('change', () => {
        saved[id] = cb.checked;
        try {
          localStorage.setItem(STORAGE_KEY, JSON.stringify(saved));
        } catch {
          // ignore storage quota errors
        }
        renderScore();
      });
    });

    if (resetBtn) {
      resetBtn.addEventListener('click', () => {
        saved = {};
        checkboxes.forEach((cb) => {
          cb.checked = false;
        });
        try {
          localStorage.removeItem(STORAGE_KEY);
        } catch {
          // ignore
        }
        renderScore();
      });
    }

    function renderScore() {
      const checkedCount = checkboxes.filter((c) => c.checked).length;
      if (!statusEl) return;
      if (checkedCount === checkboxes.length) {
        statusEl.className = 'verdict-banner verdict-pass';
        statusEl.style.color = '#0b5d3f';
        statusEl.style.background = '#e7f6ef';
        statusEl.textContent =
          '12 / 12 Checklist Points Verified: Safe to retain ring! Store your screenshot, invoice, scale photo, and XRF printout permanently.';
      } else {
        statusEl.className = 'callout-box';
        statusEl.textContent =
          checkedCount +
          ' of ' +
          checkboxes.length +
          ' checklist items verified. Walk away immediately (CHK-12) if the seller refuses written gram weight/karat confirmation, blocks returns, or discourages independent XRF testing.';
      }
    }

    renderScore();
  }

  document.addEventListener('DOMContentLoaded', function () {
    initCalculator();
    initRingTableFilters();
    initFlaggedFilters();
    initChecklistScorecard();
  });
})();
