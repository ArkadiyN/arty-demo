# Provenance-section coverage — post-hardening sweep

`.claude/rules/source-data-fidelity.md` ("A card states what the source says")
requires every `card.md` to carry a `## Provenance` section; `incidents.md #card-as-modelling-claim` found every interpretive defect in an 18-card sweep
sitting in the 7 that lacked one. That sweep and the closure-invariant /
anchor-verification hardening it produced (`21c0f51`, `72c4549`) both landed
2026-08-02/03.

This is the same check re-run against every `card.md` added **after** that
hardening (first-commit date 2026-08-08 through 2026-08-10, 14 cards) — a
provenance record for the sources currently under discussion for extending
the count-gap-1938 / drag-gap-1944 fragmentation-drag investigation. Checked
by `grep -L '^## .*Provenance' <card.md>`.

**2 of 14 have a `## Provenance` section**
(`ww2-shells/ordnance-ammunition-drawings-book-4`,
`ww2-shells/paine-1929-centrifugal-casting`). **12 do not:**

- `ww2-shells/tm-9-1901-artillery-ammunition`
- `ww2-shells/tm-9-1904-fuze-fitting`
- `fragmentation/ada300526-picatinny-cylinder-test`
- `fragmentation/ada462991-fragment-velocity`
- `fragmentation/ada540284-gurney-2d-extension`
- `fragmentation/kennedy1970-gurney-energy`
- `fragmentation/martineau1998-viscoplastic-shell-expansion`
- `fragmentation/sanborn2019-clt-ballistic-performance`
- `fragmentation/ufc-4-023-07-direct-fire-weapons-effects`
- `mott-distribution-small-fragments/carmona-2007`
- `mott-distribution-small-fragments/elek-jaramaz-2009`
- `mott-distribution-small-fragments/tavassoli-2000`

(`wound-ballistics/cunniff-2014` is a separate, worse case — no `card.md` at
all — already flagged in `cunniff-2014.md`, commit `cf402a8`.)

This is a coverage gap, not a demonstrated defect: none of these 12 has been
shown to misstate its source the way the pre-hardening 7 did. It is the same
structural precondition, is cheap to close (add the section; the mechanical
half of a card carries no interpretive risk per source-data-fidelity.md), and
should be closed before any of these 12 is cited as a modelling premise
(criterion-match or calibration-anchor claims especially) rather than after.

FINDING\[deferrable\]: 12 of 14 post-hardening cards (2026-08-08–10) lack a Provenance section per source-data-fidelity.md; same structural precondition as incidents.md#card-as-modelling-claim, no defect confirmed yet (affects: doc-reference/ww2-shells/tm-9-1901-artillery-ammunition/card.md, doc-reference/ww2-shells/tm-9-1904-fuze-fitting/card.md, doc-reference/fragmentation/ada300526-picatinny-cylinder-test/card.md, doc-reference/fragmentation/ada462991-fragment-velocity/card.md, doc-reference/fragmentation/ada540284-gurney-2d-extension/card.md, doc-reference/fragmentation/kennedy1970-gurney-energy/card.md, doc-reference/fragmentation/martineau1998-viscoplastic-shell-expansion/card.md, doc-reference/fragmentation/sanborn2019-clt-ballistic-performance/card.md, doc-reference/fragmentation/ufc-4-023-07-direct-fire-weapons-effects/card.md, doc-reference/mott-distribution-small-fragments/carmona-2007/card.md, doc-reference/mott-distribution-small-fragments/elek-jaramaz-2009/card.md, doc-reference/mott-distribution-small-fragments/tavassoli-2000/card.md; since: 2026-08-16)
