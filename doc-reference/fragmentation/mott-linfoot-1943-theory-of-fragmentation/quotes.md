# Mott & Linfoot (1943) — verbatim passages

**This is a quotation set, not an extraction.** It exists so that every anchor
string cited by `card.md` can be found by `grep` — nothing more. It reproduces
only the passages this repo actually cites, in the report's own words, and makes
no attempt to cover the document.

**Provenance.** Each passage was read off a 300 dpi render of the page —
`experiment/fragmentation-field/challenges/source-data-audit/checks/mott-linfoot-1943-page-render.py`,
which renders one report page as two overlapping halves. **The scan's own embedded OCR
layer was not used and must not be** — it is unusable, and eight of the nine
anchors below do not appear in it at all. See `card.md`, "There is no markdown
extraction of this document, deliberately."

Both halves of that claim are checked, not asserted:

```
uv run python experiment/fragmentation-field/challenges/source-data-audit/checks/mott-linfoot-1943-anchor-greppability.py
uv run python experiment/fragmentation-field/challenges/source-data-audit/checks/mott-linfoot-1943-page-render.py
```

Headings below give the **report page number** (add 4 for the pdf page). Editorial
insertions are in `[…]`; everything else is as printed, including the report's
own spacing of formulae into display lines. Where the page prints a formula as
handwritten mathematics, it is rendered here in plain notation and marked so.

Do not cite this file as a source. Cite the report, and use these strings to
find the place.

**Line breaks here are load-bearing.** An anchor string that straddles a
newline is not greppable — `grep -F "our theory is incomplete"` returns nothing
if the phrase wraps. Two of the nine anchors below failed on exactly that when
this file was first written. The quoted paragraphs are therefore wrapped so that
every anchor cited elsewhere in the repo sits unbroken on one line; when adding
or re-flowing a passage, re-run the anchor grep before committing.

______________________________________________________________________

## p. 1 — title and summary

> A THEORY OF FRAGMENTATION
>
> by
>
> N. F. MOTT and E. H. LINFOOT,
> Bristol University Extra-Mural Group.
>
> SUMMARY. A tentative theory is given to account for the mean fragment sizes
> of certain types of bomb and shell, and for the relative numbers of large and
> small fragments.

Stamped `RESTRICTED` (struck through) and `UNCLASSIFIED`; a handwritten `15`
sits in the top-right corner.

## p. 1 — §1 opening, and the observed fragment shape

> 1\. THE MEAN FRAGMENT SIZE. The theory given here is applicable only to
> casings which expand plastically before rupture. This may not be the case
> for brittle materials such as cast iron.
>
> We consider first fragmentation of the type occurring in the 3.7 inch A.A.
> shell. The larger fragments appear from inspection to be formed as shown in
> fig. 1, which represents a section through part of the casing. Cracks start
> on the inside, at such points as A₁, A₂, A₃ …. and spread outwards to B₁,
> B₂, B₃. This type of break-up has been discussed in Report No. 2232 from the
> Dept. of Metallurgy of the University of Sheffield, Ref. A.C.3098. The widths
> of typical fragments are of the order 1 cm; the length, parallel to the axis
> of the shell, is considerably greater.

## p. 1 — the energy-of-fracture argument and eq. (2)

> At the moment of rupture, let r be the radius of the shell casing, t its
> thickness and V the velocity with which it is moving outwards. We suppose
> that rupture takes place when work-hardening has proceeded to such an extent
> that a crack will propagate itself with the expenditure of less energy than
> further plastic flow. Suppose that the casing then splits along two lines
> distant a apart; the cracks are represented by AB, A'B' in fig. 2, which,
> like fig. 1, represents a cross section through the shell casing. A splinter
> of cross section ABB'A' is then flying outwards with velocity V. The top
> surface AB of the fragment will have, in addition to the large outward
> velocity V, a velocity at right angles to it of amount ½Vα, where α = a/r.
> Similarly the bottom surface A'B' will have a downward velocity of the same
> amount. Referred to axes moving with the fragment, the metal will have
> kinetic energy, per unit length parallel to the axis of the shell, equal to
>
> \[handwritten\]
>
> where ρ is the density of the metal. Since rα = a, this becomes
>
> \[handwritten\] (1/24)
>
> We now make the assumption that if the energy (1) is great enough to form a
> new crack through the fragment, it will do so, and the fragment will break
> into two. If W is the energy per unit area required to form a crack, the
> energy required for this is Wt. Thus no fragment will be formed with
> thickness a greater than that given by equating Wt to (1), which gives
>
> [handwritten] a = [ 24 r² W / (ρ V²) ]^(1/3) (2)

