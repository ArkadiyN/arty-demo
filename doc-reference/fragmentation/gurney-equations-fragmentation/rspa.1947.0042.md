# Fragmentation of shell cases

By N. F. Mott, F.R.S.

(Received 14 December 1945)

**Extraction note (resolved 2026-07-25):** pp. 304–308 were previously
OCR-garbled (symbols σ, ε, ρ, c, s, e inconsistently substituted for each
other; eq. (11) reduced to a circular `N = 1/log(NV)`). Root cause was
`google_timeout_ms` (`src/utils/settings.py`) being too short for the vision
model's server-side processing budget, causing spurious 504 DEADLINE_EXCEEDED
responses — fixed by raising `GOOGLE_TIMEOUT_MS` (now 300000 in `.env`). All
pages were re-ingested with the corrected timeout and are now clean.

**Downstream impact — flagged, not yet fixed:** the composition→γ table on
p. 308 changed materially versus the previously-cited (garbled) version:
steel-0.1%C is γ=**42** (was misread as 32), and the row after 0.1%C is
0.25%C (was misread as 0.2%C). `experiment/fragmentation-field/updates/wdss1-steel-grade/derivation.md`
§2 interpolates the WDSS-1 calibration constant (adopted γ=47) using the old,
now-known-wrong bracketing points (0.1%C→32, 0.2%C→53). That derivation needs
re-checking against the corrected table — this is a modeling correctness
question (Gate 3), not a documentation fix, and hasn't been done here.

A theory is given of the break-up of a metal shell of a cylindrical ring-form, to which the lines of fracture perpendicularly to the axis of the shell are predetermined. From the theory the average fragment length is given for the length of the average fragment; this is shown to depend, if certain hypotheses are made, on the radius and velocity of the shell at the moment of break-up, and on the mechanical properties of the metal.

## 1. INTRODUCTION

This paper is the outcome of attempts made by the present author to find a theoretical basis for the prediction of the distribution in weight of the fragments of a shell or bomb case after detonation of the filling. Little attempt will be made here to relate the theory to experiment; because experimental determinations of the distribution of the weights of fragments have not usually been made under the conditions that are best suited for theoretical interpretation. The purpose of this paper is to present a theory, and to show that it is consistent with the general features of the experimental results, without claiming that it is correct or not. It is conjectured that here the average size of the fragments from a shell case of a ductile metal depends on a property of the metal which is not usually measured, namely, the order in the values of the reduction in area at which fracture occurs. No systematic investigation of the magnitude of the scatter in the values of the reduction in area has been made, but the a priori distribution of the reduction in area at fracture in metals, and measurements of the weight distribution of fragments are therefore capable of giving informative general information about the internal properties of the metals.

When the explosive filling of a shell or bomb detonates, the case is subject initially to an extremely high pressure from the gaseous products of detonation; under this pressure it begins to move rapidly outwards. If the case is made of a ductile material such as steel, very considerable plastic expansion, as much as $5%$, occurs before the case breaks; this is most easily seen by examination of the larger fragments from the shell cases, which show that the wall of the case has been thinned. The gaps between these surfaces will be less than in the original case. By the time that fracture occurs the velocity with which the case is moving will be nearly equal to the final velocity with which the fragments are projected, and the gas pressure will have dropped to a value which is small compared to the flow stress of the metal. The fragmentation of a shell case must therefore be thought of as the tearing apart of a rapidly expanding tube when the material of the tube reaches the limit of its ductility.

Fracture in forged steel shell cases occurs normally by the formation of cracks parallel to the axis of the cylindrical part of the case, giving the familiar long thin fragments from broken shells. A complete theory of fragmentation must therefore have to account for both the width and length of fragments. If, however, the wall

(300)

______________________________________________________________________

Downloaded from http://royalgovernments publishing.org/article_pdf/109/109/300/307/page.109.300.pdf
by guest on 22 May 2021

# Fragmentation of shell cases 301

of the shell consists of a number of coaxial circular rings, all with the same inner and outer radii, stacked one above the other round a thin steel inner lining, the problem is simpler; each ring will break into a number of pieces, and the planes of fracture will be parallel to the axis of the cylinder. Ring-bombs of this type have been made, and found to break up in the way stated here.

![fig1.jpx](images/fig1.jpx)

before detonation at moment of fracture
FIGURE 1. Case of shell before detonation and at moment of fracture.

![fig1.jpx](images/fig1.jpx)

