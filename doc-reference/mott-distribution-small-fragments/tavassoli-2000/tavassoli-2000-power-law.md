# Models of fragmentation with power law log-normal distributions
## Z. Tavassoli 1
Department of Mathematical Sciences, Brunel University, Uxbridge, Middlesex, UB8 3PH, U. K.
## and
## A. Esmaeilnia Shirvani
Physics Department, Shahid Beheshti University, Ewin, Tehran 19834, Iran
## Abstract
Two models of binary fragmentation are introduced in which a time depen- dent transition size produces two regions of fragment sizes above and below the transition size. In the models we consider a ﬁxed rate of fragmentation for the largest fragment and two diﬀerent rates of fragmentation for the two regions of sizes above and below the transition size. The models are solved exactly in the long time limit to reveal stable time-invariant solutions for the fragment size distributions. A rate of fragmentation proportional to the inverse of fragment size in the smaller size region produces a power law dis- tribution in that region. A rate of fragmentation combined of two terms, one proportional to the inverse of the fragment size and the other proportional to a logarithmic function of the fragment size, in the larger size region produces a log-normal distribution in that region. Special cases of the models with no fragmentation for the smaller fragments are also considered. The similarities between the stable distributions in our models and power law log-normal dis- tributions from experimental work on shock fragmentation of long thin glass rods and rupture of mercury droplets are investigated.
Keywords: Shock fragmentation, fragmentation, log-normal distribution, power law distribution
# arXiv:cond-mat/0003092v2  [cond-mat.stat-mech]  4 Apr 2000
PACS numbers: 02.50.-r, 05.40.+j, 82.20.Mj
1corresponding author: zohreh.tavassoli@brunel.ac.uk
1

# 1 Introduction
Fragmentation is an irreversible kinetic phenomenon which occurs in many physical and chemical processes. Because of broad range of applications, many recent studies have been carried out to investigate the kinetics of the processes by introducing simple fragmentation models [1–10]. In [1–3] Ziﬀ and MaGrady presented a model of fragmentation in which the rate of break up depends on the size of the fragments. A general discussion of the kinetics of continuous fragmentation processes was given by Cheng and Redner in [5]. In [7,8] Krapivsky and Ben-Naim studied the kinetics of random fragmenta- tion of multidimensional objects. In [9] three models of binary fragmentation were investigated analytically in which at each time step, the largest frag- ment in the system is broken with some externally tuneable probability. In the second model of that paper, at each time step, there is a ﬁxed rate of fragmentation for the largest fragment and a rate proportional to the inverse of the fragment size for all other fragments smaller than the largest one. The model was solved exactly in the long time limit to reveal a power law distribution with an exponent, which depends on the precise details of the fragmentation process. Surprisingly, there is a similarity between the result of the stable distri- bution from the second model of [9], with some experimental and analytical results of fragment size and mass distributions with power law forms in the shock fragmentation [11–20]. In [10] a generalization of the second model of [9] was carried out. Some models of binary fragmentation were introduced which revealed composite power law distributions for the mass and size of the fragments [10]. Another behaviour of distribution which is observed in many diﬀerent processes has a log-normal form [18–24]. In [22] a comprehensive study in the log-normal distribution is given. The application of these distributions in many diﬀerent areas of science is discussed in [22], such as economics, biology, astronomy, philology, small particle statistics and physical and industrial processes. The log-normal behaviour is known to be able to describe the size distribution well in a wide variety of geological situations [24], such as that of rocks in a boulder ﬁeld. In [18] an analytical and numerical study was carried out on the fragmentation of long thin glass rods. Some stochastic models for one-dimensional brittle fracture were introduced. The models successively extended to describe cascade fracture of long thin glass rods. They are found to give the fragment size distribution close to a log-normal one. In
2

$$
terms of rupture in liquids, experiments in rupture of mercury drops were performed [19]. The result of size distribution for the cumulative number of droplets showed a log-normal distribution at the small falling heights. A transition of the distribution from log-normal to scaling behaviour was observed as the falling height was increased. In [20] an experimental work on the shock fragmentation of long thin glass rods was carried out by Ishii and Matsushita. The results of fragment size and mass distributions at small falling heights showed a log-normal form for larger fragments and a power law form for smaller fragments. The crossover was seen to be at length scales around the rod diameter. The mass and size distributions for the larger fragments showed a power law form as the falling height was increased. This paper is organised as follows. In sections 2 and 3 we introduce two new models, which are generalisations of the second model of [9] and the mod- els of fragmentation in [10]. In the models we introduce a time dependent transition size which produces two regions of fragment sizes with diﬀerent rates of fragmentation above and below the transition size. A rate of frag- mentation proportional to the inverse of the fragment size in the smaller size region produces a power law distribution in that region. A rate of fragmenta- tion combined of two terms, one proportional to the inverse of the fragment size and the other proportional to a logarithmic function of the fragment size yield a log-normal distribution in the larger size region. Finally in section 4 we summarise our conclusions and discuss the application of our results to experimental work on the shock fragmentation of long thin glass rods [20] and the rupture of mercury drops [19]. For the rest of this introduction we give a very brief summary of previous work on models of binary fragmentation. In these models, the density of fragments of size y at time t, n(y, t), evolves according to
$$
$$
n(y, t + δt) = n(y, t) −δt n(y, t) Z y
$$
$$
y R(y, z−y) n(z, t)dz,
$$
$$
0 R(z, y−z)dz + 2 δt Z L(t)
$$
$$
(1) where R(y, z) is the intrinsic rate that a fragment of size (y + z) breaks into fragments of size y and z. The ﬁrst term on the right hand side is the contribution from those fragments not chosen for the fragmentation in time (t, t + δt). The second term represents the decrease in the number of fragments of size y by the fragmentation into fragments of size z and (y −z)(y > z). The third term represents the increase in the number of
$$
3

