(() => {
  'use strict';

  const root = document.body.dataset.root || '.';
  const dataUrl = (name) => new URL(`${root}/data/${name}`, window.location.href).toString();
  const page = document.body.dataset.page || '';

  const readJson = async (name) => {
    const response = await fetch(dataUrl(name), { cache: 'no-cache' });
    if (!response.ok) throw new Error(`Unable to load ${name} (${response.status})`);
    return response.json();
  };

  const element = (tag, text, className) => {
    const node = document.createElement(tag);
    if (text !== undefined && text !== null) node.textContent = String(text);
    if (className) node.className = className;
    return node;
  };

  const setText = (selector, value) => {
    const node = document.querySelector(selector);
    if (node) node.textContent = value;
  };

  const linkFor = (url, label, className = 'source-link') => {
    const link = element('a', label, className);
    try {
      const parsed = new URL(url);
      if (parsed.protocol !== 'https:') throw new Error('HTTPS required');
      link.href = parsed.toString();
      link.target = '_blank';
      link.rel = 'noopener noreferrer';
      link.referrerPolicy = 'no-referrer';
    } catch {
      link.removeAttribute('href');
      link.setAttribute('aria-disabled', 'true');
      link.classList.add('cell-muted');
    }
    return link;
  };

  const sourceIndex = (data) => new Map((data.sources || []).map((source) => [source.id, source]));

  function appendSources(container, sourceIds, sources) {
    container.replaceChildren();
    const stack = element('div', null, 'source-stack');
    for (const id of sourceIds || []) {
      const source = sources.get(id);
      if (source) stack.append(linkFor(source.url, source.title));
    }
    if (!stack.childElementCount) stack.append(element('span', 'No source link recorded', 'cell-muted'));
    container.append(stack);
  }

  function statusPill(text, type = 'unverified') {
    const classByType = {
      unverified: 'status-unverified',
      review: 'status-review',
      pass: 'status-pass',
      neutral: 'status-neutral'
    };
    return element('span', text, `status-pill ${classByType[type] || classByType.neutral}`);
  }

  const formatUSD = (amount, currency = 'USD') => {
    if (!Number.isFinite(amount)) return '—';
    return new Intl.NumberFormat('en-US', { style: 'currency', currency, minimumFractionDigits: 0, maximumFractionDigits: 2 }).format(amount);
  };

  const formatDate = (dateString) => {
    const date = new Date(`${dateString}T00:00:00Z`);
    if (Number.isNaN(date.getTime())) return dateString || '—';
    return new Intl.DateTimeFormat('en-US', { year: 'numeric', month: 'short', day: 'numeric', timeZone: 'UTC' }).format(date);
  };

  function renderFullCandidates(tbody, candidates, sources) {
    tbody.replaceChildren();
    for (const candidate of candidates) {
      const row = document.createElement('tr');

      const productCell = element('td');
      const productAnchor = linkFor(candidate.productUrl, candidate.name, 'product-name');
      productCell.append(productAnchor);
      productCell.append(element('span', `${candidate.category} · Stock Number ${candidate.stockNumber}`, 'product-sub'));
      productCell.append(element('span', candidate.listingStatus.value, 'product-sub'));

      const metalCell = element('td');
      metalCell.append(element('strong', candidate.metal.sellerDescription.value));
      metalCell.append(element('span', 'Seller-page claim; actual alloy not independently tested.', 'product-sub'));

      const solidCell = element('td', null, 'cell-small');
      const solidField = candidate.metal.explicitSolidGoldStatement;
      const platingField = candidate.metal.platingExcluded;
      solidCell.append(statusPill(solidField?.value ? 'Explicit wording found' : 'Not stated', solidField?.status === 'verified' ? 'pass' : 'unverified'));
      const platingText = platingField?.value === true
        ? 'Seller says no plating/coating.'
        : (platingField?.value === false ? 'Seller identifies coating.' : 'Plating/coating not ruled out.');
      solidCell.append(element('span', platingText, 'product-sub'));

      const weightCell = element('td', null, 'cell-small');
      weightCell.append(statusPill('Not stated', 'unverified'));
      weightCell.append(element('span', 'Gold-only grams: —', 'product-sub'));

      const marksCell = element('td', null, 'cell-small');
      marksCell.append(element('span', 'Karat stamp: —'));
      marksCell.append(element('span', 'Maker mark: —', 'product-sub'));
      marksCell.append(element('span', 'Not documented on listing', 'product-sub'));

      const priceCell = element('td');
      priceCell.append(element('span', formatUSD(candidate.price.amount, candidate.price.currency), 'price'));
      priceCell.append(element('span', `Checked ${formatDate(candidate.price.checkedOn)}`, 'price-date'));
      priceCell.append(element('span', candidate.price.scope, 'product-sub'));
      const priceLink = linkFor(sources.get(candidate.price.sourceId)?.url || candidate.productUrl, 'Seller price source');
      priceCell.append(priceLink);

      const returnCell = element('td', null, 'cell-small');
      returnCell.append(statusPill('XRF return terms unverified', 'unverified'));
      const returnSource = sources.get(candidate.returnPolicySourceId);
      if (returnSource) returnCell.append(linkFor(returnSource.url, 'Seller return policy'));
      returnCell.append(element('span', 'Ask in writing before purchase.', 'product-sub'));

      const resultCell = element('td');
      resultCell.append(statusPill('Not cleared', 'review'));
      resultCell.append(element('span', `${candidate.flagIds.length} open flags · no full checklist pass`, 'product-sub'));
      resultCell.append(linkFor(candidate.productUrl, 'Open listing'));

      for (const cell of [productCell, metalCell, solidCell, weightCell, marksCell, returnCell, priceCell, resultCell]) row.append(cell);
      tbody.append(row);
    }
  }

  function renderPreviewCandidates(tbody, candidates, sources) {
    tbody.replaceChildren();
    for (const candidate of candidates) {
      const row = document.createElement('tr');
      const nameCell = element('td');
      nameCell.append(linkFor(candidate.productUrl, candidate.name, 'product-name'));
      nameCell.append(element('span', candidate.category, 'product-sub'));
      const metalCell = element('td', candidate.metal.sellerDescription.value);
      const priceCell = element('td');
      priceCell.append(element('span', formatUSD(candidate.price.amount, candidate.price.currency), 'price'));
      priceCell.append(element('span', `As of ${formatDate(candidate.price.checkedOn)}`, 'price-date'));
      priceCell.append(linkFor(sources.get(candidate.price.sourceId)?.url || candidate.productUrl, 'Price source'));
      const stateCell = element('td');
      stateCell.append(statusPill('Not cleared', 'review'));
      stateCell.append(element('span', 'Weight and marks not confirmed', 'product-sub'));
      row.append(nameCell, metalCell, priceCell, stateCell);
      tbody.append(row);
    }
  }

  function renderSourceTable(tbody, sources) {
    tbody.replaceChildren();
    for (const source of sources) {
      const row = document.createElement('tr');
      const typeCell = element('td');
      typeCell.append(element('strong', source.kind));
      typeCell.append(element('span', source.publisher, 'product-sub'));
      const claimCell = element('td');
      claimCell.append(linkFor(source.url, source.title, 'product-name'));
      claimCell.append(element('span', (source.supports || []).join(' · '), 'product-sub'));
      const caveatCell = element('td', source.caveat, 'cell-muted');
      const dateCell = element('td');
      dateCell.append(element('span', formatDate(source.checkedOn)));
      row.append(typeCell, claimCell, caveatCell, dateCell);
      tbody.append(row);
    }
  }

  function renderFindings(tbody, findings, sources, query = '') {
    tbody.replaceChildren();
    const filter = query.trim().toLowerCase();
    const visible = findings.filter((finding) => {
      const text = `${finding.id} ${finding.title} ${finding.finding} ${finding.action}`.toLowerCase();
      return !filter || text.includes(filter);
    });

    for (const finding of visible) {
      const row = document.createElement('tr');
      const idCell = element('td');
      idCell.append(element('span', finding.id, 'finding-id'));
      idCell.append(element('span', finding.severity, 'product-sub'));
      const findingCell = element('td', null, 'finding-text');
      findingCell.append(element('div', finding.title, 'finding-title'));
      findingCell.append(element('div', finding.finding, 'product-sub'));
      const actionCell = element('td', finding.action, 'finding-action');
      const stateCell = element('td');
      stateCell.append(element('span', finding.status, 'status-text'));
      const sourceCell = element('td');
      appendSources(sourceCell, finding.sourceIds, sources);
      row.append(idCell, findingCell, actionCell, stateCell, sourceCell);
      tbody.append(row);
    }
    setText('#finding-count', `${visible.length} finding${visible.length === 1 ? '' : 's'}`);
    if (!visible.length) {
      const row = document.createElement('tr');
      const cell = element('td', 'No findings match that search.', 'empty-state');
      cell.colSpan = 5;
      row.append(cell);
      tbody.append(row);
    }
  }

  function renderChecklist(tbody, checks, sources) {
    tbody.replaceChildren();
    for (const check of checks) {
      const row = document.createElement('tr');
      const req = element('td', null, 'cell-small');
      req.append(element('strong', check.requirement));
      req.append(element('span', check.id.replaceAll('-', ' '), 'product-sub'));
      const status = element('td', null, 'cell-small');
      const statusText = check.status.toLowerCase();
      const statusType = statusText.includes('mixed') || statusText.includes('unresolved') || statusText.includes('review')
        ? 'review'
        : (statusText.includes('unverified') || statusText.includes('blank') || statusText.includes('not stated') || statusText.includes('not documented') || statusText.includes('not fully verified')
          ? 'unverified'
          : (statusText.includes('recommended') || statusText.includes('buyer safeguard') ? 'neutral' : 'pass'));
      status.append(statusPill(check.status, statusType));
      const evidence = element('td', check.currentEvidence);
      const action = element('td', check.nextStep);
      const sourceCell = element('td');
      appendSources(sourceCell, check.sourceIds, sources);
      row.append(req, status, evidence, action, sourceCell);
      tbody.append(row);
    }
  }

  function renderReputation(tbody, merchant, sources) {
    if (!tbody || !merchant) return;
    tbody.replaceChildren();
    for (const signal of merchant.reputationSignals || []) {
      const row = document.createElement('tr');
      row.append(element('td', signal.label));
      row.append(element('td', signal.summary));
      row.append(element('td', signal.sourceNote, 'cell-muted'));
      const sourceCell = element('td');
      appendSources(sourceCell, [signal.sourceId], sources);
      row.append(sourceCell);
      tbody.append(row);
    }
  }

  function updateFreshness(reviewDate) {
    const dateText = formatDate(reviewDate);
    document.querySelectorAll('[data-review-date]').forEach((node) => { node.textContent = dateText; });
    const warning = document.querySelector('#freshness-warning');
    if (!warning) return;
    const date = new Date(`${reviewDate}T00:00:00Z`);
    const today = new Date();
    today.setUTCHours(0, 0, 0, 0);
    const ageDays = Number.isFinite(date.getTime()) ? Math.floor((today.getTime() - date.getTime()) / 86400000) : 0;
    if (ageDays > 0) {
      warning.hidden = false;
      const age = ageDays === 1 ? 'one day old' : `${ageDays} days old`;
      const message = warning.querySelector('[data-freshness-copy]');
      if (message) message.textContent = `Price snapshots are ${age} (reviewed ${dateText}); reopen the seller pages and recheck before purchase.`;
    } else {
      warning.hidden = true;
    }
  }

  async function initDataPages() {
    const [sourcesData, ringsData, findingsData, checklistData, merchantsData] = await Promise.all([
      readJson('sources.json'), readJson('rings.json'), readJson('findings.json'), readJson('checklist.json'), readJson('merchants.json')
    ]);
    const sources = sourceIndex(sourcesData);
    const candidateList = ringsData.candidates || [];
    const findings = findingsData.findings || [];
    const merchant = (merchantsData.merchants || [])[0];

    updateFreshness(ringsData.reviewedOn);
    setText('#candidate-count', String(candidateList.length));
    setText('#hero-candidate-count', String(candidateList.length));
    setText('#qualified-count', String(ringsData.qualifyingCandidateCount));
    setText('#hero-qualified-count', String(ringsData.qualifyingCandidateCount));
    setText('#finding-total', String(findings.length));
    setText('#snapshot-date', formatDate(ringsData.reviewedOn));
    setText('#source-count', String((sourcesData.sources || []).length));

    const candidateTbody = document.querySelector('#candidate-rows');
    if (candidateTbody) renderFullCandidates(candidateTbody, candidateList, sources);
    const previewTbody = document.querySelector('#dashboard-candidate-rows');
    if (previewTbody) renderPreviewCandidates(previewTbody, candidateList, sources);

    const sourceTable = document.querySelector('#source-rows');
    if (sourceTable) renderSourceTable(sourceTable, sourcesData.sources || []);

    const findingTbody = document.querySelector('#finding-rows');
    if (findingTbody) {
      const input = document.querySelector('#finding-search');
      const draw = () => renderFindings(findingTbody, findings, sources, input?.value || '');
      input?.addEventListener('input', draw);
      draw();
    }

    const checklistTbody = document.querySelector('#checklist-rows');
    if (checklistTbody) renderChecklist(checklistTbody, checklistData.checks || [], sources);

    const reputationTbody = document.querySelector('#reputation-rows');
    if (reputationTbody) renderReputation(reputationTbody, merchant, sources);

    if (merchant) {
      setText('#merchant-contact-phone', merchant.contact.phone);
      const emailLink = document.querySelector('#merchant-contact-email');
      if (emailLink) {
        emailLink.textContent = merchant.contact.email;
        emailLink.href = `mailto:${merchant.contact.email}`;
      }
      setText('#merchant-reputation-summary', merchant.reputationAssessment);
      const contactSource = sources.get(merchant.contact.sourceId);
      const contactLink = document.querySelector('#merchant-contact-source');
      if (contactSource && contactLink) {
        contactLink.href = contactSource.url;
        contactLink.target = '_blank';
        contactLink.rel = 'noopener noreferrer';
        contactLink.referrerPolicy = 'no-referrer';
      }
    }

    const market = await readJson('market.json');
    setText('#market-quote-status', market.goldSpotQuote.status);
  }

  function setupCalculator() {
    const form = document.querySelector('#gold-calculator');
    if (!form) return;
    const weightInput = form.elements.namedItem('alloyWeightG');
    const weightSourceInput = form.elements.namedItem('weightSource');
    const weightDateInput = form.elements.namedItem('weightDate');
    const karatInput = form.elements.namedItem('karat');
    const spotInput = form.elements.namedItem('spotAmount');
    const unitInput = form.elements.namedItem('spotUnit');
    const sourceInput = form.elements.namedItem('spotSource');
    const dateInput = form.elements.namedItem('spotDate');
    const resultFine = document.querySelector('#result-fine-gold');
    const resultValue = document.querySelector('#result-metal-value');
    const resultPrice = document.querySelector('#result-price-per-gram');
    const status = document.querySelector('#calculator-status');
    const sourceNote = document.querySelector('#quote-source-note');
    const troyOunceGrams = 31.1034768;

    const clearOutputs = () => {
      resultFine.textContent = '—';
      resultValue.textContent = '—';
      resultPrice.textContent = '—';
      resultFine.removeAttribute('aria-label');
      sourceNote.replaceChildren();
    };

    const calculate = () => {
      clearOutputs();
      const grams = Number(weightInput.value);
      const karat = Number(karatInput.value);
      const validWeight = weightInput.value !== '' && Number.isFinite(grams) && grams > 0;
      const validKarat = Number.isFinite(karat) && karat > 0 && karat <= 24;
      const weightDate = weightDateInput.value;
      const weightDay = weightDate ? new Date(`${weightDate}T00:00:00Z`) : null;
      const today = new Date();
      today.setUTCHours(0, 0, 0, 0);
      const validWeightDate = Boolean(weightDay && !Number.isNaN(weightDay.getTime()) && weightDay <= today);
      let parsedWeightSource = null;
      try {
        parsedWeightSource = new URL(weightSourceInput.value);
      } catch {
        parsedWeightSource = null;
      }
      const validWeightSource = parsedWeightSource?.protocol === 'https:';
      if (!validWeight || !validKarat || !validWeightDate || !validWeightSource) {
        status.textContent = 'Enter a seller-confirmed gold-only mass in grams, the seller-stated karat, and a dated HTTPS source that supports both inputs. The calculator will not estimate or calculate unsourced values.';
        return;
      }

      const nominalPurity = karat === 24 ? 0.999 : karat / 24;
      const fineGoldGrams = grams * nominalPurity;
      resultFine.textContent = `${fineGoldGrams.toFixed(6)} g`;
      resultFine.setAttribute('aria-label', `${fineGoldGrams.toFixed(6)} grams nominal fine gold`);
      sourceNote.append(linkFor(parsedWeightSource.toString(), `Gold mass/karat source · ${formatDate(weightDate)}`, 'source-link'));

      const spot = Number(spotInput.value);
      const unit = unitInput.value;
      const date = dateInput.value;
      let parsedSource = null;
      try {
        parsedSource = new URL(sourceInput.value);
      } catch {
        parsedSource = null;
      }
      const validSpot = spotInput.value !== '' && Number.isFinite(spot) && spot > 0;
      const validUnit = unit === 'gram' || unit === 'troy-ounce';
      const validSource = parsedSource?.protocol === 'https:';
      const quoteDay = date ? new Date(`${date}T00:00:00Z`) : null;
      const validDate = Boolean(quoteDay && !Number.isNaN(quoteDay.getTime()) && quoteDay <= today);
      if (validSpot && validUnit && validSource && validDate) {
        const usdPerGram = unit === 'troy-ounce' ? spot / troyOunceGrams : spot;
        const rawValue = fineGoldGrams * usdPerGram;
        resultPrice.textContent = `${formatUSD(usdPerGram)} / g`;
        resultValue.textContent = formatUSD(rawValue);
        sourceNote.append(linkFor(parsedSource.toString(), `User-entered quote source · ${formatDate(date)}`, 'source-link'));
        status.textContent = 'Arithmetic only. The gold mass/karat and quote/date came from your inputs; this site does not fetch, verify, or endorse them. A quote older than today is historical, not a current-price claim. Excludes stones, other materials, retail markup, labor, taxes, and any buyer discount.';
      } else {
        resultValue.textContent = 'Not calculated';
        status.textContent = 'Nominal fine-gold mass is calculated from the dated, linked mass and karat inputs. For raw-metal arithmetic, add a positive quote, its date, and an HTTPS source link. This site does not fetch or verify the quote.';
      }
    };

    form.addEventListener('input', calculate);
    form.addEventListener('change', calculate);
    document.querySelector('#calculate-button')?.addEventListener('click', calculate);
    form.addEventListener('reset', () => window.setTimeout(() => {
      clearOutputs();
      status.textContent = 'Calculator is blank by design. Provide a seller-confirmed gold-only mass, karat, and dated HTTPS source supporting both before calculating; a dated quote and source are additionally required for raw-metal arithmetic.';
    }, 0));
  }

  function showDataError(error) {
    const status = document.querySelector('#data-load-error');
    if (!status) return;
    status.hidden = false;
    status.textContent = `Some research data could not be loaded: ${error.message}. Reopen the source page or refresh the site.`;
  }

  setupCalculator();
  if (page !== 'calculator') initDataPages().catch(showDataError);
})();