Note on wording: the page calls `a` the fragment's *thickness* here, but fig. 2
labels `t` as the casing thickness and `a` as the arc dimension, and eq. (1) is
built from `α = a/r` — so `a` is the **circumferential breadth**, the dimension
the theory bounds. `card.md` uses "breadth" throughout for that reason.

## p. 1–2 — the value of W, and its stated uncertainty

> For W we may take a value given by impact tests; according to Southwell
> (Trans. Manchester Assoc. of Engineers, 1937) this ranges from 70 to 800
> ft/lbs. per sq. inch. We should take a value appropriate to the metal at the
> moment of rupture, i.e. after plastic deformation, when it will be very
> brittle. We therefore take the lower value, 70 ft/lbs. It is realised that
> the energy of rupture is not, in practice, proportional to the area, so our
> value will be very approximate. Moreover heating of the metal during its
> expansion may have an effect. Fortunately, since W occurs as W^(1/3), the
> value of a is not very sensitive to the value of W. A measurement of the
> rupture energy for cold-worked H.E. steel would be of interest\*.
>
> \* It is of interest to compare the much smaller rupture energy for a brittle
> substance such as quartz, which from experiments on grinding sand appears to
> be of the order 61 ft/lbs. per sq. ft. (Martin, Trans. Ceramic Society, 23,
> 61, 1923).

## p. 2 — the worked example

> For r we take 2.2 inches, and for V, the velocity of the fragments, 2500
> ft/sec. We obtain for a
>
> = 0.55 inches
>
> in good agreement with the observed value.
>
> For steels where fracture is due to shear we have no information from which
> the magnitude of W can be estimated.

## p. 2 — the first length disclaimer

> We have not been able to find a theory to account for the average length of
> the splinters in this type of shell. For shells or bombs which bulge out in
> the middle before breaking up, the dimension parallel to the axis might be
> determined by the same mechanism, r being the radius of curvature of an axial
> section of the casing.

## p. 2 — the second length disclaimer, and eq. (3)

> We may use formula (2) to compare the mean fragment sizes of bombs with
> different charge-weight ratios, sizes etc., Since, however,
> we have no theory of what determines the lengths of the splinters from a shell,
> we confine ourselves to a bomb which, at the moment of bursting, is roughly
> spherical. Then we can take the mean weight of a fragment to be proportional
> to ρa²t, and thus to
>
> \[handwritten\]
>
> If r₀, t₀ refer to the bomb before expansion, and r, the radius at the moment
> of burst is equal to ε r₀ , then t = t₀/ε², so that the mean fragment weight
> is proportional to
>
> \[handwritten\]
>
> If we keep the charge constant and vary the thickness t₀, we expect for heavy
> casings that V² will be proportional to 1/t₀ ; thus the average weight of
> fragment is proportional to t₀^(5/3) if ε is constant; actually, however,
> thick cased shells expand further than thin ones before breaking up, so we
> expect a rather less rapid variation with t₀ than this.

Eq. (3) closes against eq. (2) algebraically: `ρa²t` with
`a = (24r²W/ρV²)^(1/3)` gives `ρ^(1/3) r^(4/3) W^(2/3) V^(−4/3) t` exactly, which
is the first display above. That agreement is an independent confirmation of the
exponents read off eq. (2) — and eq. (2)'s exponents are what the `(r/V)^(2/3)`
finding in `card.md` turns on.

## p. 2 — §2, the Welch distribution and its parameters

> 2\. DISTRIBUTION OF FRAGMENT WEIGHTS.
>
> It was pointed out to the present authors by Dr. D. L. Welch (private
> communication dated 24th Sept. 1941) that the distributions of fragments from
> two such different projectiles as the 3" U.P. (initial fragment velocity 4500
> ft/sec.) and the 3.7" A.A. shell (fragment velocity about 2500 ft/sec) can be
> fitted approximately to the same law. This law is the following : if N(m)dm
> is the number of fragments with weights between m and m + dm, then
>
> \[handwritten\]
>
> where M = m^(1/3) and C and M₀ are constants. For the shell and the U.P., M₀
> has respectively the values (in (ounces)^(1/3))
>
> ```
>              3.7" shell        3" U.P.
>     M₀          0.33             0.15
> ```
>
> The agreement is shown below :-