(a) (b)
FIGURE 2. Types of fracture of bomb casings.

The experimental arrangement to which the present theory will be applied will thus be as follows: The explosive is in the form of a cylindrical tube with a thin metal wall, of length several times the diameter to ensure that a steady detonation wave is set up. The tube is encased in a series of metal rings all of the same dimensions, which are stacked one above the other. The rings are then detonated. The theoretical problem is to calculate the distribution of lengths (as in figure 4) with which the fragments of the rings will be found to have.

Two main types of fracture have been observed in bomb and shell casings; shear fracture, which tends to occur in a direction perpendicular to the circumference of the case, as in figure 2a, and a combination of fibrous fracture (of the same type as at the bottom of the cup and cone fracture in a tensile test) and shear fracture as in figure 2b. In $\S 3$ considerations are given to the mechanism of fracture; for the purpose of the mathematical

______________________________________________________________________

Downloaded from http://royalgovernments publishing.org/article_pdf/109/109/300/307/page.109.301.pdf
by guest on 22 May 2021

302 N. F. Mott

theory to be developed here, it need only be assumed that fracture, once it begins, takes place so rapidly that it can be considered instantaneous compared with the rate of strain of the metal.

## 2. THEORY OF FRAGMENT LENGTH

The tensile strength of a brittle material such as glass shows a very considerable scatter, of the order $\pm 20\%$, from specimen to specimen. This is because fracture begins at one of a number of weak spots on the surface (the Griffith cracks); the strength is believed to depend on the depth of the deepest crack, and this will vary from one specimen to another. The true stress at fracture of ductile materials such as steel shows much less variation, as does also the reduction in area at which fracture occurs. No systematic investigation of the magnitude of the scatter has been made, but for specimens cut from the same bar it can be less than $\pm 1\%$ for a steel showing a total reduction in area of $50\%$. Initiation of fracture in metals is not necessarily a surface phenomenon; in a tensile test it starts in the interior of the specimen and little is known of the nature of the points of weakness responsible. Nevertheless, it is unlikely that even in a homogeneous material there will be no scatter. In any case it will be assumed that there does exist a scatter characteristic of the homogeneous material, and not due to inaccuracies in the apparatus. It will be found that the magnitude of this scatter determines the fragment size.

Denote by $s$ the plastic strain of the specimen, so that if the cross-sectional area is $A$ and the original area $A_0$,

$$s = \frac{A_0 - A}{A}.$$

Assume that the chance that an unfractured specimen of unit length will fracture when the strain increases from $s$ to $s + \mathrm{d}s$ is

$$C e^{\gamma s} \mathrm{d}s, \quad (1)$$

where $C$ and $\gamma$ are constants. The exponential expression is chosen as the simplest form which gives a rapid increase from negligible to large values as $s$ increases. With this assumption, the chance $p$ that the specimen breaks before a strain $s$ is reached is given by

$$\frac{\mathrm{d}p}{\mathrm{d}s} = (1 - p) C e^{\gamma s},$$

whence

$$p = 1 - \exp \left[ -\frac{C}{\gamma} e^{\gamma s} \right],$$

The average strain for fracture $s_0$ is given by

$$s_0 = \int_0^\infty s \frac{\mathrm{d}p}{\mathrm{d}s} \mathrm{d}s$$

$$= -\frac{1}{\gamma} \left[ \log \left( \frac{\gamma}{C} \right) + \epsilon \right],$$

where

$$\epsilon = \int_{-\infty}^\infty z e^z \exp(-e^z) \mathrm{d}z = 0.577.$$

______________________________________________________________________

Downloaded from http://royalgovernments publishing.org/article_pdf/109/109/300/307/page.109.302.pdf
by guest on 22 May 2021

# Fragmentation of shell cases 303

and the r.m.s. of the scatter in the strains at fracture is

$$\left( \int_0^\infty (s - s_0)^2 \frac{dp}{ds} ds \right)^{\frac{1}{2}} \approx \frac{1.28}{\gamma}.$$

A value of $\gamma$ equal to 128 would thus give a r.m.s. scatter of 0.01 in the strain at which fracture occurs.

