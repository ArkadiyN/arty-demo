K. Sanborn et al. International Journal of Impact Engineering 128 (2019) 11–23
Fig. 11. Euler–Robins, Poncelet, and Resal penetration depth models calibrated with CLT data.
m, and n. Finally, assuming that the relation holds between predicting the perforation thickness, Tw, and the penetration depth, d, the equation can be written in terms of penetration depth as shown in Eq. (10) with different calibration constants f, g, and h.
compelling it to reduce its velocity or even stop completely. The re- sisting force is included as a general quadratic form and the residual velocity, vr, can be calculated as shown in Eq. (6). In the equation, vs, is the striking velocity, x is the distance traveled in the target, and a, b, and c are model constants.
= v v ax bx c r s 2 (6)
= T A v w 1 10 w s l
m n (9)
s f
= d A v w 1 10
g h (10)
When the CLT specimen stopped the projectile and the residual velocity was zero the equation can be rewritten and solved for the distance, x, as shown in Eq. (7). If the depth of penetration is considered x is the distance traveled in the target, Tw.
= = + x d a b v a ac b 1 2 ( 4 4 ) s 2
(7)
Eq. (7) was calibrated to the CLT ballistic data, creating an em- pirical, physics-based model. Using the Levenberg–Marquardt method, the parameters were found for the Force Law model. This model con- sidered no material factors for the target or the projectile other than striking velocity. Fig. 12 shows the curve of the model fit to both species of data combined. The calibration constants for each of the is given in Table 6. The errors from the models are discussed in Section 6.6.
5.4. THOR models
Using the same nonlinear least square fitting method as the previous models, the general THOR model was calibrated to the SPF-S CLT and SYP CLT data combined as shown in Fig. 13, with calibration constants given in Table 7. The error from the model is discussed in Section 6.6. Since the general THOR equation is an empirical formula, it is pos- sible to include additional variables of interest with little difficulty. This led to the development of a new CLT model based on the general THOR equation but with the addition of the target density, ρ, and a strength parameter, wood hardness, H. Since it was observed in previous models and documented in the THOR reports that unchanging variables could effectively be excluded from the curve-fitting model for simplification, the variable for projectile weight, w, was removed. Because the same projectile weight was used in all tests, inclusion in the model simply acts as an additional constant instead of a calibrating parameter.
Eq. (11) gives the CLT THOR-based equation developed for the CLT experiments. The equation includes the striking velocity, vs, of the projectile but no other projectile variables since the same projectile was used for the entire data set. It also includes the density, ρ, and hardness values, H, of the CLT specimens. The calibration constants are re- presented as C1, a, b, f, and g.
s f
= d C v
g a b 1
H 10
(11)
An example of a purely empirical approach is the equation given in the THOR reports [32]. In the 1960s the Ballistic Analysis Laboratory and Ballistic Research Laboratory studied penetration for metallic and non-metallic materials and published reports with empirical equations developed from testing. The projectiles used in the THOR research were steel fragments and experimental data was characterized by fragment size, striking velocity, and the angle of obliquities. A base equation was developed with five experimental variables and five adjustable con- stants. This equation, for calculating residual velocity, is shown in Eq. (8). In the equation, vr represents fragment residual velocity, vs is the fragment striking velocity, t is the target thickness, A is the average impact area of fragment, θ is the angle of obliquity, w is the weight of the original fragment, mr is weight of residual fragment, and c, α, β, γ and λ are calibration constants.
Because the model is material dependent, two curves are generated from the single calibrated calibrated model: one curve for SPF-S and one curve for SYP. Fig. 13 shows the CLT THOR curves calibrated to both species of CLT data with calibration constants given in Table 7. The errors from the models are discussed in Section 6.6.
= v v tA w sec v 10 ( ) ( ) r s c s (8)
5.5. CLT UFC Model
The general THOR equation shown above can be rewritten for conditions when the residual velocity is zero as there is no perforation. The scope of this research is limited to normal impacts, an angle of obliquity of zero, which simplifies the formula and allows for exclusion of the variable, θ, and its associated parameter, γ. Next, the equation can be rearranged to solve for the thickness at which the residual ve- locity is zero, as shown in Eq. (9), where the constants are renamed to l,
While the UFC model for wood discussed in Section 5.1 did not fit the experimental data of embedment depth well, it did incorporate variables both measurable and relevant to a ballistic penetration event. A generic version of the UFC equation with unsolved calibration con- stants (C1, a, b, c, and d) is shown in Eq. (12).
19

# K. Sanborn et al. International Journal of Impact Engineering 128 (2019) 11–23 Fig. 12. Force Law penetration depth model calibrated with CLT data. Table 6 Calibration constants for Force Law model for CLT. Data Calibrated constants SPF-S and SYP CLT = = = a b c 3.550, 190.5, 574.7 a b d C v w