The table that follows on p. 3 is transcribed at
`tables/section2-fragment-weight-distribution.csv`; its closure invariant and the
check script that closes the calculated column against eq. (4) are named in
`card.md`.

## p. 3 — what the fitted constants mean

> The total number of fragments is CM₀ and the total weight 6M₀⁴C, so the
> average weight is 6M₀³, or 0.21 ounces for the 3.7 inch shell. The
> distribution is very skew, however, so that there are a large number of
> fragments with weights considerably greater than the average.

## p. 4 — the third length disclaimer

> We have not, however, attempted at this stage to compare formulae such as (3)
> with the mean fragment weight of any bomb or shell, because
> our theory is incomplete, as it does not account for the length of splinters
> from shells, but only for their breadth, and for bombs which do not give long
> splinters we have not been able to find experimental information about mean
> weights and speeds. Further, a direct comparison with theory would only be
> possible where most fragments are projected under the same conditions, e.g.
> from a long cylinder detonated from one end, or a spherical bomb detonated in
> the middle.

## p. 4 — §3, the ruled-line model: breadth and length are independent

> 3\. MATHEMATICAL DISCUSSION OF THE DISTRIBUTION LAW FOR FRAGMENT SIZES.
>
> Distribution laws of the types (4) and (6) have been proposed in a number of
> papers for the weights or diameters of mineral particles after crushing, of
> sand particles and so on\*. We do not know of any attempt to derive
> mathematically the two or three dimensional formulae.
>
> \* cf. Lienau. J. Franklin Inst. 1936, p.485, where other references are given.
>
> We discuss first the case where a thin sheet is broken up into rectangular
> fragments by two sets of parallel lines. The analysis will be appropriate if a
> shell casing is broken up by cracks parallel to the axis at an average
> distance, say, x₀ apart, and the lengths have an average value y₀ independent
> of the breadth and are distributed according to the usual law. According to
> our assumptions, the number with breadths between x and x + dx is proportional
> to exp(−x/x₀)dx, and the number with lengths between y and y + dy proportional
> to exp(−y/y₀)dy. Thus the number per unit area with area greater than a² is
> given by
>
> \[handwritten\] (1/(x₀y₀)
>
> where the integration is for all positive values of xy for which xy > a².

## p. 4 — the Bessel-function result

> \[…\]
>
> \[handwritten\] (z/(x₀y₀)
>
> Differentiating with respect to a, we find for the number of fragments for
> which a lies between a and a + da
>
> \[handwritten\] (2/(x₀y₀)
>
> for large z this behaves like
>
> \[handwritten\] (½πz)
>
> and for small z like
>
> \[handwritten\]

with `z = 2a/√(x₀y₀)`, defined two displays earlier on the same page.

## p. 5 — random fragmentation gives the straighter line

> The function log(zK₀(z)) is plotted against z in fig. 5; it will be seen that
> it is nearly linear except for small z.
>
> If a thin shell casing is broken up at random, and a denotes the square root
> of the area, and νda the number of fragments such that a lies between a and
> a + da, then a plot of log ν against a should give a closer approximation to a
> straight line than fig. 5. The proof is as follows :

> \[…\]
>
> than that shown in fig. 7.
>
> We can prove that ν tends to a constant non-zero value as a → 0. The very
> small fragments will nearly all be triangles.

______________________________________________________________________

## Not quoted here

- **§2's alternative law (6)** for the heavier fragments, and its fit to
    Payman's model-bomb data (figs. 3–4) — `card.md` names it but cites no digit
    from it.
- **Figures 1–7.** Figs. 1 and 2 are inline line drawings on report pp. 1–2 and
    are described above in the report's own words; figs. 3–7 are the plates on pdf
    pp. 10–12, which carry no text layer and were not digitized.
- The remainder of §3's random-fragmentation proof (report p. 5).

## Second use: prose ground truth

This file is the repo's **only** verbatim prose transcription of a scanned
source, and the only one whose provenance is a controlled high-dpi read rather
than a pipeline. When the vision extractor is repaired (`plan` Phase 7), running
it over `source.pdf` and diffing against these passages measures its prose
fidelity — a case the Tolch `tables/*.csv` regression, which covers only tables,
cannot supply. The failure mode that fix targets is invented content in cells the
source leaves empty; the prose analogue is a fluent sentence the page does not
contain, and this file is what would catch it.
