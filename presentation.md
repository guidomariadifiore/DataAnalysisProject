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

## Slide 2: Project Workflow (The 7 Guideline Steps)
1. **Description of the Dataset:** Origin, physical sensors, 36,733 hourly observations, train/test protocol.
2. **Data Cleaning:** Missing values check, physical consistency verification, $\sigma$-clipping, standardization.
3. **Exploratory Data Analysis:** Course definition, size & spread synthesis, correlation structure, PCA exploration.
4. **Main Analysis & Methodology:** Dimensionality reduction (PCA), linear regression, diagnostic tests.
5. **Preview of Results:** High-level summary of model performance and emission trade-offs.
6. **Detailed Results:** R², RMSE, residual analysis, out-of-sample test evaluation.
7. **Conclusions:** Operational insights and recommendations for emission mitigation.

---

## Slide 3: 1. Description of the Dataset & Sensor Features
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

## Slide 4: 2. Data Cleaning, Quality Validation & Preprocessing
### 1. Data Integrity & Deduplication
* **Missing Data:** 0 missing / null values across all 11 sensor channels.
* **Duplicates:** 7 duplicate sensor records identified and pruned (36,726 clean records remaining).
* **Sensor Health:** All readings reside within physically coherent ranges (no negative pressures or aberrant extremes).

### 2. Course $\sigma$-Clipping Analysis ($\hat{\sigma} = \frac{IQR}{1.35}$)
* **Methodology:** Robust estimation of dispersion using $\hat{\sigma} = \frac{Q_3 - Q_1}{1.35}$ and median ($Q_2$) to prevent outlier masking.
* **Ambient & Operating Variables:** 0 anomalies outside $[Q_2 - 5\hat{\sigma},\; Q_2 + 5\hat{\sigma}]$; 100% physically valid.
* **Emissions Behavior ($\text{CO}$, $\text{NO}_x$):** Asymmetric distributions with high tail values correspond to physical transient regimes (startup, low-load incomplete combustion, and high-temperature peaks); retained for modeling.

### 3. Chronological Protocol & Z-Score Scaling
* **Training Set (2011–2013):** 22,187 instances (60.4%).
* **Test Holdout Set (2014–2015):** 14,539 instances (39.6%).
* **Standardization:** $z = \frac{x - \mu_{\text{train}}}{\sigma_{\text{train}}}$ computed strictly on the training set to prevent data leakage.

---

## Slide 5: 3. Exploratory Analysis: Distributions & Correlation Structure
### Course Definition & Statistical Synthesis (Slides 3, 10–18, 64)
* **Definition:** Unsupervised synthesis of empirical distributions into **Size / Center** ($\mu, Q_2$) and **Spread / Dispersion** ($\sigma^2, \text{IQR}, G$).
* **Size vs. Spread Findings:**
  * `CO` mean ($2.21$) exceeds its median ($1.52$) by ~45%, accompanied by a high Gini coefficient ($G = 0.442$), revealing strong right-skewness and episodic emission spikes during off-design loads.
  * Turbine operating parameters (`TIT`, `TAT`, `CDP`) exhibit tight symmetric distributions concentrated around nominal baseload.
* **Multivariate Pearson Correlation ($r_{XY}$):**
  * **Thermodynamic Coupling:** $\text{CDP} \leftrightarrow \text{TEY}$ ($r = 0.99$), $\text{GTEP} \leftrightarrow \text{TEY}$ ($r = 0.98$), $\text{TIT} \leftrightarrow \text{TEY}$ ($r = 0.89$) indicate strong mutual collinearity.
  * **Atmospheric Density Penalty:** $\text{AT} \leftrightarrow \text{TEY}$ ($r = -0.58$) and $\text{AT} \leftrightarrow \text{CDP}$ ($r = -0.51$) confirm that higher ambient temperatures decrease intake air density, reducing net energy output.
  * **Combustion Trade-off:** $\text{CO} \leftrightarrow \text{NO}_x$ ($r = -0.37$) illustrates the physical trade-off between complete fuel oxidation and thermal $\text{NO}_x$ generation.

---

## Slide 6: 3. Exploratory Analysis: PCA Dimensionality Reduction & Biplot
### PCA as an Exploratory Technique (Slide 70 & Exercise 2.3)
* **Formulation:** Eigen-decomposition of sample Covariance Matrix: $C v_i = \lambda_i v_i$.
* **Variance Decomposition (PVE):**
  * **PC1 (48.28% PVE):** Turbine thermodynamic load component (heavy positive loadings on `CDP`, `TEY`, `GTEP`, `TIT`).
  * **PC2 (20.48% PVE):** Environmental temperature & combustion trade-off axis (opposing loadings on `AT`/`NOx` vs `CO`).
  * **Cumulative Coverage:** First 2 components explain **68.76%** of total variance; first 5 components explain **92.02%** (Scree plot elbow at $p=5$).
* **Exploratory Takeaway:** The 11 physical sensor variables collapse into an effective low-dimensional manifold governed primarily by power dispatch demand and ambient weather conditions.
