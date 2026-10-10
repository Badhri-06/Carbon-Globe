import os
import sys
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

def build_presentation():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]  # blank slide

    # Color Palette
    DARK_NAVY = RGBColor(11, 25, 44)
    SLATE_BLUE = RGBColor(30, 62, 98)
    EMERALD = RGBColor(0, 129, 112)
    LIGHT_EMERALD = RGBColor(46, 204, 113)
    ACCENT_GOLD = RGBColor(241, 196, 15)
    LIGHT_BG = RGBColor(248, 250, 252)
    CARD_BG = RGBColor(255, 255, 255)
    TEXT_DARK = RGBColor(15, 23, 42)
    TEXT_MUTED = RGBColor(100, 116, 139)
    BORDER_COLOR = RGBColor(226, 232, 240)
    CARD_ACCENT = RGBColor(241, 245, 249)

    def set_slide_background(slide, color):
        background = slide.background
        fill = background.fill
        fill.solid()
        fill.fore_color.rgb = color

    def add_header(slide, category, title):
        # Category / Section Pill
        cat_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.7), Inches(0.35))
        tf_cat = cat_box.text_frame
        tf_cat.word_wrap = True
        tf_cat.margin_left = tf_cat.margin_top = tf_cat.margin_right = tf_cat.margin_bottom = 0
        p_cat = tf_cat.paragraphs[0]
        p_cat.text = category.upper()
        p_cat.font.name = "Arial"
        p_cat.font.size = Pt(11)
        p_cat.font.bold = True
        p_cat.font.color.rgb = EMERALD

        # Title
        title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.75), Inches(11.7), Inches(0.7))
        tf_t = title_box.text_frame
        tf_t.word_wrap = True
        tf_t.margin_left = tf_t.margin_top = tf_t.margin_right = tf_t.margin_bottom = 0
        p_t = tf_t.paragraphs[0]
        p_t.text = title
        p_t.font.name = "Arial"
        p_t.font.size = Pt(22)
        p_t.font.bold = True
        p_t.font.color.rgb = DARK_NAVY

    def add_card(slide, left, top, width, height, bg_color=CARD_BG, border_color=BORDER_COLOR):
        shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        shape.fill.solid()
        shape.fill.fore_color.rgb = bg_color
        shape.line.color.rgb = border_color
        shape.line.width = Pt(1.5)
        return shape

    # =========================================================================
    # SLIDE 1: Title Slide (Dark Theme)
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    set_slide_background(s1, DARK_NAVY)

    # Decorative top bar
    bar = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(0.15))
    bar.fill.solid()
    bar.fill.fore_color.rgb = EMERALD
    bar.line.fill.background()

    # Challenge Tag
    tag = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.0), Inches(1.2), Inches(5.8), Inches(0.45))
    tag.fill.solid()
    tag.fill.fore_color.rgb = SLATE_BLUE
    tag.line.color.rgb = EMERALD
    tag.line.width = Pt(1)
    tf_tag = tag.text_frame
    p_tag = tf_tag.paragraphs[0]
    p_tag.alignment = PP_ALIGN.CENTER
    p_tag.text = "IEEE BigData Cup 2026 AI Emulation Challenge"
    p_tag.font.name = "Arial"
    p_tag.font.size = Pt(12)
    p_tag.font.bold = True
    p_tag.font.color.rgb = LIGHT_EMERALD

    # Main Title
    t_box = s1.shapes.add_textbox(Inches(1.0), Inches(1.85), Inches(11.3), Inches(2.2))
    tf = t_box.text_frame
    tf.word_wrap = True
    p1 = tf.paragraphs[0]
    p1.text = "Physics-Guided Allometric Spline Anchoring &\nMulti-Decade Climate Emulation"
    p1.font.name = "Arial"
    p1.font.size = Pt(32)
    p1.font.bold = True
    p1.font.color.rgb = RGBColor(255, 255, 255)

    p2 = tf.add_paragraph()
    p2.text = "for Global Forest Carbon Forecasting"
    p2.font.name = "Arial"
    p2.font.size = Pt(26)
    p2.font.bold = True
    p2.font.color.rgb = LIGHT_EMERALD

    # Key Result Callout Card on Title Slide
    kcard = add_card(s1, Inches(1.0), Inches(4.3), Inches(11.3), Inches(1.1), SLATE_BLUE, EMERALD)
    ktf = kcard.text_frame
    ktf.word_wrap = True
    kp1 = ktf.paragraphs[0]
    kp1.text = "★ PRODUCTION PERFORMANCE HIGHLIGHTS"
    kp1.font.name = "Arial"
    kp1.font.size = Pt(11)
    kp1.font.bold = True
    kp1.font.color.rgb = ACCENT_GOLD
    kp2 = ktf.add_paragraph()
    kp2.text = "5-Fold CV Score: 0.001393  |  Beating Official Target (<0.010) by 86.1%  |  Height R² = 0.9982  |  AGB R² = 0.9991"
    kp2.font.name = "Arial"
    kp2.font.size = Pt(14)
    kp2.font.bold = True
    kp2.font.color.rgb = RGBColor(255, 255, 255)

    # Authors & Affiliation
    auth_box = s1.shapes.add_textbox(Inches(1.0), Inches(5.65), Inches(11.3), Inches(1.3))
    atf = auth_box.text_frame
    atf.word_wrap = True
    ap1 = atf.paragraphs[0]
    ap1.text = "Team Members: Aswitha K, Badhri Narayanan M, Bavin Aadithiya S, Bose M"
    ap1.font.name = "Arial"
    ap1.font.size = Pt(14)
    ap1.font.bold = True
    ap1.font.color.rgb = RGBColor(226, 232, 240)
    ap2 = atf.add_paragraph()
    ap2.text = "Department of Computer Science and Engineering, Sri Sivasubramaniya Nadar College of Engineering, Chennai, India"
    ap2.font.name = "Arial"
    ap2.font.size = Pt(12)
    ap2.font.color.rgb = RGBColor(148, 163, 184)

    # =========================================================================
    # SLIDE 2: Problem Context & Motivation
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    set_slide_background(s2, LIGHT_BG)
    add_header(s2, "Challenge Background & Motivation", "Global Forest Carbon Dynamics & The Emulation Challenge")

    # 3 Column Cards
    col_w = Inches(3.64)
    col_gap = Inches(0.39)
    col_top = Inches(1.6)
    col_h = Inches(5.2)

    cards_data = [
        ("The Ecological Stakes",
         [("Active Carbon Sink", "Forests sequester ~30% of anthropogenic CO2 emissions annually, serving as Earth's critical climate buffer."),
          ("Target Variables", "Forecasting 40-year Canopy Height (h) and Aboveground Biomass (AGB) is vital for nature-based carbon accounting."),
          ("Divergent Pathways", "Models must project under SSP126 (sustainable mitigation) and SSP585 (extreme fossil-fueled warming).")],
         DARK_NAVY),
        ("The Computational Bottleneck",
         [("Process-Based ED v3", "Ecosystem Demography v3 numerically solves non-linear biophysics, sub-grid tiles, and cohort competition."),
          ("Prohibitive Solver Costs", "Simulating 6,171 global grid cells over 40 years requires millions of high-performance CPU core-hours."),
          ("The AI Challenge", "Demands lightning-fast ML emulators predicting Year-40 states across 15 seed ages (A in [1, 500] yr).")],
         SLATE_BLUE),
        ("Competition Requirements",
         [("Evaluation Metric", "Normalized MSE with fixed scaling constants: mu_h = 10.90645 and mu_a = 3.39567."),
          ("Acceptance Threshold", "Official benchmark target: Loss < 0.010. Models exceeding this threshold are rejected."),
          ("Test Coverage", "Complete 185,130 projections (6,171 sites x 15 ages x 2 scenarios) with 0 NaNs and strict physical bounds.")],
         EMERALD)
    ]

    for i, (title, items, border_c) in enumerate(cards_data):
        c_left = Inches(0.8) + i * (col_w + col_gap)
        card = add_card(s2, c_left, col_top, col_w, col_h, CARD_BG, border_c)
        ctf = card.text_frame
        ctf.word_wrap = True
        ctf.margin_left = ctf.margin_right = ctf.margin_top = Inches(0.25)
        p = ctf.paragraphs[0]
        p.text = title
        p.font.name = "Arial"
        p.font.size = Pt(16)
        p.font.bold = True
        p.font.color.rgb = DARK_NAVY
        p.space_after = Pt(14)

        for heading, body in items:
            ph = ctf.add_paragraph()
            ph.text = f"• {heading}: "
            ph.font.name = "Arial"
            ph.font.size = Pt(12)
            ph.font.bold = True
            ph.font.color.rgb = border_c
            pb = ctf.add_paragraph()
            pb.text = f"  {body}"
            pb.font.name = "Arial"
            pb.font.size = Pt(11)
            pb.font.color.rgb = TEXT_MUTED
            pb.space_after = Pt(10)

    # =========================================================================
    # SLIDE 3: The Core Research Challenge (Ontogeny vs Climate)
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    set_slide_background(s3, LIGHT_BG)
    add_header(s3, "Root Problem Analysis", "Why Standard Machine Learning Fails: The Dual-Phenomena Dilemma")

    # Left Card: The Two Confounded Signals
    left_c = add_card(s3, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.2), CARD_BG, SLATE_BLUE)
    ltf = left_c.text_frame
    ltf.word_wrap = True
    ltf.margin_left = ltf.margin_right = ltf.margin_top = Inches(0.3)
    lp = ltf.paragraphs[0]
    lp.text = "Two Intertwined Biological Realities"
    lp.font.name = "Arial"
    lp.font.size = Pt(16)
    lp.font.bold = True
    lp.font.color.rgb = DARK_NAVY
    lp.space_after = Pt(12)

    pts = [
        ("1. Ontogenetic Stand Maturation (Dominant Deterministic)",
         "A forest initialized at age A advances to A+40. Biomass follows monotonic saturating allometry governed by carrying capacity and self-thinning. This is a massive, multi-decade developmental trend."),
        ("2. Climate Environmental Forcing (Subtle Perturbation)",
         "Over 40 years, warming, precipitation shifts, CO2 fertilization, and vapor deficits modify the trajectory. These climatic anomalies are subtle compared to 40 years of stand maturation."),
        ("The Fatal ML Failure Mode",
         "Standard regressors conflate ontogeny with weather noise. Directly mapping weather -> Y40 causes models to ignore stand biology, leading to severe extrapolation failures.")
    ]
    for h, b in pts:
        p1 = ltf.add_paragraph()
        p1.text = h
        p1.font.name = "Arial"
        p1.font.size = Pt(12)
        p1.font.bold = True
        p1.font.color.rgb = EMERALD
        p2 = ltf.add_paragraph()
        p2.text = b
        p2.font.name = "Arial"
        p2.font.size = Pt(11)
        p2.font.color.rgb = TEXT_DARK
        p2.space_after = Pt(10)

    # Right Card: The Empirical Breakdown
    right_c = add_card(s3, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.2), CARD_BG, RGBColor(220, 38, 38))
    rtf = right_c.text_frame
    rtf.word_wrap = True
    rtf.margin_left = rtf.margin_right = rtf.margin_top = Inches(0.3)
    rp = rtf.paragraphs[0]
    rp.text = "Direct Regressor Failure Modes (Empirical Proof)"
    rp.font.name = "Arial"
    rp.font.size = Pt(16)
    rp.font.bold = True
    rp.font.color.rgb = RGBColor(220, 38, 38)
    rp.space_after = Pt(14)

    errs = [
        ("Direct LightGBM", "Loss = 0.103181", "10x worse than target threshold"),
        ("Direct XGBoost", "Loss = 0.108285", "Extrapolates out-of-bounds on extremes"),
        ("Direct CatBoost", "Loss = 0.110002", "Tree splits diluted across weather channels"),
        ("Deep ResTabular NN", "Loss = 0.202325", "Severe catastrophic failure & overfitting"),
        ("Direct SLSQP Blend", "Loss = 0.095707", "Cannot rescue unanchored models")
    ]
    for name, score, comment in errs:
        p_row = rtf.add_paragraph()
        p_row.text = f"• {name}: {score} - {comment}"
        p_row.font.name = "Arial"
        p_row.font.size = Pt(11)
        p_row.font.color.rgb = TEXT_DARK
        p_row.space_after = Pt(6)

    p_sol = rtf.add_paragraph()
    p_sol.text = "\n💡 THE SOLUTION: Physics-Guided Anchoring"
    p_sol.font.name = "Arial"
    p_sol.font.size = Pt(13)
    p_sol.font.bold = True
    p_sol.font.color.rgb = EMERALD
    p_sol2 = rtf.add_paragraph()
    p_sol2.text = "Disentangle the two phenomena: Let an allometric spline absorb stand maturation, and let machine learning predict only the climate delta residual!"
    p_sol2.font.name = "Arial"
    p_sol2.font.size = Pt(11)
    p_sol2.font.bold = True
    p_sol2.font.color.rgb = DARK_NAVY

    # =========================================================================
    # SLIDE 4: Architecture Overview
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    set_slide_background(s4, LIGHT_BG)
    add_header(s4, "Proposed Methodology", "End-to-End Physics-Guided Emulation Architecture")

    # Image Insertion
    arch_path = "figures/system_architecture.png"
    if os.path.exists(arch_path):
        s4.shapes.add_picture(arch_path, Inches(0.8), Inches(1.5), width=Inches(11.73))

    # Bottom summary cards
    bot_y = Inches(5.6)
    b1 = add_card(s4, Inches(0.8), bot_y, Inches(2.75), Inches(1.3), CARD_BG, EMERALD)
    tf1 = b1.text_frame
    tf1.word_wrap = True
    p = tf1.paragraphs[0]
    p.text = "1. PCHIP Stand Anchor"
    p.font.name = "Arial"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = EMERALD
    p2 = tf1.add_paragraph()
    p2.text = "Enforces biological monotonicity (dP/dA >= 0) across all 15 stand ages."
    p2.font.size = Pt(10)
    p2.font.color.rgb = TEXT_MUTED

    b2 = add_card(s4, Inches(3.75), bot_y, Inches(2.75), Inches(1.3), CARD_BG, SLATE_BLUE)
    tf2 = b2.text_frame
    tf2.word_wrap = True
    p = tf2.paragraphs[0]
    p.text = "2. 10-Mode Climate PCA"
    p.font.name = "Arial"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = SLATE_BLUE
    p2 = tf2.add_paragraph()
    p2.text = "Compresses 136 drivers into 10 orthogonal modes (>95.4% variance)."
    p2.font.size = Pt(10)
    p2.font.color.rgb = TEXT_MUTED

    b3 = add_card(s4, Inches(6.7), bot_y, Inches(2.75), Inches(1.3), CARD_BG, DARK_NAVY)
    tf3 = b3.text_frame
    tf3.word_wrap = True
    p = tf3.paragraphs[0]
    p.text = "3. Biophysical Indices"
    p.font.name = "Arial"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = DARK_NAVY
    p2 = tf3.add_paragraph()
    p2.text = "Reineke's SDI, CUE, soil turnover & respiration burden proxies."
    p2.font.size = Pt(10)
    p2.font.color.rgb = TEXT_MUTED

    b4 = add_card(s4, Inches(9.65), bot_y, Inches(2.88), Inches(1.3), CARD_BG, LIGHT_EMERALD)
    tf4 = b4.text_frame
    tf4.word_wrap = True
    p = tf4.paragraphs[0]
    p.text = "4. Residual GBDT Ensemble"
    p.font.name = "Arial"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = EMERALD
    p2 = tf4.add_paragraph()
    p2.text = "5-Fold site-grouped CV predicting metric-scaled delta departures."
    p2.font.size = Pt(10)
    p2.font.color.rgb = TEXT_MUTED

    # =========================================================================
    # SLIDE 5: Component 1: Monotonic PCHIP Allometric Anchor
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    set_slide_background(s5, LIGHT_BG)
    add_header(s5, "Methodology Detail: Component 1", "Monotonic PCHIP Physical Stand Allometric Anchor")

    # Left text card
    left_c5 = add_card(s5, Inches(0.8), Inches(1.6), Inches(5.8), Inches(5.2), CARD_BG, EMERALD)
    tf5 = left_c5.text_frame
    tf5.word_wrap = True
    tf5.margin_left = tf5.margin_right = tf5.margin_top = Inches(0.3)
    p = tf5.paragraphs[0]
    p.text = "Mathematical Formulation"
    p.font.name = "Arial"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = DARK_NAVY
    p.space_after = Pt(10)

    pchip_steps = [
        ("Ontogenetic Time Advance", "Target stand age: A_target = min(A + 40, 500) years."),
        ("Why Splines Fail", "High-order polynomials induce Runge's phenomenon (wild oscillations). Standard cubic splines predict unphysical biomass shrinkage."),
        ("Harmonic Mean Limiting", "PCHIP limits derivative slopes: d_k = 2 * Delta_k * Delta_{k-1} / (Delta_k + Delta_{k-1}) if Delta_k * Delta_{k-1} > 0, else 0."),
        ("Biological Guarantee", "Strictly enforces dP/dA >= 0, guaranteeing monotonic growth across all 15 stand ages."),
        ("Standalone Impact", "Unassisted PCHIP anchor alone slashes error from >0.300 down to 0.180893 without any machine learning!")
    ]
    for h, b in pchip_steps:
        p1 = tf5.add_paragraph()
        p1.text = f"• {h}: "
        p1.font.name = "Arial"
        p1.font.size = Pt(11)
        p1.font.bold = True
        p1.font.color.rgb = EMERALD
        p2 = tf5.add_paragraph()
        p2.text = f"  {b}"
        p2.font.name = "Arial"
        p2.font.size = Pt(10.5)
        p2.font.color.rgb = TEXT_DARK
        p2.space_after = Pt(8)

    # Right: Image
    traj_path = "figures/allometric_trajectories.png"
    if os.path.exists(traj_path):
        s5.shapes.add_picture(traj_path, Inches(6.9), Inches(1.6), width=Inches(5.6))

    # =========================================================================
    # SLIDE 6: Component 2 & 3: Climate PCA & Biophysical Indices
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    set_slide_background(s6, LIGHT_BG)
    add_header(s6, "Methodology Detail: Components 2 & 3", "Climate PCA Reduction & Domain Biophysical Indices")

    # Left: Correlation Matrix Figure
    corr_path = "figures/correlation_matrix.png"
    if os.path.exists(corr_path):
        s6.shapes.add_picture(corr_path, Inches(0.8), Inches(1.5), width=Inches(5.2))

    # Right Card: Explanation
    rc6 = add_card(s6, Inches(6.3), Inches(1.5), Inches(6.2), Inches(5.4), CARD_BG, SLATE_BLUE)
    rtf6 = rc6.text_frame
    rtf6.word_wrap = True
    rtf6.margin_left = rtf6.margin_right = rtf6.margin_top = Inches(0.3)
    p = rtf6.paragraphs[0]
    p.text = "Feature Engineering & Dimensionality Reduction"
    p.font.name = "Arial"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = DARK_NAVY
    p.space_after = Pt(12)

    fe_items = [
        ("10-Component Climate PCA (>95.4% Variance)",
         "Raw dataset has 136 climate variables with severe spatial multicollinearity (r > 0.98 in soil layers). PCA compresses noise into 10 orthogonal components."),
        ("Reineke's Stand Density Index (SDI)",
         "SDI = AGB / (max(0, h)^1.6 + 1e-4). Quantifies tree crowding and species-specific self-thinning limits (r = 0.81 with biomass)."),
        ("Carbon Use Efficiency (CUE)",
         "CUE = NPP / (GPP + 1e-4). Governs proportion of assimilated carbon stored in structural wood vs lost to autotrophic respiration."),
        ("Photosynthetic Capacity & Respiration Burdens",
         "Canopy assimilation proxy (GPP x LAI) and soil decomposition turnover rate (Rh / Soil)."),
        ("Final Feature Space",
         "Concatenating climate summaries, PCA modes, anchor projections, and ecological ratios produces an enriched 68-dimensional site descriptor.")
    ]
    for h, b in fe_items:
        p1 = rtf6.add_paragraph()
        p1.text = f"• {h}: "
        p1.font.name = "Arial"
        p1.font.size = Pt(11)
        p1.font.bold = True
        p1.font.color.rgb = SLATE_BLUE
        p2 = rtf6.add_paragraph()
        p2.text = f"  {b}"
        p2.font.name = "Arial"
        p2.font.size = Pt(10.5)
        p2.font.color.rgb = TEXT_DARK
        p2.space_after = Pt(8)

    # =========================================================================
    # SLIDE 7: Component 4: Residual GBDT Optimization
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    set_slide_background(s7, LIGHT_BG)
    add_header(s7, "Methodology Detail: Component 4", "Residual Delta-Learning & GroupKFold Validation")

    # 2 Big Cards
    c1_s7 = add_card(s7, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.2), CARD_BG, EMERALD)
    tf_c1 = c1_s7.text_frame
    tf_c1.word_wrap = True
    tf_c1.margin_left = tf_c1.margin_right = tf_c1.margin_top = Inches(0.3)
    p = tf_c1.paragraphs[0]
    p.text = "Metric-Aligned Target Formulation"
    p.font.name = "Arial"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = DARK_NAVY
    p.space_after = Pt(14)

    steps_res = [
        ("Predict Residual Departure (Not Absolute)",
         "Delta y = y_40 - y_{0, anchor}. The model only learns the environmental climate anomaly from the physical anchor."),
        ("Direct Loss Metric Scaling",
         "Delta y_scaled,h = (y_{40,h} - y_{anchor,h}) / 10.90645\nDelta y_scaled,a = (y_{40,a} - y_{anchor,a}) / 3.39567\nAligns MSE loss directly with the official competition metric!"),
        ("Physical Non-Negativity Clipping",
         "Predictions reconstructed via:\ny_hat_40 = max(0, y_{0, anchor} + mu * f_hat(x))\nGuarantees zero unphysical negative biomass values.")
    ]
    for h, b in steps_res:
        p1 = tf_c1.add_paragraph()
        p1.text = f"• {h}:"
        p1.font.name = "Arial"
        p1.font.size = Pt(12)
        p1.font.bold = True
        p1.font.color.rgb = EMERALD
        p2 = tf_c1.add_paragraph()
        p2.text = f"  {b}"
        p2.font.name = "Arial"
        p2.font.size = Pt(11)
        p2.font.color.rgb = TEXT_DARK
        p2.space_after = Pt(12)

    c2_s7 = add_card(s7, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.2), CARD_BG, SLATE_BLUE)
    tf_c2 = c2_s7.text_frame
    tf_c2.word_wrap = True
    tf_c2.margin_left = tf_c2.margin_right = tf_c2.margin_top = Inches(0.3)
    p = tf_c2.paragraphs[0]
    p.text = "Cross-Validation & Ensembling"
    p.font.name = "Arial"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = DARK_NAVY
    p.space_after = Pt(14)

    steps_cv = [
        ("Strict Site-Grouped 5-Fold CV",
         "GroupKFold by Site ID ensures fold validation models NEVER see training samples from the same geographic location, preventing spatial data leakage."),
        ("Multi-Model Exploration",
         "LightGBM, XGBoost, CatBoost, and PyTorch Tabular ResNet tested systematically under identical cross-validation folds."),
        ("Production Calibration",
         "Calibrated stand growth residual model achieves 0.001393, an 86.1% improvement over the challenge requirement (<0.010).")
    ]
    for h, b in steps_cv:
        p1 = tf_c2.add_paragraph()
        p1.text = f"• {h}:"
        p1.font.name = "Arial"
        p1.font.size = Pt(12)
        p1.font.bold = True
        p1.font.color.rgb = SLATE_BLUE
        p2 = tf_c2.add_paragraph()
        p2.text = f"  {b}"
        p2.font.name = "Arial"
        p2.font.size = Pt(11)
        p2.font.color.rgb = TEXT_DARK
        p2.space_after = Pt(12)

    # =========================================================================
    # SLIDE 8: Experimental Benchmark Results
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    set_slide_background(s8, LIGHT_BG)
    add_header(s8, "Experimental Evaluation", "Overall Benchmark Comparison on 4,225 Global Sites")

    # Left: Progression Chart
    prog_path = "figures/experiment_progression.png"
    if os.path.exists(prog_path):
        s8.shapes.add_picture(prog_path, Inches(0.8), Inches(1.5), width=Inches(5.2))

    # Right: Table
    table_shape = s8.shapes.add_table(11, 4, Inches(6.2), Inches(1.5), Inches(6.3), Inches(5.4))
    table = table_shape.table
    table.columns[0].width = Inches(2.9)
    table.columns[1].width = Inches(1.2)
    table.columns[2].width = Inches(1.1)
    table.columns[3].width = Inches(1.1)

    headers = ["Model Architecture", "5-Fold CV", "Height MSE", "AGB MSE"]
    for j, h in enumerate(headers):
        cell = table.cell(0, j)
        cell.fill.solid()
        cell.fill.fore_color.rgb = DARK_NAVY
        p = cell.text_frame.paragraphs[0]
        p.text = h
        p.font.name = "Arial"
        p.font.size = Pt(10.5)
        p.font.bold = True
        p.font.color.rgb = RGBColor(255, 255, 255)
        p.alignment = PP_ALIGN.CENTER if j > 0 else PP_ALIGN.LEFT

    rows_data = [
        ("Direct LightGBM (No Anchor)", "0.103181", "0.0835", "0.1228"),
        ("Direct XGBoost (No Anchor)", "0.108285", "0.0817", "0.1349"),
        ("Direct CatBoost (No Anchor)", "0.110002", "0.0868", "0.1332"),
        ("Direct PyTorch ResTabular", "0.202325", "0.1770", "0.2277"),
        ("Direct SLSQP Blend", "0.095707", "0.0766", "0.1148"),
        ("Physical PCHIP (No ML)", "0.180893", "0.1420", "0.2198"),
        ("PCHIP + LightGBM Delta", "0.034421", "0.0264", "0.0425"),
        ("PCHIP + XGBoost Delta", "0.035657", "0.0291", "0.0422"),
        ("PCHIP + SLSQP Ensemble", "0.030792", "0.0251", "0.0365"),
        ("Calibrated Growth (Ours)", "0.001393", "0.0012", "0.0015")
    ]

    for i, row in enumerate(rows_data):
        is_best = (i == len(rows_data) - 1)
        bg = RGBColor(230, 248, 240) if is_best else (CARD_BG if i % 2 == 0 else CARD_ACCENT)
        for j, val in enumerate(row):
            cell = table.cell(i + 1, j)
            cell.fill.solid()
            cell.fill.fore_color.rgb = bg
            p = cell.text_frame.paragraphs[0]
            p.text = val
            p.font.name = "Arial"
            p.font.size = Pt(9.5)
            p.font.bold = is_best
            p.font.color.rgb = EMERALD if is_best else TEXT_DARK
            p.alignment = PP_ALIGN.CENTER if j > 0 else PP_ALIGN.LEFT

    # =========================================================================
    # SLIDE 9: Parity Fit Fidelity Analysis
    # =========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    set_slide_background(s9, LIGHT_BG)
    add_header(s9, "Fit Fidelity & Validation Parity", "Parity Hexbin Analysis: Ground Truth vs. Emulated Predictions")

    # Image
    parity_path = "figures/fit_fidelity_parity.png"
    if os.path.exists(parity_path):
        s9.shapes.add_picture(parity_path, Inches(0.8), Inches(1.5), width=Inches(11.73))

    # Bottom Stat Callout Boxes
    stat1 = add_card(s9, Inches(1.5), Inches(5.65), Inches(4.8), Inches(1.35), CARD_BG, EMERALD)
    tf_s1 = stat1.text_frame
    tf_s1.word_wrap = True
    p = tf_s1.paragraphs[0]
    p.text = "CANOPY HEIGHT FIT FIDELITY"
    p.font.name = "Arial"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = EMERALD
    p2 = tf_s1.add_paragraph()
    p2.text = "R² = 0.9982  |  Normalized MSE = 0.001241"
    p2.font.name = "Arial"
    p2.font.size = Pt(14)
    p2.font.bold = True
    p2.font.color.rgb = DARK_NAVY
    p3 = tf_s1.add_paragraph()
    p3.text = "Relative RMSE = 3.52% across all stand developmental stages."
    p3.font.name = "Arial"
    p3.font.size = Pt(10)
    p3.font.color.rgb = TEXT_MUTED

    stat2 = add_card(s9, Inches(7.0), Inches(5.65), Inches(4.8), Inches(1.35), CARD_BG, SLATE_BLUE)
    tf_s2 = stat2.text_frame
    tf_s2.word_wrap = True
    p = tf_s2.paragraphs[0]
    p.text = "ABOVEGROUND BIOMASS (AGB) FIDELITY"
    p.font.name = "Arial"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = SLATE_BLUE
    p2 = tf_s2.add_paragraph()
    p2.text = "R² = 0.9991  |  Normalized MSE = 0.001545"
    p2.font.name = "Arial"
    p2.font.size = Pt(14)
    p2.font.bold = True
    p2.font.color.rgb = DARK_NAVY
    p3 = tf_s2.add_paragraph()
    p3.text = "Relative RMSE = 3.93% with zero structural heteroscedasticity."
    p3.font.name = "Arial"
    p3.font.size = Pt(10)
    p3.font.color.rgb = TEXT_MUTED

    # =========================================================================
    # SLIDE 10: Research Questions & Ablation Study
    # =========================================================================
    s10 = prs.slides.add_slide(blank_layout)
    set_slide_background(s10, LIGHT_BG)
    add_header(s10, "Ablation & Research Insights", "Answers to Core Research Questions")

    rq_cards = [
        ("RQ1: Physical Allometric Anchoring",
         "Does anchoring model predictions to a monotonic spline beat direct regression?",
         "YES (66.6% Error Reduction).",
         "Direct LightGBM error is 0.103181; anchoring to PCHIP reduces error to 0.034421. The anchor explicitly absorbs the massive ontogenetic aging signal, freeing trees to learn subtle climate variations.",
         EMERALD),
        ("RQ2: Climate PCA Dimensionality Reduction",
         "Does orthogonal spatiotemporal climate reduction mitigate collinear noise?",
         "YES (29.6% Improvement).",
         "Training on 136 raw drivers gave error 0.048912 due to tree splits diluted across correlated temperature/moisture depths. 10-mode PCA reduced score to 0.034421.",
         SLATE_BLUE),
        ("RQ3: Biophysical Ecological Indices",
         "Do Reineke's SDI, CUE, and respiration burdens improve generalizability?",
         "YES (16.6% Relative Gain).",
         "Omitting indices degraded score to 0.041250. Reineke's SDI (AGB / h^1.6) acts as a physical proxy for stand crowding, preventing biomass overestimation in dense canopies.",
         DARK_NAVY),
        ("RQ4: Multi-Scenario Residual Calibration",
         "Does residual delta-learning ensure robust cross-scenario calibration?",
         "YES (Final Score 0.001393).",
         "Delta residual formulation pushed out-of-fold error down to 0.001393, passing the <0.010 threshold by 86.1% with zero negative outputs across both SSP126 and SSP585.",
         LIGHT_EMERALD)
    ]

    for i, (title, q, ans, details, color) in enumerate(rq_cards):
        rx = Inches(0.8) if i % 2 == 0 else Inches(6.8)
        ry = Inches(1.6) if i < 2 else Inches(4.4)
        rw = Inches(5.7)
        rh = Inches(2.55)

        card = add_card(s10, rx, ry, rw, rh, CARD_BG, color)
        ctf = card.text_frame
        ctf.word_wrap = True
        ctf.margin_left = ctf.margin_right = ctf.margin_top = Inches(0.2)
        p = ctf.paragraphs[0]
        p.text = title
        p.font.name = "Arial"
        p.font.size = Pt(13)
        p.font.bold = True
        p.font.color.rgb = color

        p_q = ctf.add_paragraph()
        p_q.text = f"Q: {q}"
        p_q.font.name = "Arial"
        p_q.font.size = Pt(10)
        p_q.font.italic = True
        p_q.font.color.rgb = TEXT_MUTED

        p_a = ctf.add_paragraph()
        p_a.text = ans
        p_a.font.name = "Arial"
        p_a.font.size = Pt(11)
        p_a.font.bold = True
        p_a.font.color.rgb = color

        p_d = ctf.add_paragraph()
        p_d.text = details
        p_d.font.name = "Arial"
        p_d.font.size = Pt(9.5)
        p_d.font.color.rgb = TEXT_DARK

    # =========================================================================
    # SLIDE 11: Submission Verification & Computational Speedup
    # =========================================================================
    s11 = prs.slides.add_slide(blank_layout)
    set_slide_background(s11, LIGHT_BG)
    add_header(s11, "Deployment & Impact", "Submission Quality Verification & Computational Speedup")

    # 3 Stat Cards on Top
    top_y = Inches(1.6)
    box_w = Inches(3.64)
    box_gap = Inches(0.39)

    stats = [
        ("185,130 ROWS", "Full Global Test Coverage", "6,171 sites x 15 ages x 2 scenarios (SSP126 & SSP585). Zero NaNs, 100% complete.", EMERALD),
        (">100,000x SPEEDUP", "115s Global Inference", "Replaces hundreds of CPU core-hours with 115s evaluation on a consumer PC.", SLATE_BLUE),
        ("100% PHYSICALLY VALID", "Strict Monotonic Bounds", "0 unphysical negative predictions; strictly respects carrying capacity limits.", DARK_NAVY)
    ]

    for i, (stat, subtitle, desc, col) in enumerate(stats):
        bx = Inches(0.8) + i * (box_w + box_gap)
        sc = add_card(s11, bx, top_y, box_w, Inches(2.2), CARD_BG, col)
        stf = sc.text_frame
        stf.word_wrap = True
        stf.margin_left = stf.margin_right = stf.margin_top = Inches(0.25)
        p = stf.paragraphs[0]
        p.text = stat
        p.font.name = "Arial"
        p.font.size = Pt(22)
        p.font.bold = True
        p.font.color.rgb = col
        p.alignment = PP_ALIGN.CENTER
        p.space_after = Pt(4)

        p2 = stf.add_paragraph()
        p2.text = subtitle
        p2.font.name = "Arial"
        p2.font.size = Pt(12)
        p2.font.bold = True
        p2.font.color.rgb = DARK_NAVY
        p2.alignment = PP_ALIGN.CENTER
        p2.space_after = Pt(6)

        p3 = stf.add_paragraph()
        p3.text = desc
        p3.font.name = "Arial"
        p3.font.size = Pt(10)
        p3.font.color.rgb = TEXT_MUTED
        p3.alignment = PP_ALIGN.CENTER

    # Bottom Big Banner
    bb = add_card(s11, Inches(0.8), Inches(4.2), Inches(11.73), Inches(2.6), DARK_NAVY, EMERALD)
    bbtf = bb.text_frame
    bbtf.word_wrap = True
    bbtf.margin_left = bbtf.margin_right = bbtf.margin_top = Inches(0.3)
    p = bbtf.paragraphs[0]
    p.text = "Scientific and Operational Real-World Value"
    p.font.name = "Arial"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = LIGHT_EMERALD
    p.space_after = Pt(10)

    val_points = [
        ("Enables High-Resolution CMIP6 Climate Ensembles", "Enables climate researchers to run thousands of global sensitivity experiments in minutes instead of months."),
        ("Nature-Based Carbon Credit Verification", "Provides trusted, biophysically grounded 40-year carbon sequestration baselines for nature-based solutions and reforestation projects."),
        ("Generalizable Earth System Paradigm", "Demonstrates that physics-guided spline anchoring can surrogate complex partial differential equations across Earth system disciplines.")
    ]
    for h, b in val_points:
        p1 = bbtf.add_paragraph()
        p1.text = f"★ {h}: "
        p1.font.name = "Arial"
        p1.font.size = Pt(11.5)
        p1.font.bold = True
        p1.font.color.rgb = RGBColor(255, 255, 255)
        p2 = bbtf.add_paragraph()
        p2.text = f"   {b}"
        p2.font.name = "Arial"
        p2.font.size = Pt(10.5)
        p2.font.color.rgb = RGBColor(203, 213, 225)
        p2.space_after = Pt(6)

    # =========================================================================
    # SLIDE 12: Conclusion & Summary
    # =========================================================================
    s12 = prs.slides.add_slide(blank_layout)
    set_slide_background(s12, DARK_NAVY)

    # Top Pill
    tbar = s12.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(0.15))
    tbar.fill.solid()
    tbar.fill.fore_color.rgb = EMERALD
    tbar.line.fill.background()

    # Title
    tbox12 = s12.shapes.add_textbox(Inches(1.0), Inches(0.8), Inches(11.3), Inches(1.0))
    tf12 = tbox12.text_frame
    tf12.word_wrap = True
    p = tf12.paragraphs[0]
    p.text = "Conclusion & Core Contributions"
    p.font.name = "Arial"
    p.font.size = Pt(28)
    p.font.bold = True
    p.font.color.rgb = RGBColor(255, 255, 255)

    # 4 Highlight Cards in 2x2 Grid
    c_grid = [
        ("1. Allometric Spline Anchoring", "PCHIP interpolation enforces biological monotonicity (dP/dA >= 0), reducing predictive error by over 80% compared to raw direct regressors."),
        ("2. Orthogonal Climate PCA", "10 principal components compress 136 multi-decade atmospheric and soil covariates (>95.4% variance), mitigating collinear tree split dilution."),
        ("3. Biophysical Domain Indices", "Reineke's SDI, CUE, and respiration ratios embed carrying capacities and tree crowding limits directly into the gradient boosted feature space."),
        ("4. SOTA Calibrated Production Model", "Achieved 5-fold cross-validation score of 0.001393 (R² > 0.998), beating the challenge target by 86.1% with complete 185,130-row verified submission.")
    ]
    for i, (head, body) in enumerate(c_grid):
        gx = Inches(1.0) if i % 2 == 0 else Inches(6.8)
        gy = Inches(2.0) if i < 2 else Inches(4.0)
        card = add_card(s12, gx, gy, Inches(5.5), Inches(1.75), SLATE_BLUE, EMERALD)
        ctf = card.text_frame
        ctf.word_wrap = True
        ctf.margin_left = ctf.margin_right = ctf.margin_top = Inches(0.25)
        p = ctf.paragraphs[0]
        p.text = head
        p.font.name = "Arial"
        p.font.size = Pt(13)
        p.font.bold = True
        p.font.color.rgb = LIGHT_EMERALD
        p.space_after = Pt(6)
        p2 = ctf.add_paragraph()
        p2.text = body
        p2.font.name = "Arial"
        p2.font.size = Pt(10.5)
        p2.font.color.rgb = RGBColor(226, 232, 240)

    # Footer Thanks
    ft_box = s12.shapes.add_textbox(Inches(1.0), Inches(6.1), Inches(11.3), Inches(0.8))
    ft_tf = ft_box.text_frame
    p_ft = ft_tf.paragraphs[0]
    p_ft.text = "Thank you!  |  Sri Sivasubramaniya Nadar College of Engineering, Chennai  |  Questions & Discussion"
    p_ft.font.name = "Arial"
    p_ft.font.size = Pt(13)
    p_ft.font.bold = True
    p_ft.font.color.rgb = ACCENT_GOLD
    p_ft.alignment = PP_ALIGN.CENTER

    output_path = "presentation.pptx"
    prs.save(output_path)
    print(f"Presentation saved successfully to {output_path} ({len(prs.slides)} slides)")

if __name__ == "__main__":
    build_presentation()
