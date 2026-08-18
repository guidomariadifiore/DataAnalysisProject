import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Load data
data_dir = os.path.join('data', 'gas+turbine+co+and+nox+emission+data+set')
train_dfs = []
for y in [2011, 2012, 2013]:
    df_y = pd.read_csv(os.path.join(data_dir, f'gt_{y}.csv'))
    df_y['year'] = y
    train_dfs.append(df_y)
train_df = pd.concat(train_dfs, ignore_index=True).drop_duplicates().reset_index(drop=True)

test_dfs = []
for y in [2014, 2015]:
    df_y = pd.read_csv(os.path.join(data_dir, f'gt_{y}.csv'))
    df_y['year'] = y
    test_dfs.append(df_y)
test_df = pd.concat(test_dfs, ignore_index=True).drop_duplicates().reset_index(drop=True)

all_dfs = train_dfs + test_dfs
full_df = pd.concat(all_dfs, ignore_index=True).drop_duplicates().reset_index(drop=True)

feature_cols = ['AT', 'AP', 'AH', 'AFDP', 'GTEP', 'TIT', 'TAT', 'CDP']
ambient_cols = ['AT', 'AP', 'AH']

# 1. Feature normalization based strictly on Training set
mean_tr = train_df[feature_cols].mean()
std_tr = train_df[feature_cols].std()

X_tr_full = train_df[feature_cols].values
X_te_full = test_df[feature_cols].values
X_tr_std = (X_tr_full - mean_tr.values) / std_tr.values
X_te_std = (X_te_full - mean_tr.values) / std_tr.values

# PCA for PCR (5 components)
cov_C = np.cov(X_tr_std, rowvar=False)
evals, evecs = np.linalg.eigh(cov_C)
idx = np.argsort(evals)[::-1]
V_5 = evecs[:, idx[:5]]

Z_tr = X_tr_std @ V_5
Z_te = X_te_std @ V_5

# Polynomial features for CO (TIT, TAT, CDP squared)
poly_cols_idx = [feature_cols.index(c) for c in ['TIT', 'TAT', 'CDP']]
X_tr_poly = np.column_stack([X_tr_full, X_tr_full[:, poly_cols_idx]**2])
X_te_poly = np.column_stack([X_te_full, X_te_full[:, poly_cols_idx]**2])

# Detailed Model Evaluator
def evaluate_model(name, X_tr, y_tr, X_te, y_te, feature_names=None):
    X_tr_c = np.column_stack([np.ones(len(X_tr)), X_tr])
    X_te_c = np.column_stack([np.ones(len(X_te)), X_te])
    
    # OLS Solution (Slide 106)
    beta = np.linalg.lstsq(X_tr_c, y_tr, rcond=None)[0]
    
    # Train metrics
    y_tr_pred = X_tr_c @ beta
    res_tr = y_tr - y_tr_pred
    rss_tr = np.sum(res_tr**2)
    tss_tr = np.sum((y_tr - np.mean(y_tr))**2)
    r2_tr = 1 - rss_tr / tss_tr
    rmse_tr = np.sqrt(np.mean(res_tr**2))
    mae_tr = np.mean(np.abs(res_tr))
    
    # Test metrics
    y_te_pred = X_te_c @ beta
    res_te = y_te - y_te_pred
    rss_te = np.sum(res_te**2)
    tss_te = np.sum((y_te - np.mean(y_te))**2)
    r2_te = 1 - rss_te / tss_te
    rmse_te = np.sqrt(np.mean(res_te**2))
    mae_te = np.mean(np.abs(res_te))
    
    # Standard Errors of Coefficients (Slide 111)
    m, p = X_tr_c.shape[0], X_tr_c.shape[1] - 1
    sigma_eps_sq = rss_tr / (m - p - 1)
    try:
        inv_XtX = np.linalg.inv(X_tr_c.T @ X_tr_c)
        se_beta = np.sqrt(np.diag(inv_XtX) * sigma_eps_sq)
        ci_lower = beta - 2 * se_beta
        ci_upper = beta + 2 * se_beta
    except Exception:
        se_beta = np.zeros(len(beta))
        ci_lower, ci_upper = beta, beta

    # Year-by-year test breakdown
    yearly_metrics = {}
    for y in [2011, 2012, 2013, 2014, 2015]:
        sub_df = full_df[full_df['year'] == y]
        target_name = name.split()[0]
        if 'PCR' in name:
            sub_X_std = (sub_df[feature_cols].values - mean_tr.values) / std_tr.values
            sub_X_mat = sub_X_std @ V_5
        elif 'Ambient' in name:
            sub_X_mat = sub_df[ambient_cols].values
        elif 'Poly' in name:
            sub_X_mat = np.column_stack([sub_df[feature_cols].values, sub_df[feature_cols].values[:, poly_cols_idx]**2])
        else:
            sub_X_mat = sub_df[feature_cols].values
            
        sub_X_c = np.column_stack([np.ones(len(sub_X_mat)), sub_X_mat])
        sub_y = sub_df[target_name].values
        sub_pred = sub_X_c @ beta
        sub_r2 = 1 - np.sum((sub_y - sub_pred)**2) / np.sum((sub_y - np.mean(sub_y))**2)
        sub_rmse = np.sqrt(np.mean((sub_y - sub_pred)**2))
        yearly_metrics[y] = (sub_r2, sub_rmse)
        
    return {
        'name': name,
        'beta': beta,
        'se_beta': se_beta,
        'ci': (ci_lower, ci_upper),
        'metrics_tr': (r2_tr, rmse_tr, mae_tr),
        'metrics_te': (r2_te, rmse_te, mae_te),
        'yearly': yearly_metrics,
        'y_te_pred': y_te_pred,
        'res_te': res_te,
        'y_te': y_te
    }

