# Research Report
# Of
SC-RR-7P-790
DECEMBER 197O
GURHEY ENERGY OF EXPLOSIVES:
ESTIMATION OF THE VELOCITY AND
IMPULSE IMPARTED TO DRIVEN METAL
J. E, KEINNEDY, 5133
# ^T^SZ-
This is a SANDIA CORPORATION working paper and is intended primsirily for internal distribution; the ideas expressed herein do not necessarily reflect the opinion of the Corporation.
ThJB memi>r««4vHiru produced wlthoi express-wrtttfflS^eSaiasioo of SANDIA, S B B P O R A T I O N .
# MASTER
In . 5 UNLIMITED
# SANDIA LABORATORIES
OPERATED FOR THE UNITED STATES ATOMir ENERGY COMMISSION BY SANDIA CORPORATION} ALBUQUERQUE. NEW MEXICO LIVERMORE CALIFORNIA

NOTICE
This report was prepared as an account of work sponsored hy the United States Government. Neither the United States nor the United States Atomic Energy Commission, nor any of their employees, nor any of their contractors, sub- contractors, or their employees, makes any warranty, express or implied, or assumes any legal liability or responsibility for the ac- curacy, completeness of usefulness of any in- formation, apparatus, product or process dis- disclosed, or represents that its use would not infringe privately-owned rights.

## DISCLAIMER
## This report was prepared as an account of work sponsored by an agency of the United States Government.  Neither the United States Government nor any agency Thereof, nor any of their employees, makes any warranty, express or implied, or assumes any legal liability or responsibility for the accuracy, completeness, or usefulness of any information, apparatus, product, or process disclosed, or represents that its use would not infringe privately owned rights.  Reference herein to any specific commercial product, process, or service by trade name, trademark, manufacturer, or otherwise does not necessarily constitute or imply its endorsement, recommendation, or favoring by the United States Government or any agency thereof.  The views and opinions of authors expressed herein do not necessarily state or reflect those of the United States Government or any agency thereof.

# DISCLAIMER Portions of this document may be illegible in electronic image products.  Images are produced from the best available original document.

SC-RR-70-790
Gurney Energy of Explosives:
Estimation of the Velocity and
Impulse Imparted to Driven Metal*
J. E. Kennedy
Sandia Laboratories
Albuquerque, New Mexico 87115
December I97O
- N O T I C E - This report was prepared as an account of work sponsored by the United States Government. Neither the United States nor the United States Atomic Energy Commission, nor any of their employees, nor any of their contractors, subcontractors, or their employees, makes any warranty, express or implied, or assumes any legal liability or responsibility for the accuracy, com- pleteness or usefulness of any information, apparatus, product or process disclosed, or represents that its use would not infringe privately owned rights.
ABSTRACT
The Gurney method, which yields simple equations for evaluating the velocity of metals driven by detonating explosives in many geometries, is reviewed. The method is extended by relating the specific impulse of an explosive to its Gurney energy parameter, and by noting that for most explosives the Gurney energy is a nearly constant proportion of the chemical energy. Several diverse examples illustrate application of the Gurney equations in the utilization of explosives.
* This work was supported by the U. S. Atomic Energy Commission.
BTED
DISTRIBUTION OF THIS DOCUMENT IS 11:

ACKNOWLEDGMENTS
Suggestions by Dr. Fritz Herlach of the Illinois Institute of
Technology provided the incentive for developing these extensions of the
Gurney method. Helpful discussions concerning applications with T. J.
Tucker and E. C. Cnare of Sandia Laboratories are also acknowledged.

1. INTRODUCTION
The motion of metal driven by detonating explosive can be very
1 2 accurately calculated by complex computer codes ' using detonation pro- duct equations of state which have been calibrated to reproduce precise
2 3 experimental data. ' On the other hand, the Gurney method for estimating
the velocity imparted to a metal by an explosive is simple and approximate
(nominally IC^ uncertain).
The method, based on energy and momentum balances, was devised in
19^3 ^y R- W. Gurney of BRL to correlate fragment velocities from
artillery shells and grenades of widely varying sizes and proportions.
It is a simple, but rational, approach to explosive system performance
calculations in which the main interest is the final velocity imparted
to the metal elements. Calculations done by this method show excellent
correlation with experimental data, in spite of two gross assumptions
made to obtain mathematical tractability.
The Gurney method is reviewed in detail in the next section of this
report, and equations resulting for several simple geometries are given.
We then derive a relationship between the Gurney energy and the specific
impulse of an explosive. An empirical basis for estimating the Gurney
energy of an explosive from calorimetric data is suggested in Section 3-
Finally, examples are given to show that the Gurney method can be
profitably used in many diverse engineering applications, principally
because the equations permit direct calculation of the effect of changing
the value of any system parameter.

2. THE GURNEY METHOD
The Gurney method may be applied to any explosive/metal system with a
cross-section admitting one-dimensional translational motion of the metal
normal to its surface, regardless of the direction of detonation propaga-
tion. A specific energy, E(in kcal/g), with a characteristic value for
each explosive, is assumed to be converted from chemical energy in the
initial state to kinetic energy in the final state. This final kinetic
energy is partitioned between the metal and the detonation product gases
in a manner dictated by an assumed linear velocity profile in the gases.
Figure 1 illustrates such a gas velocity profile for a cylindrical charge
in a metal tube. The velocity of the metal is assumed to be constant
throughout its thickness. The velocity of each gas element and metal
element is taken to be normal to the axis.
Metal, M = total mass in
the given length
# vfr.r„) = v
Detonation product gases, C - total mass in a given length
## vCr)
# v(0) = 0
Centerline
FIG, 1
Linear Gas Velocity Profile,
Based on these assumptions we can write an energy balance for any
simple geometry which can be easily integrated to provide an analytical
expression for the final metal velocity v as a function of Gurney specific

