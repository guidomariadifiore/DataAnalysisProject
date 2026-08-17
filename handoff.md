# Project Work Handoff & Continuity Document

**Course:** Data Analytics (and Data Driven Decision) — University of L'Aquila (DISIM)  
**Instructor:** Prof. Andrea Manno  
**Dataset:** Gas Turbine CO and NOx Emission Dataset (2011–2015)  
**Workspace:** `C:\Users\lampa\Desktop\DataAnalysisProject`  
**Status:** Steps 1 through 4 completed. Steps 5, 6, and 7 ready for implementation.

---

## 1. Project Overview & Deliverable Requirements

According to [project_work_guidelines.pdf](file:///C:/Users/lampa/Desktop/DataAnalysisProject/project_work_guidelines.pdf), the project work consists of two synchronized deliverables following a **7-point sequential structure**:

| Part | Deliverable | Format & Requirements |
| :--- | :--- | :--- |
| **Part A** | **Presentation** | PowerPoint ([`presentation.pptx`](file:///C:/Users/lampa/Desktop/DataAnalysisProject/presentation.pptx)) & Markdown ([`presentation.md`](file:///C:/Users/lampa/Desktop/DataAnalysisProject/presentation.md)). Strict maximum of **15 slides** and **15 minutes duration**. |
| **Part B** | **Supplementary Material** | Jupyter Notebook ([`gas_turbine_analysis.ipynb`](file:///C:/Users/lampa/Desktop/DataAnalysisProject/gas_turbine_analysis.ipynb)). Highly technical, self-contained, commented code, strictly adhering to course models and libraries. |

### The 7-Step Guidelines Roadmap
1. ✅ **Description of the dataset** *(Completed)*
2. ✅ **Data cleaning (if needed)** *(Completed)*
3. ✅ **Exploratory analysis** *(Completed)*
4. ✅ **Main analysis: objective and methods adopted** *(Completed)*
5. ⏳ **Preview / summary of the results** *(Next Step)*
6. ⏳ **Detailed results** *(Pending)*
7. ⏳ **Conclusions** *(Pending)*

---

## 2. Current State of Deliverables

### A. Jupyter Notebook (`gas_turbine_analysis.ipynb`)
The notebook contains clean, tested code and theoretical markdown notes for:
* **Section 0:** Library setup (`pandas`, `numpy`, `matplotlib`, `seaborn`).
* **Section 1 (Description):** Background, variable definitions, and multi-year ingestion of 36,733 records.
* **Section 2 (Cleaning):** Null check, duplicate removal (7 dropped $\to$ 36,726 clean), $\sigma$-clipping ($\hat{\sigma} = \frac{\text{IQR}}{1.35}$), chronological Train (2011–13) / Test (2014–15) partitioning, and Z-score standardization.
* **Section 3 (EDA):** Course Size vs. Spread synthesis (Mean, Median, Std, IQR, Gini $G$), Pearson correlation heatmap, physical bivariate plots, and Covariance-based PCA (Scree plot & Biplot).
* **Section 4 (Main Analysis):** Variance Inflation Factor (VIF) collinearity diagnostics, OLS regression engine, Principal Component Regression (PCR), Polynomial feature expansion for $\text{CO}$, and K-Means clustering with Silhouette validation.

### B. PowerPoint Presentation (`presentation.pptx` & `presentation.md`)
Currently structured into **7 polished 16:9 slides**:
* **Slide 1:** Title Slide (Project context & metadata).
* **Slide 2:** Project Workflow & The 7 Guidelines Steps.
* **Slide 3:** *1. Description of the Dataset & Sensor Features* (Origins, split protocol, sensor table).
* **Slide 4:** *2. Data Cleaning, Quality Validation & Preprocessing* ($\sigma$-clipping summary table, deduplication, scaling).
* **Slide 5:** *3. Exploratory Analysis: Distributions & Correlation Structure* (Size/spread findings, high-res correlation heatmap).
* **Slide 6:** *3. Exploratory Analysis: PCA Dimensionality Reduction & Biplot* (PVE decomposition, 2D biplot graphic).
* **Slide 7:** *4. Main Analysis: Objectives & Methodological Framework* (The 3 core objectives, VIF table, mathematical equations).

### C. Generated Visual Figures (`figures/`)
* [`figures/eda_correlation_heatmap.png`](file:///C:/Users/lampa/Desktop/DataAnalysisProject/figures/eda_correlation_heatmap.png)
* [`figures/eda_pca_scree.png`](file:///C:/Users/lampa/Desktop/DataAnalysisProject/figures/eda_pca_scree.png)
* [`figures/eda_pca_biplot.png`](file:///C:/Users/lampa/Desktop/DataAnalysisProject/figures/eda_pca_biplot.png)
* [`figures/eda_physical_relationships.png`](file:///C:/Users/lampa/Desktop/DataAnalysisProject/figures/eda_physical_relationships.png)
* [`figures/main_kmeans_silhouette.png`](file:///C:/Users/lampa/Desktop/DataAnalysisProject/figures/main_kmeans_silhouette.png)

---

## 3. Key Analytical Findings Established So Far

1. **Severe Multicollinearity Diagnosed (Slide 115 of `DA.pdf`):**
   * Operational predictors exhibit massive variance inflation: $\text{CDP}$ ($\text{VIF} = 342.82$), $\text{TIT}$ ($\text{VIF} = 262.12$), and $\text{GTEP}$ ($\text{VIF} = 260.47$).
2. **Principal Component Regression (PCR) Superiority:**
   * Fitting OLS with all 8 collinear predictors produces out-of-sample Test $R^2 = 0.9501$ ($\text{RMSE} = 3.35\text{ MWh}$).
   * Using PCR with 5 orthogonal principal components ($Z = X_{\text{std}} V_p$) eliminates variance inflation and boosts Test $R^2$ to **$0.9828$** ($\text{RMSE} = 1.96\text{ MWh}$).
3. **Non-Linear Emissions Modeling ($\text{CO}$):**
   * Second-degree polynomial expansion (Slide 116 & Ex 4.1) increases $\text{CO}$ $R^2$ from $0.5728$ to **$0.6439$**, capturing steep emission surges during off-design low-temperature firing.
4. **Operational Regimes (K-Means & Silhouette, Slides 90–94):**
   * Optimal clustering ($K=3$, $\text{Silhouette} = 0.323$) establishes three regimes:
     * **Peak Load:** $\text{TEY} \approx 157.0\text{ MWh}, \text{TIT} \approx 1100^\circ\text{C}, \text{CO} \approx 1.00\text{ mg/m}^3$ (high efficiency).
     * **Nominal Baseload:** $\text{TEY} \approx 133.9\text{ MWh}, \text{TIT} \approx 1088^\circ\text{C}, \text{CO} \approx 1.53\text{ mg/m}^3$ ($53.5\%$ of hours).
     * **Part-Load / Transient:** $\text{TEY} \approx 111.8\text{ MWh}, \text{TIT} \approx 1056^\circ\text{C}, \text{CO} \approx 4.79\text{ mg/m}^3$ (incomplete combustion peaks).

---

## 4. Next Action Plan for the Incoming Agent

When resuming work, execute the following three remaining steps:

### Step 5: Preview / Summary of the Results
* **In Notebook:** Add Section 5 with high-level comparison tables summarizing Model performance ($R^2$, RMSE on Train vs Test) across Energy Yield ($\text{TEY}$), $\text{CO}$, and $\text{NO}_x$.
* **In Presentation:** Add **Slide 8: 5. Preview & Summary of Results** with concise scorecard cards and radar/bar comparisons.

### Step 6: Detailed Results & Model Diagnostics
* **In Notebook:** Add Section 6 containing:
  - In-depth residual analysis ($e_i = y_i - \hat{y}_i$) vs predicted values and normality QQ plots (Slide 109).
  - Cross-year validation across 2011, 2012, 2013, 2014, 2015.
  - Regression coefficient tables with confidence intervals (Slide 111).
* **In Presentation:** Add **Slide 9 & Slide 10: 6. Detailed Model Results & Residual Diagnostics** with generated diagnostic plots.

### Step 7: Conclusions & Operational Recommendations
* **In Notebook:** Add Section 7 summarizing engineering takeaways, trade-off management ($\text{CO}$ vs $\text{NO}_x$), and decision-support guidance for power plant operators.
* **In Presentation:** Add **Slide 11 & Slide 12: 7. Conclusions & Industrial Implications**.

---

## 5. Helpful Commands & Generator Scripts

* **To regenerate/update the PowerPoint deck:**
  ```powershell
  python create_presentation.py
  ```
* **To regenerate/update the Jupyter Notebook:**
  ```powershell
  python create_notebook.py
  ```
* **Course Slide Reference:**
  The complete lecture slide deck is stored in [`lectures/Slides/Slides/DA.pdf`](file:///C:/Users/lampa/Desktop/DataAnalysisProject/lectures/Slides/Slides/DA.pdf).