# Execute evaluations
m_tey_amb = evaluate_model('TEY Ambient Baseline', train_df[ambient_cols].values, train_df['TEY'].values,
                           test_df[ambient_cols].values, test_df['TEY'].values, ['Intercept'] + ambient_cols)
m_tey_ols = evaluate_model('TEY Full OLS (8 Features)', X_tr_full, train_df['TEY'].values,
                           X_te_full, test_df['TEY'].values, ['Intercept'] + feature_cols)
m_tey_pcr = evaluate_model('TEY PCR (5 Components)', Z_tr, train_df['TEY'].values,
                           Z_te, test_df['TEY'].values, ['Intercept', 'PC1', 'PC2', 'PC3', 'PC4', 'PC5'])
m_co_lin = evaluate_model('CO Linear OLS', X_tr_full, train_df['CO'].values,
                          X_te_full, test_df['CO'].values, ['Intercept'] + feature_cols)
m_co_poly = evaluate_model('CO Polynomial (Degree 2)', X_tr_poly, train_df['CO'].values,
                           X_te_poly, test_df['CO'].values, ['Intercept'] + feature_cols + ['TIT^2', 'TAT^2', 'CDP^2'])
m_nox_ols = evaluate_model('NOX Full OLS', X_tr_full, train_df['NOX'].values,
                           X_te_full, test_df['NOX'].values, ['Intercept'] + feature_cols)

models = [m_tey_amb, m_tey_ols, m_tey_pcr, m_co_lin, m_co_poly, m_nox_ols]

print('=== Point 5: Preview / Summary of Results Table ===')
summary_rows = []
for m in models:
    summary_rows.append({
        'Model Name': m['name'],
        'Train R2': round(m['metrics_tr'][0], 4),
        'Train RMSE': round(m['metrics_tr'][1], 3),
        'Test R2 (2014-15)': round(m['metrics_te'][0], 4),
        'Test RMSE': round(m['metrics_te'][1], 3),
        'Test MAE': round(m['metrics_te'][2], 3)
    })
df_summary = pd.DataFrame(summary_rows)
print(df_summary.to_string(index=False))

print('\n=== Point 6: Year-by-Year R2 Breakdown (2011 to 2015) ===')
yearly_rows = []
for m in models:
    row = {'Model': m['name']}
    for y in [2011, 2012, 2013, 2014, 2015]:
        r2_val, rmse_val = m['yearly'][y]
        row[f'{y} R2'] = round(r2_val, 3)
    yearly_rows.append(row)