$$
particles of size y due to the fragmentation of particles of size z(> y), such that one of the products is of size y. The upper limit of the second integral on the right-hand side is usually set to some ﬁxed value greater than the size of the largest particle in the system. This value is usually 1 or ∞depending on the details of the model. To connect with the analysis of our models in the following sections, we have set the upper limit to L(t), the size of the largest particle at time t. As n(y, t) = 0 for all y > L(t), this choice has no eﬀect on our results. We now turn to a detailed investigation of our models.
$$
# 2 Model A
$$
Firstly, we introduce a time dependent transition size, ym(t), between zero and the size of the largest particle in the system at time t, L(t). The transi- tion size produces two regions of fragment sizes with diﬀerent rates of frag- mentation above and below the transition size. At each time step there is a ﬁxed probability, p1, for the fragmentation of the largest particle in the system. A particle of size smaller than the transition size breaks with a probability p2 and a rate proportional to the inverse of the fragment size, at each time step. Any other particle of size larger than the transition size can be fragmented, at each time step, either with a probability p3 and a rate proportional to the inverse of the fragment size, or with a probability p4 and
$$
$$
y(t)
$$
$$
a rate proportional to δt
$$
$$
! . Here y(t) is the size of the fragment at
$$
$$
y(t) ln
$$
$$
˜y(t)
$$
$$
time t and ˜y(t) is a size for which the logarithmic rate is zero at time t. In the model we have p1 + p2 + p3 + p4 = 1. We also assume that ym(t) ≥˜y(t), such that for all fragments of sizes larger than the transition size, the logarithmic term in the rate of fragmentation is positive. In order to make the model tractable, we will later choose to have ym(t) proportional to L(t). In the model the distribution function of daughter fragments is uniform. Therefore the rate of breaking of a particle into two smaller pieces is indepen- dent of the daughter fragment sizes. With probability p2 every particle of size smaller than ym(t) is equally likely to be chosen for the fragmentation. With probabilities p3 and p4, every particle of size larger than the transition size is equally likely to be selected for the fragmentation with the correspondence rate. We assume that in time (t, t + δt) the largest size changes from L(t) to L(t) −p1δL and the transition size changes from ym(t) to ym(t) −δym.
$$
4

Then, the fragmentation rate for this model is given by
$$
δt R(y, z) = p1 δL
$$
$$
L(t) δ(y + z −L(t)) + p2 δt
$$
$$
y + z θ(ym(t) −(y + z))
$$
$$
y + z
$$
+
$$
" p3 δt
$$
$$
y + z + p4 δt
$$
$$
y + z ln
$$
$$
˜y(t)
$$
$$
!# θ((y + z) −ym(t)).
$$
(2)
$$
The δ-function in the ﬁrst term on the right-hand side ensures that only the
$$
$$
largest particle is fragmented and δL
$$
$$
L(t) is the probability of placing the cut
$$
$$
in the largest particle in a particular inﬁnitesimal length δL. The second term on the right-hand side of (2) represents the rate of fragmentation for the particles of sizes smaller than ym(t) in time (t, t + δt). The remaining terms on the right hand side of (2) represent the rate of fragmentation for the fragments of sizes between ym(t) and L(t) in time (t, t+δt). Inserting the rate (2) into the kinetic equation (1) for the fragments in both size regions smaller and larger than ym(t), yields
$$
$$
L(t) n2(L(t), t)
$$
$$
n1(y, t + δt) = n1(y, t) −p2 δt n1(y, t) + 2 p1 δL
$$
$$
+ 2 p2 δt Z ym(t)
$$
$$
y n1(z, t) dz
$$
$$
z
$$
$$
z + 2 p3 δt Z L(t)
$$
$$
ym(t) n2(z, t) dz
$$
$$
! dz
$$
$$
z
$$
$$
+ 2 p4 δt Z L(t)
$$
$$
z (3)
$$
$$
˜y(t)
$$
$$
ym(t) n2(z, t) ln
$$
$$
for y < ym(t) and
$$
$$
y
$$
$$
! n2(y, t)
$$
$$
˜y(t)
$$
$$
n2(y, t + δt) = n2(y, t) −p3 δt n2(y, t) −p4 δt ln
$$
$$
+ 2 p1 δL
$$
$$
y n2(z, t) dz
$$
$$
z
$$
$$
L(t) n2(L(t), t) + 2 p3 δt Z L(t)
$$
$$
! dz
$$
$$
z
$$
$$
+ 2 p4 δt Z L(t)
$$
$$
y n2(z, t) ln
$$
$$
z (4)
$$
$$
˜y(t)
$$
$$
for y > ym(t). Here n1(y, t) and n2(y, t) are the densities of fragments of size y at time t which is smaller and larger than ym(t), respectively. The second
$$
5

