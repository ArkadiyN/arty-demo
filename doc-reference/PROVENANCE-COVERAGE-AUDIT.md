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

This was a coverage gap, not a demonstrated defect: none of the 12 was shown
to misstate its source the way the pre-hardening 7 did. It was the same
structural precondition, and was cheap to close (add the section; the
mechanical half of a card carries no interpretive risk per
source-data-fidelity.md).

**Closed 2026-08-16.** All 12 cards now carry a `## Provenance of this card`
section, added by five parallel @librarian passes. Closing this sweep surfaced
concrete findings rather than a bare coverage gap — 2 `blocking`
(`sanborn2019-clt-ballistic-performance/card.md:249`,
`ufc-4-023-07-direct-fire-weapons-effects/card.md:167`, both: source.pdf
missing and a claimed verification can no longer be re-audited) and 7
`deferrable` (source.pdf retention gaps on
`ada300526-picatinny-cylinder-test`, `ada462991-fragment-velocity`,
`ada540284-gurney-2d-extension`, `kennedy1970-gurney-energy`,
`martineau1998-viscoplastic-shell-expansion`,
`tm-9-1901-artillery-ammunition`, `tm-9-1904-fuze-fitting`). The three
`mott-distribution-small-fragments` cards and `ordnance-ammunition-drawings-book-4`
/ `paine-1929-centrifugal-casting` closed clean. See each card's own
`## Provenance` section and `OPEN-FINDINGS.md` for the live findings register.
