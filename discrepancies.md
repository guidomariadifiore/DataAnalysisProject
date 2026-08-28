# Notebook Discrepancies and Required Checks

This document records the discrepancies, omissions, and methodological points identified in `gas_turbine_analysis.ipynb`.

The review assumes that notebook points 1-5 are required in the supplementary material, while points 6-7 are presentation-only.

## 1. Project Structure and Requirements

### 1.1 Missing Section 5

The notebook currently contains sections 0, 1, 2, 3, and 4. It does not contain:

- `## 5. Preview / Summary of Results`

If point 5 is required in the notebook, this section must be added with a concise comparison of the model results.

### 1.2 Points 6 and 7

The following are not currently present in the notebook:

- detailed results and diagnostics;
- final conclusions and operational recommendations.

This is acceptable only because they have been designated as presentation-only. They should not be treated as missing notebook requirements under that assumption.

### 1.3 Handoff Document Does Not Match the Notebook

`handoff.md` states that the notebook already contains:

- Principal Component Regression (PCR);
- polynomial regression for CO;
- completed predictive models;
- clustering figures;
- numerical model results.

The actual notebook currently contains only a generic linear-model function, VIF, and K-Means code. PCR, polynomial regression, model execution, and model-performance tables are absent.

Any numerical results in `handoff.md` must therefore be verified again after the corresponding notebook cells are actually implemented.

## 2. Dataset Description and Ingestion

### 2.1 Missing Explicit Statement About Dates

The source dataset does not provide dates. The rows are chronologically ordered, and the year is inferred from the filename.

The notebook adds `year` using the CSV filename, which is reasonable, but it should explicitly state that the dates are unavailable and that the year labels are assigned by file.

### 2.2 Target and Predictor Roles Are Not Clearly Separated

The notebook lists all 11 measurements in `sensor_cols`, but does not clearly establish the modeling roles:

- predictors: `AT`, `AP`, `AH`, `AFDP`, `GTEP`, `TIT`, `TAT`, `CDP`;
- targets: `TEY`, `CO`, `NOX`.

This distinction is required to avoid accidentally using target variables as predictors.

### 2.3 Dataset Objective Is Incomplete

The description focuses mainly on CO and NOx emissions. The source description also explicitly identifies prediction of turbine energy yield as an important use of the dataset.

The notebook should present both objectives clearly:

- energy-yield prediction;
- emissions analysis and prediction.

## 3. Data Cleaning and Quality Validation

### 3.1 Physical-Range Validation Is Announced but Not Implemented

The cleaning section promises physical range and sanity validation, but no code checks the ranges.

At minimum, the notebook should verify that:

- pressures are positive;
- humidity is within a physically plausible percentage range;
- energy yield and emissions are non-negative;
- temperature and sensor values are within the documented dataset ranges.

The presentation claim that there are no invalid physical readings is not supported by the current notebook code.

### 3.2 Duplicate Definition Requires Justification

Duplicates are detected using only `sensor_cols`, and `year` is excluded:

```python
df_raw[sensor_cols].duplicated()
```

Consequently, two equal sensor measurements from different years are treated as duplicates. This may be intended, but it must be explained.

The notebook should distinguish between:

- completely identical rows;
- repeated sensor measurements occurring in different years.

### 3.3 Outliers Are Counted but Not Treated

The outlier section calculates robust 5-sigma limits and reports counts, but it does not:

- remove outliers;
- replace outliers;
- flag them in the dataset;
- explain whether they represent errors or legitimate operating conditions.

Therefore, this is an outlier inspection, not an outlier-cleaning step. The terminology should be consistent with the actual behavior.

### 3.4 Outlier Thresholds Use the Complete Dataset

The outlier limits are calculated on `df_clean` before the train/test split. If the thresholds were used to alter observations, this could introduce information from the test period into preprocessing.

The current code does not alter the data, so the practical leakage is limited. Nevertheless, the methodology should state clearly whether the analysis is descriptive only or whether outliers are used in preprocessing.

### 3.5 No Explicit Post-Cleaning Verification

After duplicate handling and preprocessing, the notebook does not explicitly verify:

- final row count;
- final column count;
- missing values in `df_clean`;
- duplicate count in `df_clean`;
- train/test overlap;
- year distribution in each partition.

These checks would make the cleaning pipeline easier to audit.

## 4. Descriptive Statistics and EDA

### 4.1 Initial Summary and EDA Summary Use Different Populations

The initial summary table uses all years through `df_raw`.

The EDA synthesis table uses only the training period through `train_df`.

This is methodologically acceptable, but the notebook should state this difference prominently so that the two tables are not interpreted as equivalent summaries.

### 4.2 Variance Is Mentioned but Not Calculated

The EDA description promises a spread analysis including variance:

> Variance, IQR, and Gini coefficient