$$
term on the right hand side of (3) and the second and third terms on the right hand side of (4) represent the decrease in the number of particles of size y from fragmentation into smaller particles, with probabilities p2, p3 and p4, respectively. The next term on the right hand sides of (3,4) describes the gain in the number of particles of size y from the fragmentation of the largest fragment of size L(t). The remaining terms on the right hand sides of (3,4) are the increase in the number of particles of size y from the fragmentation of all particles larger than y and smaller than L(t). Now we deﬁne densities of fragments of length y at time t, which are normalised to a positive constant value A for two regions of sizes smaller and larger than ym(t),
$$
$$
g1(y, t) = A n1(y, t)
$$
$$
Z ym(t)
$$
$$
0 n1(z, t) dz + Z L(t)
$$
$$
ym(t) n2(z, t) dz (5)
$$
$$
for y < ym(t) and
$$
$$
g2(y, t) = A n2(y, t)
$$
$$
Z ym(t)
$$
$$
0 n1(z, t) dz + Z L(t)
$$
$$
ym(t) n2(z, t) dz (6)
$$
$$
for y > ym(t). In time t →t + δt as L(t) →L(t) −p1 δL and ym(t) → ym(t) −δym they yield
$$
$$
g1(y, t + δt) = A n1(y, t + δt)
$$
$$
Z ym(t)−δym(t)
$$
$$
0 n1(z, t + δt) dz + Z L(t)−p1δL
$$
$$
ym(t)−δym(t) n2(z, t + δt) dz
$$
$$
(7) for y < ym(t) and
$$
$$
g2(y, t + δt) = A n2(y, t + δt)
$$
$$
Z ym(t)−δym(t)
$$
$$
0 n1(z, t + δt) dz + Z L(t)−p1δL
$$
$$
ym(t)−δym(t) n2(z, t + δt) dz
$$
$$
(8) for y > ym(t). Inserting (3), (4) in (7), (8), respectively, gives us
$$
$$
g1(y, t + δt) =
$$
6

$$
2 p1 δL
$$
$$
y g1(z, t) dz
$$
$$
z
$$
$$
L(t) g2(L(t), t) + 2 p2 δt Z ym(t)
$$
$$
! dz
$$
$$
z
$$
$$
+ 2 p3 δt Z L(t)
$$
$$
z
$$
$$
z + 2 p4 δt Z L(t)
$$
$$
˜y(t)
$$
$$
ym(t) g2(z, t) ln
$$
$$
ym(t) g2(z, t)dz
$$
$$
+ g1(y, t)
$$
$$
0 g1(z, t)dz
$$
$$
A δt Z ym(t)
$$
$$
" 1 −p2 δt −p1
$$
$$
A g2(L(t), t) δL −p2
$$
$$
z
$$
$$
! dz
$$
$$
# (9)
$$
$$
A δt Z L(t)
$$
$$
A δt Z L(t)
$$
$$
˜y(t)
$$
$$
−p3
$$
$$
ym(t) g2(z, t)dz −p4
$$
$$
ym(t) g2(z, t) ln
$$
$$
for y < ym(t) and
$$
$$
g2(y, t + δt) =
$$
$$
2 p1 δL
$$
$$
y g2(z, t) dz
$$
$$
z
$$
$$
L(t) g2(L(t), t) + 2 p3 δt Z L(t)
$$
$$
z
$$
$$
! dz
$$
$$
+ 2 p4 δt Z L(t)
$$
$$
y g2(z, t) ln
$$
$$
˜y(t)
$$
$$
z + g2(y, t)
$$
$$
" 1 −p3 δt
$$
$$
y
$$
$$
0 g1(z, t)dz
$$
$$
A δt Z ym(t)
$$
$$
˜y(t)
$$
$$
−p4 δt ln
$$
$$
! −p1
$$
$$
A g2(L(t), t) δL −p2
$$
$$
z
$$
$$
! dz
$$
$$
# (10)
$$
$$
A δt Z L(t)
$$
$$
A δt Z L(t)
$$
$$
˜y(t)
$$
$$
−p3
$$
$$
ym(t) g2(z, t)dz −p4
$$
$$
ym(t) g2(z, t) ln
$$
$$
for y > ym(t). In order to solve (9) and (10) we introduce two functions F1(x, t) and F2(x, t) deﬁned by
$$
$$
F1(x, t) = L(t) g1(xL(t), t) (11)
$$
$$
for x < xm and
$$
$$
F2(x, t) = L(t) g2(xL(t), t) (12)
$$
$$
for x > xm. Here we have deﬁned dimensionless and time independent
$$
$$
variables x = y(t)
$$
$$
L(t), xm = ym(t)
$$
$$
L(t) and ˜x = ˜y(t)
$$
$$
L(t), where x changes in the range
$$
$$
[0, 1]. xm and ˜x are ﬁxed values and restricted to the same range. Using (9- 12) we can obtain two partial diﬀerential equations for F1(x, t) and F2(x, t) as
$$
7

$$
∂F1(x, t)
$$
$$
∂t =
$$
$$
Z 1
$$
$$
Z xm
$$
$$
x F1(z, t) dz
$$
$$
∂x + 2 ν F2(1, t) + 2 p2
$$
$$
x
$$
$$
z + 2 p3
$$
$$
−ν x ∂F1(x, t)
$$
$$
xm F2(x, t) dx
$$
$$
Z 1
$$
$$
 dx
$$
$$
+ 2 p4
$$
$$
" ν + p2 + ν
$$
$$
A F2(1, t)
$$
$$
˜x
$$
$$
xm F2(x, t) ln x
$$
$$
#
$$
$$
x −F1(x, t)
$$
$$
Z 1
$$
$$
Z 1
$$
$$
Z xm
$$
$$
 dx
$$
$$
+ p2
$$
$$
0 F1(x, t)dx + p3
$$
$$
A
$$
$$
A
$$
$$
A
$$
$$
˜x
$$
$$
xm F2(x, t)dx + p4
$$
$$
xm F2(x, t) ln x
$$
(13)
$$
for x < xm and
$$
$$
∂F2(x, t)
$$
$$
∂t =
$$
$$
Z 1
$$
$$
∂x + 2 ν F2(1, t) + 2 p3
$$
$$
z
$$
$$
−ν x ∂F2(x, t)
$$
$$
x F2(z, t) dz
$$
$$
Z 1
$$
$$
 dz
$$
$$
+ 2 p4
$$
$$
" ν + p3
$$
$$
˜x
$$
$$
x F2(z, t) ln z
$$
$$
z −F2(x, t)
$$
$$
Z xm
$$
$$
 + ν
