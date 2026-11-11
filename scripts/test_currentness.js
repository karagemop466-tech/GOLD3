// Offline regression tests: these do not verify external sources.
const assert = require('assert');
const fs = require('fs');
const vm = require('vm');
for (const file of fs.readdirSync('.').filter(f => f.endsWith('.html'))) {
  const html = fs.readFileSync(file, 'utf8');
  assert(html.includes('Currentness alert') && html.includes('unverified'), `${file}: missing currentness alert`);
  assert(html.includes('flagged.html#currentness-review'), `${file}: missing review flag link`);
}
assert(fs.readFileSync('flagged.html', 'utf8').includes('id="currentness-review"'));
const ids = ['gold-calc','calc-spot','calc-karat','calc-grams','calc-stone-ct','calc-tolerance','calc-price',
  'out-spot-gram','out-melt-gram','out-fine-gold','out-melt-value','out-tolerance-note','out-purity','out-implied','out-ratio','out-premium','out-verdict'];
const elements = Object.fromEntries(ids.map(id => [id, {
  value: '', textContent: '', className: '', classList: {add() {}}, handlers: {},
  addEventListener(event, fn) {this.handlers[event] = fn;}
}]));
elements['calc-spot'].value = '4022.22';
elements['calc-karat'].value = '14K';
elements['calc-tolerance'].value = 'none';
const document = {getElementById: id => elements[id], querySelectorAll: () => [],
  addEventListener: (event, fn) => {if (event === 'DOMContentLoaded') fn();}};
vm.runInNewContext(fs.readFileSync('assets/app.js', 'utf8'), {document, location: {hash: ''}, isFinite, setTimeout});
assert.equal(elements['out-melt-value'].textContent, '—', 'blank weight must not produce zero value');
elements['calc-grams'].value = '3';
elements['calc-price'].value = '100';
elements['calc-grams'].handlers.input();
assert.equal(elements['out-melt-value'].textContent, '$226.31');
assert.equal(elements['out-fine-gold'].textContent, '1.75 g');
assert(elements['out-verdict'].textContent.includes('below the estimated gold value'));
assert(!elements['out-verdict'].textContent.includes('Impossible'));
elements['calc-stone-ct'].value = '20';
elements['calc-stone-ct'].handlers.input();
assert.equal(elements['out-melt-value'].textContent, '—', 'stone heavier than total cannot yield a metal value');
elements['calc-stone-ct'].value = '';
elements['calc-spot'].value = '0';
elements['calc-spot'].handlers.input();
assert.equal(elements['out-melt-value'].textContent, '—', 'zero spot is not a valid quote');
console.log('Currentness banners and calculator safety: PASS');
