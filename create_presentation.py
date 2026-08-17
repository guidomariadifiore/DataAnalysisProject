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
    TEXT_MUTED = RGBColor(108, 117, 125)
    WHITE = RGBColor(255, 255, 255)
    BORDER_COLOR = RGBColor(220, 225, 230)
    GREEN_ACCENT = RGBColor(40, 167, 69)

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

    # --- SLIDE 4: 2. Data Cleaning & Preprocessing ---
    slide4 = prs.slides.add_slide(blank_layout)
    add_header(slide4, "2. Data Cleaning, Quality Validation & Preprocessing")
    
    # 3 Summary Cards
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
    items_c1 = [
        "• Missing Values: 0 nulls across all 11 columns.",
        "• Duplicates: 7 identical sensor rows detected and pruned.",
        "• Chronology: Preserved time order across 2011–2015.",
        "• Sensor Health: No negative pressures or invalid readings."
    ]
    for it in items_c1:
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
    items_c2 = [
        "• Robust Dispersion: $\\hat{\\sigma} = \\frac{IQR}{1.35} = \\frac{Q_3 - Q_1}{1.35}$",
        "• Robust Centering: Uses Median ($Q_2$) to resist leverage.",
        "• Boundaries: $[\\text{Med} - 5\\hat{\\sigma},\\; \\text{Med} + 5\\hat{\\sigma}]$",
        "• Ambient/Turbine: 0 outliers (100% physically valid).",
        "• Emissions (CO/NOx): Skewed tail corresponds to true combustion events (retained)."
    ]
    for it in items_c2:
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
    items_c3 = [
        "• Train Set (2011–13): 22,187 samples (60.4%)",
        "• Test Set (2014–15): 14,539 samples (39.6%)",
        "• No Leakage: Fit scaler strictly on Train, transform Test.",
        "• Z-Score Standardization: $z = \\frac{x - \\mu_{train}}{\\sigma_{train}}$ for PCA & Regression."
    ]
    for it in items_c3:
        p = tf_c3.add_paragraph()
        p.text = it
        p.font.size = Pt(10.5)
        p.font.color.rgb = TEXT_DARK

    # Bottom Table: Sigma-Clipping Bounds Summary
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

    prs.save("presentation.pptx")
    print("presentation.pptx updated with Slide 4 (Data Cleaning).")

update_presentation()