energy, E, and the ratio of total metal mass to total explosive mass, M/C,
In addition, asymmetric one-dimensional configurations such as a sandwich
of explosive between layers of metal of differing thickness require a
momentum balance, which is solved simultaneously with the energy balance.
The quantity M/C is dimensionless because it is the ratio of the total
metal mass to the total explosive mass in a metal/explosive assembly. For
purposes of calculating M/C it will often be convenient to consider a
representative volume element of the assembly. This could be the volume
normal to a unit area for a flat configuration; a unit length or a solid
sector for a cylindrical configuration; or a spherical sector or spherical
wedge for a spherical configuration.
While some assumptions upon which the Gurney method is based indeed
deviate significantly from reality, these deviations usually affect the
correlation only at extreme values of M/C (i.e., M/C > 10 or M/C < 0.2).
Restrictions on the range of applicability of the Gurney methods due to
the assumptions are collected and discussed later in this section. At
this point, allow us to develop the equations which result from these
assumptions, for various simple geometries. As sketched in Fig, 2, the
velocity distribution in the detonation product gases as a function of
Lagrangian position* y is
V (y) = (v + v) ^^^ V (l) gas^-^' ' o ' y^
*Coordinate positions are identified with particles rather than spatial position, A given particle is assumed to move at constant speed at all times in constructing energy and momentum balances.

V = V gas,max o
Velocity distribution, V .(y) 2;as
# TV
V = 0
Explosive ' ^ ^ /_ C = mass/unit area
v \ \ Metal p l a t e , M = m a s s / u n i t a r e a \ \ \ \ \ \ \ \ \ \ \
V = V m e t a l
FIG. 2
Assumed Velocity Distribution in Open-Faced Sandwich Configuration.
and the velocity of the metal plate is v across its entire thickness. The
initial thickness and density of the explosive are y^ and p^, respectively.
Energy and momentum balances for a unit area may be written respectively as
1 (v + v) ^ - V dy (2)
1 2 CE = I Mv +
and
0 = -Mv - Pe/"'° [('o - ' ) f; - ] ^y (3)

Integration of these equations and substitution of M/C for the equivalent
ratio M/P y yields
•1/2
1 + 2' M\
V = ^
## W
M ^ C
and
^ = 2 ^ + 1 . (5) V C
2.1 Gurney Equations
Henry provided a comprehensive review of the Gurney method and
derivation of many formulae. Gurney equations for some common symmetric
and asymmetric configurations are presented in Fig. 3. The quantity ^/2^
occurs in each expression; its units are velocity and it is known as the
Gurney characteristic velocity for a given explosive. The ratio of final
metal velocity v to the characteristic velocity /\/§E is an explicit function
of the metal to charge mass ratio, M/C, and, in the case of the asymmetric
sandwich where the second plate may be considered to be a tamper, is a
function also of tamper mass to charge mass ratio, N/C. In all cases the
velocity derived is that of the metal plate M.
Figure k presents a plot of the dimensionless velocity, •v/j2^, of
metal M as a function of the loading factor M/C for the geometries shown
in Fig. 3. Values of the Gurney velocity, V^E, are tabulated for several
common explosives in Sec. 3 of this report, hence Fig. k can be used
directly to estimate the metal velocity to be expected from any given
explosive/metal system of simple geometry.

SYMMETRIC CONFIGURATIONS
Flat Sandwich:
-1/2
# \\\\\\\\\\\miM/2
V
(6)
C (explosive) /2E l \ \ \ \ \ \ \ \ \ \ W s ^ M / 2 (metal) = [i^i]
Cylindrical Case;
# U////////T7T2
-1/2
(7)
## /2l L^ 2j
# n n f / f n-rrry M
Spherical Case;
-1/2
(8)
ASYMMETRIC CONFIGURATIONS
Open-faced Sandwich:
-1/2
# r
M ^ C
# (M
# ezzzzzzzHzzzzzj
/2E t Ff
Asymmetric Sandwich:
# (--^) KWWNWWWI
M 1 + 2 ^
Define A =
V
3
# { c V//////////MZZ 1-1/2 1 + A-^ N 2 M 3(1 + A) + C ^ ^ C (9)
/2E .
N _ total tamper mass C ~ total explosive mass
Symbols; M total metal mass C "" total explosive mass '
V = metal velocity
Gurney energy, E = kinetic energy/unit explosive mass
FIG. 3 Gurney Equations for Common Geometries

