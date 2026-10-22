# Anti-hallucination audit report

- Run: 2026-10-22 23:25 UTC
- Rows audited: **19**
- Sellers audited: **8**
- Flag definitions: **28**
- Result: **PASS** — 0 error(s), 0 warning(s), 93 check(s) passed

## What this pass is looking for

| Failure mode | Check |
|---|---|
| invented price | every price must appear in its own quoted source text |
| invented weight | every gram figure must appear in a quoted seller statement |
| invented purity claim | a PASS needs the seller's word 'solid'; a FAIL needs plating evidence |
| phantom source | every row needs https source links it actually cites |
| dangling flag | every flag id must be defined |
| bad bookkeeping | a field cannot be both verified and unverified |
| fake contact details | phone/email require a contact_source |
| broken site | local links must resolve |
| stray number on the site | every $ figure in HTML must exist in the data |

## Errors

None.

## Warnings

None.

## Passed checks

- [files] data/gold-price.json present
- [files] data/rings.json present
- [files] data/sellers.json present
- [files] data/standards.json present
- [files] data/flags.json present
- [gold-price] spot price present: 4024.36 USD/oz
- [gold-price] source is the World Gold Council (gold.org)
- [gold-price] per-gram value reproduces: $129.3862/g (computed, not stored)
- [sources] R01: 2 official source link(s)
- [price] R01: $2,900 matches its quoted source text
- [solid] R01: PASS backed by a quote containing 'solid'
- [sources] R02: 2 official source link(s)
- [price] R02: $1,500 matches its quoted source text
- [solid] R02: PASS backed by a quote containing 'solid'
- [sources] R03: 2 official source link(s)
- [price] R03: $648 matches its quoted source text
- [solid] R03: PASS backed by a quote containing 'solid'
- [sources] R04: 2 official source link(s)
- [price] R04: $228 matches its quoted source text
- [solid] R04: FAIL backed by plating/vermeil evidence
- [sources] R05: 2 official source link(s)
- [price] R05: $1,255 matches its quoted source text
- [sources] R06: 3 official source link(s)
- [price] R06: $1,000 matches its quoted source text
- [sources] R07: 3 official source link(s)
- [price] R07: $2,320 matches its quoted source text
- [sources] R08: 3 official source link(s)
- [price] R08: $2,210 matches its quoted source text
- [sources] R09: 3 official source link(s)
- [price] R09: $1,500 matches its quoted source text
- [sources] R10: 2 official source link(s)
- [price] R10: price honestly left blank and labelled
- [sources] R11: 1 official source link(s)
- [price] R11: $3,725 matches its quoted source text
- [weight] R11: 6.1 g traced to a quoted seller statement
- [sources] R12: 1 official source link(s)
- [price] R12: $5,350 matches its quoted source text
- [weight] R12: 2.2 g traced to a quoted seller statement
- [sources] R13: 1 official source link(s)
- [price] R13: $2,850 matches its quoted source text
- [sources] R14: 2 official source link(s)
- [price] R14: $1,145 matches its quoted source text
- [sources] R15: 1 official source link(s)
- [price] R15: $249 matches its quoted source text
- [weight] R15: 0.7 g traced to a quoted seller statement
- [sources] R16: 1 official source link(s)
- [price] R16: $299 matches its quoted source text
- [weight] R16: 0.8 g traced to a quoted seller statement
- [sources] R17: 2 official source link(s)
- [price] R17: $1,600 matches its quoted source text
- [sources] R18: 1 official source link(s)
- [price] R18: $276 matches its quoted source text
- [sources] R19: 2 official source link(s)
- [price] R19: $178 matches its quoted source text
- [solid] R19: FAIL backed by plating/vermeil evidence
- [sellers] S-BN: Blue Nile checked
- [sellers] S-MJ: Mejuri checked
- [sellers] S-CO: Costco checked
- [sellers] S-WE: Wilson's Estate Jewelry checked
- [sellers] S-RS: Ross-Simons checked
- [sellers] S-TI: Tiffany & Co. checked
- [sellers] S-CB: Catbird checked
- [sellers] S-JA: James Allen checked
- [domain] R01: mejuri.com belongs to mejuri.com
- [domain] R02: mejuri.com belongs to mejuri.com
- [domain] R03: mejuri.com belongs to mejuri.com
- [domain] R04: mejuri.com belongs to mejuri.com
- [domain] R05: bluenile.com belongs to bluenile.com
- [domain] R06: bluenile.com belongs to bluenile.com
- [domain] R07: bluenile.com belongs to bluenile.com
- [domain] R08: bluenile.com belongs to bluenile.com
- [domain] R09: bluenile.com belongs to bluenile.com
- [domain] R10: costco.com belongs to costco.com
- [domain] R11: wilsonsestatejewelry.com belongs to wilsonsestatejewelry.com
- [domain] R12: wilsonsestatejewelry.com belongs to wilsonsestatejewelry.com
- [domain] R13: wilsonsestatejewelry.com belongs to wilsonsestatejewelry.com
- [domain] R14: bluenile.com belongs to bluenile.com
- [domain] R15: ross-simons.com belongs to ross-simons.com
- [domain] R16: ross-simons.com belongs to ross-simons.com
- [domain] R17: tiffany.com belongs to tiffany.com
- [domain] R18: catbirdnyc.com belongs to catbirdnyc.com
- [domain] R19: mejuri.com belongs to mejuri.com
- [flags] 28 flag definitions validated
- [standards] all karat fractions reproduce n/24
- [standards] 8 legal rules carry citations
- [links] analysis.html: local links resolved
- [links] calculator.html: local links resolved
- [links] flagged.html: local links resolved
- [links] index.html: local links resolved
- [links] methodology.html: local links resolved
- [links] rings.html: local links resolved
- [links] sellers.html: local links resolved
- [links] standards.html: local links resolved

## Standing recommendation

Re-run this audit after **every** data review, and specifically re-read the dataset looking
for hallucinations: a number that no cited page actually prints. If a value cannot be matched
to a quote, delete it and mark the field unverified.