The argument now is, that if $\gamma$ were infinite so that the strain at fracture were perfectly definite, the expanding shell case would break in all points at once. With the assumption (1), however, there is in any length of the material a finite probability of fracture which increases rapidly as $s$ approaches the critical value $s_0$. As soon as fracture takes place at one point, stress is released in the neighbourhood, and the unstressed regions spread with a velocity which can be calculated. This is shown in figure 3; a fracture is supposed to have occurred at $A$ and stress has been released in the regions $AB$ and $A'B'$ which are shaded. Fracture can no longer take place in the shaded regions; on the other hand, in the unshaded regions plastic flow is still going on, $s$ is increasing and according to formula (1) fracture becomes more and more likely. The average size of fragment will be determined by the rate at which the shaded regions in figure 3 spread and so prevent further fracture. Thus this rate must be calculated.

![fig2.jpx](images/fig2.jpx)

FIGURE 3. Release of strain round a tensile fracture.

Let $r$ be the radius of the case and $v$ its velocity outwards at the moment of break-up; it will be supposed that the thickness of the case is small compared with $r$, and that the whole process of break-up takes place in a time interval during which there is little change in $r$ or $v$. Then the rate of strain $ds/dt$ of the material is given by

$$\frac{ds}{dt} = \frac{v}{r}.$$

If in figure 3 an arbitrary point $C$ be taken on the circumference of the case at a distance $a$ from the point of fracture, then relative to $C$ the velocity of the whole stress-free region $AB$ is

$$\frac{v}{r}(a - x),$$

where $x$ is the length $AB$. If $\rho$ is the density of the material and $P_y$ is its flow stress in tension at the moment of fracture for the rates of strain concerned, then the equation of motion of $AB$ is

$$P_y = -\rho x \frac{d}{dt} \left( \frac{v}{r}(a - x) \right),$$

______________________________________________________________________

Downloaded from http://royalgovernments publishing.org/article_pdf/109/109/300/307/page.109.303.pdf
by guest on 22 May 2021

304 N. F. Mott

which gives on integrating ($r/v$ being treated as constant)

$$x^2/t = 2rP_y/\rho v. \tag{2}$$

The width $x$ of the unrestressed region thus increases as the square root of the time. This solution treats the metal as inelastic, and gives an infinite value for the initial velocity of the boundary $B$. A more exact solution\* gives a value of the velocity equal initially to that of sound in steel, but except in the opening stages approximating closely to that given by (2).

Making use of (1) and (2), the distribution of fragment lengths can be found. In a ring of diameter $l$ ($= 2\pi r$), suppose that at any moment $s$ fractures have formed. Then the rate of increase of $s$ with increasing strain is given by the equation

$$\frac{dn}{ds} = lfCe^{\alpha s}, \tag{3}$$

where $f$ is the proportion of the ring which is still stressed. It is convenient to introduce a new variable

$$\sigma = \gamma s.$$

Then (3) becomes

$$\frac{dn}{d\sigma} = \frac{lfC}{\gamma} e^{\alpha\sigma}, \tag{4}$$

and if a fracture occurs when $\sigma = \sigma_1$, the region round it which is unrestressed and thus safe from further fracture (shaded in figure 3) is at any subsequent value of $\sigma$, by (2), equal to

$$x_0(\sigma - \sigma_1)^{1/2}, \tag{5}$$

where

$$x_0 = (2P_y/\rho v)^{1/2} r/v.$$

The length $x_0$ is on dimensional grounds obviously proportional to the average fragment length. The distribution of average fragment lengths was found empirically as follows: Using equation (4) it was assumed that the first crack would form when $s$ was unity and thus for a value $\sigma_0$ of $\sigma$ given by

$$\frac{lC}{\gamma} e^{\alpha\sigma_0} = 1.$$

A line of length $l$ (say $10\text{ cm}$.) was ruled on paper to represent the circumference of the cylinder and a mark, representing a fracture, made on it at a point $P$ chosen at random. The next fracture will occur when $s = 2$; before the line is cut at random a second time to represent this happening, a range $dx$ must be marked off round the first cut to represent the shaded region where the strain has disappeared. By (4) the increase in $\sigma$ is unity, so the interval marked off on each side is $x_0$. The second cut must now be placed on any part of the line excluding the shaded region. $f$ is now $(l - 2x_0)/l$; the increase in $\sigma$ before the third cut is made is by (4) given by

$$\Delta\sigma = 1/fCe^{\alpha\sigma} \quad (\sigma - \sigma_0 = 1).$$

\* E. H. Lee (to be published).

______________________________________________________________________

Downloaded from http://royalgovernments publishing.org/article_pdf/109/109/300/307/page.109.304.pdf
by guest on 22 May 2021

# Fragmentation of shell cases 305