$$
$$
+ p4 ln x
$$
$$
0 F1(x, t)dx
$$
$$
A F2(1, t) + p2
$$
$$
A
$$
$$
˜x
$$
$$
Z 1
$$
$$
Z 1
$$
$$
 dx
$$
$$
+ p3
$$
$$
# (14)
$$
$$
A
$$
$$
A
$$
$$
˜x
$$
$$
xm F2(x, t)dx + p4
$$
$$
xm F2(x, t) ln x
$$
$$
for x > xm. Here we have set p1 δL
$$
$$
L(t)δt = ν to be a ﬁxed value, and assumed
$$
$$
that p1 > 0. ν is equal to the rate of fragmentation for the largest fragment, and determines the relationship between the real time and the length of the largest fragment at time t, L(t). In the limit t →∞, we assume that F1(x, t) and F2(x, t) evolve to time-independent quantities,
$$
$$
F1(x) = lim t→∞F1(x, t) (15)
$$
$$
for x < xm and
$$
$$
F2(x) = lim t→∞F2(x, t) (16)
$$
8

$$
∂t →0 and ∂F2(x, t)
$$
$$
∂t →0. To
$$
$$
for x > xm. So that, as t →∞then ∂F1(x, t)
$$
solve (13,14) in the long time limit using (15,16), we anticipate solutions as
$$
F1(x) = B x−α (17)
$$
$$
for x < xm and
$$
$$
i2
$$
$$
˜x
$$
$$
F2(x) = C exp  −β h ln  x
$$
$$
x (18)
$$
$$
for x > xm. Substituting (17,18) in (13,14) in the long time limit, using (15,16) give us
$$
$$
α = p2
$$
$$
p3 , (19)
$$
$$
β = p4
$$
$$
2 p3 (20)
$$
and
$$
ν = p3. (21)
$$
$$
B and C in (17),(18), respectively, are constant values and can be obtained using (13,14) in the long time limit and the continuity condition at xm,
$$
$$
F1(xm) = F2(xm). (22)
$$
These give
$$
s
$$
$$
(
$$
$$
C = A
$$
$$

$$
$$
2)
$$
$$
 p3
$$
$$
2πp3
$$
$$
p4
$$
$$
p4
$$
$$
 P r
$$
$$
 exp
$$
+
$$
˜x
$$
$$
˜x
$$
$$
˜x
$$
$$
−β  ln xm
$$
$$
 −P r
$$
$$
p4
$$
$$
p3 ln 1
$$
$$
p3 ln xm
$$
$$
p3 −p2
$$
(23)
and
$$
2)
$$
$$
 ln xm
$$
$$
˜x
$$
$$
( −p4
$$
$$
2p3
$$
$$

$$
$$
, (24)
$$
$$
B = C exp
$$
$$
 1 −p2
$$
$$
p3
$$
$$
m
$$
$$
x
$$
9

where the second and third terms in the denominator of (23) are a proportion of the normal probability distribution function deﬁned as
$$
Z x
$$
$$
P(x) = 1
$$
$$
−∞e−t2/2dt. (25)
$$
$$
√
$$
$$
2π
$$
We have also assumed that
$$
0 ≤α = p2
$$
$$
p3 < 1. (26)
$$
Solutions (17,18) using (19,20,23-26) satisfy the normalisation relation
$$
Z xm
$$
$$
0 F1(x) dx + Z 1
$$
$$
xm F2(x) dx = A. (27)
$$
$$
If A = 1, the normalisation is equal to 1. For a choice of A as
$$
$$
(
$$
$$
2)
$$
$$
p3
$$
$$
p4
$$
$$
p4
$$
$$
p4
$$
$$
 ,
$$
$$
A = r
$$
$$
+ P r
$$
$$
˜x
$$
$$
˜x
$$
$$
˜x
$$
$$
−β  ln xm
$$
$$
 −P r
$$
$$
2πp3
$$
$$
p3 ln  1
$$
$$
p3 ln xm
$$
$$
p3 −p2 exp
$$
(28)
the solutions (17,18) using (19,20,23,24) yield
$$
2)
$$
$$
s
$$
$$
 ln xm
$$
exp
$$
˜x
$$
$$
( −p4
$$
$$
p4
$$
$$
2p3
$$
$$

$$
$$
x−p2
$$
$$
p3 (29)
$$
$$
F1(x) =
$$
$$
 1 −p2
$$
$$
2πp3
$$
$$
p3
$$
$$
m
$$
$$
x
$$
$$
for x < xm and
$$
$$
2)
$$
$$
s
$$
$$
 ln x
$$
exp
$$
˜x
$$
$$
( −p4
$$
$$
p4
$$
$$
2p3
$$
$$
F2(x) =
$$
$$
x (30)
$$
$$
2πp3
$$
$$
for x > xm. We see that the stable distribution has a power law behaviour in the smaller region, x < xm. For a log-normal distribution, the probability of ﬁnding a fragment of size between x and x + dx is given by n(x)dx, where
$$
$$
n(x) = exp n −[ln (x/˜x)]2 /2σ2o
$$
$$
(2πσ2)1/2 x , (31)
$$
10

$$
where ˜x is the mean and σ is the dispersion of the distribution. Comparing (30) with (31) shows that the stable distribution F2(x) in the larger region exhibits a log-normal behaviour with a mean and a dispersion of the distri-
$$
$$
s
$$
$$
p3
$$
$$
bution equal to ˜x and σ =
$$
$$
p4 , respectively. To have a positive value for A
$$
$$
in (28) and therefore physically meaningful distributions, we require p3 > p2. This requirement is satisﬁed in (26). Now we consider some special cases of the model.
$$
$$
1. There is no fragmentation for the fragments smaller than ym(t), i.e. p2 = 0 and p1 + p3 + p4 = 1. The stable distribution then from (29) yields
$$
$$
2)
$$
$$
s
$$
$$
 ln xm