print(pd.DataFrame(yearly_rows).to_string(index=False))

# Save figures for Detailed Results
os.makedirs('figures', exist_ok=True)

# Figure 1: Actual vs. Predicted
fig, axes = plt.subplots(1, 3, figsize=(16, 5))

axes[0].scatter(m_tey_pcr['y_te'], m_tey_pcr['y_te_pred'], color='#296299', alpha=0.3, s=15)
min_t, max_t = min(m_tey_pcr['y_te']), max(m_tey_pcr['y_te'])
axes[0].plot([min_t, max_t], [min_t, max_t], 'r--', linewidth=2, label='Ideal 1:1 Line')
axes[0].set_title(f"TEY: Principal Component Regression (PCR)\nTest R² = {m_tey_pcr['metrics_te'][0]:.4f} | RMSE = {m_tey_pcr['metrics_te'][1]:.2f} MWh", fontweight='bold', fontsize=11)
axes[0].set_xlabel('Actual Energy Yield TEY (MWh)')
axes[0].set_ylabel('Predicted Energy Yield TEY (MWh)')
axes[0].legend()

axes[1].scatter(m_co_poly['y_te'], m_co_poly['y_te_pred'], color='#e67e22', alpha=0.3, s=15)
min_co, max_co = min(m_co_poly['y_te']), max(m_co_poly['y_te'])
axes[1].plot([min_co, max_co], [min_co, max_co], 'r--', linewidth=2, label='Ideal 1:1 Line')
axes[1].set_title(f"CO: Polynomial Regression (Degree 2)\nTest R² = {m_co_poly['metrics_te'][0]:.4f} | RMSE = {m_co_poly['metrics_te'][1]:.2f} mg/m³", fontweight='bold', fontsize=11)
axes[1].set_xlabel('Actual Carbon Monoxide CO (mg/m³)')
axes[1].set_ylabel('Predicted Carbon Monoxide CO (mg/m³)')
axes[1].legend()

axes[2].scatter(m_nox_ols['y_te'], m_nox_ols['y_te_pred'], color='#27ae60', alpha=0.3, s=15)
min_nox, max_nox = min(m_nox_ols['y_te']), max(m_nox_ols['y_te'])
axes[2].plot([min_nox, max_nox], [min_nox, max_nox], 'r--', linewidth=2, label='Ideal 1:1 Line')
axes[2].set_title(f"NOx: Multivariate Regression (OLS)\nTrain R² = {m_nox_ols['metrics_tr'][0]:.4f} | Test RMSE = {m_nox_ols['metrics_te'][1]:.2f} mg/m³", fontweight='bold', fontsize=11)
axes[2].set_xlabel('Actual Nitrogen Oxides NOx (mg/m³)')
axes[2].set_ylabel('Predicted Nitrogen Oxides NOx (mg/m³)')
axes[2].legend()

plt.tight_layout()
plt.savefig('figures/results_actual_vs_predicted.png', dpi=200)
plt.close()

# Figure 2: Residual Diagnostics
fig, axes = plt.subplots(2, 2, figsize=(14, 9))

axes[0, 0].scatter(m_tey_pcr['y_te_pred'], m_tey_pcr['res_te'], color='#296299', alpha=0.3, s=15)
axes[0, 0].axhline(0, color='r', linestyle='--', linewidth=1.5)
axes[0, 0].set_title('TEY (PCR): Residuals vs Predicted Values', fontweight='bold')
axes[0, 0].set_xlabel('Predicted TEY (MWh)')
axes[0, 0].set_ylabel('Residual (Actual - Predicted)')

sns.histplot(m_tey_pcr['res_te'], kde=True, ax=axes[0, 1], color='#296299', bins=50)
axes[0, 1].axvline(0, color='r', linestyle='--', linewidth=1.5)
axes[0, 1].set_title('TEY (PCR): Residual Distribution (Zero Centered)', fontweight='bold')
axes[0, 1].set_xlabel('Residual Error (MWh)')

