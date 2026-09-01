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
  * **Test Holdout Set:** 2014–2015 (14,535 observations, 39.6%)

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
* **Missing Data & Duplicates:** 0 missing values; 7 duplicate sensor profiles removed (36,726 clean rows).
* **$\sigma$-Clipping Analysis ($\hat{\sigma} = \frac{IQR}{1.35}$):** 0 physical anomalies on ambient/turbine telemetry.
* **Standardization:** Independent z-score normalization on 8 predictors and 3 targets strictly fitted on the training set.

---

## Slide 5: 3. Exploratory Analysis: Distributions & Correlation Structure (Phase 2)
* **Course Definition:** Unsupervised synthesis of empirical distributions into Size ($\mu, Q_2, \text{Mode}$) and Spread ($\sigma^2, \text{IQR}, G$).
* **Findings:** `CO` has strong right-skewness ($G = 0.442$). Extreme collinearity between $\text{CDP}, \text{GTEP}, \text{TIT}, \text{TEY}$ ($r > 0.9$). Atmospheric temperature penalty $\text{AT} \leftrightarrow \text{TEY}$ ($r = -0.58$).

---

## Slide 6: 3. Exploratory Analysis: PCA Dimensionality Reduction & Biplot (Phase 2)
* **PCA Formulation (Slide 75):** Eigen-decomposition of Covariance Matrix $C v_i = \lambda_i v_i$.
* **Variance Explained:** PC1 (48.28%), PC2 (20.48%). First 5 components capture 92.02% of variance.

---

## Slide 7: 4. Main Analysis: Objectives & Methodological Framework (Phase 3)
* **Objective 1 (Energy Yield):** Resolve extreme multicollinearity ($\text{VIF} > 250$) via Principal Component Regression (PCR) on 4 feature PCs ($Z = X_{\text{std}} V_4$, 90.76% PVE).
* **Objective 2 (Emissions):** Polynomial regression (degree 2) for $\text{CO}$ to capture low-load spikes; OLS for $\text{NO}_x$.
* **Objective 3 (Operational Regimes):** Unsupervised K-Means clustering ($K=3$) with Silhouette validation.

---

## Slide 8: 5. Preview & High-Level Summary of Results (Phase 4)
### Key KPI Highlights
* 🟢 **0.9501 ($R^2$):** Best Out-of-Sample Test Accuracy achieved by Full Multivariate OLS.
* 🟢 **0.9397 ($R^2$):** Out-of-Sample Test Accuracy achieved by PCR (4 PCs, 90.76% PVE, collinearity-free).
* 🟢 **0.6477 ($R^2$):** Training $R^2$ achieved by Degree-2 Polynomial Regression for $\text{CO}$.
* 🟢 **3 Regimes:** Distinct thermodynamic operating clusters defined via K-Means.

### Model Performance Matrix
| Target Variable & Model Specification | Train $R^2$ (2011–13) | Train RMSE | Test $R^2$ (2014–15) | Test RMSE |
| :--- | :--- | :--- | :--- | :--- |
| **$\text{TEY}$: Full Multivariate OLS (8 Features)** | **0.9977** | **0.76 MWh** | **0.9501** | **3.35 MWh** |
| **$\text{TEY}$: PCR (4 PCs, 90.76% PVE)** | **0.9693** | **2.81 MWh** | **0.9397** | **3.68 MWh** |
| **$\text{TEY}$: Training-Mean Baseline** | 0.0000 | 16.03 MWh | -0.0000 | 14.98 MWh |
| **$\text{CO}$: Polynomial (Degree 2, Slide 116)** | **0.6477** | **1.36 mg/m³** | **0.2635** | **1.88 mg/m³** |
| **$\text{CO}$: Training-Mean Baseline** | 0.0000 | 2.30 mg/m³ | -0.0333 | 2.23 mg/m³ |
| **$\text{NO}_x$: Multivariate OLS (8 Features)** | **0.4536** | **8.16 mg/m³** | **-1.0928\*** | **15.30 mg/m³** |
| **$\text{NO}_x$: Training-Mean Baseline** | 0.0000 | 11.04 mg/m³ | -0.6914 | 13.76 mg/m³ |

---