# h
—1
11111II1 mil'
1.6
i; 1' 1 I I I ' M njm
TMllKI'lI uiic +-. [ 1 n
X
1 { ' 1: 1 I I I s a ! M
MSN-
I . I ll tllTlttif SYMMEQ
### s
1 |i 1 lUi 1 :RIC"LB •;' t .CH ll "' • r
MWW ' siintiifn
1 1 S s L J "> >L ^ N - Irr^ P T V L
1.2
1 il rr4-
1
rj"H ]]]"
M I M I I I I IIIIIIII ~ L i 11 1 1 1 mWUIiiliMLIJiiK ',/- ui. 3- •• ff > I Ba S ' !' ? S ! -ilZ^^
1 ' 1 ' LIT
0.8
1 1 M l 1 1
```
S A N D W : rn^ ' ' 1 jlllHm'klliJlH- ll • ^ m Ifr ^*44i.i!ii iii!^ «.' II ,s'sii' 'iff $'5j^'5 n [ t IJ.'^ t ; ,, L -illlBjy ::., ,:: L! r I M iinlnit''!. '•'•W TTrmllliff fl • 1 \\\\ r 1 lllllilllli'l' M h J l i qprnro-p, ' ; 11
```
>
^ <JHJ rSstsL ps^v p4> M i
'^^ 'A i > tu • fflf'
1 ll IM! II
### Fir
# iJ iSfe.. jl 1-^ . - Ml
N^ 1
1 ' s
' 1 1 1 C
X.
[' i n riiii )PEN-F SANDW
A G E D [ TrtiT L l U H '[t
Irs. 1 1 1
## "ll ' ij J u
0.4
i
MW
t m
xU
1 1 ll m i
i 1 1 1 1 1 1
rrrriiJ i urrtL 11II11II Ii •
LL 1 L L
J 1 ' l,,l
! ': ':'!
1 1 M M I , i l . i i , , , ! ' . !
1 I I I ,
' j
i l l 1 1 1 1
1 1
II IHIIIIIIIIIII
7 10
.2 .7 1. M/C
FIG. h
Dimensionless Velocity of Metal as Function of Loading Factor M/C.

The calculated velocity of the driven plate in an open-faced sandwich
configuration is plotted in Fig. 5 as a function of M/C for a few common
explosives. Estimates for other explosives can be read from the graph
by interpolation between curves based on appropriate values of v^E.
Equations can be derived for other geometries and conditions by use
of the Gurney model,
2.1.1 Division of Gas Flow. The partitioning of gas flow in the symmetric
sandwich configuration is obvious -- half the detonation product gases
flow in the direction of each metal plate. However, for asymmetric sand-
wich configurations, the proportion of gas flowing in the direction of
plate M varies with M/C and N/C. In view of the linear velocity profile
assumed for constant-density gases in the Gurney method, the proportion
of the total detonation product gases which flows in the direction of
plate M may be seen to be v /(v + v ). The two velocities, v.. and v^, ,
M N m IVI N
may be evaluated by individual applications of Eq. (9). For an open-
faced sandwich, the proportion of gas flowing in the direction of plate
M is found to be "^/(v + v ), which may be evaluated from Eqs. (h) and (5).
2.1.2 Range of Applicability. A restricted range of applicability pertains
for the Gurney method as a result of the simplifying assumptions made
explicitly or implicitly in the model. Effects of many of these assumptions
and limitations are presented briefly in Table 1.
The Gurney assumption of a linear velocity profile of constant density
detonation product gases is a substantial departure from gasdynamic theory,
and merits additional attention. This assumption introduces the largest
errors in configurations involving a free explosive surface such as the
open-faced sandwich, for which the Gurney approach may overestimate the

TABLE 1 APPLICABILITY OF THE GURNEY APPROACH
RESTRICTION
REMARKS AND RECOMMENDATIONS j
1. Range of M/C Ratio
Henry recommends restriction to the range 0.2 < M/C < 10 for velocity calcula- tions. Impulse calculations may be done if M/C > 0.2 on basis of data from Ref. 1.
2. Acceleration Phase
Gurney method is not capable of analyzing motion during acceleration. Accelera- tion is completed after detonation products have expanded to twice that original charge volume for normal incidence of detonation onto metal, or to seven times original charge volume for grazing incidence onto metal (see Appendix B ) . The metal will reach its calculated velocity only if no external forces of inter- actions are applied during acceleration.
3- Direction of Detonation Propagation
Detonation drives metal at a given velocity, within a few percent, for a given M/C regardless of the angle between the detonation front and the metal surface.15 The direction in which the metal is driven will vary slightly with the angle (see Appendix A).
h. Gas Velocity
Profile Inaccuracy
Assumed linear velocity profile and constant density are gross oversimplifica- tions. Ignoring effects both of rarefaction waves and of pressure peaks near the metal appear to be cancelling errors.5 See text concerning effects of free explosive surface.
5- One-dimensional Motion
Approach cannot be used to estimate variations in local velocities of a plate driven ty a charge with a steep taper in its thickness. Some averaged value of M/C could be used to estimate final velocity of entire plate.
6. Metal Strength Effects
No forces exerted by the metal to oppose deformation are considered, other than inertia. Hoop stresses in cylinders and spheres can reduce metal velocity by a few percent2 at moderate M/C values (~ 2.5) in explosions, and by a greater amount ^'n implosions.-'-3
7. Metal Spallation
May occur when M/C < 2 for high density explosives and metals. Can be avoided by spacing charge a few millimeters from metal, with very little decrease in metal velocity.1
8. Early Case Fracture
Leakage of product gases through fractures in the metal case can decrease the final metal velocity by no more than 10^, the value calculated for a case composed of preformed fragments.-*
M

### 4 K
### _J..
PBX.,9l^.0l^. Charge; / 2 l " = 2.90 ram/jisec
. . . j —
COMP B Charge; / S E 2.71 mm/|isec
1.
•TNT Charge; /aE '-2.37 mm/|isec I
I -H4H
i I
i 1
10
I ,.L- .4
.7 1. M/C
FIG. 5
Driven Metal Velocity for Open-Faced Sandwich.

metal velocity (and impulse) by as much as 7^- Henry employed a variable
pressure profile of a simple mathematical form in the detonation products
in an attempt to reduce this discrepancy. He concluded that the additional
mathematical complexity, which was inconsistent with the Gurney philosophy
of simplicity, was not justified by the small improvement achieved in
accuracy,
2,2 Impulse Estimation
Since the Gurney method provides an estimate of the final velocity
imparted to an explosively loaded body, the total momentum c//i^of the body
can be readily calculated as the product of the body's mass and velocity.
We divide by the total charge mass C to derive the specific impulse
delivered by the explosive,
I = ^//C = ^ V . (10) sp ' C
2,2,1 Specific Impulse of Unconfined Surface Charges, Explosive is often
detonated directly on the surface of a very heavy body in order to deliver
a desired impulse for testing purposes. If we consider the loaded body to
be rigid, all detonation gases will flow away from the surface and maximum
specific impulse will be delivered to the body. For a very large body
mass to explosive mass ratio, M/C » 1, Eq, (J+) reduces to
# - v ^ • VI S • ^^1)
By utilizing this expression for v in Eq, (lO), the relationship for
specific impulse is found to be
I ~ VI. 5 E , (12) sp

Upon detonation of an unconfined surface charge as described above,
essentially all the gas must flow backward away from the plate. Because
the gas is perfectly confined on the metal side in this configuration, the
peak backward velocity v along the linear gas velocity profile should
assume a maximum value. By equating the specific momentum of this flowing
gas to the specific impulse driven into the metal according to Eq, (l2),
C V /2 — ^ — = 1 = VI. 5 E , C sp '
we derive a relation for the maximum free gas velocity:
\ , m a x = ^ ^ ' (^3)
2.2,2 Impulse Modification by Tamping. The impulse imparted to a body by
detonation of explosive at a given areal density (grams explosive/cm of
body surface) can be increased by tamping the explosive with an outer layer
of metal. The Gurney method can be used to estimate the change in impulse
as a function of tamper areal density. If the heavy body surface is con-
sidered to be rigid, it resembles the symmetry plane in a symmetrical
sandwich configuration. The velocity of the tamper plate will then be
given by Eq, (6), where the tamper to explosive mass ratio N/C is taken
to represent M/C, The impulse imparted to the heavy body per unit mass
of explosive will be equal to the momentum of the tamper and the gas
following it. The effective specific impulse of the explosive when the

tamping ratio is N/C can be shown to be
Note that when no tamper is present (N/C = O), this expression reduces to
that for an untamped charge as given in Eq. (I3).
3. GURNEY ENERGY OF EXPLOSIVES
Table 2 lists Gurney velocities calculated from data given for care-
fully conducted experiments in which there were no end losses and no gas
leakage through metal walls until after their acceleration was completed.
Occurrence of end losses (e.g. charges in short tubes, L/D < 6, with open
ends) or early fracturing of driven metal may decrease the effective
value of v ^ by 10^ to 20^ or more. Values of specific impulse calculated
from Gurney velocities are also tabulated in Table 2,
Explicit forms may be derived to express efficiency of energy transfer
from explosive to metal. Let us define efficiency, e, as the ratio of the
kinetic energy of plate M to the explosive energy which is the product of
the heat of detonation, AH , of the explosive and the charge mass, C. By
introducing the Gurney energy E and rearranging, we derive the following
expression:
2
/'v/V^\
~ 2CAH, • E d
d

TABLE 2
ENERGIES AND SPECIFIC IMPULSES OF EXPLOSIVES
E/AH^
k c a l / g (Ref. )
Explosive
ram/nsec ( R e f . )
s p ' p k t a p s / ( g expl./cm ) ( R e f . )
k c a l / g
RDX
0.61+
0.96
2.83 (5)
21+5
1.51 (11)
1.09 (10)
TNT
0.67 0 . 7 1
205 211
2.37 (2) 2.1+^ (5)
0.61 0.65
1.20 (11)
Comp. B
0.87 0.91 0.87 0.86
0.72 0.76 0.72 0.72
235 21+0 231+ 232
2 . 7 1 (2) 2.77 (1) 2.70 (7) 2.68 (5)
HMX
1.06
1.1+8 (10)
0.72
2.97 (2)
257
PBX-914-Ol;
0.7I+
1.01
2.90 (2)
251
1.37 (11)
PETN
1.03
251+
0.69
2.93 (2)
l.i+9 (9)
EL506D
2.28
0.62
197 (8)
EL506D,* Reconstituted
ll+l (8)
0.32
1.63
NM
2.1+1 (2)
209
0.56
1.23 (10)
0.69
*Density assumed to be 1.1*6 g/cm .
NOTES: 1. The following identities pertain for conversion from velocity to specific impulse units in the context of quantities in this table:
1 mm/nsec = 10 dyn-sec/g explosive.
1 mm/|j.sec = 10 taps/(g explosive/cm ).
2. Corrections were applied to the data of Refs. 1 and 2 as discussed in Appendix A to estimate the true speed of the metal before calculating Gurney energy, E.
3. Eq. (12) was used to calculate values of I from values of -V/SE, or vice versa. ^

The first term of the result is the fraction of the Gurney energy which is
in the form of kinetic energy of plate M, and this term is solely a
function of M/C (and N/C where applicable). We can evaluate this term
immediately for any given configuration, using the appropriate form for
V/A/^E for the geometry of interest.
The second term, E/AH,, is the ratio of Gurney energy (the total
kinetic energy in the direction of metal motion) to chemical energy of the
explosive. Since chemical energy data are available for many explosives
for which Gurney velocities have not been measured, we should like to
devise a method for estimating the value of this ratio of Gurney energy
to chemical energy. For chemical energy we shall use experimental values
of heat of detonation, where available.
Values of Gurney energy E in kcal/g and heat of detonation AH, are
tabulated in Table 2 for several explosives. The ratio E/AH, is observed
12 to lie in the range from O.6I to O.76 for all explosives reported, except
for nitromethane (NM) for which the ratio was O.56. In the absence of
suitable performance data from which to calculate E, one might estimate
that
E =s 0.7 AH . (16)
A series of one-dimensional computer calculations was conducted to
determine whether the efficiency of conversion of chemical to kinetic
energy was a sensitive function of the properties of an explosive. Those
calculations are explained and their results are presented in detail in
Appendix B. In summary, the calculations indicated only a slight
dependence of conversion efficiency on the equation of state and sound
speed of the detonation products. The slight trends indicated by those

calculations with a constant-7 law equation of state are in fact contrary
to the slight trends indicated in the experimental data. It is concluded
that an equation of state more accurate than the constant-7 law is needed
to permit interpretation of fine details of energy transfer, but that
Eq. (16) remains a satisfactory method for estimating E or E/AH .
k. DESIGN APPLICATIONS
Equations (1+) and (6) through (9) represent the metal velocity v as
functions of A/^E, M/C, and N/C for some simple symmetric and asymmetric
system geometries. This section discusses diverse engineering applications
of these relations, to illustrate the range of problems that can be treated
by the Gurney method. General areas include parametric studies of the
effects of given variables, scaling laws, and efficiency of energy conversion.
k.l Parametric Studies
4.1.1 Tamping Effectiveness. The form of the Gurney equations (explicit
in Y/AJ2E) is well suited to directly reveal the effect of a change in
configuration (i.e. M/C or N/C) upon the velocity imparted to metal. The
effectiveness of a metal tamper plate N in an asymmetric sandwich (Eq.
(9)) in increasing the velocity of plate M is calculated as an example.
Fig. 6 is a plot of the proportionate velocity increase of plate M due
to tamping for various loading ratios M/C. The figure illustrates that
tamping a relatively heavy charge (M/C = 0.2) increases the velocity of
plate M by very little, whereas adding tamping to a light charge (M/C = 5 )
increases the velocity considerably, particularly in the range of N/C < 5.

" ^
M/C = 5
OJ 2.0
—
P
## — y
M/C = 1
M/C = 0 . 2
1 1 1
1,0
## L. 1
1 2 J+ 6
10
N/C, tamping factor
FIG. 6
Effectiveness of Tamping in Increasing Metal Velocity
4.1.2 Efficiency of Energy Conversion. For the same problem discussed
above, let us calculate the efficiency of conversion of chemical energy
of plate M to kinetic energy. Eq. (15) presented an expression for this
overall efficiency, e, which we rewrite here for convenience.
e = (v/v^)^ M
## M: (15)
The second factor of this expression, E/AH , is constant for a given
explosive; it can be calculated directly from experimental values of both
E and AH , or can be estimated to be O.7 according to Eq, (16), The first
term in the expression, denoted as e , represents the fraction of the
Gurney energy (total kinetic energy of gas and metal) which is delivered

to one driven metal plate M; this term is a function of M/C and N/C (which
may alternatively be expressed as N/M) for an asymmetric sandwich
configuration and can be evaluated with the aid of Eq, (9). Variation of
e as a function of C/M and N/M for an asymmetric sandwich is illustrated
in Fig, 7, in a form following that used by Hoskin et al. The condition
N/M = 0 corresponds to a bare charge, N/M = 00 corresponds to a rigid rear
support of the charge (or symmetry plane). Efficiency is seen to be
strongly influenced by the tamper ratio at low values of C/M, but very
slightly at high values of C/M where the efficiency decreases because of
the large amount of kinetic energy remaining in the large, moving gas cloud.
i+,2 Scaling
Circumstances and configurations often arise in the utilization of
explosives which do not permit direct application of a Gurney equation.
Perhaps an explosive is to be used for which neither E nor AH is known,
or significant two-dimensional (edge loss) effects may be present which
will degrade performance substantially.
In such cases it is recommended that metal velocity and M/C measure-
ments taken in the first shot of a series be utilized to calculate an
effective value of v ^ , based on the equation of the nearest "ideal" one-
dimensional geometry as sketched in Fig. 3- This effective value of ^J2^
will usually be no more than 30^ lower than the ideal value. The effective
value of -s/§^ can than be used to estimate the metal velocity when the value
of M/C is changed.
Effective use of scaling in configurations with substantial end losses
7 is illustrated in the following two examples, Weinland has correlated
the effective value of v^E with the L/D ratio of open-ended tubes filled

NOTES: 1, Observe that abscissa, C/M, is inverse of loading factor generally used in this report.
2, This figure has been reproduced from Hoskin et al, with addition of the two center curves. Calculated points were obtained by Hoskin using constant-/ law.
FIG, 7
Efficiency of Kinetic Energy Partitioning to Plate M in Asymmetric Sandwich.
21

with explosive. For tubes of large L/D, the value of ^/^ is the limiting
or ideal value quoted in Table 2, whereas the effective value of v§E
decreases at an increasing rate as L/D is reduced below 6, The decrease in
in effective value of v ^ ™3-y "be estimated from this equation derived by
the author to describe Weinland's data, for L/D > O.5,
V^^.p .,. = ^/^.^ , (1 - 0,36 e-°'^^^/^) , (17) effective ideal
As a second example, the implosive collapse of thin-walled cylindrical
tubes driven by an explosive charge wrapped about the tube exterior was
13 treated by use of the Gurney open-faced flat sandwich equation by Kennedy,
There were significant edge losses from the rather short length wrapped
with the charge. For two experiments in which the value of M/C was changed
by kO'fo, the effective values of v§E calculated from the measured velocities
agreed within ifo, although the values of A^^E were 20^ lower than that
pertaining to the same explosive in configurations free of edge losses.
Those experiments demonstrated that the open-faced sandwich equation with
an effective value of v ^ determined by a single experiment represented a
good scaling law. After completion of the explosive acceleration of the
tube walls, a progressive decrease in kinetic energy of the walls also
occurred as a result of plastic work done upon the walls in dynamic
deformation,
4.3 Direction of Metal Projection
In the derivation of Gurney equations, it is assumed that the metal
moves in a direction normal to its surface. This is true when the
detonation wave encounters the metal at a normal angle of incidence, but
is not true when the metal is driven by "grazing detonation," which
propagates parallel to the metal surface.

A derivation presented in Appendix A shows that the angle at which
the metal is driven by grazing detonation is halfway between the normals
to the axis and to the deflection angle of the liner as detonation pro-
e gresses along the charge. The angle of projection, ^, is
e . -1 V 2 = ^""^ 2D
off the normal to the original metal surface, in the direction of detonation
1,12 propagation.
When detonation strikes the metal surface obliquely, at an angle
between 0° (grazing or parallel incidence) and 90° (normal incidence), the
metal is projected at an angle between 90° and (90° - — ) ,
c
4,4 Propellant Charges
The Gurney approach may be used also for interior ballistics problems,
in which a propellant or a pyrotechnic charge drives a mass. The
appropriate equation for projection of a bullet or shell from a gun,
including the recoil effect, is that for the asymmetric flat sandwich,
Eq, (9), in which the projectile mass is M, the propellant mass is C, and
the gun mass is N, Note that if the gun mass is taken to be infinite,
recoil is absent and use of the symmetric sandwich equation is appropriate.
Effective Gurney energy values have been determined for some propellants
in the presence of barrel friction or rifling; for example, v ^ = 1.7 mm/|j.sec
for smokeless powder and A;5E = 0.94 ram/|j.sec for black powder. Gurney energy
values may be calculated from almost any performance data, and have been
2

found to apply to systems of similar design but widely different loading
factors (M/C), as a scaling law should.
5. SUMMARY
The Gurney method results in explicit algebraic equations for
estimating the velocity imparted to metal in contact with detonating
explosives. Gurney equations have been presented for several simple
explosive/metal system geometries. Specific impulse of an explosive has
been related to the Gurney energy of the explosive, and values of both
these parameters are tabulated for several high explosives. The Gurney
energy of an explosive may be empirically estimated from calorimetric
data if suitable performance data on the explosive are not available.
The Gurney method can be applied to many design problems involving
the utilization of explosives. Examples have been given to illustrate
this point.

REFERENCES
N, E, Hoskin, J. W. S. Allan, W. A. Bailey, J, W, Lethaby, and I, C,
Skidmore, "The Motion of Plates and Cylinders Driven by Detonation
Waves at Tangential Incidence," Fourth Symp, on Detonation,
ONR ACR-126, 14-26, I965.
J, W, Kury et al, "Metal Acceleration by Chemical Explosives," Fourth
Symp, on Detonation, ONR ACR-126, 1-13, 1965.
M, L, Wilkins, B, Squier, and B, Halperin, "The Equation of State of
PBX-9404 and LX04-01, "UCRL 7797, Lawrence Radiation Laboratory, 1964,
R. W. Gurney, "The Initial Velocities of Fragments from Bombs, Shells,
and Grenades," BRL Report 405, I943.
I. G. Henry, "The Gurney Formula and Related Approximations for High-
Explosive Deployment of Fragments," presented to the A.O.A., April,
1967. AD813398, Hughes Aircraft Co., Report No. PUB-I89.
M. De'fourneaux and L. Jacques, "Explosive Deflection of a Liner as a
Diagnostic of Detonation Flows," Preprints, Fifth Symp. on Detonation,
ONR Report DR-I63, 347-55, 1970.
C. E. Weinland, "A Scaling Law for Fragmenting Cylindrical Warheads,"
NWC TP 4735, April, I969.
R. P. May, R. G. Biesecker, and E. G. Young, "Determination of the
Specific Impulse, Pressure-Time Profile, and Explosive Reflection
Characteristic for a Reconstituted Sheet Explosive," SC-DR-70-432,
August, 1970.
D. L. Ornellas, J. H. Carpenter, and S. R. Gunn, "A Detonation
Calorimeter and the Heat of Products of Detonation of PETN," Rev. Sci,
Instr, 37, 907 (1966),

D. L. Ornellas, J. Phys. Chem. 22, 2390-239i+, I968.
D. L. Ornellas, Private Communication, 1970.
F. Herlach in private communication, 1969^ pointed out that Reference
1 data indicated 75^ conversion of chemical to kinetic energy for
Composition B, and suggested the form of the metal projection model
in Appendix A.
J. E. Kennedy, "Explosive System Design for Magnetic Flux Compression
by Implosion," Dissertation, 111. Inst, of Tech., Chicago, 1970-
¥. Herrmann, P. Holzhauser, and R. J. Thompson, "WOWDY-A Computer
Program for Calculating Problems of Motion in One Dimension,"
SC-RR-66-601, Feb., 1967.
E, L. Lee and H. Pfeifer, "Velocities of Fragments from Exploding
Metal Cylinders," UCRL 505^5, Jan. 6, I969.
C. L. Mader, Los Alamos Scientific Laboratory Report LA-2900, I963.

APPENDIX A
Direction of Metal Projection
The one-dimensional Gurney analysis assumes that the metal moves in
a direction normal to its surface. For some applications it -will be of
interest to determine the small angular deflection from the normal vhich
pertains for grazing (parallel) incidence of detonation to the metal
surface.
Figure 8 depicts grazing detonation driving a metal plate. Accelera-
tion of the plate to its final velocity is assumed to be instantaneous for
purposes of analysis. The plate is deflected at an angle 0 to its rest
plane.
At steady state, the plate is assumed to undergo no net shear flow,
and therefore •will undergo no change in length or thickness as a result of
being launched. This requires that the plate element that was at point P
at rest will be at point P' after launch and that
AP = AP^
where the superior bar ( ) denotes length between two points. Next, we
construct a line from A normal to line PP'. Note that this bisects angle
6, since APP' is an isosceles triangle. We can now recognize that
V = 2D sin I . (18)
A first order estimate of the actual direction in which metal is projected
is the angle — which can be evaluated from Eq. (l8) by knowledge of v and
D. Gurney Eq. (ij-), (6), or (9) can be used to estimate v from knowledge
of M/C, W/C, and E. As the plate travels, it will be tilted at an angle
9 to its rest position and, according to this model, will not be rotating.

Air shock front Product gas boundary
Detonation front
Original '
Detonation velocity, D
Original metal position
/
FIG. 8
Direction of Metal Projection by Grazing Detonation.
28

In measuring the velocities of plates driven by grazing detonation it
is more convenient to measure components of velocity other than that along
PP'. With a streak camera set perpendicular to the rest plane or charge
2 axis, an "apparent velocity" v has been measured by Kury et al. This
quantity can be related to v by geometry.
V = D tan 6 . (19) a
v/v = cos 6/cos — . (20) a £_
Hoskin et al have expressed their results in terms of v , the
velocity component normal to the flight plane of the plate, since this
velocity component is of interest when the flying plate is used in impact
studies. Noting that the angle between v and v is 9, geometry again
allows us to relate v and v .
n
V = D sin 9 . (21) n
v/v = sec - . (22) ' n 2
The difference between v, v , and v , are in most cases only a few
' n' a' "^
percent. Where data have been extracted from Ref. 1 or Ref. 2 and listed
in Table 2, this correction has been made and the velocity v has been used
in calculating E in all cases.

APPEKDIX B
Effect of Detonation Product Equation of State on Efficiency
Hoskin et al, correlated their experimental results for tubular
cylinders and flat plates driven by Comp B very nicely by Gurney equationsj
their experimental results also agreed well with their computer calculations
on those configurations. Our values of chemical to kinetic energy conver-
sion efficiencies (E/AH ) calculated from their Gurney equation showed little
variation as the metal to charge mass ratio was varied, as listed in Table 3.
This encouraged us to run computer calculations for various explosives in
order to study the effect of the detonation product equation of state on
energy conversion efficiency.
In our computations a Taylor wave drove a flat metal plate in an open-
Ik faced sandwich configuration. The one-dimensional WONDY code was used,
with detonation product isentropes represented by the constant 7 law,
where 7 is the polytropic gas exponent. The chemical energy Q was repre-
sented as a function of the detonation properties, Q = D /2(7 - l), where
D denotes detonation velocity.
For late times (large displacements), these WONDY calculations indi-
cated a plate velocity higher by about 10^ than was found experimentally
by Hoskin et al. It was believed that this discrepancy was due to our
use of a constant value of 7 rather than a value which decreased as expansion
progressed. We therefore chose to interpret our computed results on the
basis explained below.
2 Kury et al. of LRL have reported that, over a range of common values
of M/C, detonation at normal incidence to a metal drives the metal
essentially to its final velocity by the time the detonation products have

expanded to twice the original volume occupied by the explosive. The same
work reported that the effective value of 7 varies as a function of
volumetric expansion, V/v . In particular, 7 drops off sharply at
v/v = 3 to 5j probably as a result of chemical recombination and inter-
molecular potential changes in this dense plasma. This has the effect of
retaining most of the remaining internal energy in the gases rather than
transferring it to the metal. Because we used a constant 7 rather than
some more realistic but more complex function, we decided to normalize the
results of our calculations on AWRE Comp B with Hoskin's results. We did
this by finding an expansion ratio V/V at which our computed efficiency
matched that of Hoskin's observations, and accepted as "final velocity"
the value obtained at that expansion ratio in all our calculations. This
matching was done at a metal to charge mass ratio of l/3^ as noted on
Table 3^ and was attained at a v/V value of 2.7- Our computed efficiencies
of energy conversion, E/Q, were subsequently found to be in accordance with
the experimental values for Comp B over the range 0 ^ M/C ^ 2.
Conversion of chemical energy to kinetic energy was calculated by
WONDY for three other explosives in addition to Comp B, with gamma values
spread over a wide range. All calculations were performed at V/V =2.7^
for a metal to charge mass ratio arbitrarily set at one-third (1/3). These
calculations indicated a correlation between the value of 7 and the
efficiency of conversion from chemical to kinetic energy as graphed in
Fig. 9^ for high values of 7, the efficiency was higher. If we consider
the ratio of the gas cloud's internal energy, pV/(7 - l), to the initial
p P chemical energy, D /2(7 - l), we reach the same general conclusion; that
Atomic Weapons Research Establishment, Aldermaston, England.

TABLE 3
EFFECTS OF M/C AND y ON EFFICIENCY
Results
Explosive
mm/|j.sec
Cranputed Configuration
ExTPerlmental Results Configuration M / C E / A H ^
AHa,* kcal/g
E/Q
M/C
7
1.20
2
2
2.85
7.75
Comp. B (AWRE)
Open sandwich, grazing detonation
Open sandwich, normal detonation incidence
0.72 0.73 0.75 0.76** 0.775 0.7lj.
1 0.5 0.333 0.1 0
1 0.5 0.333 0.1 0
0.72 0.7i<. 0.76 0.76 0.76 0.73
TNT
0.61
3.16
1.09
6.95
0.333
0.79
2.5
Tube grazing ^ detonation
Open sandwich, normal incidence
8.03
1.20
2.76
0.725
0.333
0.73
2.'5
T.I6 Comp. B (LASL)
Tube grazing ^ detonation
Open sandwich, normal incidence
0.714.
PBx-gi^oij.
8.80
0.71
2.66^
2.5
0.333
1.37
Tube, grazing ^ detonation
Open sandwich, normal Incidence
Fictitious** 8.80
Nonexistent material
3.16
0.815
0.333
1.37
Open sandwich, normal Incidence
*From Ref. 10 and 11,
**Computed efficiency E/Q was matched to experimental result E/AH at this value of M/C by use of computed metal velocity at v/v =2.7. All computed results are reported at v/v = 2 . 7 accordingly.
***Fictitlous set of properties: y value of TNT, but detonation velocity of PBX-9lj-0l+,

Is, higher values of 7 result In greater conversion of the gas cloud's
Internal energy into pV work at a given point In the expansion (i.e. a
given v/V ).
Perhaps the most obvious factor besides the 7 value which might affect
the efficiency of energy conversion is the speed of sound in the detonation
products, which is the mechanism by which the various parts of the gas
cloud communicate with one another and with the plate they are pushing.
To see how significant "enhanced communication" might be In increasing
energy conversion, we calculated a case for an explosive with the 7 value
of TNT but the detonation properties of PBX-9^0i|-, hence increased sound
velocity in the detonation products. Only a slight Increase in efficiency
(2^) was Indicated, showing that the 7 value is the major factor contributing
to calculated differences in efficiency.
Fictitious Condition*
® E/AH , Experimental
0.80
0,tll E/Q, Computed
# 0 D
I
I
S ®
E/AH^,
D
0.70
or
I
Relation for , 7 - law I computations,
E/Q
I I 7 9401^ Xomp B, ^Comp B,
TNT
AWRE
I ®
0.60
LASL 1 1
# 1 2.6 2.7 2.8 2.9 3.0
3.1
3.2
7, Polytropic Gas Exponent
'See Table 3.
FIG. 9
Chemical to Kinetic Energy Conversion Efficiency

The comparison in Table 3 of experimental results obtained for grazing
incidence of detonation with calculated results for normal incidence re-
quires justification, Lee and Pfeifer of LRL found in two-dimensional
computer experiments that a tubular cylinder was driven to essentially the
same final velocity whether it was axially initiated so as to provide
normal Incidence of detonation on the wall, or end-Initiated so as to
provide tangential incidence.
On an overall basis, the main point is that energy conversion
efficiency does not change very greatly as a function of detonation pro-
duct 7 value. The calculated slight upward trend of E/Q with 7 runs
counter to a slight downward trend in the experimental data taken from
Table 3 and also shown in Fig, 9. We conclude that the simple 7 law
equation of state for detonation products is not accurate enough to permit
interpretation of the fine details of energy transfer, at least not in the
manner of the interpretation attempted above.

Distribution:
Cover, 2332 Abegg, 23I+O
J. M.
Kleldgaard, 23ij-l
E. J. P.
E. T. A. P. w.
Los Alamos Scientific Laboratory P. 0. Box 1663 Los Alamos, New Mexico 8755^4- Attn: A. Popolato, GMX-3 J. W. Taylor, GMX-6
Weber, 23I+2 Cooper, 231+2 Skolnick, 231+2 C. E. B.
S. A. D. w. R.
B. G. Craig, GMX-8 J . D. Wackerle, GMX-7 C. L. Mader, T-5
Schwarz, 23^+2 Bennett, 231+6 Leslie, 23I+6 Claassen, 2600 Beavis, 26I3 Rodgers, 2620
L. G.
S. C. w. J.
Gobeli, 5110 Jones, 5130
Buchsbaum, 5OOO Narath, 5IOO W. E, A.
University of California Lawrence Radiation Laboratory P. 0. Box 808 Livermore, California Attn: J. W. Kury E. James D. L. Ornellas E. L. Lee H. C. Hornlg J. R. Stroud
Samara, 5132 Davison, 5133 Tucker, 5133 Kennedy, 5133 (25) Johnson, 513^
Benedick, 513!)- Champlon, 513I+
W, J. E. T. B. R.
D. W.
B. C.
E.
Shuster, 1200 Myre, 1210 Thunborg, 1213
May, 5163 Hebel, 5200 McDonald, 53OO
S. G. A. R.
Berry, 5500 Rohde, 5531
Schirber, 5150 Herrmann, 516O P. C. E. M. W. L. M.
VI. D. W. W. J.
S. J. R. A. M. R. E. F. W.
S.
15^1
Kinoshita, 1221 Chabai, 122k- Boade, !??!+ Gardner, I5OO Olson, 1510 Hoagland, I513 Alzheimer, I517 Ney, 1518 Key, I5UI Attn: R. D. Krleg, A.
Brooks, 73I+6 Cnare, 731+6 Neilson, 736O Warne, 813I
T. E. W.
Duffey, 15kk Bruce, 155^ Halpin, 161^1
Ledman, 5535 Stuetzer, 7210 Torkelson, 7325 Cowan, 73ij-0 P. C. W. E. E. L. A.
Spray, 1652 Smith, 2300 McCarapbell, 23IO
Hardin, 2312 Mauldin, 2313 Parsons, 2314
Stanton, 231^4- Young, 231^ Barnett, 2315 Marron, 2318
S. L. C. K. G. M. P. T. H. J.
I. J. D. D. B. D, H. K. L. J. M. J.
S. A. G. 0. G. L. T. J. R. W, A. J. W. R. L. G. L. R. J. 0. L. M. W. E. F, D. L. G. R. A. J. G. J. R. B. J. J. W.
C. W. w. L. C. G. C. D. F.
Davies, 815O Clark, 8155 Baroody, 816O Skinrood, 8172 Wirth 8320 Anderson, 833O Wirth, 831+0 Bass, 9111 Edwards, 9133 Dresser, 9133 Kennedy, 913I+ Carstens, Attn: R, S. Gillespie,
Binder, 2318 James, 23I8 Leeman, 2318
J. J. J.
C. F.
E. B. E. P. G.
McDonald, 3i+l6 Hefley, 3^21 Cox, 3^22-1 (15)
## c. F.
B.
Shoup, 2330 Scott, 2332 Brumley, 2332
G. B. W. L.
S. Ostrander, Jr., 8232
