# Project Work: Data Analytics & Predictive Modeling
**Flue Gas Emissions ($\text{CO}$, $\text{NO}_x$) and Energy Yield in Gas Turbines**
*Course: Data Analytics (and Data Driven Decision) — University of L'Aquila*

---

## Slide 1: Title Slide
* **Title:** Gas Turbine Emissions ($\text{CO}$, $\text{NO}_x$) and Energy Yield ($\text{TEY}$) Analytics
* **Subtitle:** Descriptive & Predictive Analytics on Multi-Year Hourly Sensor Measurements
* **Presenter:** Group Members
* **Context:** Department of Information Engineering, Computer Science and Mathematics (DISIM), University of L'Aquila

---

## Slide 2: Project Workflow & Guidelines Structure (Methodological Roadmap)
1. **Description of the Dataset:** Origin, physical sensors, 36,733 hourly observations, train/test protocol.
2. **Data Cleaning:** Missing values check, physical consistency verification, $\sigma$-clipping, standardization.
3. **Exploratory Data Analysis:** Course definition, size & spread synthesis, correlation structure, PCA exploration.
4. **Main Analysis & Methodology:** Dimensionality reduction (PCR), polynomial regression, VIF diagnostics, K-Means clustering.
5. **Preview of Results:** High-level summary of model performance and emission trade-offs.
6. **Detailed Results:** R², RMSE, residual analysis, out-of-sample test evaluation.
7. **Conclusions:** Operational insights and recommendations for emission mitigation.

---

## Slide 3: 1. Description of the Dataset & Sensor Features (Phase 1)
### Dataset Characteristics
* **Origin:** Operational gas turbine power plant in north-western Turkey.
* **Timeframe:** 2011 – 2015 (5 consecutive years).
* **Total Instances:** 36,733 hourly aggregated observations (0 missing values).
* **Protocol Split:**
  * **Training / CV Set:** 2011–2013 (22,191 observations, 60.4%)
  * **Test Holdout Set:** 2014–2015 (14,542 observations, 39.6%)

### Sensor Variables Breakdown
| Category | Variable | Unit | Description & Physical Role |
| :--- | :--- | :--- | :--- |
| **Ambient** | `AT` | °C | Ambient Temperature (influences air density & turbine mass flow) |
| | `AP` | mbar | Ambient Atmospheric Pressure |
| | `AH` | % | Ambient Relative Humidity (affects flame temperature) |
| **Turbine** | `AFDP` | mbar | Air Filter Difference Pressure (filter clogging/resistance) |
| | `GTEP` | mbar | Gas Turbine Exhaust Pressure |
| | `TIT` | °C | Turbine Inlet Temperature (primary thermodynamic efficiency driver) |
| | `TAT` | °C | Turbine After Temperature (exhaust gas temperature) |
| | `CDP` | mbar | Compressor Discharge Pressure |
| **Yield** | `TEY` | MWh | Turbine Energy Yield (hourly electrical output) |
| **Emissions**| `CO` | $\text{mg/m}^3$ | Carbon Monoxide (incomplete combustion indicator) |
| | `NOx` | $\text{mg/m}^3$ | Nitrogen Oxides ($\text{NO} + \text{NO}_2$, thermal NOx mechanism) |

---

## Slide 4: 2. Data Cleaning, Quality Validation & Preprocessing (Phase 1)
* **Missing Data & Duplicates:** 0 missing values; 7 duplicate records removed (36,726 clean rows).
* **$\sigma$-Clipping Analysis ($\hat{\sigma} = \frac{IQR}{1.35}$):** 0 physical anomalies on ambient/turbine telemetry.
* **Standardization:** $z = \frac{x - \mu_{\text{train}}}{\sigma_{\text{train}}}$ computed strictly on the training set.

---

## Slide 5: 3. Exploratory Analysis: Distributions & Correlation Structure (Phase 2)
* **Course Definition:** Unsupervised synthesis of empirical distributions into Size ($\mu, Q_2$) and Spread ($\sigma^2, \text{IQR}, G$).
* **Findings:** `CO` has strong right-skewness ($G = 0.442$). Extreme collinearity between $\text{CDP}, \text{GTEP}, \text{TIT}, \text{TEY}$ ($r > 0.9$). Atmospheric temperature penalty $\text{AT} \leftrightarrow \text{TEY}$ ($r = -0.58$).

---

## Slide 6: 3. Exploratory Analysis: PCA Dimensionality Reduction & Biplot (Phase 2)
* **PCA Formulation (Slide 75):** Eigen-decomposition of Covariance Matrix $C v_i = \lambda_i v_i$.
* **Variance Explained:** PC1 (48.28%), PC2 (20.48%). First 5 components capture 92.02% of variance.

---

## Slide 7: 4. Main Analysis: Objectives & Methodological Framework (Phase 3)
* **Objective 1 (Energy Yield):** Resolve extreme multicollinearity ($\text{VIF} > 250$) via Principal Component Regression (PCR).
* **Objective 2 (Emissions):** Polynomial regression (degree 2) for $\text{CO}$ to capture low-load spikes; OLS for $\text{NO}_x$.
* **Objective 3 (Operational Regimes):** Unsupervised K-Means clustering ($K=3$) with Silhouette validation.

---