Round the second cut a shaded zone of $x_0(\Delta\sigma)^4$ must be drawn in, and the first must be widened according to equation (5). The process was repeated until the whole line was covered.

By repeating the whole procedure a number of times and measuring the lengths of the intervals between adjacent cuts on the line, a histogram was drawn giving the numbers of intervals between $0 \cdot 4x_0$ and $0 \cdot 8x_0$, and so on. This is shown in figure 4. The curve drawn through the histogram should give approximately the numbers of fragments with lengths between $x$ and $x + dx$.

![fig3.jpx](images/fig3.jpx)

FIGURE 4

The calculations were made with $l/x_0 = 20$: the distribution would not be sensibly different for larger values.

It will be seen that:
(1) The fragments have lengths most of which lie between $x_0$ and $2x_0$, and that the average length is about $1.5x_0$.
(2) $x_0$ is proportional to $r$, so that if the linear proportions of the bomb are scaled up by a given factor, the average fragment length is changed by the same factor.
(3) $x_0$ is inversely proportional to $v$, the velocity of the case at the moment of break-up.

______________________________________________________________________

Downloaded from http://royalgovernments publishing.org/article_pdf/109/109/300/307/page.109.305.pdf
by guest on 22 May 2021

306 N. F. Mott

As a numerical example, consider a bomb of diameter 3 in. so that $r$ will be about 2 in. at the moment of break-up. Suppose that the wall thickness is such that $v = 2000 \text{ ft./sec.}$, and that a steel case with $\rho = 480 \text{ lb./cu.in.}$ has a flow stress in the work-hardened state of 50 tons/sq.in. Then we find

$$x_g = 1.6 / \sqrt{\gamma} \text{ in.}$$

Thus if $\gamma \sim 100$, the average fragment length is about 0.24 in.

## 3. A THEORETICAL ESTIMATE OF THE CONSTANT $\gamma$ WHICH DEFINES THE SCATTER IN THE VALUES OF STRAIN AT FRACTURE

In the theory of A. A. Griffith of the strength of brittle solids, it is assumed that fracture starts at the deepest of a number of surface cracks. If $c$ is the depth of a crack, then according to Griffith the stress at which the crack will spread is

$$P = \sqrt{\frac{ET}{\pi c}}, \tag{6}$$

where $E$ is the elastic modulus and $T$ the surface tension. The variation in the depth of the deepest crack determines the variation in the tensile stress from specimen to specimen.

For ductile metals no satisfactory theory exists which accounts for the initiation of fracture at a given tensile stress. It will, however, be assumed that fracture begins, as in brittle materials, at one of a number of 'weak points' distributed throughout the material, and that the relation between the 'size' $c$ of a weak point and the stress required to start a fracture there is of the same type as (6), namely,

$$P = \text{const.} / c^n. \tag{7}$$

Fracture will then occur when, owing to the work-hardening of the material, the maximum principal stress reaches a value great enough to start a crack at the weak point for which $c$ is largest. It will be assumed, moreover that the values of $c$ are distributed about a mean value $c_0$ according to the Gaussian distribution function; thus the chance per unit volume that there is a weak point with parameter between $c$ and $c+dc$ will be taken to be equal to

$$B dc \exp \left[ -\frac{(c - c_0)^2}{2r^2} \right]. \tag{8}$$

Thus, if a specimen of volume $V$ has not fractured for a smaller stress, the chance that it will fracture for a stress between $P$ and $P+dP$ is

$$BV \exp \left[ -\frac{(c - c_0)^2}{2r^2} \right] \frac{dc}{dP} dP,$$

where $c$ is given in terms of $P$ by (7).

Interest is centred only in a small range of values of $c$ in the neighbourhood of the largest. Therefore let

$$c = c_R + x,$$

______________________________________________________________________

Downloaded from http://royalgovernments publishing.org/article_pdf/109/109/300/307/page.109.306.pdf
by guest on 22 May 2021

# Fragmentation of shell cases 307

where $c_R$ is defined by

$$\int_{c_R}^{\infty} BV dc \exp \left[ -\frac{(c-c_0)^2}{2\tau^2} \right] = 1. \tag{9}$$

Neglecting terms in $x^2$, it is found that

$$(c-c_0)^2 = (c_R-c_0)^2 + 2x(c_R-c_0), \tag{10}$$

and, using this approximation, (9) gives

$$\frac{(c_R-c_0)^2}{2\tau^2} = \log_e \left( \frac{BV\tau^2}{c_R-c_0} \right).$$