axes[1, 0].scatter(m_co_poly['y_te_pred'], m_co_poly['res_te'], color='#e67e22', alpha=0.3, s=15)
axes[1, 0].axhline(0, color='r', linestyle='--', linewidth=1.5)
axes[1, 0].set_title('CO (Poly): Residuals vs Predicted Values', fontweight='bold')
axes[1, 0].set_xlabel('Predicted CO (mg/m³)')
axes[1, 0].set_ylabel('Residual (Actual - Predicted)')

sns.histplot(m_co_poly['res_te'], kde=True, ax=axes[1, 1], color='#e67e22', bins=50)
axes[1, 1].axvline(0, color='r', linestyle='--', linewidth=1.5)
axes[1, 1].set_title('CO (Poly): Residual Distribution', fontweight='bold')
axes[1, 1].set_xlabel('Residual Error (mg/m³)')

plt.tight_layout()
plt.savefig('figures/results_residuals_diagnostics.png', dpi=200)
plt.close()

# Figure 3: Operational Regimes in Feature Space (K-Means K=3)
from numpy.linalg import norm
np.random.seed(42)
cents = X_tr_std[np.random.choice(len(X_tr_std), 3, replace=False)]
for _ in range(50):
    dists = norm(X_tr_std[:, np.newaxis] - cents, axis=2)
    labs = np.argmin(dists, axis=1)
    new_cents = np.array([X_tr_std[labs == j].mean(axis=0) for j in range(3)])
    if np.allclose(cents, new_cents): break
    cents = new_cents

fig, axes = plt.subplots(1, 2, figsize=(14, 5.5))
palette = ['#e74c3c', '#3498db', '#2ecc71']

for k_id, col, name in zip([0, 1, 2], palette, ['Peak Load', 'Part-Load', 'Baseload']):
    mask = labs == k_id
    sample_mask = np.random.choice(np.where(mask)[0], size=min(1000, mask.sum()), replace=False)
    axes[0].scatter(train_df.iloc[sample_mask]['TIT'], train_df.iloc[sample_mask]['TEY'], 
                    color=col, alpha=0.5, s=20, label=name)
    axes[1].scatter(train_df.iloc[sample_mask]['CO'], train_df.iloc[sample_mask]['NOX'], 
                    color=col, alpha=0.5, s=20, label=name)

axes[0].set_title('Operational Regimes: Firing Temp (TIT) vs Yield (TEY)', fontweight='bold')
axes[0].set_xlabel('Turbine Inlet Temperature TIT (°C)')
axes[0].set_ylabel('Turbine Energy Yield TEY (MWh)')
axes[0].legend()

axes[1].set_title('Operational Regimes: Emissions Space (CO vs NOx)', fontweight='bold')
axes[1].set_xlabel('Carbon Monoxide CO (mg/m³)')
axes[1].set_ylabel('Nitrogen Oxides NOx (mg/m³)')
axes[1].legend()

plt.tight_layout()
plt.savefig('figures/results_kmeans_regimes_scatter.png', dpi=200)
plt.close()

# Figure 4: Model Comparison Bar Chart
fig, ax = plt.subplots(figsize=(10, 5))
model_labels = ['TEY Ambient', 'TEY Full OLS', 'TEY PCR (5 PCs)', 'CO Linear', 'CO Polynomial (Deg 2)', 'NOx OLS']
tr_r2 = [m['metrics_tr'][0] for m in models]
te_r2 = [max(0, m['metrics_te'][0]) for m in models]

x = np.arange(len(model_labels))
width = 0.35

ax.bar(x - width/2, tr_r2, width, label='Train R² (2011–2013)', color='#296299', alpha=0.85)
ax.bar(x + width/2, te_r2, width, label='Test R² (2014–2015)', color='#27ae60', alpha=0.85)
ax.set_ylabel('Coefficient of Determination R²', fontweight='bold')
ax.set_title('Model Performance Comparison: Training vs. Out-of-Sample Test R²', fontweight='bold', fontsize=12)
ax.set_xticks(x)
ax.set_xticklabels(model_labels, rotation=20, ha='right', fontsize=9.5)
ax.set_ylim(0, 1.1)
ax.legend()
plt.tight_layout()
plt.savefig('figures/results_model_comparison_r2.png', dpi=200)
plt.close()

print('Detailed results script finished successfully. All figures saved.')