$$
exp
$$
˜x
$$
$$
( −p4
$$
$$
p4
$$
$$
2p3
$$
$$
F1(x) =
$$
$$
2πp3
$$
$$
xm (32)
$$
$$
for x < xm and is the same as (30) for x > xm. We see that the distribution is a constant value in the smaller region and has a log- normal form in the larger region.
$$
$$
2. As ym(t) = ˜y(t) and therefore xm = ˜x, the distributions (29,30) give
$$
$$

$$
$$
s
$$
$$
p3
$$
$$
p4
$$
$$
m x−p2
$$
$$
p3 (33)
$$
$$
F1(x) =
$$
$$
2πp3 x −  1 −p2
$$
$$
for x < xm and
$$
$$
2)
$$
$$
s
$$
$$
 ln  x
$$
exp
$$
( −p4
$$
$$
p4
$$
$$
2p3
$$
$$
xm
$$
$$
F2(x) =
$$
$$
x (34)
$$
$$
2πp3
$$
$$
for x > xm. Again the distribution reveals a power law form in the smaller region and has a log-normal behaviour in the larger region.
$$
$$
p4 →∞, the distribution (30) in the
$$
$$
3. As p4 →0 and therefore σ2 = p3
$$
$$
larger region yield F2(x) ∼x−1. On the other hand as p4 →0 the rate of fragmentation (2) for the fragments of sizes larger than ym(t)
$$
11

$$
ν in the smaller and larger region, respectively. In our
$$
$$
is only proportional to the inverse of the fragment size. Consequently, at each time step either the largest fragment breaks with probability p1, or a fragment smaller than ym(t) is chosen for fragmentation with probability p2, or a fragment larger than ym(t) is selected with proba- bility p3, where p1 + p2 + p3 = 1. The stable distributions then exhibit a composite power law behaviour with power laws of exponents equal to −p2
$$
$$
ν and −p3
$$
$$
case since from (21) we have ν = p3, the exponents reduce to −p2
$$
$$
p3 and
$$
$$
−1 in the two regions. The power law distribution in the smaller region is similar to that from (17,19) and in the larger region has an exponent of −1 as expected. The latter is consistent with one of interesting prop- erties of the log-normal distribution where as the variance σ2 is pretty large, then the distribution can be approximated by a power law form with an exponent equal to −1, [18].
$$
# 3 Model B
$$
In this model again a time dependent transition size, ym(t), produces two regions of fragment sizes with diﬀerent rates of fragmentation above and below the transition size. At each time step either the largest fragment in the system breaks with a ﬁxed probability, p1, or a fragment smaller than the transition size is chosen for the fragmentation with probability p2 and a rate proportional to the inverse of fragment size, or another fragment larger than ym(t) is selected with probability (1 −p1 −p2) and a rate proportional
$$
$$
y(t)
$$
$$
to δt
$$
$$
" 1 + λ ln
$$
$$
!# . Here y(t) is the size of fragment at time t, λ is a
$$
$$
y(t)
$$
$$
˜y(t)
$$
$$
positive and constant value and ˜y(t) is a size for which the logarithmic term is zero at time t. In this model we assume that ym(t) < ˜y(t). For a fragment of size y > ˜y(t) the logarithmic term in the rate of fragmentation is always positive, but a fragment of size ym(t) < y < ˜y(t) gives a negative value for the logarithmic term. In order to have a positive rate of fragmentation for
$$
$$
y(t)
$$
$$
" 1 + λ ln
$$
$$
!# > 0 which gives
$$
$$
all particles larger than ym(t), we require
$$
$$
˜y(t)
$$
$$
y(t) > ˜y(t) e−1/λ. If we choose ym(t) to be
$$
$$
ym(t) = ˜y(t) e−1/λ, (35)
$$
12

$$
then the rate of fragmentation for all fragments of sizes larger than ym(t) is positive. Consequently, the rate of fragmentation for this model is given by
$$
$$
δt R(y, z) = p1 δL
$$
$$
L(t) δ(y + z −L(t)) + p2 δt
$$
$$
y + z θ(ym(t) −(y + z))
$$
$$
y + z
$$
$$
" 1 + λ ln
$$
$$
y + z
$$
$$
˜y(t)
$$
$$
!# θ((y + z) −ym(t)),
$$
$$
+ (1 −p1 −p2) δt
$$
(36)
$$
where ym(t) is deﬁned as (35). The ﬁrst two terms on the right hand side of (36) are the same as those in (2) and have the same deﬁnitions as before. The last term represents the rate of fragmentation for the fragments of sizes larger than ym(t) in time (t, t + δt). Using (1,36) for the both size regions give the kinetic equations
$$
$$
n1(y, t + δt) =
$$
$$
L(t) n2(L(t), t)
$$
$$
n1(y, t) −p2 δt n1(y, t) + 2 p1 δL
$$
$$
+ 2 p2 δt Z ym(t)
$$
$$
y n1(z, t) dz
$$
$$
z
$$
$$
ym(t) n2(z, t) dz
$$
$$
z + 2 (1 −p1 −p2) δt Z L(t)
$$
$$
z
$$
$$
! dz
$$
$$
z (37)
$$
$$
˜y(t)
$$
$$
ym(t) n2(z, t) ln
$$
$$
+ 2 λ (1 −p1 −p2) δt Z L(t)
$$
$$
for y < ym(t) and
$$
$$
n2(y, t + δt) =
$$
$$
y
$$
$$
! n2(y, t)
$$
$$
˜y(t)
$$
$$
n2(y, t) −(1 −p1 −p2) δt n2(y, t) −λ (1 −p1 −p2) δt ln
$$
$$
+ 2 p1 δL
$$
$$
y n2(z, t) dz
$$
$$
z
$$
$$
L(t) n2(L(t), t) + 2 (1 −p1 −p2) δt Z L(t)
$$
$$
z
$$
$$
! dz
$$
$$
y n2(z, t) ln
$$
$$
z (38)
$$
$$
˜y(t)
$$
$$
+ 2 λ (1 −p1 −p2) δt Z L(t)
$$
$$
for y > ym(t). Following the same procedure as that used in the model A, we obtain
$$
13

$$
∂F1(x, t)
$$
$$
∂t =
$$
$$
Z xm
$$
$$
x F1(z, t) dz
$$
$$
∂x + 2 ν F2(1, t) + 2 p2
$$
$$
z
$$
$$
−ν x ∂F1(x, t)
$$
$$
 dx
$$
$$
x
$$
$$
˜x
$$
$$
xm F2(x, t)dx
$$
$$
xm F2(x, t) ln x
$$
$$
+ 2 (1 −p1 −p2) Z 1
$$
$$
x + 2 λ (1 −p1 −p2) Z 1
$$
$$
Z xm
$$
$$
" ν + p2 + ν
$$
$$
0 F1(x, t)dx
$$
$$
A F2(1, t) + p2
$$
$$
A
$$
$$
−F1(x, t)
$$
$$
#
$$
$$
Z 1
$$
$$
Z 1
$$
$$
 dx
$$
$$
+ (1 −p1 −p2)
$$
$$
A
$$
$$
A
$$
$$
˜x
$$
$$
xm F2(x, t)dx + λ (1 −p1 −p2)
$$
$$
xm F2(x, t) ln x
$$
(39)
$$
for x < xm and
$$
$$
∂F2(x, t)
$$
$$
∂t =
$$
$$
z
$$
$$
−ν x ∂F2(x, t)
$$
$$
x F2(z, t) dz
$$
$$
∂x + 2 ν F2(1, t) + 2 (1 −p1 −p2) Z 1
$$
$$
 dz
$$
$$
˜x
$$
$$
x F2(z, t) ln z
$$
$$
+ 2 λ (1 −p1 −p2) Z 1
$$
$$
" ν + (1 −p1 −p2)
$$
$$
z −F2(x, t)
$$
$$
Z xm
$$
$$
 + ν
$$
$$
0 F1(x, t)dx
$$
$$
A F2(1, t) + p2
$$
$$
A
$$
$$
˜x
$$
$$
+ λ (1 −p1 −p2) ln x
$$
$$
#
$$
$$
Z 1
$$
$$
Z 1
$$
$$
 dx
$$
$$
+ (1 −p1 −p2)
$$
$$
A
$$
$$
A
$$
$$
˜x
$$
$$
xm F2(x, t)dx + λ (1 −p1 −p2)
$$
$$
xm F2(x, t) ln x
$$
(40)
$$
for x > xm. Here x, xm, ˜x and ν have the same deﬁnitions as before and from (35) we get
$$
$$
xm = ˜x e−1/λ. (41)
$$
$$
In the long time limit as t →∞, we assume that F1(x, t) and F2(x, t) evolve to the same time-independent variables as (15) and (16), respectively. In order to solve (39,40) in this limit we anticipate solutions as
$$
$$
F1(x) = G x−γ (42)
$$
14

$$
for x < xm and
$$
$$
i2
$$
$$
˜x
$$
$$
F2(x) = H exp  −η h ln  x
$$
$$
x (43)
$$
$$
for x > xm. Substituting (42,43) in (39,40) in the long time limit, gives us
$$
$$
γ = p2
$$
$$
1 −p1 −p2 , (44)
$$
$$
η = λ
$$
2 (45)
and
$$
ν = 1 −p1 −p2. (46)
$$
$$
G and H in (42,43) are constant values and can be obtained using (39,40) in the long time limit and the continuity condition at xm, (22). These give
$$
$$
s
$$
$$
H = A
$$
$$
!#
$$
$$
2π
$$
$$
" P √
$$
$$
 +
$$
$$
λ ln 1
$$
$$
1 −p1 −p2
$$
$$
√
$$
$$
λ
$$
$$
2λ
$$
$$
˜x
$$
$$
 −P
$$
$$
−1
$$
$$
λ
$$
$$
1 −p1 −2p2 exp  −1
$$
(47) and
$$

$$
$$
2λ
$$
$$
G = H exp  −1
$$
$$
1−p1−p2 , (48)
$$
$$
 ˜x e−1/λ 1−p1−2p2
$$
where we have assumed that
$$
0 ≤γ = p2
$$
$$
1 −p1 −p2 < 1. (49)
$$
$$
The second and third terms in the denominator of (47) are a proportion of the normal probability distribution function with the same deﬁnition as (25). Solutions (42,43) using (44-49) satisfy the normalisation relation (27). If A = 1, the normalisation is equal to 1. For a choice of A as
$$
15

$$
s
$$
$$
λ
$$
$$
A =
$$
$$
λ ln 1
$$
$$
! , (50)
$$
$$
 + P √
$$
$$
√
$$
$$
2π 1 −p1 −p2
$$
$$
2λ
$$
$$
˜x
$$
$$
 −P
$$
$$
−1
$$
$$
λ
$$
$$
1 −p1 −2p2 exp  −1
$$
the solutions (42,43) using (44,45,47,48) yield
$$

$$
$$
s
$$
$$
λ
$$
$$
2λ
$$
$$
exp  −1
$$
$$
1−p1−p2 (51)
$$
$$
F1(x) =
$$
$$
2π
$$
$$
1−p1−p2 x− p2
$$
$$
 ˜x e−1/λ 1−p1−2p2
$$
$$
for x < ˜x e−1/λ and
$$
$$
2)
$$
$$
s
$$
$$
 ln x