Now from (8), integrating over all values of $c$, it is clear that $\tau B$, apart from a numerical factor of order unity, is equal to the total number of weak points per unit volume. This is denoted by $N$, and $N$ is assumed to be a very large number. Thus the error will be small if

$$\frac{(c_R-c_0)^2}{2\tau^2} = \log_e (NV). \tag{11}$$

If (10) is substituted in (8), then

$$\text{const. } dx \exp \left[ -\frac{c_R(c_R-c_0)}{\tau^2} \frac{x}{c_R} \right]. \tag{12}$$

A broad distribution of values of $c$ will be assumed, so that $\tau$ and $c_0$ are of the same order of magnitude. Thus from (11) $c_R \gg c_0$. Hence approximately

$$\frac{c_R(c_R-c_0)}{\tau^2}, \frac{(c_R-c_0)^2}{\tau^2} = 2 \log_e (NV).$$

Thus the chance that the material contains a weak point with parameter $x$ between $x$ and $dx$ is, if $x$ is small

$$\text{const. } dx \exp \left[ -2 \frac{x}{c_R} \log_e (NV) \right].$$

If the stress-strain curve for the material in tension is

$$P = f(s),$$

the constant $\gamma$ is thus

$$\gamma = -2 \log(NV) \frac{dc}{c dP} \frac{dP}{ds},$$

which gives from (7)

$$\gamma = 2 \log(NV) \frac{1}{n} \frac{d(\log P)}{ds},$$

If the stress-strain curve for large strains is of the type

$$P = P_1 + P_2 \log (1+s),$$

this gives

$$\gamma = 2 \log(NV) \frac{1}{n} \frac{P_2}{P_f} \frac{1}{1+s_f},$$

where $P_f$ is the true stress and $s_f$ the plastic strain at fracture.

For $n$ the most likely hypothesis will be to take $n = \frac{1}{2}$, as for Griffith cracks, but obviously other values are possible. The value of $N$, also, can only be guessed; it

______________________________________________________________________

Downloaded from http://royalgovernments publishing.org/article_pdf/109/109/300/307/page.109.307.pdf
by guest on 22 May 2021

308 N. F. Mott

may be bound up with the dislocations in cold-worked metals, which are of the order $10^{-3}\text{ cm.}$ apart. Fortunately, since $N$ occurs in a logarithm only, the exact value is not important. If $N = 10^{13}$, then, if $V$ does not differ by more than a few powers of 10 from $1\text{ c.c.}$,

$$\gamma \sim 160 P_y / P_f(1+s_f).$$

Some values of $P_y, P_f, s_f$ have been deduced below from curves given by Körber & Rohland (1924):

| material   | reduction in area | true U.T.S. $P_f$ ($\text{kg./mm.}^2$) | $P_y$ | $\gamma$ |
| :--------- | :---------------: | :------------------------------------: | :---: | :------: |
| iron       |       0.83        |                   54                   |  34   |    20    |
| steel 0.1C |       0.70        |                   70                   |  42   |    42    |
| 0.25C      |       0.63        |                   80                   |  45   |    53    |
| 0.45C      |       0.57        |                   82                   |  38   |    67    |

For mild steel, then, according to the formulae of $\S 2$, a bomb of the design suggested there would give fragments of average length 0.6 in.

Referring to formula (5), and assuming that $\log N$ is about the same for all materials, it is seen that the average fragment length is proportional to the following term which depends on the properties of the material:

$$P_f \sqrt{\left(\frac{1+s_f}{\rho P_y}\right)}.$$

Thus a material with a high-stress $P_f$ at fracture gives large fragments, and a high ductility ($s_f$ is the strain at fracture) also gives large fragments. A rapid rate of hardening near the fracture point (i.e. a large value of $P_y$) will lead to small fragments. Since most metals harden much more rapidly in the initial stages of cold work, low ductility will for this reason also lead to small fragments.

This work was carried out while the author was working in the Ministry of Supply and he wishes to thank the Director-General for Scientific Research and Development for permission to publish it.

### REFERENCE

Körber, F. & Rohland, W. 1924 Mitt. K.-Wilh.-Inst. Eisenforsch. 8, 55. (See also Körber, F. & Krisch, A. 1934 Handbuch der Werkstoffprüfung, 2, 44.)

______________________________________________________________________

Downloaded from http://royalgovernments publishing.org/article_pdf/109/109/300/307/page.109.308.pdf
by guest on 22 May 2021
