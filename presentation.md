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
4. **Main Analysis & Methodology:** Dimensionality reduction (PCR), polynomial regression, VIF diagnostics, K-Means clustering.
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

---

## Slide 4: 2. Data Cleaning, Quality Validation & Preprocessing
* **Missing Data & Duplicates:** 0 missing values; 7 duplicate records removed (36,726 clean rows).
* **$\sigma$-Clipping Analysis ($\hat{\sigma} = \frac{IQR}{1.35}$):** 0 physical anomalies on ambient/turbine telemetry.
* **Standardization:** $z = \frac{x - \mu_{\text{train}}}{\sigma_{\text{train}}}$ computed strictly on the training set.

---

## Slide 5: 3. Exploratory Analysis: Distributions & Correlation Structure
* **Course Definition:** Unsupervised synthesis of empirical distributions into Size ($\mu, Q_2$) and Spread ($\sigma^2, \text{IQR}, G$).
* **Findings:** `CO` has strong right-skewness ($G = 0.442$). Extreme collinearity between $\text{CDP}, \text{GTEP}, \text{TIT}, \text{TEY}$ ($r > 0.9$). Atmospheric temperature penalty $\text{AT} \leftrightarrow \text{TEY}$ ($r = -0.58$).

---

## Slide 6: 3. Exploratory Analysis: PCA Dimensionality Reduction & Biplot
* **PCA Formulation (Slide 75):** Eigen-decomposition of Covariance Matrix $C v_i = \lambda_i v_i$.
* **Variance Explained:** PC1 (48.28%), PC2 (20.48%). First 5 components capture 92.02% of variance.

---

## Slide 7: 4. Main Analysis: Objectives & Methodological Framework
### Core Analytical Objectives
1. **Energy Yield Prediction ($\text{TEY}$) & Collinearity Resolution:**
   * *Problem:* Severe Multicollinearity among predictors ($\text{VIF} > 250$ for `CDP`, `TIT`, `GTEP`, Slide 115).
   * *Method:* Principal Component Regression (PCR, Slides 70, 106) using 5 orthogonal components ($Z = X V_p$) to guarantee numerical stability and out-of-sample generalization.
2. **Emissions Modeling ($\text{CO}$ & $\text{NO}_x$):**
   * *Problem:* Strong non-linear emission spikes at low turbine temperatures (incomplete combustion).
   * *Method:* Polynomial Feature Expansion (Slide 116 & Ex 4.1) for $\text{CO}$ ($x \to [x, x^2]$) while maintaining linear parameter estimation. Multivariate linear regression for $\text{NO}_x$.
3. **Operational Regime Discovery (Unsupervised):**
   * *Method:* K-Means Clustering (Slides 90–91) validated with Silhouette Coefficient analysis (Slide 94, Ex 3.1): $\text{SIL}_i = \frac{b_i - a_i}{\max(a_i, b_i)}$.
   * *Outcome:* Identifies 3 operational regimes: Peak Load (high yield, low CO), Baseload (nominal), and Part-load (high CO).

### Mathematical Formulations & Accuracy Metrics (Course Standards)
* **OLS Estimation:** $\hat{\beta} = (X^T X)^{-1} X^T y$ (Slide 106)
* **PCR Formulation:** $\hat{\beta}_{\text{PCR}} = (Z^T Z)^{-1} Z^T y$, where $Z = X_{\text{std}} V_p$
* **Multicollinearity VIF:** $\text{VIF}(\hat{\beta}_j) = \frac{1}{1 - R^2_{x_j|x_{-j}}}$ (Slide 115)
* **Accuracy Metrics:** $R^2 = 1 - \frac{\text{RSS}}{\text{TSS}}$ (Slide 108), $\text{RMSE} = \sqrt{\frac{1}{m}\sum (y_i - \hat{y}_i)^2}$
