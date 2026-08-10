# Section 5.7-5.8: Radial Velocity as a Function of Time

**Source Pages:** 103–105 (printed pages 88–90)

## Gurney Equation and Maximum Velocity

From page 103 (printed page 88):

In Chapter 1, a brief discussion was provided regarding an equation developed by Gurney (1943) for predicting the maximum velocity, V_max, of shells subjected to internal explosive detonations. Gurney's equation for a cylindrical shell is written as,

$$V_{\max} = \sqrt{2E\left(\frac{M}{C} + \frac{1}{2}\right)^{-1/2}$$ (6.1)

where M/C is the ratio of the mass of the shell to the mass of the explosive and √(2E) is called the Gurney constant. The empirical constant, √(2E), was determined from experiments involving a particular type of explosive. For PBX-9501, √(2E) is equal to 2900 m/s. The results shown in Table 5.3 indicate the calculated values of the Gurney velocity for the experiments conducted in this dissertation.

## Table 5.3: Gurney Velocity for Cylindrical Shell Experiments

| Shell Thickness     | Mass of HE (kg/m) | Mass of Shell (kg/m) | M/C   | V_max (m/s) |
| ------------------- | ----------------- | -------------------- | ----- | ----------- |
| 2.54 mm Thick Shell | 14.98             | 7.46                 | 0.498 | 2902        |
| 5.08 mm Thick Shell | 14.98             | 15.29                | 1.02  | 2351        |

**Criteria tabulated:** Maximum radial velocity predicted by Gurney's equation for each test cylinder, indexed by M/C ratio and shell thickness. Units: velocity in m/s, mass per unit length in kg/m.

## Figure 5.7: Radial Velocity as a Function of Time for the 2.54 mm Thick Cylinder

**Source Page:** 104 (printed page 89)

- **Y-axis:** Velocity (m/s), range 0–3000
- **X-axis:** Time (microseconds), range 0–40
- **Curves plotted:**
    - Numerical Results (solid line)
    - Gurney Velocity (dashed line, constant ~2900 m/s)
    - Experimental Data (solid line with markers, from Fabry-Perot instrumentation)
- **Key observations:**
    - Rapid velocity acceleration phase occurs between 25–30 microseconds
    - Maximum velocity reached ~2750–2800 m/s
    - Numerical model and experimental data show close agreement through the acceleration phase
    - Plateau phase begins around 30 microseconds at ~2700–2750 m/s
    - Gurney velocity provides an upper bound (~2900 m/s)

**Figure caption (verbatim):** "Figure 5.7: Radial Velocity as a Function of Time for the 2.54 mm Thick Cylinder"

## Figure 5.8: Radial Velocity as a Function of Time for the 5.08 mm Thick Cylinder

**Source Page:** 104 (printed page 89)

- **Y-axis:** Velocity (m/s), range 0–2500
- **X-axis:** Time (microseconds), range 0–65
- **Curves plotted:**
    - Numerical Results (solid line)
    - Gurney Velocity (dashed line, constant ~2350 m/s)
    - *Note: No Experimental Data (Fabry-Perot equipment experienced hardware failure for this cylinder)*
- **Key observations:**
    - Longer acceleration phase compared to 2.54 mm cylinder (extends to ~50 microseconds)
    - Maximum velocity reached ~2300–2350 m/s
    - Numerical model predicts smooth acceleration profile
    - Plateau phase begins around 50 microseconds
    - Gurney velocity aligns closely with numerical plateau (~2350 m/s)

**Figure caption (verbatim):** "Figure 5.8: Radial Velocity as a Function of Time for the 5.08 mm Thick Cylinder"

## Discussion and Results Comparison (Page 105, printed page 90)

From page 104 (printed page 89), immediately following the figures:

"Figures 5.7 and 5.8 show the velocity of the cylinder wall for the 2.54 and 5.08 mm thick cylinders. The plots shown in Figure 5.7 include the velocities from the empirical Gurney equation, the Fabry-Perot instrumentation, and the numerical model. The plots shown in Figure 5.8 only include the velocities from the empirical Gurney equation and the numerical model. Recall the Fabry-Perot equipment experienced a hardware failure and as a result, was not able to record data for the 5.08 mm thick cylinder. However, good agreement with the available data is shown in both figures."

From page 105 (printed page 90):

"The experiments documented in Chapter 4 of this dissertation were designed to verify the numerical model and good agreement is shown in Figures 5.3 to 5.8. The deformed geometry plots in Figures 5.3 and 5.4 are reasonably close. At locations away from the cylinder ends, the correlation of the deformed shape is very good. The radial displacement plots in Figures 5.5 and 5.6 are also quite close and again a slight variation is observed at the ends of the cylinders. In Figures 5.7, excellent correlation exists between the radial velocity obtained from the experimental data and the predictions from [continued on next page]"

## Table 5.4: Number of Instabilities for Each Cylinder (Page 105, printed page 90)

| Shell Thickness     | Number of Instabilities |
| ------------------- | ----------------------- |
| 2.54 mm Thick Shell | 298                     |
| 5.08 mm Thick Shell | 343                     |

**Table caption (verbatim):** "Table 5.4: Number of Instabilities for Each Cylinder as Determined from the Fast Framing Camera Photographs"

**Criteria tabulated:** Count of circumferential instabilities observed in framing camera imagery for each test cylinder, extracted via image digitization and circumferential analysis.

______________________________________________________________________

## Summary of Key Findings

1. **Predicted vs. Measured Maximum Velocity:**

    - 2.54 mm cylinder: Gurney prediction 2902 m/s; experimental/numerical plateau ~2750–2800 m/s
    - 5.08 mm cylinder: Gurney prediction 2351 m/s; numerical plateau ~2300–2350 m/s

1. **Acceleration Timescales:**

    - 2.54 mm: ~25–30 microseconds to reach maximum velocity
    - 5.08 mm: ~50 microseconds to reach maximum velocity (longer acceleration phase due to greater mass)

1. **Model Validation:**

    - Numerical model shows excellent agreement with experimental (Fabry-Perot) data for 2.54 mm cylinder
    - Numerical model aligns well with Gurney predictions for both cylinders
    - Instability growth observed: 298 instabilities (2.54 mm), 343 instabilities (5.08 mm)
