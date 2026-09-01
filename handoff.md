# Project Work Handoff & Continuity Document

**Course:** Data Analytics (and Data Driven Decision) — University of L'Aquila (DISIM)  
**Instructor:** Prof. Andrea Manno  
**Dataset:** Gas Turbine CO and NOx Emission Dataset (2011–2015)  
**Workspace:** `C:\Users\patma\Desktop\code\progetto manno`  
**Status:** Steps 1 through 5 completed and verified. Steps 6 and 7 remain presentation-only.

---

## 1. Project Overview & Deliverable Requirements

According to the project work guidelines, the project work consists of two synchronized deliverables following a **7-point sequential structure**:

| Part | Deliverable | Format & Requirements |
| :--- | :--- | :--- |
| **Part A** | **Presentation** | PowerPoint and Markdown presentation. Strict maximum of **15 slides** and **15 minutes duration**. |
| **Part B** | **Supplementary Material** | Jupyter Notebook (`gas_turbine_analysis.ipynb`). Highly technical, self-contained, commented code, strictly adhering to course models and libraries. |

### The 7-Step Guidelines Roadmap
1. ✅ **Description of the dataset** *(Completed)*
2. ✅ **Data cleaning (if needed)** *(Completed)*
3. ✅ **Exploratory analysis** *(Completed)*
4. ✅ **Main analysis: objective and methods adopted** *(Completed)*
5. ✅ **Preview / summary of the results** *(Completed in the notebook)*
6. ⏳ **Detailed results** *(Presentation only)*
7. ⏳ **Conclusions** *(Presentation only)*

---

## 2. Current State of Deliverables

### A. Jupyter Notebook (`gas_turbine_analysis.ipynb`)
The notebook contains clean, tested code and theoretical markdown notes for:
* **Section 0:** Library setup (`pandas`, `numpy`, `matplotlib`, `seaborn`).
* **Section 1 (Description):** Background, variable definitions, and multi-year ingestion of 36,733 records.
* **Section 2 (Cleaning):** Null check, physical sanity validation, duplicate removal (7 dropped $\to$ 36,726 clean), descriptive $\sigma$-clipping ($\hat{\sigma} = \frac{\text{IQR}}{1.35}$), chronological Train (2011–13) / Test (2014–15) partitioning, and training-only standardization.
* **Section 3 (EDA):** Course Size vs. Spread synthesis (Mean, Median, Mode, Variance, Std, IQR, Gini $G$), Pearson correlation heatmap with calculated correlations, physical bivariate plots, and descriptive covariance-based PCA (Scree plot & Biplot).
* **Section 4 (Main Analysis):** Variance Inflation Factor (VIF) collinearity diagnostics, OLS evaluation, Principal Component Regression (PCR), second-degree polynomial feature expansion for $\text{CO}$, and K-Means clustering with corrected Silhouette validation.
* **Section 5 (Preview):** Comparative table with training/test $R^2$ and RMSE for OLS, PCR, polynomial CO regression, NOX regression, and a training-mean baseline. The complete notebook has been executed sequentially with no cell errors.

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
* [`figures/eda_correlation_heatmap.png`](figures/eda_correlation_heatmap.png)
* [`figures/eda_pca_scree.png`](figures/eda_pca_scree.png)
* [`figures/eda_pca_biplot.png`](figures/eda_pca_biplot.png)
* [`figures/eda_physical_relationships.png`](figures/eda_physical_relationships.png)
* [`figures/main_kmeans_silhouette.png`](figures/main_kmeans_silhouette.png)

---

## 3. Key Analytical Findings Established So Far

1. **Severe Multicollinearity Diagnosed (Slide 115 of `DA.pdf`):**
   * Operational predictors exhibit massive variance inflation: $\text{CDP}$ ($\text{VIF} = 342.82$), $\text{TIT}$ ($\text{VIF} = 262.12$), and $\text{GTEP}$ ($\text{VIF} = 260.47$).
2. **Energy Yield Models:**
  * OLS with all 8 predictors produces Test $R^2 = 0.9501$ and RMSE $= 3.35\text{ MWh}$.
  * PCR retains 4 orthogonal principal components covering 90.76% of feature variance and produces Test $R^2 = 0.9397$ and RMSE $= 3.68\text{ MWh}$.
  * In this verified run, OLS has better predictive test performance than the 4-component PCR model, although PCR remains useful for reducing multicollinearity.
3. **Non-Linear Emissions Modeling ($\text{CO}$):**
  * The degree-2 polynomial model produces Train $R^2 = 0.6477$ and Test $R^2 = 0.2635$ (RMSE $= 1.88\text{ mg/m}^3$).
4. **NOX Modeling:**
  * The multivariate OLS model produces Train $R^2 = 0.4536$ but Test $R^2 = -1.0928$ (RMSE $= 15.30\text{ mg/m}^3$), so generalization is poor and the result must be reported transparently.
5. **Operational Regimes (K-Means & Silhouette, Slides 90–94):**
  * $K=3$ is retained for interpretability, with Silhouette $= 0.3023$. The highest tested silhouette is $K=2$ with $0.3763$.
  * **Peak Load:** $\text{TEY} \approx 158.16\text{ MWh}, \text{TIT} \approx 1099.61^\circ\text{C}, \text{CO} \approx 1.00\text{ mg/m}^3$.
  * **Nominal Load:** $\text{TEY} \approx 134.45\text{ MWh}, \text{TIT} \approx 1090.73^\circ\text{C}, \text{CO} \approx 1.48\text{ mg/m}^3$.
  * **Part Load:** $\text{TEY} \approx 122.28\text{ MWh}, \text{TIT} \approx 1070.06^\circ\text{C}, \text{CO} \approx 3.30\text{ mg/m}^3$.

---

## 4. Next Action Plan

The notebook steps 1-5 are complete. The remaining work concerns the presentation-only points 6-7 and the final synchronization of project documents.

### Step 5: Preview / Summary of the Results
* **In Notebook:** Completed and verified in Section 5.
* **In Presentation:** Add **Slide 8: 5. Preview & Summary of Results** with concise scorecard cards and model comparisons.

### Step 6: Detailed Results & Model Diagnostics (Presentation Only)
* **In Notebook:** Not required under the current project scope.
* **In Presentation:** Add **Slide 9 & Slide 10: 6. Detailed Model Results & Residual Diagnostics** with:
  - In-depth residual analysis ($e_i = y_i - \hat{y}_i$) vs predicted values and normality QQ plots (Slide 109).
  - Cross-year validation across 2011, 2012, 2013, 2014, 2015.
  - Regression coefficient tables with confidence intervals (Slide 111).

### Step 7: Conclusions & Operational Recommendations (Presentation Only)
* **In Notebook:** Not required under the current project scope.
* **In Presentation:** Add **Slide 11 & Slide 12: 7. Conclusions & Industrial Implications**.

### Final Synchronization
* Update `presentation.md` and the PowerPoint using only the verified notebook results.
* Mark resolved items in `discrepancies.md`.
* Re-run the notebook after any subsequent code changes.

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
  The complete lecture slide deck is stored in [`lectures/Slides/Slides/DA.pdf`](lectures/Slides/Slides/DA.pdf).
