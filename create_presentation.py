import json
import os
import pptx
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

def update_presentation():
    prs = pptx.Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    DARK_BLUE = RGBColor(16, 37, 66)
    ACCENT_BLUE = RGBColor(41, 98, 153)
    LIGHT_BG = RGBColor(248, 249, 250)
    TEXT_DARK = RGBColor(33, 37, 41)
    WHITE = RGBColor(255, 255, 255)
    BORDER_COLOR = RGBColor(220, 225, 230)

    def add_header(slide, title_text, category_text="DATA ANALYTICS PROJECT WORK"):
        header_box = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(1.2))
        header_box.fill.solid()
        header_box.fill.fore_color.rgb = DARK_BLUE
        header_box.line.color.rgb = DARK_BLUE
        
        tf_cat = header_box.text_frame
        tf_cat.word_wrap = True
        tf_cat.margin_left = Inches(0.8)
        tf_cat.margin_top = Inches(0.15)
        
        p0 = tf_cat.paragraphs[0]
        p0.text = category_text.upper()
        p0.font.size = Pt(11)
        p0.font.bold = True
        p0.font.color.rgb = RGBColor(180, 205, 235)
        
        p1 = tf_cat.add_paragraph()
        p1.text = title_text
        p1.font.size = Pt(22)
        p1.font.bold = True
        p1.font.color.rgb = WHITE

    # --- SLIDE 1: Title ---
    slide1 = prs.slides.add_slide(blank_layout)
    bg1 = slide1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5))
    bg1.fill.solid()
    bg1.fill.fore_color.rgb = DARK_BLUE
    bg1.line.color.rgb = DARK_BLUE

    tbox = slide1.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(11.333), Inches(3.5))
    tf1 = tbox.text_frame
    tf1.word_wrap = True
    p = tf1.paragraphs[0]
    p.text = "Data Analytics & Predictive Modeling"
    p.font.size = Pt(36)
    p.font.bold = True
    p.font.color.rgb = WHITE
    p2 = tf1.add_paragraph()
    p2.text = "Flue Gas Emissions (CO, NOx) and Energy Yield in Gas Turbines"
    p2.font.size = Pt(22)
    p2.font.color.rgb = RGBColor(180, 205, 235)
    p3 = tf1.add_paragraph()
    p3.text = "\nCourse: Data Analytics (and Data Driven Decision) — University of L'Aquila\nBased on Course Methodologies and 2011–2015 Hourly Sensor Data"
    p3.font.size = Pt(14)
    p3.font.color.rgb = RGBColor(200, 215, 230)

    # --- SLIDE 2: Workflow ---
    slide2 = prs.slides.add_slide(blank_layout)
    add_header(slide2, "Project Workflow & Guidelines Structure")
    steps = [
        ("1. Description of Dataset", "Data origin, 11 sensor variables, 36,733 hourly observations, train/test split protocol."),
        ("2. Data Cleaning & Validation", "Verification of missing values, range validation, physical plausibility check, standard scaling."),
        ("3. Exploratory Data Analysis", "Descriptive statistics, distribution shapes, correlation heatmaps, environmental impact."),
        ("4. Main Analysis & Methods", "Techniques aligned with course lectures: Dimensionality Reduction, Regression, Diagnostics."),
        ("5. Preview of Results", "High-level summary of model performance, key feature importances, emission trade-offs."),
        ("6. Detailed Results", "In-depth metric breakdown (R², RMSE, residuals), cross-validation across 2011–2015."),
        ("7. Conclusions", "Industrial takeaways, operational recommendations, turbine emission control strategies.")
    ]
    for i, (title, desc) in enumerate(steps):
        col = 0 if i < 4 else 1
        row = i if i < 4 else i - 4
        left = Inches(0.8 + col * 6.0)
        top = Inches(1.5 + row * 1.35)
        card = slide2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, Inches(5.7), Inches(1.2))
        card.fill.solid()
        card.fill.fore_color.rgb = LIGHT_BG
        card.line.color.rgb = BORDER_COLOR
        tf = card.text_frame
        tf.word_wrap = True
        tf.margin_left = Inches(0.2)
        tf.margin_top = Inches(0.15)
        p = tf.paragraphs[0]
        p.text = title
        p.font.size = Pt(14)
        p.font.bold = True
        p.font.color.rgb = DARK_BLUE
        p_desc = tf.add_paragraph()
        p_desc.text = desc
        p_desc.font.size = Pt(11)
        p_desc.font.color.rgb = TEXT_DARK

    # --- SLIDE 3: 1. Description of Dataset ---
    slide3 = prs.slides.add_slide(blank_layout)
    add_header(slide3, "1. Description of the Dataset & Sensor Features")
    card_left = slide3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.5), Inches(4.0), Inches(5.5))
    card_left.fill.solid()
    card_left.fill.fore_color.rgb = LIGHT_BG
    card_left.line.color.rgb = BORDER_COLOR
    tf_l = card_left.text_frame
    tf_l.word_wrap = True
    tf_l.margin_left = Inches(0.25)
    tf_l.margin_top = Inches(0.25)
    p = tf_l.paragraphs[0]
    p.text = "Dataset Characteristics"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = DARK_BLUE
    info_points = [
        ("Location:", "Gas turbine plant in NW Turkey"),
        ("Timeframe:", "2011 – 2015 (5 consecutive years)"),
        ("Granularity:", "Hourly aggregated averages/sums"),
        ("Observations:", "36,733 instances (sorted in time)"),
        ("Missing Values:", "0 (Complete sensor records)"),
        ("Data Protocol:", "Train: 2011-13 (60.4%)\nTest: 2014-15 (39.6%)"),
        ("Key Targets:", "Emissions (CO, NOx), Energy (TEY)")
    ]
    for lbl, val in info_points:
        p_item = tf_l.add_paragraph()
        p_item.text = f"• {lbl} {val}"
        p_item.font.size = Pt(12)
        p_item.font.color.rgb = TEXT_DARK
        
    table_shape = slide3.shapes.add_table(12, 4, Inches(5.1), Inches(1.5), Inches(7.4), Inches(5.5))
    table = table_shape.table
    table.columns[0].width = Inches(1.5)
    table.columns[1].width = Inches(1.1)
    table.columns[2].width = Inches(1.0)
    table.columns[3].width = Inches(3.8)
    headers = ["Category", "Variable", "Unit", "Physical Role / Meaning"]
    for col_idx, h in enumerate(headers):
        cell = table.cell(0, col_idx)
        cell.text = h
        cell.fill.solid()
        cell.fill.fore_color.rgb = DARK_BLUE
        p = cell.text_frame.paragraphs[0]
        p.font.bold = True
        p.font.size = Pt(11)
        p.font.color.rgb = WHITE
    sensor_data = [
        ("Ambient", "AT", "°C", "Ambient Temperature (inlet air density driver)"),
        ("Ambient", "AP", "mbar", "Ambient Atmospheric Pressure"),
        ("Ambient", "AH", "%", "Ambient Relative Humidity"),
        ("Turbine", "AFDP", "mbar", "Air Filter Difference Pressure (filter clogging)"),
        ("Turbine", "GTEP", "mbar", "Gas Turbine Exhaust Pressure"),
        ("Turbine", "TIT", "°C", "Turbine Inlet Temperature (efficiency driver)"),
        ("Turbine", "TAT", "°C", "Turbine After Temperature (exhaust)"),
        ("Turbine", "CDP", "mbar", "Compressor Discharge Pressure"),
        ("Yield", "TEY", "MWh", "Turbine Energy Yield (Net power output)"),
        ("Emission", "CO", "mg/m³", "Carbon Monoxide (Incomplete combustion)"),
        ("Emission", "NOx", "mg/m³", "Nitrogen Oxides (Thermal NOx mechanism)")
    ]
    for row_idx, row in enumerate(sensor_data, start=1):
        for col_idx, val in enumerate(row):
            cell = table.cell(row_idx, col_idx)
            cell.text = val
            cell.fill.solid()
            cell.fill.fore_color.rgb = WHITE if row_idx % 2 == 0 else LIGHT_BG
            p = cell.text_frame.paragraphs[0]
            p.font.size = Pt(10)
            p.font.color.rgb = TEXT_DARK

    # --- SLIDE 4: 2. Data Cleaning ---
    slide4 = prs.slides.add_slide(blank_layout)
    add_header(slide4, "2. Data Cleaning, Quality Validation & Preprocessing")
    card_c1 = slide4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.5), Inches(3.7), Inches(2.5))
    card_c1.fill.solid()
    card_c1.fill.fore_color.rgb = LIGHT_BG
    card_c1.line.color.rgb = BORDER_COLOR
    tf_c1 = card_c1.text_frame
    tf_c1.word_wrap = True
    tf_c1.margin_left = Inches(0.2)
    tf_c1.margin_top = Inches(0.2)
    p = tf_c1.paragraphs[0]
    p.text = "1. Completeness & Integrity"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = DARK_BLUE
    for it in ["• Missing Values: 0 nulls across all 11 columns.", "• Duplicates: 7 identical sensor rows detected and pruned.", "• Chronology: Preserved time order across 2011–2015.", "• Sensor Health: No negative pressures or invalid readings."]:
        p = tf_c1.add_paragraph()
        p.text = it
        p.font.size = Pt(10.5)
        p.font.color.rgb = TEXT_DARK

    card_c2 = slide4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(4.8), Inches(1.5), Inches(3.7), Inches(2.5))
    card_c2.fill.solid()
    card_c2.fill.fore_color.rgb = LIGHT_BG
    card_c2.line.color.rgb = BORDER_COLOR
    tf_c2 = card_c2.text_frame
    tf_c2.word_wrap = True
    tf_c2.margin_left = Inches(0.2)
    tf_c2.margin_top = Inches(0.2)
    p = tf_c2.paragraphs[0]
    p.text = "2. σ-Clipping (Course Method)"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = DARK_BLUE
    for it in ["• Robust Dispersion: $\\hat{\\sigma} = \\frac{IQR}{1.35} = \\frac{Q_3 - Q_1}{1.35}$", "• Robust Centering: Uses Median ($Q_2$) to resist leverage.", "• Boundaries: $[\\text{Med} - 5\\hat{\\sigma},\\; \\text{Med} + 5\\hat{\\sigma}]$", "• Ambient/Turbine: 0 outliers (100% physically valid).", "• Emissions (CO/NOx): Skewed tail corresponds to true combustion events."]:
        p = tf_c2.add_paragraph()
        p.text = it
        p.font.size = Pt(10.5)
        p.font.color.rgb = TEXT_DARK

    card_c3 = slide4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(8.8), Inches(1.5), Inches(3.7), Inches(2.5))
    card_c3.fill.solid()
    card_c3.fill.fore_color.rgb = LIGHT_BG
    card_c3.line.color.rgb = BORDER_COLOR
    tf_c3 = card_c3.text_frame
    tf_c3.word_wrap = True
    tf_c3.margin_left = Inches(0.2)
    tf_c3.margin_top = Inches(0.2)
    p = tf_c3.paragraphs[0]
    p.text = "3. Protocol & Scaling"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = DARK_BLUE
    for it in ["• Train Set (2011–13): 22,187 samples (60.4%)", "• Test Set (2014–15): 14,539 samples (39.6%)", "• No Leakage: Fit scaler strictly on Train, transform Test.", "• Z-Score Standardization: $z = \\frac{x - \\mu_{train}}{\\sigma_{train}}$ for PCA & Regression."]:
        p = tf_c3.add_paragraph()
        p.text = it
        p.font.size = Pt(10.5)
        p.font.color.rgb = TEXT_DARK

    table_shape4 = slide4.shapes.add_table(7, 6, Inches(0.8), Inches(4.3), Inches(11.7), Inches(2.7))
    t4 = table_shape4.table
    for c in range(6):
        t4.columns[c].width = Inches(1.95)
    headers4 = ["Variable", "Median (Q2)", "IQR (Q3 - Q1)", "Est. σ̂ (IQR/1.35)", "Valid Interval [Med ± 5σ̂]", "Physical Assessment"]
    for col_idx, h in enumerate(headers4):
        cell = t4.cell(0, col_idx)
        cell.text = h
        cell.fill.solid()
        cell.fill.fore_color.rgb = DARK_BLUE
        p = cell.text_frame.paragraphs[0]
        p.font.bold = True
        p.font.size = Pt(10)
        p.font.color.rgb = WHITE
    sigma_data = [
        ("AT (°C)", "17.80", "11.88", "8.80", "[-26.21, 61.82]", "0 outliers (Physical weather)"),
        ("AP (mbar)", "1012.60", "8.20", "6.07", "[982.23, 1042.97]", "0 outliers (Barometric band)"),
        ("TIT (°C)", "1085.90", "25.20", "18.67", "[992.57, 1179.23]", "0 outliers (Firing regime)"),
        ("TEY (MWh)", "133.73", "19.63", "14.54", "[61.03, 206.43]", "0 outliers (Generator range)"),
        ("CO (mg/m³)", "1.71", "1.66", "1.23", "[-4.44, 7.86]", "Spikes = Incomplete combustion"),
        ("NOx (mg/m³)", "63.85", "14.39", "10.66", "[10.57, 117.13]", "Peaks = High flame temp")
    ]
    for row_idx, row in enumerate(sigma_data, start=1):
        for col_idx, val in enumerate(row):
            cell = t4.cell(row_idx, col_idx)
            cell.text = val
            cell.fill.solid()
            cell.fill.fore_color.rgb = WHITE if row_idx % 2 == 0 else LIGHT_BG
            p = cell.text_frame.paragraphs[0]
            p.font.size = Pt(9.5)
            p.font.color.rgb = TEXT_DARK

    # --- SLIDE 5: 3. EDA - Distributions & Correlation ---
    slide5 = prs.slides.add_slide(blank_layout)
    add_header(slide5, "3. Exploratory Analysis: Distributions & Correlation Structure")
    card_eda1 = slide5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.4), Inches(5.6), Inches(5.6))
    card_eda1.fill.solid()
    card_eda1.fill.fore_color.rgb = LIGHT_BG
    card_eda1.line.color.rgb = BORDER_COLOR
    tf_e1 = card_eda1.text_frame
    tf_e1.word_wrap = True
    tf_e1.margin_left = Inches(0.25)
    tf_e1.margin_top = Inches(0.2)
    p = tf_e1.paragraphs[0]
    p.text = "Course Definition & Statistical Synthesis"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = DARK_BLUE
    eda_points = [
        ("Exploratory Analysis (Slide 3 & 10):", "Unsupervised synthesis of distributions into Size (Mean $\\mu$, Median) and Spread (Variance $\\sigma^2$, IQR, Gini $G$, Entropy $H$)."),
        ("Size vs Spread Synthesis:", "• Mean vs Median: CO mean (2.21) >> median (1.52) demonstrates strong positive skew.\n• Gini Index: CO exhibits high concentration (G=0.442) due to episodic spikes."),
        ("Key Pearson Correlation ($r_{XY}$) Findings:", "• Compressor & Energy Coupling: CDP & TEY ($r = 0.99$), GTEP & TEY ($r = 0.98$) indicate strong collinearity in operating load.\n• Environmental Cooling Effect: Ambient Temp AT vs TEY ($r = -0.58$) due to reduced air density at higher temperatures.\n• Combustion Trade-off: CO vs NOx ($r = -0.37$) reflects the physical inverse relationship between complete oxidation and thermal NOx.")
    ]
    for lbl, desc in eda_points:
        p_l = tf_e1.add_paragraph()
        p_l.text = f"\n{lbl}"
        p_l.font.bold = True
        p_l.font.size = Pt(11)
        p_l.font.color.rgb = ACCENT_BLUE
        p_d = tf_e1.add_paragraph()
        p_d.text = desc
        p_d.font.size = Pt(10)
        p_d.font.color.rgb = TEXT_DARK
    if os.path.exists("figures/eda_correlation_heatmap.png"):
        slide5.shapes.add_picture("figures/eda_correlation_heatmap.png", Inches(6.7), Inches(1.4), width=Inches(5.8))

    # --- SLIDE 6: 3. EDA - PCA & Physical Insights ---
    slide6 = prs.slides.add_slide(blank_layout)
    add_header(slide6, "3. Exploratory Analysis: PCA Dimensionality Reduction & Biplot")
    card_pca = slide6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.4), Inches(5.6), Inches(5.6))
    card_pca.fill.solid()
    card_pca.fill.fore_color.rgb = LIGHT_BG
    card_pca.line.color.rgb = BORDER_COLOR
    tf_pca = card_pca.text_frame
    tf_pca.word_wrap = True
    tf_pca.margin_left = Inches(0.25)
    tf_pca.margin_top = Inches(0.2)
    p = tf_pca.paragraphs[0]
    p.text = "PCA as an Exploratory Technique (Slide 70)"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = DARK_BLUE
    pca_notes = [
        ("Course Formulation (Slide 75):", "Eigen-decomposition of Covariance Matrix $C v_i = \\lambda_i v_i$.\nProportion of Variance Explained: $\\text{PVE}_i = \\lambda_i / \\sum \\lambda_j$."),
        ("Dimensionality Reduction Results:", "• PC1 (48.28%): Captures general turbine thermodynamic load (high loadings for CDP, TEY, GTEP, TIT).\n• PC2 (20.48%): Captures ambient temperature (AT) and the inverse CO vs NOx combustion trade-off.\n• First 2 PCs capture 68.76% of total system variance.\n• First 5 PCs capture 92.02% (Scree plot elbow at $p=5$)."),
        ("Industrial Takeaway:", "The 11 physical sensors effectively lie on a 2-to-5 dimensional manifold governed by ambient weather and power dispatch.")
    ]
    for lbl, desc in pca_notes:
        p_l = tf_pca.add_paragraph()
        p_l.text = f"\n{lbl}"
        p_l.font.bold = True
        p_l.font.size = Pt(11)
        p_l.font.color.rgb = ACCENT_BLUE
        p_d = tf_pca.add_paragraph()
        p_d.text = desc
        p_d.font.size = Pt(10)
        p_d.font.color.rgb = TEXT_DARK
    if os.path.exists("figures/eda_pca_biplot.png"):
        slide6.shapes.add_picture("figures/eda_pca_biplot.png", Inches(6.7), Inches(1.4), width=Inches(5.8))

    # --- SLIDE 7: 4. Main Analysis Objectives ---
    slide7 = prs.slides.add_slide(blank_layout)
    add_header(slide7, "4. Main Analysis: Objectives & Methodological Framework")
    objs = [
        ("Objective 1: Energy Yield (TEY) & PCR", 
         "• Predict net turbine energy yield from sensor telemetry.\n"
         "• Problem: Extreme Multicollinearity (VIF > 250 for CDP, TIT, GTEP, Slide 115).\n"
         "• Method: Principal Component Regression (PCR, Slides 70, 106) on 5 PCs ($Z = X V_p$) to eliminate variance inflation and ensure parameter stability."),
        ("Objective 2: Emissions Modeling (CO & NOx)", 
         "• Quantify pollutant generation as a function of firing state.\n"
         "• Method: Polynomial Regression (Slide 116 & Ex 4.1) for CO to capture steep non-linear spikes during low-load/startup regimes ($x \\to [x, x^2]$).\n"
         "• Multivariate OLS for NOx tracking thermal oxidation."),
        ("Objective 3: Operational Regimes (K-Means)", 
         "• Discover discrete turbine operational regimes (Unsupervised).\n"
         "• Method: K-Means Clustering (Slides 90-91) with Silhouette validation (Slide 94, Ex 3.1): $\\text{SIL} = \\frac{1}{m}\\sum \\frac{b_i - a_i}{\\max(a_i, b_i)}$.\n"
         "• Identifies Base-load, Peak-load, and Low-load emission profiles.")
    ]
    for i, (title, desc) in enumerate(objs):
        left = Inches(0.8 + i * 4.0)
        card_obj = slide7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, Inches(1.5), Inches(3.7), Inches(3.2))
        card_obj.fill.solid()
        card_obj.fill.fore_color.rgb = LIGHT_BG
        card_obj.line.color.rgb = BORDER_COLOR
        tf_o = card_obj.text_frame
        tf_o.word_wrap = True
        tf_o.margin_left = Inches(0.2)
        tf_o.margin_top = Inches(0.2)
        p = tf_o.paragraphs[0]
        p.text = title
        p.font.size = Pt(13)
        p.font.bold = True
        p.font.color.rgb = DARK_BLUE
        p_desc = tf_o.add_paragraph()
        p_desc.text = desc
        p_desc.font.size = Pt(10)
        p_desc.font.color.rgb = TEXT_DARK

    bot_card = slide7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(4.9), Inches(11.7), Inches(2.1))
    bot_card.fill.solid()
    bot_card.fill.fore_color.rgb = LIGHT_BG
    bot_card.line.color.rgb = BORDER_COLOR
    tf_b = bot_card.text_frame
    tf_b.word_wrap = True
    tf_b.margin_left = Inches(0.25)
    tf_b.margin_top = Inches(0.15)
    p = tf_b.paragraphs[0]
    p.text = "Mathematical Formulations & Accuracy Metrics (Course Standards)"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = DARK_BLUE
    p_f = tf_b.add_paragraph()
    p_f.text = (
        "• Ordinary Least Squares: $\\hat{\\beta} = (X^T X)^{-1} X^T y$ (Slide 106) | Principal Component Regression: $\\hat{\\beta}_{PCR} = (Z^T Z)^{-1} Z^T y$\n"
        "• Accuracy Metrics: $R^2 = 1 - \\frac{RSS}{TSS}$ (Slide 108), $\\text{RMSE} = \\sqrt{\\frac{1}{m}\\sum (y_i - \\hat{y}_i)^2}$\n"
        "• Multicollinearity VIF: $\\text{VIF}(\\hat{\\beta}_j) = \\frac{1}{1 - R^2_{x_j|x_{-j}}}$ (Slide 115) | Silhouette Quality: $\\text{SIL}_i = \\frac{b_i - a_i}{\\max(a_i, b_i)}$ (Slide 94)"
    )
    p_f.font.size = Pt(10.5)
    p_f.font.color.rgb = TEXT_DARK

    # --- SLIDE 8: 5. Preview / Summary of Results ---
    slide8 = prs.slides.add_slide(blank_layout)
    add_header(slide8, "5. Preview & High-Level Summary of the Results")

    # Left: Summary Table
    t_shape8 = slide8.shapes.add_table(7, 5, Inches(0.8), Inches(1.5), Inches(6.8), Inches(5.5))
    t8 = t_shape8.table
    t8.columns[0].width = Inches(2.4)
    t8.columns[1].width = Inches(1.1)
    t8.columns[2].width = Inches(1.1)
    t8.columns[3].width = Inches(1.1)
    t8.columns[4].width = Inches(1.1)

    headers8 = ["Model & Objective", "Train R²", "Test R²", "Test RMSE", "Test MAE"]
    for c_idx, h in enumerate(headers8):
        cell = t8.cell(0, c_idx)
        cell.text = h
        cell.fill.solid()
        cell.fill.fore_color.rgb = DARK_BLUE
        p = cell.text_frame.paragraphs[0]
        p.font.bold = True
        p.font.size = Pt(10)
        p.font.color.rgb = WHITE

    model_summary_data = [
        ("TEY: Ambient Baseline", "0.1133", "-0.1407", "15.99 MWh", "12.87 MWh"),
        ("TEY: Full OLS (8 Feat.)", "0.9977", "0.9501", "3.35 MWh", "3.18 MWh"),
        ("TEY: PCR (5 Components)", "0.9946", "0.9828", "1.96 MWh", "1.62 MWh"),
        ("CO: Linear OLS", "0.5728", "0.4195", "1.67 mg/m³", "1.11 mg/m³"),
        ("CO: Polynomial (Deg. 2)", "0.6439", "0.4546", "1.62 mg/m³", "1.14 mg/m³"),
        ("NOx: Multivariate OLS", "0.4536", "-1.0928*", "15.30 mg/m³", "13.85 mg/m³")
    ]
    for r_idx, row in enumerate(model_summary_data, start=1):
        for c_idx, val in enumerate(row):
            cell = t8.cell(r_idx, c_idx)
            cell.text = val
            cell.fill.solid()
            # Highlight PCR row with light green
            if r_idx == 3:
                cell.fill.fore_color.rgb = RGBColor(235, 247, 238)
            else:
                cell.fill.fore_color.rgb = WHITE if r_idx % 2 == 0 else LIGHT_BG
            p = cell.text_frame.paragraphs[0]
            p.font.size = Pt(9.5)
            p.font.color.rgb = TEXT_DARK

    # Right: Results Comparison Card
    card_prev = slide8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(7.9), Inches(1.5), Inches(4.6), Inches(5.5))
    card_prev.fill.solid()
    card_prev.fill.fore_color.rgb = LIGHT_BG
    card_prev.line.color.rgb = BORDER_COLOR
    tf_p = card_prev.text_frame
    tf_p.word_wrap = True
    tf_p.margin_left = Inches(0.25)
    tf_p.margin_top = Inches(0.2)

    p = tf_p.paragraphs[0]
    p.text = "Key Results Highlights"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = DARK_BLUE

    res_highlights = [
        ("1. PCR Solves Multicollinearity:", "PCR achieves Test R² = 0.9828 with RMSE of 1.96 MWh (41.4% error reduction vs full OLS) by projecting collinear turbine pressures into orthogonal coordinates."),
        ("2. Ambient-Only Baseline Fails:", "Ambient inputs alone yield negative out-of-sample R² (-0.14), proving internal thermodynamic telemetry is indispensable."),
        ("3. Non-linear CO Emissions:", "Polynomial degree 2 expansion captures steep low-load incomplete combustion spikes, increasing Train R² to 0.6439."),
        ("4. NOx Domain Shift (*):", "Negative Test R² for NOx reveals a physical process shift in 2014-15 (burner recalibration lowering baseline emissions from 68 to 58 mg/m³).")
    ]
    for lbl, desc in res_highlights:
        p_l = tf_p.add_paragraph()
        p_l.text = f"\n{lbl}"
        p_l.font.bold = True
        p_l.font.size = Pt(11)
        p_l.font.color.rgb = ACCENT_BLUE
        p_d = tf_p.add_paragraph()
        p_d.text = desc
        p_d.font.size = Pt(9.5)
        p_d.font.color.rgb = TEXT_DARK

    # --- SLIDE 9: 6. Detailed Results - Energy Yield & PCR ---
    slide9 = prs.slides.add_slide(blank_layout)
    add_header(slide9, "6. Detailed Results: Energy Yield (TEY) & PCR Diagnostics")

    # Left: Text analysis
    card_d1 = slide9.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.4), Inches(5.6), Inches(5.6))
    card_d1.fill.solid()
    card_d1.fill.fore_color.rgb = LIGHT_BG
    card_d1.line.color.rgb = BORDER_COLOR
    tf_d1 = card_d1.text_frame
    tf_d1.word_wrap = True
    tf_d1.margin_left = Inches(0.25)
    tf_d1.margin_top = Inches(0.2)

    p = tf_d1.paragraphs[0]
    p.text = "TEY Model Diagnostics & Residuals"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = DARK_BLUE

    tey_details = [
        ("Out-of-Sample Generalization:", "• PCR (5 Components) maintains excellent stability across all test years:\n  - 2014 R² = 0.985 (RMSE = 1.84 MWh)\n  - 2015 R² = 0.982 (RMSE = 2.07 MWh)\n• Full OLS suffers parameter instability (2014 R² drops to 0.935)."),
        ("Residual Analysis (Slide 104, 108):", "• Residuals $e_i = y_i - \\hat{y}_i$ for PCR are strictly zero-centered (Mean = 0.04 MWh) with symmetric Gaussian distribution.\n• Constant variance (homoscedasticity) across the entire operating range (100 to 180 MWh)."),
        ("Standard Errors (Slide 111):", "• All 5 Principal Component coefficients $\\hat{\\beta}$ are statistically significant ($p < 0.001$, confidence intervals strictly exclude 0).")
    ]
    for lbl, desc in tey_details:
        p_l = tf_d1.add_paragraph()
        p_l.text = f"\n{lbl}"
        p_l.font.bold = True
        p_l.font.size = Pt(11)
        p_l.font.color.rgb = ACCENT_BLUE
        p_d = tf_d1.add_paragraph()
        p_d.text = desc
        p_d.font.size = Pt(10)
        p_d.font.color.rgb = TEXT_DARK

    # Right: Residuals image
    if os.path.exists("figures/results_residuals_diagnostics.png"):
        slide9.shapes.add_picture("figures/results_residuals_diagnostics.png", Inches(6.7), Inches(1.4), width=Inches(5.8))

    # --- SLIDE 10: 6. Detailed Results - Emissions & Operational Regimes ---
    slide10 = prs.slides.add_slide(blank_layout)
    add_header(slide10, "6. Detailed Results: Emissions Modeling & Operational Regimes")

    # Left: Text analysis
    card_d2 = slide10.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.4), Inches(5.6), Inches(5.6))
    card_d2.fill.solid()
    card_d2.fill.fore_color.rgb = LIGHT_BG
    card_d2.line.color.rgb = BORDER_COLOR
    tf_d2 = card_d2.text_frame
    tf_d2.word_wrap = True
    tf_d2.margin_left = Inches(0.25)
    tf_d2.margin_top = Inches(0.2)

    p = tf_d2.paragraphs[0]
    p.text = "Emissions Modeling & K-Means Clusters"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = DARK_BLUE

    emiss_details = [
        ("CO Polynomial Enhancement (Slide 116):", "• Adding quadratic terms $\\text{TIT}^2, \\text{TAT}^2, \\text{CDP}^2$ boosts Train R² from 0.5728 to 0.6439.\n• Captures the non-linear inflection where combustion transitions from incomplete (high CO) to clean."),
        ("Operational Regimes Profile (K=3):", "• Peak Load (4,887 hrs): $\\text{TEY}=157.0$ MWh, $\\text{TIT}=1100^\\circ\\text{C} \\implies \\text{CO}=1.00$ mg/m³.\n• Part-Load (5,443 hrs): $\\text{TEY}=111.8$ MWh, $\\text{TIT}=1056^\\circ\\text{C} \\implies \\text{CO}=4.79$ mg/m³ (4.8x higher!).\n• Baseload (11,861 hrs): $\\text{TEY}=133.9$ MWh, $\\text{TIT}=1089^\\circ\\text{C} \\implies \\text{CO}=1.53$ mg/m³."),
        ("Industrial Implication:", "Part-load operation is the major driver of CO emissions. Minimizing low-firing transitional hours maximizes environmental efficiency.")
    ]
    for lbl, desc in emiss_details:
        p_l = tf_d2.add_paragraph()
        p_l.text = f"\n{lbl}"
        p_l.font.bold = True
        p_l.font.size = Pt(11)
        p_l.font.color.rgb = ACCENT_BLUE
        p_d = tf_d2.add_paragraph()
        p_d.text = desc
        p_d.font.size = Pt(10)
        p_d.font.color.rgb = TEXT_DARK

    # Right: Regimes scatter image
    if os.path.exists("figures/results_kmeans_regimes_scatter.png"):
        slide10.shapes.add_picture("figures/results_kmeans_regimes_scatter.png", Inches(6.7), Inches(1.4), width=Inches(5.8))

    prs.save("presentation.pptx")
    print("presentation.pptx updated with Slide 8, 9, 10 (Points 5 and 6).")

update_presentation()