The code calculates standard deviation, IQR, and Gini coefficient, but not variance.

Therefore, either variance must be added or the text must be changed to describe standard deviation instead.

### 4.3 Mode Is Now Implemented Correctly

The mode is calculated in the EDA cell using:

```python
mode_val = pd.Series(vals).mode().iloc[0]
```

This resolves the earlier omission. The initial `describe()` table does not include the mode, but that is normal because `describe()` does not calculate it. The mode is present in the dedicated EDA table.

Because the variables are continuous, the mode can be weakly informative. Its inclusion is nevertheless consistent with the course formulation.

### 4.4 Hardcoded Correlation Values in Plot Titles

The thermodynamic plots display values such as:

- `r = -0.58`;
- `r = +0.99`;
- `r = -0.37`.

These values are written manually rather than calculated in the plotting cell. They may become inconsistent with the actual data or with the selected subset.

The displayed correlations should be calculated from the data used for the analysis.

### 4.5 EDA Is Not Fully Reproducible From the Text

The scatterplots use a random sample of 3,000 observations, which is reproducible because `random_state=42` is specified. However, the notebook does not report the actual correlation values or sample size in a separate result table.

The visual analysis would be stronger if the numerical relationships shown in the plots were also explicitly computed and reported.

## 5. Standardization and Data Leakage Risks

### 5.1 Targets Are Standardized Together With Predictors

`train_scaled` and `test_scaled` are built from all `sensor_cols`, including:

- `TEY`;
- `CO`;
- `NOX`.

For exploratory PCA this can be acceptable if explicitly described. For predictive modeling, predictors and targets must be handled separately. Target variables must not enter the feature matrix.

### 5.2 PCA Includes Target Variables

The PCA uses:

```python
X_std = train_scaled.values
```

Since `train_scaled` contains all 11 sensor variables, the PCA includes the targets `TEY`, `CO`, and `NOX`.

This is acceptable only if the PCA is strictly exploratory. It is not acceptable if the resulting components are used as predictors in a model, because the components would contain target information.

### 5.3 Inconsistent Standard-Deviation Conventions

The standardization cell uses pandas standard deviation, which uses sample standard deviation by default.

The VIF cell uses NumPy standard deviation, which uses population standard deviation by default.

The difference is small for this dataset, but the notebook should use one convention consistently or explain the choice.

### 5.4 Reuse of `X_std` Creates Hidden State Dependence

`X_std` is first assigned to the 11-variable PCA matrix and later reassigned to the 8-variable predictor matrix in the VIF cell.

As a result, the meaning of `X_std` changes during notebook execution. Running cells out of order can produce different analyses or incorrect results.

Separate names should be used for:

- exploratory PCA data;
- regression feature data;
- clustering feature data.

## 6. Main Analysis: Regression and PCR

### 6.1 Regression Function Is Defined but Never Used

The function `fit_linear_model` calculates training and test `R^2` and RMSE, but the notebook never calls it.

There is no actual OLS result for:

- `TEY`;
- `CO`;
- `NOX`.

### 6.2 PCR Is Described but Not Implemented

The notebook explains PCR mathematically and states that PCR will solve multicollinearity, but it does not:

- select principal components for regression;
- compute the component scores used for modeling;
- fit PCR coefficients;
- generate predictions;
- compare PCR with OLS;
- report PCR performance.

This is the largest discrepancy between the stated objective and the executable code.

### 6.3 Polynomial Regression for CO Is Described but Not Implemented

The notebook states that a polynomial expansion will model non-linear CO behavior, but no code creates features such as:

```python
[x, x**2]
```

and no polynomial CO model is fitted or evaluated.

### 6.4 NOX Model Is Not Implemented

The notebook identifies NOX as a modeling target, but there is no NOX regression model, prediction, or performance metric.

### 6.5 No Model Comparison Table

There is no table comparing training and test performance using:

- `R^2`;
- RMSE;
- target variable;
- model type.

This table is needed for section 5, even if detailed diagnostics are reserved for the presentation.

### 6.6 No Baseline Model

The notebook does not define a simple baseline for comparison, such as predicting the training mean on the test set.

Without a baseline, it is harder to demonstrate whether OLS, PCR, and polynomial regression provide meaningful predictive improvement.

### 6.7 OLS Formula Uses an Inverse That the Code Does Not Use

The markdown presents:

$$\hat{\beta} = (X^T X)^{-1}X^Ty$$

The code correctly uses `np.linalg.lstsq`, which is numerically safer than directly computing a matrix inverse. This is not a code error, but the text should explain that least squares is used for numerical stability, especially under multicollinearity.

## 7. VIF Analysis

### 7.1 VIF Calculation Is Conceptually Correct

The VIF procedure regresses each standardized predictor on the other predictors and computes:

$$\mathrm{VIF}_j = \frac{1}{1-R_j^2}$$

