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
2. **Data Cleaning:** Missing values check, physical consistency verification, standardization.
3. **Exploratory Data Analysis:** Summary stats, distributions, correlation matrices, ambient effects.
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
*(Additional slides will be expanded as we complete subsequent steps 2 through 7)*