2
D c d 1
H
4

## ( )

(12)
Using the experimental data and the procedures for calibrating constants discussed previously, the UFC equation for wood was re-ca- librated for the CLT data to predict penetration depth. The results for both the SPF-S and SYP models as well as those from the original UFC equation are given in Fig. 14, with calibration constants given in Table 8. Note that the UFC calibration constants are those published in the UFC 4-023-07 and were not recalibrated to the data. The errors and comparison from the various models are discussed in the following section.
5.6. Model comparison and recommendations
The classical penetration mechanics models of Euler–Robins, Poncelet and Resal, along with the Force Law model, are all physics- based empirical models. The Force Law model, with a MSE of 1.32, was the best fitting model for the combined species CLT data set. The THOR models and the UFC model are curve-fitting empirical models. The THOR-based CLT model and the CLT UFC model performed better than the classical penetration models, likely because they include material parameters in the model. The THOR-based CLT model had a slightly better fit than the CLT UFC model. That said, all models that were re- calibrated to the CLT data performed better than the existing model using the UFC equation for predicting the thickness of solid wood re- quired to prevent perforation. This comparison is by now means all inclusive and additional models, such as those involving a linear ap- proach [33–35] and those involving dimensionless optimization [36], could also be considered as a means to predict the response. Based on this data set and the MSE, it is recommended that the THOR CLT model be used for predicting penetration depth for striking velocity ranging between 400 and 3,000 ft/s (120 to 910 m/s), for CLT of a thickness of greater than 4 in. (10.1 cm), and for projectiles with weights and areas similar to the 0.50 in. (12.7 mm) sphere projectile. Different weight, diameter, or nose shape projectiles could use a similar model, but it would require re-calibration of the model parameters. Additionally, for design purposes, a factor of safety should be implemented when de- termining how thick a CLT panel should be as there is variability in both the velocity of ballistic projectiles and in the wood material and it is ex- pected that the CLT will provide less resistance near the back face. Further research is needed to quantify the effect of these these factors.
Table 9 provides a summary of all the penetration depth models calibrated and/or developed in this research for CLT based on the two species of CLT considered. The table lists the model, constants, factors considered, and the mean square error (MSE) for the models.
Fig. 13. General THOR model and CLT THOR model calibrated with CLT data.
20

K. Sanborn et al. International Journal of Impact Engineering 128 (2019) 11–23
Table 7 Calibration constants for general THOR and CLT THOR model.
Model Data Calibrated constants
General THOR SPF-S and SYP CLT = = = f g h 1.305, 12.58, 3.967 CLT THOR SPF-S and SYP CLT = = = = = C f g a b 164.3, 1.493, 4.022, 1.373, 0.102 1
Fig. 14. UFC model and CLT UFC model calibrated with CLT data for both species of CLT.
Table 8 Calibration constants for CLT UFC model.
Data Calibrated constants
intermediate velocity range, such as those seen with munitions pro- jected from conventional weapons systems. Further evaluation would be needed for hypervelocity ranges, and it is likely that an upper bound exists for these models.
UFC Equation = = = = = C a b c d 9, 837, 0.411, 1.490, 1.360, 0.541 1 CLT UFC Equation = = = = = C e a b c d 6.91 6, 1.495, 1.434, 0.201, 0.237 1
6\. Residual velocity models
6.1. United facilities criteria (UFC) model
It is important to note that while the curves developed with these models appear to continue on to predict more wood thickness required at high velocities, these models likely do not apply to the hypervelocity range. For this research, the velocity ranges evaluated are limited to the
Similar to the equation for predicting the thickness of wood re- quired to prevent perforation, the UFC 4-023-07 also has a suggested equation for predicting the residual velocity of a projectile that has
Table 9 Summary of models considered for predicting depth of penetration of CLT.
Model Equation Constants Parameters included MSE
2
Euler–Robins
C1 striking velocity, vs 3.11
= d vs C
2 1
Poncelet
2 B, C striking velocity, vs 1.34
= + d ln 1 B Bvs C 1 2
Resal = + ( ) d ln 1 B Bvs A 1 B, A striking velocity, vs 1.71
Force law = + d b v a ac b ( 4 4 ) a s 1 2 2 a, b, c striking velocity, vs 1.32
General THOR
f, g, h striking velocity, vs 1.532
= d A vsf
gwh 1
10
projectile area, A projectile weight, w CLT THOR
C1, f, g, a, b striking velocity, vs 0.303
= d C vsf
g aHb 1 10
projectile weight, w target density, ρ target hardness, H CLT UFC
C1, a, b, c, d striking velocity, vs 0.330
= d C vsf
g aHb 1 10
projectile weight, w projectile area, A target density, ρ target hardness, H
21