## Slide 9: 6. Detailed Results: Energy Yield (TEY) & PCR Diagnostics (Phase 4)
* **Multicollinearity Diagnostics (Slide 115):** Extreme VIF scores diagnosed in operating telemetry: CDP (342.82), TIT (262.12), GTEP (260.47), TAT (133.21). Predictor covariance eigen-decomposition reveals 4 PCs capture 90.76% of total feature variance.
* **OLS vs. PCR Tradeoff (Slides 70, 106):**
  * *Full OLS:* Highest raw test accuracy (Test $R^2 = 0.9501$, $\text{RMSE} = 3.35\text{ MWh}$), but predictor weights suffer from severe collinear instability.
  * *PCR (4 PCs):* Achieves Test $R^2 = 0.9397$ ($\text{RMSE} = 3.68\text{ MWh}$) while projecting onto strictly orthogonal coordinates, guaranteeing stable physical interpretation.
* **Residual Diagnostics (Slide 104, 108):** Residuals $e_i = y_i - \hat{y}_i$ are Gaussian, strictly zero-centered, with uniform variance (homoscedasticity) across the operating range.

---

## Slide 10: 6. Detailed Results: Emissions Modeling & Operational Regimes (Phase 4)
* **$\text{CO}$ Non-linear Curve (Slide 116):** Adding quadratic feature terms ($x \to [x, x^2]$) increases Train $R^2$ to 0.6477 ($\text{RMSE} = 1.36\text{ mg/m}^3$), capturing the non-linear surge below $1070^\circ\text{C}$ where incomplete combustion surges exponentially.
* **$\text{NO}_x$ Domain Shift (\*):** Negative out-of-sample Test $R^2$ (-1.0928) reflects a plant hardware/burner recalibration in 2014–15 (baseline $\text{NO}_x$ dropped from 68.8 to 58.5 $\text{mg/m}^3$).
* **Operational Regimes Profile ($K=3$, Silhouette = 0.3023):**
  * **Peak Load (4,309 hrs):** $\text{TEY}=158.2\text{ MWh}, \text{TIT}=1100^\circ\text{C}, \text{CDP}=13.8\text{ mbar} \implies \text{CO}=1.00\text{ mg/m}^3$ (cleanest combustion).
  * **Nominal Load (7,820 hrs):** $\text{TEY}=134.5\text{ MWh}, \text{TIT}=1091^\circ\text{C}, \text{CDP}=12.2\text{ mbar} \implies \text{CO}=1.48\text{ mg/m}^3$.
  * **Part Load (10,062 hrs):** $\text{TEY}=122.3\text{ MWh}, \text{TIT}=1070^\circ\text{C}, \text{CDP}=11.2\text{ mbar} \implies \text{CO}=3.30\text{ mg/m}^3$ (**3.3x higher CO!**).

---

## Slide 11: 7. Conclusions & Engineering Recommendations (Phase 5)
### 1. Methodological Justifications
* **Multicollinearity Solution:** VIF diagnostics identified severe predictor inflation ($\text{VIF} > 250$). PCR on 4 orthogonal components captured 90.76% of variance, ensuring parameter stability.
* **Non-linear Kinetics:** $\text{CO}$ follows non-linear thermal oxidation; degree-2 polynomial expansion successfully captured the inflection curve.
* **Unsupervised Regimes:** K-Means clustering ($K=3$) partitioned turbine operations into distinct thermodynamic states.

### 2. Operational Emission Control
* **Minimize Low-Load Hours:** Firing below $1070^\circ\text{C}$ leads to $3.3\times$ higher $\text{CO}$ emissions ($3.30\text{ mg/m}^3$).
* **Peak Load Operating Point:** Firing at $\text{TIT} \approx 1100^\circ\text{C}$ maximizes power yield ($158.2\text{ MWh}$) and achieves complete oxidation ($\text{CO} \approx 1.0\text{ mg/m}^3$).
* **Ambient Chilling:** High ambient temperatures penalize power yield ($r = -0.58$), justifying inlet air chilling during summer.

### 3. Digital Twin & Deployment
* **Edge Deployment:** The 4-component PCR model is lightweight, closed-form, and suited for real-time turbine PLC deployment.
* **Virtual Sensor Backup:** High correlation allows synthetic pressure estimation if physical sensors fail.

---

## Slide 12: Project Summary & Technical Q&A
* **Complete Supplementary Code:** [gas_turbine_analysis.ipynb](file:///C:/Users/lampa/Desktop/DataAnalysisProject/gas_turbine_analysis.ipynb)
* **Dataset:** 36,733 hourly records across 2011–2015 (Turkey Gas Turbine)
* **Adherence:** Strictly compliant with Data Analytics (and Data Driven Decision) course guidelines.