## Slide 8: 5. Preview & High-Level Summary of the Results (Phase 4)
### Key KPI Highlights
* 🟢 **98.3% ($R^2$):** Best Out-of-Sample Test Accuracy achieved by PCR.
* 🟢 **1.96 MWh:** Out-of-Sample RMSE on Test Set (2014–2015).
* 🟢 **-41.4%:** Error Reduction achieved by PCR over unregularized OLS.
* 🟢 **3 Regimes:** Distinct thermodynamic operating clusters defined via K-Means.

### Model Performance Matrix
| Model & Objective Target | Train $R^2$ | Test $R^2$ (2014–15) | Test RMSE | Test MAE |
| :--- | :--- | :--- | :--- | :--- |
| **$\text{TEY}$: Ambient Baseline** | 0.1133 | -0.1407 | 15.996 MWh | 12.868 MWh |
| **$\text{TEY}$: Full Multivariate OLS** | 0.9977 | 0.9501 | 3.346 MWh | 3.176 MWh |
| **$\text{TEY}$: PCR (5 Components)** | **0.9946** | **0.9828** | **1.963 MWh** | **1.618 MWh** |
| **$\text{CO}$: Linear Multivariate OLS** | 0.5728 | 0.4195 | 1.668 mg/m³ | 1.110 mg/m³ |
| **$\text{CO}$: Polynomial (Degree 2)** | **0.6439** | **0.4546** | **1.617 mg/m³** | **1.138 mg/m³** |
| **$\text{NO}_x$: Multivariate OLS** | 0.4536 | -1.0928* | 15.301 mg/m³ | 13.851 mg/m³ |

---

## Slide 9: 6. Detailed Results: Energy Yield (TEY) & PCR Diagnostics (Phase 4)
* **Generalization Stability:** PCR achieves consistent test performance: 2014 $R^2 = 0.985$ and 2015 $R^2 = 0.982$.
* **Residual Diagnostics (Slide 104, 108):** Residuals $e_i = y_i - \hat{y}_i$ are Gaussian, strictly centered at zero (mean error = 0.04 MWh), with uniform variance (homoscedasticity) across the operating range.
* **Coefficient Significance (Slide 111):** All 5 Principal Components have statistically significant coefficients ($p < 0.001$), with confidence intervals strictly excluding zero.

---

## Slide 10: 6. Detailed Results: Emissions Modeling & Operational Regimes (Phase 4)
* **$\text{CO}$ Non-linear Curve (Slide 116):** Adding $\text{TIT}^2, \text{TAT}^2, \text{CDP}^2$ accurately captures the inflection point below $1070^\circ\text{C}$ where incomplete combustion escalates exponentially.
* **Operational Regimes Profile ($K=3$, Silhouette = 0.323):**
  * **Peak Load (4,887 hrs):** $\text{TEY}=157.0$ MWh, $\text{TIT}=1100^\circ\text{C} \implies \text{CO}=1.00$ mg/m³ (cleanest combustion).
  * **Part-Load (5,443 hrs):** $\text{TEY}=111.8$ MWh, $\text{TIT}=1056^\circ\text{C} \implies \text{CO}=4.79$ mg/m³ (**4.8x higher CO!**).
  * **Baseload (11,861 hrs):** $\text{TEY}=133.9$ MWh, $\text{TIT}=1089^\circ\text{C} \implies \text{CO}=1.53$ mg/m³.

---

## Slide 11: 7. Conclusions & Engineering Recommendations (Phase 5)
### 1. Methodological Justifications
* **Multicollinearity Solution:** VIF diagnostics identified severe predictor inflation ($\text{VIF} > 250$). PCR on 5 orthogonal components reduced test error by $41.4\%$ ($R^2_{\text{test}} = 0.9828$).
* **Non-linear Kinetics:** $\text{CO}$ follows non-linear thermal oxidation; degree-2 polynomial expansion successfully captured the inflection curve.
* **Unsupervised Regimes:** K-Means clustering ($K=3$) partitioned turbine operations into distinct thermodynamic states.

### 2. Operational Emission Control
* **Minimize Low-Load Hours:** Firing below $1070^\circ\text{C}$ leads to $4.8\times$ higher $\text{CO}$ emissions ($4.79\text{ mg/m}^3$).
* **Peak Load Operating Point:** Firing at $\text{TIT} \approx 1100^\circ\text{C}$ maximizes power yield ($157.0\text{ MWh}$) and achieves complete oxidation ($\text{CO} \approx 1.0\text{ mg/m}^3$).
* **Ambient Chilling:** High ambient temperatures penalize power yield ($r = -0.58$), justifying inlet air chilling during summer.

### 3. Digital Twin & Deployment
* **Edge Deployment:** The 5-component PCR model is lightweight, closed-form, and suited for real-time turbine PLC deployment.
* **Virtual Sensor Backup:** High correlation allows synthetic pressure estimation if physical sensors fail.

---

## Slide 12: Project Summary & Technical Q&A
* **Complete Supplementary Code:** [gas_turbine_analysis.ipynb](file:///C:/Users/lampa/Desktop/DataAnalysisProject/gas_turbine_analysis.ipynb)
* **Dataset:** 36,733 hourly records across 2011–2015 (Turkey Gas Turbine)
* **Adherence:** Strictly compliant with Data Analytics (and Data Driven Decision) course guidelines.
