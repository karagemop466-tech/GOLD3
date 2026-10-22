#!/usr/bin/env node

/**
 * Dependency-free calculator interaction smoke test. The small DOM double
 * exercises the client logic; it does not replace testing in a real browser.
 */
import assert from 'node:assert/strict';
import fs from 'node:fs/promises';
import vm from 'node:vm';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

class FakeElement {
  constructor() {
    this.textContent = '';
    this.value = '';
    this.children = [];
    this.attributes = {};
    this.classList = { add() {} };
    this.listeners = {};
  }
  addEventListener(name, callback) { this.listeners[name] = callback; }
  append(...nodes) { this.children.push(...nodes); }
  replaceChildren(...nodes) { this.children = nodes; }
  setAttribute(name, value) { this.attributes[name] = value; }
  removeAttribute(name) { delete this.attributes[name]; }
}

const input = (value = '') => ({ value });
const today = new Date().toISOString().slice(0, 10);
const fields = {
  alloyWeightG: input('5'),
  weightSource: input(''),
  weightDate: input(today),
  karat: input('14'),
  spotAmount: input(''),
  spotUnit: input(''),
  spotSource: input(''),
  spotDate: input('')
};
const form = new FakeElement();
form.elements = { namedItem: (name) => fields[name] };
const nodes = new Map([
  ['#gold-calculator', form],
  ['#calculate-button', new FakeElement()],
  ['#result-fine-gold', new FakeElement()],
  ['#result-metal-value', new FakeElement()],
  ['#result-price-per-gram', new FakeElement()],
  ['#calculator-status', new FakeElement()],
  ['#quote-source-note', new FakeElement()]
]);
const document = {
  body: { dataset: { root: '..', page: 'calculator' } },
  querySelector: (selector) => nodes.get(selector) || null,
  createElement: () => new FakeElement()
};
const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const app = await fs.readFile(path.join(root, 'assets/app.js'), 'utf8');
const context = { document, URL, Intl, Number, Map, Date, console, window: { setTimeout } };
vm.runInNewContext(app, context, { filename: 'assets/app.js' });
const calculate = () => form.listeners.input();
const fine = nodes.get('#result-fine-gold');
const value = nodes.get('#result-metal-value');
const pricePerGram = nodes.get('#result-price-per-gram');
const secureUrl = (host, pathname) => new URL(pathname, ['https:', '', host].join('/')).toString();

calculate();
assert.equal(fine.textContent, '—', 'unsourced gold mass must not produce a fine-gold output');

fields.weightSource.value = secureUrl('seller.example', '/ring');
calculate();
assert.equal(fine.textContent, '2.916667 g', '5 g of nominal 14K should produce 2.916667 g fine gold');
assert.equal(value.textContent, 'Not calculated', 'raw-metal arithmetic must stay blank without a quote');
assert.equal(nodes.get('#quote-source-note').children.length, 1, 'the mass evidence link should be visible');

fields.spotAmount.value = '2300';
fields.spotUnit.value = 'troy-ounce';
fields.spotSource.value = secureUrl('prices.example', '/gold');
fields.spotDate.value = today;
calculate();
assert.match(pricePerGram.textContent, /^\$\d+\.\d{2} \/ g$/);
const displayedValue = Number(value.textContent.replace(/[^\d.]/g, ''));
const expectedValue = (5 * 14 / 24) * (2300 / 31.1034768);
assert.ok(Math.abs(displayedValue - expectedValue) < 0.01, 'troy-ounce conversion and raw-metal arithmetic should match the sourced inputs');
assert.equal(nodes.get('#quote-source-note').children.length, 2, 'both input evidence links should be visible');

fields.weightSource.value = ['http:', '', 'seller.example'].join('/') + '/ring';
calculate();
assert.equal(fine.textContent, '—', 'non-HTTPS mass source must be rejected');

fields.weightSource.value = secureUrl('seller.example', '/ring');
fields.spotDate.value = '2999-01-01';
calculate();
assert.equal(fine.textContent, '2.916667 g', 'valid mass arithmetic remains available with a historical quote date');
assert.equal(value.textContent, 'Not calculated', 'future quote dates must not produce raw-metal arithmetic');

console.log('Calculator interaction smoke test: PASS (evidence gate, 14K purity arithmetic, troy-ounce conversion, HTTPS links, and date checks).');