$$
exp
$$
λ
$$
2
$$
˜x
$$
$$
( −λ
$$
$$
F2(x) =
$$
$$
x (52)
$$
$$
2π
$$
$$
for x > ˜x e−1/λ. We see that the stable distribution has a power law be- haviour in the smaller region. Comparing (52) with (31) exhibits that the stable distribution F2(x) in the larger region has a log-normal form with a mean of ˜x and a dispersion of the distribution equal to
$$
$$
σ = 1
$$
$$
√
$$
$$
λ . (53)
$$
$$
It is shown that the log-normal function (52) has a maximum at x = ˜x e−1/λ
$$
$$
which we have assumed to be equal to xm. This shows that in this model the dimensionless transition size xm is chosen to be equal to the value for which the log-normal distribution in the larger region is maximum. To have a positive value for A in (50) and therefore physically meaningful distributions, it is required that (1 −p1 −p2) > p2. This inequality is satisﬁed from (49). Now we consider some special cases of the model B.
$$
$$
1. When there is no fragmentation for the fragments smaller than ym(t), i.e. p2 = 0, then the stable distribution from (51) yields
$$
$$
s
$$
$$
λ
$$
$$
F1(x) =
$$
$$
2π 1
$$
$$
˜x e1/2λ (54)
$$
$$
for x < xm and is the same as (52) for x > xm. The distribution is a constant value in the smaller region and has a log-normal behaviour in the larger region.
$$
16

$$
2. As λ →0, and therefore from (53) σ2 →∞, the situation is then simi- lar to the case 3 of model A and the log-normal distribution (52) in the larger region can be approximated by a power law form with an expo- nent equal to −1, F2(x) ∼x−1. On the other hand at this limit the rate of fragmentation (36) gives two diﬀerent probabilities in the two diﬀer- ent size regions with a rate proportional to the inverse of the fragment size in each region. The stable distribution then reveal a composite
$$
$$
power law with power laws of exponents of −p2
$$
$$
ν and −1 −p1 −p2
$$
$$
ν in the smaller and larger size regions, respectively. Since in our case from (46) we have ν = (1 −p1 −p2), the exponents yield − p2
$$
$$
1 −p1 −p2 and
$$
$$
−1, respectively. The result in the smaller size region is equivalent to that from (42,44). In the larger size region, as expected, we get a power law with an exponent of −1 which is consistent with the property of a log-normal distribution with a very large variance.
$$
$$
We see that all the results for the model B can be recovered from the model A by substituting p3 by (1 −p1 −p2), p4 by λ (1 −p1 −p2) and using equation (35).
$$
# 4 Conclusions
$$
In this paper we have studied two models of binary fragmentation. In the models we introduced a time dependent transition size, ym(t), which pro- duced two regions of fragment sizes with diﬀerent rates of fragmentation above and below the transition size. The rate of fragmentation at each time step is ﬁxed for the largest fragments and is proportional to the inverse of fragment size for the fragments smaller than the transition size. We con- sidered a rate of fragmentation combined of two terms, one proportional to the inverse of the fragment size and the other proportional to a logarithmic function of the fragment size, for the fragments larger than the transition size at each time step. For a size equal to ˜y(t) at time t, the logarithmic function is zero. In model A we assumed that the transition size, ym(t) is any arbitrary value for which ym(t) ≥˜y(t), whereas in the model B we chose a value as (35) for the transition size. The models were then solved exactly in the long time limit to reveal stable time-invariant solutions for the distribu- tions. The results of these distributions for both models A and B exhibited
$$
17

$$
a power law form with an exponent between −1 and zero, in the smaller region. For a special choice of normalisation, the distributions exhibited log- normal behaviours in the larger regions. In this region they revealed one of interesting properties of a log-normal distribution for which as the variance of the log-normal is pretty large, then the distribution is approximated by a power law form with an exponent equal to −1. Special cases of the models with no fragmentation for the smaller fragments were also examined. The stable distributions then exhibited a constant value and a log-normal form in the smaller and larger regions, respectively. Now we investigate some experimental work on the fragmentation involv- ing log-normal distributions and the transition of the distributions from a log-normal form to a power law one and vice versa. In [20] the experimental results of fragment size and mass distributions for the long thin glass rods with ﬁxed lengths of 1500mm and diameters of 2mm were reported. The rods were dropped horizontally onto a ﬂat hard ﬂoor from diﬀerent heights. At lower falling heights (about 1m drop), the distributions exhibited a log- normal form for larger fragments and a power law form for smaller ones. The crossover was seen to be at length scales around the rod diameter. This is due to the fact that fragments smaller than the rod diameter, undergo a three-dimensional fracture, whereas the larger fragments are produced by one-dimensional breaking. For a falling height of 1.20m the cumulative num- ber of fragments on their size were plotted. The data was ﬁtted to a curve calculated by assuming that the size distribution could be described by a log-normal distribution. The ﬁtting gave values of ˜l = 30mm and σ = 0.55 for the mean and the dispersion of the log-normal distribution. The ﬁtting is excellent for the fragments larger than lc = 7mm which is a length scale around the rod diameter. The size distribution of fragments smaller than lc seemed to have a power law form. As the falling height was increased, the cumulative number variation for larger fragments started to show a power law dependence on their size and mass. In [19] experiments in rupture of mercury droplets were performed. In the experiment at a height of h, the mercury droplets of about 2.0mm radius were fallen directly on a glass Petri dish. The results of the cumulative number of the drops versus the drop diameter were plotted. For small falling heights a log-normal behaviour was exhibited. The distribution showed a clear transition from a log-normal form to a scaled one as the falling height h was increased. Our models in the long time limit can be applied to the experimental systems when the fragmentation process is over and the system reaches a
$$
18

$$
stable and time-independent phase. In the models we assumed that the fragments have only one dimension, whereas in real physical systems the fragments have three dimensions. We can therefore only apply our models to the systems for which the fractures occur in one dimension. This assumption seems physically reasonable for a long thin glass rod [20] for which most of the fractures occur in the length of the rod and the cross-section remains almost ﬁxed. We can also consider this assumption for the mercury droplets [19] for which at each time step only the radius of the droplet changes and the shape of the fragments remains always spherical. Now we discuss the similarities between the results from our models and those from the experiments. The experimental results for the size distribution of long thin glass rods at low falling heights exhibited a power law and log- normal behaviour in the smaller and larger size regions, respectively [20]. We got the same behaviour for the distributions in both our models. The data from the experiments for the falling height of 1.20m revealed that lc < ˜l, where lc is the transition size and ˜l is the mean of the log-normal distribution. In the model B of our work also we have xm < ˜x. We therefore expect model B of our work to describe the experimental results. In model B, the dispersion of the log-normal distribution can be obtained from (53) and the mean and the transition values, ˜x and xm, respectively, are any arbitrary values which satisfy the relation (41). Then, by appropriate choices of ˜x and λ in the model B of our work we can match the mean and the dispersion of the log-normal distribution in the experimental results. Because of (41,53) we should expect a relation as lc = ˜l e−σ2. The values of lc and ˜l from experimental result do not satisfy this relation. As a result, although model B of our work does not match the exact relation between lc and ˜l from experimental result, but it can give an explanation for the transition of distribution from a power law to a log-normal form on the shock fragmentation of long thin glass rods [20]. Also in the smaller region of the model B, the appropriate choices of p1 and p2 can match the exponent of power law equal to − p2
$$
$$
(1 −p1 −p2) from
$$
(42,44), with the corresponding exponent of power law distribution from the experimental results. This exponent needs to satisfy the condition (49). For high falling heights a transition of the distribution from log-normal to scaling law was observed in the experiments for the larger rod fragments [20] and for the mercury droplets [19]. At high heights therefore the distributions from the experiments exhibit a composite and a single power law form for the rod fragments and mercury droplets, respectively. The models in this paper
19

suggest a power law and a log-normal behaviour for the distribution of the smaller and larger fragments, respectively. To explain composite and single power law distributions, we can however use the models in [10]. To conclude we introduced statistical models with a ﬁxed probability for the breaking the largest particle in the system. All other particles of sizes smaller than the largest size, were divided into two diﬀerent regions with diﬀerent rates of fragmentation in each region. In the models therefore the largest fragments are broken with very large probability. This fact together with the form of the fragmentation rate as a function of the fragment size in each region, give a distribution of power law or log-normal form in that region. Our models therefore give a theoretical explanation for the transition of distribution from the scaling to log-normal behaviour, which had been seen before in the experiments.
## Acknowledgement
ZT is grateful to the Soudavar Scholarship Fund for the award of a scholar- ship.
20

# References
[1] R. M. Ziﬀand E. D. McGrady, J. phys. A: Math Gen. 18 3027 (1985).
[2] R. M. Ziﬀand E. D. McGrady, Macromolecules 19 2513 (1986).
[3] E. D. McGrady and R. M. Ziﬀ, Phys. Rev. Lett. 58 892 (1987).
[4] Z. Cheng and S. Redner, Phys. Rev. Lett. 60 2450 (1988).
[5] Z. Cheng and S. Redner, J. Phys. A: Math. Gen. 23 1233 (1990).
[6] Z. Jaeger and R. Englman, J. Appl. Phys. 59 4048 (1986).
[7] P. L. Krapivsky and E. Ben-Naim, Phys. Rev. E 50 3502 (1994).
[8] E. Ben-Naim and P. L. Krapivsky, Physica D 107 156 (1997).
[9] G. J. Rodgers and M. K. Hassan, Physica A 233 19 (1996).
[10] Z. Tavassoli and G. J. Rodgers, Phys. Lett. A 256 272 (1999).
[11] D. E. Grady and M. E. Kipp, J. Appl. Phys. 58 1210 (1985).
[12] B. R. Lawn and T. R. Wilshaw, Fracture of Brittle Solids (Cambridge University Press, 1975).
[13] D. L. Turcotte, Fractals and Chaos in Geology and Geophysics (Cam- bridge University Press, 1992).
[14] R. Englman, J. Phys. C 3 1019 (1991).
[15] O. Sotolongo-Costa, E. Lopez-Pages, F. Barreras-Toledo and J. Marin- Antuna, Phys. Rev. E 49 4027 (1994).
[16] L. Oddershede, P. Dimon and J. Bohr, Phys. Rev. Lett. 71 3107 (1993).
[17] A. Meibom and I. Balslev, Phys. Rev. Lett. 76 2492 (1996).
[18] M. Matsushita and K. Sumida, Bull. Facul. Sci. & Eng. 31 69 (1988).
[19] O. Sotolongo-Costa, Y. Moreno-Vega, J. J. Lioveras-Gonzalez and J. C. Antoranz, Phys. Rev. Lett. 76 42 (1996).
21

[20] T. Ishii and M. Matsushita, J. Phys. Soc. Jpn. 61 3474 (1992).
[21] A. N. kolmogorov, Doklady Akad. Nauk. SSSR 31 99 (1941).
[22] J. Atchison and J. A. C. Brown, The LogNormal Distribution (Cam- bridge University Press, Cambridge, 1963).
[23] E. W. Montroll and M. F. Shlesinger, J. Stat. Phys. 32 209 (1983).
[24] P. Habib, Soil and Rock Mechanics (Cambridge University Press, Cam- bridge, 1983).
22