This part is consistent with the stated definition.

### 7.2 VIF Results Are Not Connected to a Model Decision

The notebook calculates VIF and labels values above 10 as severe, but it does not use the result to explain concretely:

- why OLS is problematic;
- why PCR is selected;
- how many components are retained;
- whether the chosen model improves test performance.

The diagnostic should lead directly into the implemented PCR comparison.

## 8. PCA

### 8.1 PCA Dimension Is Hardcoded

The code uses `range(1, 12)` in several places. This matches the current 11-column input, but it will fail or become misleading if the selected columns change.

The number of components and plot ranges should be derived from the matrix dimensions.

### 8.2 Biplot Interpretation Needs Clarification

The arrows use eigenvectors directly as feature loadings. Depending on the chosen PCA convention, a biplot may require scaled loadings rather than raw eigenvectors.

The notebook should state which quantity is being plotted and how the arrow scale is chosen.

### 8.3 PCA Selection Rule Is Not Applied

The scree plot shows 80% and 90% horizontal lines, but the notebook does not calculate or report the number of components required to reach those thresholds.

If five components are later used for PCR, the choice must be explicitly justified using cumulative PVE or another course-approved criterion.

## 9. K-Means and Silhouette

### 9.1 K-Means Uses a Variable Whose Meaning Changes

The clustering code uses `X_tr_std`. Because that variable was overwritten in the VIF cell, clustering uses the eight predictors only when all cells are run in the intended order.

If the PCA and VIF cells are skipped or run differently, clustering may accidentally include the target variables.

### 9.2 Best Number of Clusters Is Not Explicitly Selected

Silhouette scores are calculated for `k` from 2 to 5, but the code always profiles `k=3` regardless of which value has the best score.

The notebook should either:

- select the `k` with the maximum silhouette score; or
- justify `k=3` independently.

### 9.3 Silhouette Calculation Includes the Observation Itself

When calculating intra-cluster distance, the observation is included in its own cluster. Its distance to itself is zero.

The observation should be excluded when calculating $a_i$, otherwise the average intra-cluster distance is slightly biased downward.

### 9.4 Silhouette Cluster Labels Are Assumed to Be Consecutive

The code defines:

```python
k = len(np.unique(lab_sub))
```

and then loops over `range(k)`. This assumes that the labels present in the sample are exactly `0, 1, ..., k-1`.

If a cluster is absent from the sample, a valid label can be skipped. The implementation should iterate over the actual unique labels.

### 9.5 Fixed Sample Size Is Not General

`sample_size=2000` is valid for this dataset, but the function fails if the input contains fewer than 2,000 observations because sampling is performed without replacement.

A robust implementation should use the smaller of the requested sample size and the number of observations.

### 9.6 No Clustering Visualization

The code produces silhouette scores and a regime profile table, but it does not visualize the clusters or silhouette distribution.

A visualization is not strictly required by the project structure, but it would support the claim that the regimes are meaningfully separated.

### 9.7 Cluster Labels Are Arbitrary

K-Means labels such as 0, 1, and 2 have no intrinsic meaning. The notebook should map clusters to descriptive names only after comparing their profiles, for example peak load, nominal load, and part-load.

## 10. Reproducibility and Execution

### 10.1 Notebook Depends on Execution Order

Several variables are reused and overwritten, especially `X_std`. The notebook currently assumes that all cells are executed sequentially.

A clean notebook should be restartable and executable from top to bottom without relying on previous interactive state.

### 10.2 No Package or Environment Check

The notebook assumes that `numpy`, `pandas`, `matplotlib`, and `seaborn` are installed. No environment or package-version check is provided.

This is not necessarily a project requirement, but teachers must be able to run the notebook reliably.

### 10.3 No Final Execution Validation

The notebook should be executed from a fresh kernel after all required cells are complete. This is particularly important because the current terminal environment does not have `pandas` installed, so the notebook has not been independently executed there.

## 11. Minimum Required Corrections for Notebook Points 1-5

1. Add or document the physical-range validation.
2. Explain the duplicate definition and its effect on row counts.
3. Clarify that the outlier procedure inspects rather than removes observations.
4. Add variance to the EDA table or remove it from the description.
5. Preserve the current mode calculation.
6. Separate predictors from targets throughout preprocessing and modeling.
7. Use distinct variable names for PCA, regression, and clustering matrices.
8. Replace hardcoded correlation annotations with calculated values.
9. Implement OLS for the selected targets.
10. Implement PCR and justify the number of retained components.
11. Implement the polynomial CO model.
12. Implement the NOX model.
13. Calculate and compare training/test `R^2` and RMSE.
14. Add section 5 with a summary table of the principal results.
15. Re-execute the complete notebook from a clean kernel and verify that all cells run in order.

Points 6 and 7 may remain outside the notebook if they are intentionally reserved for the presentation.
