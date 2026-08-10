K. Sanborn et al. International Journal of Impact Engineering 128 (2019) 11–23
Fig. 9. Striking velocity versus residual velocity data from SPF-S CLT (left) and SYP CLT (right) ballistic experiments for weathered specimen (i.e., varying moisture content).
Fig. 10. Impact velocity versus residual velocity data from CLT ballistic experiments for Spruce Pine Fir-South and Southern Yellow Pine CLT targets compared with prediction model of UFC 4-023-07.
Table 5 Classic penetration equations and associated penetration depth expressions.
Model Deceleration Penetration depth Calibrated constants
2
= C e 3.776 5
Euler–Robins = = a C constant = d vs C
2
2 = C e 1.887 5, = B 0.0672
Poncelet = + a C Bv2
= + d ln 1 B Bvs C 1 2
Resal + Av Bv2 = + ( ) d ln 1 B Bvs A 1 = A 0.0497, = B 363.9
expression for the final penetration depth, d, in terms of striking velo- city, vs. Table 5 gives the penetration ballistics equations credited to each scientist as well as the calibrated constants that were derived by the authors for this dataset. The results from the ballistic test series and the Levenberg- Marquardt algorithm [30] were used to determine the constants in the three classical penetration models. The calibrated constants are given in Table 5. These models have also been used by other researchers for solid wood [31]. The results of the three models are shown in Fig. 11 for both species of CLT data combined. The errors from the models and comparisons are discussed in Section 6.6. It should be noted that the reference values [3] for hardness and density were used in this cali- bration because it is expected that a typical user would not necessarily conduct material testing. The measured values are provided above in Table 2 as well as in the spreadsheet provided in the linked document. The models can be re-calibrated using the same procedure and the measured properties, if desired.
Early in the investigation of penetration mechanics, various theories were proposed to describe the relation between deceleration and ve- locity. Most were based on a general expression for the deceleration term shown in Eq. (5), where v represents velocity, a(v) is deceleration relative to velocity and A, B, and C are constants that must be de- termined empirically. The terms on the right side of the equation are commonly associated with the cohesive resistance of the target, C, a frictional effect, Av, and acceleration of target material in the impact area, Bv2.
5.3. Force law model
= + + a v C Av Bv ( ) 2 (5)
Based on the classical equations with variations of the deceleration equation, an additional physics-based model was developed and cali- brated to the CLT data. This model was based on the concept of a re- sisting force of the target specimen reducing the velocity of the pro- jectile. This resisting force acts as an external force on the projectile,
Classic penetration equations based on these fundamental re- lationships and assumptions were developed by Euler and Robins [26,27], Poncelet [28], and Resal [29]. Through integration, the ex- pression for deceleration relative to velocity can be transformed into an
18

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

K. Sanborn et al. International Journal of Impact Engineering 128 (2019) 11–23
velocity. Because of this, a reduction factor, R, was added as a cali- bration factor. The resulting equation for residual velocity is therefore given in Eqs. (17) and (18).
perforated through the wood [21]. This equation is given in Eq. (13), where vr is the residual velocity, vs is the striking velocity, Tw is the thickness required to prevent perforation, and t is the actual thickness of the wood.
= v v Rv r s per (17)
0.5735
(1/ )
= v v t T 1.0 r s w
(13)
= v v R t C H (10 ) r s g a b f
1
(18)
Eq. (18) calibrated with the 5-ply SPF-S data and a reduction factor, R, calibrated to 0.67 was determined to yield the minimum error. The curve associated with this new model is shown in Fig. 15 along with the results from the UFC residual velocity models. Clearly, this newly de- veloped model does a better job at predicting the response than the other models, even those that were also calibrated to data. Because this data set consisted of only two wood species and one projectile, future research is recommended to validate this model over other ranges of parameters.
The 5-ply SPF-S (average thickness = 6.875 in (17.5 cm)) was used to demonstrate the fit of this equation. The CLT THOR model (Section 6.4) was used to estimate the value of Tw. Fig. 15 plots the experimental data for residual velocity, vr. The plot also shows the line for the pre- dicted residual velocity based on the suggested UFC equation. Ad- ditionally, the plot shows a newly calibrated model based on the gen- eralized form given in Eq. (14), where the α is a calibration constant and d is the penetration depth determined by the CLT THOR model. In this case, the constant α was determined to be 1.643. This model is able to only acceptably predict the response over a small range of striking velocities centered around 2,500 ft/s (762 m/s).
7\. Conclusions
= v v t d 1.0 r s (14)
6.2. THOR-based residual velocity model
Because the calibrated THOR model was able to best predict the penetration depth (see Section 6.4 and Section 6.6), a new residual velocity model was developed to take advantage of this calibrated model, given in Eq. (11). The residual velocity, vr, is zero when the final penetration depth, d, is exactly equal to (or less than) the thickness of the CLT, t. In other words, when the projectile stops exactly at the back face its residual velocity will be zero. If a new variable, vper is defined as the perforation velocity or the maximum striking velocity that results in no perforation (i.e., residual velocity of zero), then Eq. (11) can be rewritten as in Eqs. (15) and (16).
(1/ )
= v d C H (10 ) s g a b f
1
(15)
(1/ )
= v t C H (10 ) per g a b f
1
(16)
When investigating a new material, such as CLT, for ballistic pe- netration resistance, experimental testing is a critical first step. Testing helps build a database of parameters and responses that can be used to develop empirical models either through curve-fitting or applying physics-based methods. These models can in turn guide additional testing to further refine empirical models or analytical models. As the first set of ballistic experiments conducted on CLT, this research pro- vides the critical first step. This research consisted of 152 ballistic ex- periments that were conducted at the U.S. Army Engineer Research and Development Center on two species of CLT: Spruce Pine Fir-South (SPF- S) and Southern Yellow Pine (SYP). Data was generated to understand and characterize the performance of the two species with varying thicknesses (i.e., number of plies in the CLT). In general, the SYP per- formed better, in terms of penetration resistance, than the SPF-S spe- cimens. This is likely a function of the increased density and hardness of SYP relative to SPF-S. Experiments were also conducted to determine the effects of weathering (i.e., moisture content) on the ballistic per- formance. While the data set was limited, initial findings suggest that the effect of weathering on the ballistic performance within the ranges of velocity and moisture contents considered is negligible. The CLT ballistic data sets were compared to current wood predic- tion models in the U.S. Unified Facilities Criteria. Results of this ex- ercise showed the models do not accurately predict the embedment depth or residual velocity for CLT. A variety of models were developed and explored to better predict the responses, both classical (physics- based) and purely empirical. It was found that the models that
The residual velocity, vr, can then be computed as the difference between the striking velocity, vs, and the perforation velocity, vper. Because the projectile has less resistance near the back face of the CLT (see Fig. 5), it is expected that the residual velocities predicted by the equations derived in Section 6 will underpredict the actual residual
Fig. 15. 5 ply SPF-S residual velocity as a function of striking velocity with three predictive models: 1) UFC 4-023-07 wood model, 2) re-calibrated UFC model, and 3) calibrated THOR-based model.
22
