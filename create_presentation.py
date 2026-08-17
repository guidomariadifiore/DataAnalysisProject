import json
import os
import pptx
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

def create_presentation():
    prs = pptx.Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # Color Palette
    DARK_BLUE = RGBColor(16, 37, 66)      # Primary Dark
    ACCENT_BLUE = RGBColor(41, 98, 153)   # Accent
    LIGHT_BG = RGBColor(248, 249, 250)    # Card BG
    TEXT_DARK = RGBColor(33, 37, 41)      # Main text
    TEXT_MUTED = RGBColor(108, 117, 125)  # Subtitles
    WHITE = RGBColor(255, 255, 255)
    BORDER_COLOR = RGBColor(220, 225, 230)

    def add_header(slide, title_text, category_text="DATA ANALYTICS PROJECT WORK"):
        # Top banner background
        header_box = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(1.2))
        header_box.fill.solid()
        header_box.fill.fore_color.rgb = DARK_BLUE
        header_box.line.color.rgb = DARK_BLUE
        
        # Category subtitle
        tf_cat = header_box.text_frame
        tf_cat.word_wrap = True
        tf_cat.margin_left = Inches(0.8)
        tf_cat.margin_top = Inches(0.15)
        
        p0 = tf_cat.paragraphs[0]
        p0.text = category_text.upper()
        p0.font.size = Pt(11)
        p0.font.bold = True
        p0.font.color.rgb = RGBColor(180, 205, 235)
        
        # Title text
        p1 = tf_cat.add_paragraph()
        p1.text = title_text
        p1.font.size = Pt(22)
        p1.font.bold = True
        p1.font.color.rgb = WHITE

    # --- SLIDE 1: Title Slide ---
    slide1 = prs.slides.add_slide(blank_layout)
    bg1 = slide1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5))
    bg1.fill.solid()
    bg1.fill.fore_color.rgb = DARK_BLUE
    bg1.line.color.rgb = DARK_BLUE

    # Title box
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

    # --- SLIDE 2: Project Structure (The 7 Guideline Steps) ---
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

    # --- SLIDE 3: Point 1 - Description of the Dataset ---
    slide3 = prs.slides.add_slide(blank_layout)
    add_header(slide3, "1. Description of the Dataset & Sensor Features")
    
    # Left Card: General Info
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
        
    # Right Table: Sensor Variables Breakdown
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

    prs.save("presentation.pptx")
    print("presentation.pptx created successfully.")

create_presentation()
