# Anti-hallucination audit report

- Run: 2026-10-23 23:55 UTC
- Rows audited: **31**
- Sellers audited: **14**
- Flag definitions: **57**
- Result: **PASS** — 0 error(s), 0 warning(s), 176 check(s) passed

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
- [files] data/verification.json present
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
- [price] R03: $898 matches its quoted source text
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
- [sources] R11: 2 official source link(s)
- [price] R11: $3,725 matches its quoted source text
- [weight] R11: 6.1 g traced to a quoted seller statement
- [sources] R12: 2 official source link(s)
- [price] R12: $5,350 matches its quoted source text
- [weight] R12: 2.2 g traced to a quoted seller statement
- [sources] R13: 2 official source link(s)
- [price] R13: $2,850 matches its quoted source text
- [weight] R13: 6.5 g traced to a quoted seller statement
- [sources] R14: 2 official source link(s)
- [price] R14: $1,145 matches its quoted source text
- [sources] R15: 2 official source link(s)
- [price] R15: $249 matches its quoted source text
- [weight] R15: 0.7 g traced to a quoted seller statement
- [sources] R16: 2 official source link(s)
- [price] R16: $299 matches its quoted source text
- [weight] R16: 0.8 g traced to a quoted seller statement
- [sources] R17: 2 official source link(s)
- [price] R17: $1,600 matches its quoted source text
- [sources] R18: 2 official source link(s)
- [price] R18: $276 matches its quoted source text
- [sources] R19: 2 official source link(s)
- [price] R19: $178 matches its quoted source text
- [solid] R19: FAIL backed by plating/vermeil evidence
- [sources] R20: 1 official source link(s)
- [price] R20: $3,004 matches its quoted source text
- [weight] R20: 3.8 g traced to a quoted seller statement
- [solid] R20: PASS backed by a quote containing 'solid'
- [sources] R21: 1 official source link(s)
- [price] R21: $613 matches its quoted source text
- [weight] R21: 8.3 g traced to a quoted seller statement
- [solid] R21: PASS backed by a quote containing 'solid'
- [sources] R22: 1 official source link(s)
- [price] R22: $3,074 matches its quoted source text
- [weight] R22: 5.4 g traced to a quoted seller statement
- [solid] R22: PASS backed by a quote containing 'solid'
- [sources] R23: 2 official source link(s)
- [price] R23: $1,910 matches its quoted source text
- [weight] R23: 6.1 g traced to a quoted seller statement
- [solid] R23: PASS backed by a quote containing 'solid'
- [sources] R24: 2 official source link(s)
- [price] R24: $875 matches its quoted source text
- [weight] R24: 2.3 g traced to a quoted seller statement
- [solid] R24: PASS backed by a quote containing 'solid'
- [sources] R25: 2 official source link(s)
- [price] R25: $551 matches its quoted source text
- [weight] R25: 1.4 g traced to a quoted seller statement
- [solid] R25: PASS backed by a quote containing 'solid'
- [sources] R26: 2 official source link(s)
- [price] R26: $4,068 matches its quoted source text
- [weight] R26: 6.3 g traced to a quoted seller statement
- [solid] R26: PASS backed by a quote containing 'solid'
- [sources] R27: 2 official source link(s)
- [price] R27: $695 matches its quoted source text
- [weight] R27: 2.5 g traced to a quoted seller statement
- [solid] R27: PASS backed by a quote containing 'solid'
- [sources] R28: 2 official source link(s)
- [price] R28: price honestly left blank and labelled
- [weight] R28: 2.3 g traced to a quoted seller statement
- [solid] R28: PASS backed by a quote containing 'solid'
- [sources] R29: 2 official source link(s)
- [price] R29: $1,090 matches its quoted source text
- [sources] R30: 2 official source link(s)
- [price] R30: $3,253 matches its quoted source text
- [sources] R31: 2 official source link(s)
- [price] R31: $239 matches its quoted source text
- [sellers] S-BN: Blue Nile checked
- [sellers] S-MJ: Mejuri checked
- [sellers] S-CO: Costco checked
- [sellers] S-WE: Wilson's Estate Jewelry checked
- [sellers] S-RS: Ross-Simons checked
- [sellers] S-TI: Tiffany & Co. checked
- [sellers] S-CB: Catbird checked
- [sellers] S-JA: James Allen checked
- [sellers] S-SARRAF: Sarraf.com checked
- [sellers] S-AUTOMIC: Automic Gold checked
- [sellers] S-BRILLIANTEARTH: Brilliant Earth checked
- [sellers] S-VRAI: VRAI checked
- [sellers] S-LOCALECLECTIC: Local Eclectic checked
- [sellers] S-MENE: Menē checked
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
- [domain] R20: sarraf.com belongs to sarraf.com
- [domain] R21: sarraf.com belongs to sarraf.com
- [domain] R22: automicgold.com belongs to automicgold.com
- [domain] R23: automicgold.com belongs to automicgold.com
- [domain] R24: automicgold.com belongs to automicgold.com
- [domain] R25: automicgold.com belongs to automicgold.com
- [domain] R26: sarraf.com belongs to sarraf.com
- [domain] R27: sarraf.com belongs to sarraf.com
- [domain] R28: vrai.com belongs to vrai.com
- [domain] R29: brilliantearth.com belongs to brilliantearth.com
- [domain] R30: mene.com belongs to mene.com
- [domain] R31: localeclectic.com belongs to localeclectic.com
- [verify] all 253 verification check ids are unique
- [verify] all 31 rows appear in the verification log
- [verify] summary counts recomputed from the entries and match
- [flags] 57 flag definitions validated
- [verify] all 27 site-defect ids are unique
- [standards] all karat fractions reproduce n/24
- [standards] 8 legal rules carry citations
- [site] verify.html present
- [links] 14k.html: local links resolved
- [links] 18k.html: local links resolved
- [links] analysis.html: local links resolved
- [links] bands-vintage-rings.html: local links resolved
- [links] calculator.html: local links resolved
- [links] checklist-standards.html: local links resolved
- [links] checklist.html: local links resolved
- [links] combined.html: local links resolved
- [links] excluded.html: local links resolved
- [links] flagged-for-review.html: local links resolved
- [links] flagged.html: local links resolved
- [links] index.html: local links resolved
- [links] lab-grown.html: local links resolved
- [links] methodology.html: local links resolved
- [links] retailers.html: local links resolved
- [links] rings.html: local links resolved
- [links] security-audit.html: local links resolved
- [links] sellers-policies.html: local links resolved
- [links] sellers.html: local links resolved
- [links] solitaire-settings.html: local links resolved
- [links] sources.html: local links resolved
- [links] standards.html: local links resolved
- [links] under-1000.html: local links resolved
- [links] verify.html: local links resolved

## Standing recommendation

Re-run this audit after **every** data review, and specifically re-read the dataset looking
for hallucinations: a number that no cited page actually prints. If a value cannot be matched
to a quote, delete it and mark the field unverified.
