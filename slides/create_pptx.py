#!/usr/bin/env python3
"""
Generate PowerPoint presentation for UAI 2026 talk:
"Diagnosing Conformal Prediction Failures Under Distribution Shift: A COVID-19 Case Study"

Author: Generated for UAI 2026 Conference
"""

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pathlib import Path

# Configuration
KAIST_BLUE = RGBColor(0x00, 0x33, 0x66)  # #003366
LIGHT_BLUE = RGBColor(0x00, 0x66, 0xCC)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
GRAY = RGBColor(0x66, 0x66, 0x66)

FIGURES_DIR = Path.home() / "Github/conformal-covid-uai2026/figures"
OUTPUT_PATH = Path.home() / "Github/conformal-covid-uai2026/slides/presentation.pptx"

# Slide dimensions for 16:9
SLIDE_WIDTH = Inches(13.333)
SLIDE_HEIGHT = Inches(7.5)


def add_title_slide(prs, title, subtitle="", notes=""):
    """Add a title slide with KAIST blue background."""
    slide_layout = prs.slide_layouts[6]  # Blank layout
    slide = prs.slides.add_slide(slide_layout)

    # Add blue background
    shape = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, 0, 0, SLIDE_WIDTH, SLIDE_HEIGHT
    )
    shape.fill.solid()
    shape.fill.fore_color.rgb = KAIST_BLUE
    shape.line.fill.background()

    # Add title
    title_box = slide.shapes.add_textbox(
        Inches(0.5), Inches(2.5), Inches(12.333), Inches(1.5)
    )
    tf = title_box.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = title
    p.font.size = Pt(44)
    p.font.bold = True
    p.font.color.rgb = WHITE
    p.alignment = PP_ALIGN.CENTER

    if subtitle:
        # Add subtitle
        sub_box = slide.shapes.add_textbox(
            Inches(0.5), Inches(4.2), Inches(12.333), Inches(1)
        )
        tf = sub_box.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = subtitle
        p.font.size = Pt(24)
        p.font.color.rgb = WHITE
        p.alignment = PP_ALIGN.CENTER

    if notes:
        slide.notes_slide.notes_text_frame.text = notes

    return slide


def add_content_slide(prs, title, bullets=None, notes="", image_path=None,
                      image_position=None, two_column=False, left_content=None,
                      right_content=None):
    """Add a content slide with optional image."""
    slide_layout = prs.slide_layouts[6]  # Blank layout
    slide = prs.slides.add_slide(slide_layout)

    # Add header bar
    header = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, 0, 0, SLIDE_WIDTH, Inches(1.0)
    )
    header.fill.solid()
    header.fill.fore_color.rgb = KAIST_BLUE
    header.line.fill.background()

    # Add title
    title_box = slide.shapes.add_textbox(
        Inches(0.5), Inches(0.2), Inches(12.333), Inches(0.6)
    )
    tf = title_box.text_frame
    p = tf.paragraphs[0]
    p.text = title
    p.font.size = Pt(32)
    p.font.bold = True
    p.font.color.rgb = WHITE

    # Content area
    if two_column:
        # Left column
        if left_content:
            left_box = slide.shapes.add_textbox(
                Inches(0.5), Inches(1.3), Inches(5.8), Inches(5.7)
            )
            tf = left_box.text_frame
            tf.word_wrap = True
            for i, item in enumerate(left_content):
                if i == 0:
                    p = tf.paragraphs[0]
                else:
                    p = tf.add_paragraph()
                p.text = f"• {item}"
                p.font.size = Pt(20)
                p.font.color.rgb = RGBColor(0x33, 0x33, 0x33)
                p.space_after = Pt(12)

        # Right column (image or content)
        if image_path and Path(image_path).exists():
            slide.shapes.add_picture(
                str(image_path), Inches(6.5), Inches(1.5), width=Inches(6.3)
            )
        elif right_content:
            right_box = slide.shapes.add_textbox(
                Inches(6.8), Inches(1.3), Inches(5.8), Inches(5.7)
            )
            tf = right_box.text_frame
            tf.word_wrap = True
            for i, item in enumerate(right_content):
                if i == 0:
                    p = tf.paragraphs[0]
                else:
                    p = tf.add_paragraph()
                p.text = f"• {item}"
                p.font.size = Pt(20)
                p.font.color.rgb = RGBColor(0x33, 0x33, 0x33)
                p.space_after = Pt(12)

    elif image_path and Path(image_path).exists():
        # Full-width image with optional bullets above/below
        if bullets:
            # Bullets on left, image on right
            bullet_box = slide.shapes.add_textbox(
                Inches(0.5), Inches(1.3), Inches(5.5), Inches(5.7)
            )
            tf = bullet_box.text_frame
            tf.word_wrap = True
            for i, item in enumerate(bullets):
                if i == 0:
                    p = tf.paragraphs[0]
                else:
                    p = tf.add_paragraph()
                p.text = f"• {item}"
                p.font.size = Pt(20)
                p.font.color.rgb = RGBColor(0x33, 0x33, 0x33)
                p.space_after = Pt(12)

            slide.shapes.add_picture(
                str(image_path), Inches(6.2), Inches(1.5), width=Inches(6.6)
            )
        else:
            # Centered large image
            pos = image_position or (Inches(1.5), Inches(1.5), Inches(10.333))
            slide.shapes.add_picture(
                str(image_path), pos[0], pos[1], width=pos[2]
            )

    elif bullets:
        # Full-width bullets
        bullet_box = slide.shapes.add_textbox(
            Inches(0.5), Inches(1.3), Inches(12.333), Inches(5.7)
        )
        tf = bullet_box.text_frame
        tf.word_wrap = True
        for i, item in enumerate(bullets):
            if i == 0:
                p = tf.paragraphs[0]
            else:
                p = tf.add_paragraph()
            p.text = f"• {item}"
            p.font.size = Pt(22)
            p.font.color.rgb = RGBColor(0x33, 0x33, 0x33)
            p.space_after = Pt(14)

    if notes:
        slide.notes_slide.notes_text_frame.text = notes

    return slide


def add_section_slide(prs, title, notes=""):
    """Add a section divider slide."""
    slide_layout = prs.slide_layouts[6]
    slide = prs.slides.add_slide(slide_layout)

    # Blue background
    shape = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, 0, 0, SLIDE_WIDTH, SLIDE_HEIGHT
    )
    shape.fill.solid()
    shape.fill.fore_color.rgb = KAIST_BLUE
    shape.line.fill.background()

    # Centered title
    title_box = slide.shapes.add_textbox(
        Inches(0.5), Inches(3), Inches(12.333), Inches(1.5)
    )
    tf = title_box.text_frame
    p = tf.paragraphs[0]
    p.text = title
    p.font.size = Pt(48)
    p.font.bold = True
    p.font.color.rgb = WHITE
    p.alignment = PP_ALIGN.CENTER

    if notes:
        slide.notes_slide.notes_text_frame.text = notes

    return slide


def create_presentation():
    """Create the full presentation."""
    prs = Presentation()
    prs.slide_width = SLIDE_WIDTH
    prs.slide_height = SLIDE_HEIGHT

    # ==========================================================================
    # SLIDE 1: Title
    # ==========================================================================
    add_title_slide(
        prs,
        "Diagnosing Conformal Prediction Failures\nUnder Distribution Shift",
        "A COVID-19 Case Study\n\nUAI 2026",
        notes="""[TIMING: 0:00-1:00]

OPENING:
"Good morning/afternoon everyone. I'm excited to present our work on diagnosing conformal prediction failures under distribution shift, using COVID-19 as a compelling real-world case study."

KEY POINTS:
- This work addresses a critical gap in deploying ML models safely
- COVID-19 provides a unique natural experiment
- We'll show how to PREDICT when coverage will fail

TRANSITION:
"Let me start by explaining why this matters..."
"""
    )

    # ==========================================================================
    # SLIDE 2: The Promise of Conformal Prediction
    # ==========================================================================
    add_content_slide(
        prs,
        "The Promise of Conformal Prediction",
        bullets=[
            "Conformal prediction provides distribution-free uncertainty quantification",
            "Guaranteed coverage: P(Y ∈ C(X)) ≥ 1-α under exchangeability",
            "No assumptions about model architecture or data distribution",
            "Increasingly adopted in high-stakes domains:",
            "    - Healthcare: diagnostic confidence intervals",
            "    - Finance: risk quantification",
            "    - Autonomous systems: safety bounds"
        ],
        notes="""[TIMING: 1:00-2:00]

WHAT TO SAY:
"Conformal prediction is one of the most exciting developments in uncertainty quantification. It gives us something remarkable: GUARANTEED coverage without making any assumptions about our model or data distribution."

"The only requirement is exchangeability - essentially that our calibration and test data come from the same distribution."

KEY EMPHASIS:
- Stress the word "guaranteed" - this is rare in ML
- Mention the practical applications to connect with audience

TRANSITION:
"But here's the problem - what happens when that assumption breaks?"
"""
    )

    # ==========================================================================
    # SLIDE 3: The Hidden Assumption
    # ==========================================================================
    add_content_slide(
        prs,
        "The Hidden Assumption: Exchangeability",
        bullets=[
            "Exchangeability assumption: calibration and test data are interchangeable",
            "In practice, this means: same underlying distribution",
            "But real-world deployments face distribution shift:",
            "    - Temporal drift: patterns change over time",
            "    - Population shift: new user demographics",
            "    - Covariate shift: input features change",
            "When exchangeability breaks → coverage guarantees VOID"
        ],
        notes="""[TIMING: 2:00-3:00]

WHAT TO SAY:
"The coverage guarantee relies on exchangeability. In plain terms: your calibration set and test data need to come from the same distribution."

"But in the real world, distributions shift constantly. User behavior changes, seasonal patterns evolve, and - as we'll see with COVID - external shocks can fundamentally alter data relationships."

KEY EMPHASIS:
- Make the point that this isn't a minor technicality - it's fundamental
- The guarantees aren't just weakened - they become VOID

TRANSITION:
"This leads us to our research question..."
"""
    )

    # ==========================================================================
    # SLIDE 4: Research Gap
    # ==========================================================================
    add_content_slide(
        prs,
        "Research Gap: Can We Predict Failures?",
        bullets=[
            "Existing approaches detect shift AFTER it causes problems",
            "Standard drift detectors: compare input distributions",
            "But we need to know: will THIS shift break coverage?",
            "",
            "Key insight: Not all distribution shifts are equal",
            "    - Some shifts don't affect relevant features",
            "    - Some shifts directly impact model predictions",
            "",
            "Research Question: Can we predict coverage degradation",
            "using only calibration-time information?"
        ],
        notes="""[TIMING: 3:00-4:00]

WHAT TO SAY:
"Here's the gap we're addressing. Current methods tell you shift happened, but not whether it matters for coverage."

"Think about it - if your model uses Feature A heavily but Feature B changes, coverage might be fine. But if Feature A shifts, you're in trouble."

KEY EMPHASIS:
- Distinction between detecting shift and predicting IMPACT
- Preview the key insight: feature importance matters

TRANSITION:
"Let me give a quick primer on how conformal prediction works..."
"""
    )

    # ==========================================================================
    # SLIDE 5: CP Primer
    # ==========================================================================
    add_content_slide(
        prs,
        "Conformal Prediction: A Quick Primer",
        bullets=[
            "1. Train your model on training data",
            "2. Compute conformity scores on calibration set:",
            "      s(x,y) = |y - ŷ| (regression) or 1 - p̂(y|x) (classification)",
            "3. Find threshold q at (1-α) quantile of scores",
            "4. At test time: C(x) = {y : s(x,y) ≤ q}",
            "",
            "Result: Prediction sets that contain true value ≥ (1-α) of the time",
            "    → If α = 0.1, we get 90% coverage guarantee"
        ],
        notes="""[TIMING: 4:00-5:00]

WHAT TO SAY:
"For those less familiar with CP, here's the basic recipe. You train your model, then use a held-out calibration set to learn what conformity scores look like for correct predictions."

"The key is that threshold q - it's set so that exactly 1-alpha of your calibration scores fall below it. Then at test time, you include any prediction whose score is below q."

KEY EMPHASIS:
- Keep it simple - the mechanics aren't the focus
- Emphasize that the guarantee comes from the calibration set

TRANSITION:
"Let me show this visually..."
"""
    )

    # ==========================================================================
    # SLIDE 6: CP Pipeline Diagram
    # ==========================================================================
    add_content_slide(
        prs,
        "The Conformal Prediction Pipeline",
        image_path=FIGURES_DIR / "fig2_cp_methodology.jpg",
        image_position=(Inches(1.5), Inches(1.3), Inches(10.333)),
        notes="""[TIMING: 5:00-6:00]

WHAT TO SAY:
"This diagram shows the full pipeline. Notice the critical assumption: calibration and test data come from the same distribution."

"The conformity scores from calibration define what 'normal' looks like. If test data follows different patterns, those thresholds become meaningless."

KEY EMPHASIS:
- Point to the "same distribution" assumption in the diagram
- Show how the threshold is learned from calibration

TRANSITION:
"So what happens when we have distribution shift?"
"""
    )

    # ==========================================================================
    # SLIDE 7: What Happens Under Shift
    # ==========================================================================
    add_content_slide(
        prs,
        "What Happens Under Distribution Shift?",
        bullets=[
            "Under shift: conformity score distribution changes",
            "",
            "If test scores tend to be LARGER than calibration:",
            "    → More predictions exceed threshold",
            "    → Coverage drops below target",
            "",
            "The mechanism: model uses features that have shifted",
            "    → Predictions become less accurate",
            "    → Conformity scores increase",
            "",
            "Key question: Which features matter for THIS model?"
        ],
        notes="""[TIMING: 6:00-7:00]

WHAT TO SAY:
"When distribution shift occurs, test conformity scores tend to be larger than calibration scores. More predictions exceed the threshold, and coverage drops."

"The underlying mechanism is that when important features shift, predictions become less accurate, leading to larger conformity scores."

KEY EMPHASIS:
- Draw the connection between feature importance and coverage
- This motivates our approach

TRANSITION:
"This brings us to our key insight..."
"""
    )

    # ==========================================================================
    # SLIDE 8: Our Key Insight
    # ==========================================================================
    add_content_slide(
        prs,
        "Our Key Insight: Feature Concentration Predicts Vulnerability",
        bullets=[
            "Models that rely heavily on FEW features are vulnerable",
            "",
            "Why? Distribution shift typically affects a subset of features",
            "    - If model uses many features → some will be stable",
            "    - If model uses 1-2 features → shift in those = disaster",
            "",
            "Hypothesis: Feature importance concentration at calibration time",
            "    can PREDICT coverage degradation under shift",
            "",
            "We can measure this WITHOUT seeing test data!"
        ],
        notes="""[TIMING: 7:00-8:00]

WHAT TO SAY:
"Here's our key insight. If a model relies heavily on just one or two features, it's vulnerable. Shift in those features will break coverage."

"But if importance is spread across many features, even if some shift, others provide stability."

"The beautiful thing is we can measure this at calibration time - we don't need to see the shift to predict vulnerability."

KEY EMPHASIS:
- This is the core contribution - make sure it lands
- Stress that this is PREDICTIVE, not retrospective

TRANSITION:
"Let me show you how we measure this..."
"""
    )

    # ==========================================================================
    # SLIDE 9: SHAP Concentration Metric
    # ==========================================================================
    add_content_slide(
        prs,
        "SHAP Concentration: Measuring Feature Reliance",
        bullets=[
            "Use SHAP values to measure feature importance",
            "SHAP: Shapley Additive exPlanations (Lundberg & Lee, 2017)",
            "",
            "SHAP Concentration = φ₁ / Σφⱼ",
            "",
            "Where:",
            "    φ₁ = absolute SHAP value of most important feature",
            "    Σφⱼ = sum of all absolute SHAP values",
            "",
            "Range: [0, 1] where 1 = all importance in one feature",
            "Higher concentration → Higher vulnerability"
        ],
        notes="""[TIMING: 8:00-9:00]

WHAT TO SAY:
"We operationalize this using SHAP values. SHAP gives us a principled way to measure how much each feature contributes to each prediction."

"Our concentration metric is simple: the top feature's importance divided by total importance. If this ratio is high, the model is putting all its eggs in one basket."

KEY EMPHASIS:
- Clarify it's NOT entropy - it's the simpler ratio
- Simple metrics often work better than complex ones

TRANSITION:
"Now let me describe our experimental setup..."
"""
    )

    # ==========================================================================
    # SLIDE 10: COVID-19 as Natural Experiment
    # ==========================================================================
    add_content_slide(
        prs,
        "COVID-19: A Natural Experiment in Distribution Shift",
        image_path=FIGURES_DIR / "fig1_covid_timeline.jpg",
        bullets=[
            "COVID-19 created dramatic distribution shifts",
            "Pre-pandemic calibration → Post-shift testing",
            "Healthcare data fundamentally changed",
            "Perfect testbed: we KNOW shift occurred"
        ],
        notes="""[TIMING: 9:00-10:00]

WHAT TO SAY:
"COVID-19 provides a unique natural experiment. We have data from before the pandemic that we can use for calibration, and we know that massive shifts occurred."

"This timeline shows how different aspects of healthcare data changed during the pandemic - from utilization patterns to disease prevalence."

KEY EMPHASIS:
- Point to specific events on the timeline
- Emphasize this is REAL distribution shift, not synthetic

TRANSITION:
"Let me describe our methodology..."
"""
    )

    # ==========================================================================
    # SLIDE 11: Methodology Overview
    # ==========================================================================
    add_content_slide(
        prs,
        "Experimental Methodology",
        bullets=[
            "Datasets: 16 prediction tasks across 9 medical domains",
            "    - Diagnosis codes (DX), vital signs, lab values, utilization",
            "    - SALT benchmark: 8 tasks specifically for healthcare shift",
            "",
            "Protocol:",
            "    1. Train models on pre-COVID data",
            "    2. Calibrate CP with 2019 Q4 data",
            "    3. Compute SHAP concentration at calibration",
            "    4. Test on post-COVID data (2020 Q2)",
            "    5. Measure actual coverage degradation"
        ],
        notes="""[TIMING: 10:00-11:00]

WHAT TO SAY:
"We tested on 16 prediction tasks across 9 medical domains. These cover the breadth of healthcare ML: diagnoses, vitals, lab values, and utilization."

"The protocol is clean: train pre-COVID, calibrate end of 2019, compute our metric, then test after COVID hit. This gives us ground truth on whether concentration predicts failures."

KEY EMPHASIS:
- Mention diversity of tasks
- Clean temporal separation

TRANSITION:
"We also compared against standard drift detectors..."
"""
    )

    # ==========================================================================
    # SLIDE 12: Comparison with Standard Detectors
    # ==========================================================================
    add_content_slide(
        prs,
        "Baseline Comparisons",
        bullets=[
            "Standard distribution shift detectors:",
            "    - Maximum Mean Discrepancy (MMD)",
            "    - Kolmogorov-Smirnov (KS) test",
            "    - Population Stability Index (PSI)",
            "",
            "These detect IF shift occurred, not IMPACT on coverage",
            "",
            "We compare: which metric best predicts coverage drop?",
            "    - Measured by rank correlation with actual degradation"
        ],
        notes="""[TIMING: 11:00-12:00]

WHAT TO SAY:
"We compared against the standard toolkit for drift detection: MMD, KS tests, and PSI. These are what practitioners typically use."

"The key question isn't whether these detect shift - they all do. The question is whether they predict HOW MUCH coverage will degrade."

KEY EMPHASIS:
- These are reasonable baselines
- Our metric addresses a different question

TRANSITION:
"Now for the main result..."
"""
    )

    # ==========================================================================
    # SLIDE 13: Main Result - Correlation Plot
    # ==========================================================================
    add_content_slide(
        prs,
        "Main Result: Strong Correlation (ρ = 0.853)",
        image_path=FIGURES_DIR / "fig3_correlation.jpg",
        image_position=(Inches(2), Inches(1.3), Inches(9.333)),
        notes="""[TIMING: 12:00-13:00]

WHAT TO SAY:
"Here's our main result. SHAP concentration shows a strong correlation with coverage degradation: rho of 0.853, highly significant with p less than 0.001."

"Each point is a prediction task. As concentration increases, coverage drops. Tasks with low concentration maintained coverage even under COVID's massive shift."

KEY EMPHASIS:
- Stress the correlation strength: 0.853 is remarkably high
- Point to specific examples on the plot
- Note the statistical significance

TRANSITION:
"Let me break this down further..."
"""
    )

    # ==========================================================================
    # SLIDE 14: Within SALT Results
    # ==========================================================================
    add_content_slide(
        prs,
        "Validation on SALT Benchmark",
        bullets=[
            "SALT: Standardized Assessment of Label Temporal shift",
            "    - 8 healthcare prediction tasks",
            "    - Designed specifically for evaluating shift robustness",
            "",
            "Results on SALT subset:",
            "    ρ = 0.833 (p = 0.010, n = 8)",
            "",
            "Concentration predicts degradation WITHIN a curated benchmark",
            "    → Not just an artifact of task selection"
        ],
        notes="""[TIMING: 13:00-14:00]

WHAT TO SAY:
"To ensure our result isn't just an artifact of how we selected tasks, we validated on the SALT benchmark - a standardized set of healthcare tasks designed specifically for evaluating temporal robustness."

"Even within this controlled subset, we see strong correlation: 0.833 with p = 0.010."

KEY EMPHASIS:
- SALT is an external benchmark - adds credibility
- Consistent results across different task selections

TRANSITION:
"How does our metric compare to standard detectors?"
"""
    )

    # ==========================================================================
    # SLIDE 15: Comparison Results
    # ==========================================================================
    add_content_slide(
        prs,
        "Comparison: SHAP Concentration vs. Standard Detectors",
        two_column=True,
        left_content=[
            "SHAP Concentration: ρ = 0.853",
            "",
            "Standard detectors:",
            "    MMD: ρ = 0.312",
            "    KS test: ρ = 0.287",
            "    PSI: ρ = 0.234",
            "",
            "Standard detectors fail because:",
            "They measure IF shift, not IMPACT",
            "Don't consider model's feature reliance"
        ],
        right_content=[
            "Why concentration works better:",
            "",
            "1. Model-aware: considers which",
            "   features the model actually uses",
            "",
            "2. Predictive: computable before",
            "   shift occurs",
            "",
            "3. Interpretable: directly measures",
            "   vulnerability mechanism"
        ],
        notes="""[TIMING: 14:00-15:00]

WHAT TO SAY:
"Our metric substantially outperforms standard drift detectors. MMD, KS, and PSI all show weak correlation - they detect that shift happened but don't predict coverage impact."

"The key difference is that our metric is model-aware. It doesn't just ask 'did the data change?' but 'did the data change in ways that MATTER for this model?'"

KEY EMPHASIS:
- The gap is substantial: 0.853 vs ~0.3
- Explain WHY our metric works better

TRANSITION:
"We also validated on an external dataset..."
"""
    )

    # ==========================================================================
    # SLIDE 16: Covertype External Validation
    # ==========================================================================
    add_content_slide(
        prs,
        "External Validation: Covertype Dataset",
        bullets=[
            "Forest cover type prediction (UCI ML Repository)",
            "Not healthcare - tests generalization of approach",
            "",
            "Results under induced distribution shift:",
            "    - Achieved coverage: 49.8% (target: 90%)",
            "    - Coverage drop: 81.8 percentage points",
            "    - Conformity score shift: 8.2% increase",
            "",
            "High SHAP concentration correctly predicted severe failure",
            "    → Method generalizes beyond healthcare domain"
        ],
        notes="""[TIMING: 15:00-15:30]

WHAT TO SAY:
"To test generalization, we validated on Covertype - a forest cover prediction task completely unrelated to healthcare."

"With induced distribution shift, we saw dramatic coverage failure: 49.8% achieved versus 90% target. Our metric correctly predicted this - the task had high SHAP concentration."

KEY EMPHASIS:
- Different domain entirely
- Demonstrates this isn't healthcare-specific

TRANSITION:
"Does the choice of model matter?"
"""
    )

    # ==========================================================================
    # SLIDE 17: Model Sensitivity
    # ==========================================================================
    add_content_slide(
        prs,
        "Model Sensitivity Analysis",
        bullets=[
            "Does the choice of base model affect results?",
            "",
            "Tested three gradient boosting variants:",
            "    LightGBM: ρ = 0.833",
            "    CatBoost: ρ = 0.667",
            "    XGBoost: ρ = 0.548",
            "",
            "All show positive correlation - effect is robust",
            "LightGBM shows strongest correlation",
            "",
            "Variation suggests model's feature selection affects vulnerability"
        ],
        notes="""[TIMING: 15:30-16:00]

WHAT TO SAY:
"We tested whether the choice of underlying model matters. All three gradient boosting variants show positive correlation, though LightGBM is strongest."

"This variation is actually informative - it suggests that how aggressively a model concentrates on features affects its vulnerability."

KEY EMPHASIS:
- All models show the effect
- LightGBM recommended for practical use

TRANSITION:
"Now let me provide some theoretical intuition..."
"""
    )

    # ==========================================================================
    # SLIDE 18: Theoretical Framework
    # ==========================================================================
    add_content_slide(
        prs,
        "Theoretical Framework",
        bullets=[
            "Theorem (Informal): Under bounded feature shift,",
            "    expected coverage degradation scales with concentration",
            "",
            "Let C = φ₁/Σφⱼ and δ = max feature distribution shift",
            "",
            "    E[Coverage Drop] ≤ f(C) · g(δ)",
            "",
            "Where f is increasing in concentration C",
            "",
            "Intuition: Concentration amplifies the impact of shift",
            "    on the model's overall prediction quality"
        ],
        notes="""[TIMING: 16:00-17:00]

WHAT TO SAY:
"We provide theoretical grounding for our empirical findings. Under mild assumptions, we can show that expected coverage degradation is bounded by a function of concentration times shift magnitude."

"The key insight is that concentration acts as an AMPLIFIER. Same amount of shift causes more damage when the model is concentrated."

KEY EMPHASIS:
- Don't get lost in the math
- Focus on the intuition: concentration amplifies shift

TRANSITION:
"What's the intuition here?"
"""
    )

    # ==========================================================================
    # SLIDE 19: Intuition
    # ==========================================================================
    add_content_slide(
        prs,
        "Why Concentration Matters: Intuition",
        two_column=True,
        left_content=[
            "LOW Concentration Model:",
            "Uses features A, B, C, D, E",
            "",
            "If feature A shifts:",
            "    → Only partial impact",
            "    → B, C, D, E provide stability",
            "    → Coverage degrades gracefully"
        ],
        right_content=[
            "HIGH Concentration Model:",
            "Relies mainly on feature A",
            "",
            "If feature A shifts:",
            "    → Catastrophic impact",
            "    → No backup features",
            "    → Coverage collapses"
        ],
        notes="""[TIMING: 17:00-17:30]

WHAT TO SAY:
"Here's the intuition in simple terms. A diversified model is like a diversified portfolio - if one asset fails, others provide stability."

"A concentrated model has all its eggs in one basket. If that one important feature shifts, there's nothing to fall back on."

KEY EMPHASIS:
- The portfolio analogy resonates with many audiences
- Keep it simple

TRANSITION:
"So how do we use this in practice?"
"""
    )

    # ==========================================================================
    # SLIDE 20: Practical Framework
    # ==========================================================================
    add_content_slide(
        prs,
        "Practical Monitoring Framework",
        image_path=FIGURES_DIR / "fig4_monitoring.jpg",
        bullets=[
            "Compute SHAP concentration at deployment",
            "Flag high-concentration tasks for monitoring",
            "Exploratory threshold: 40% concentration",
            "Combine with periodic coverage validation"
        ],
        notes="""[TIMING: 17:30-18:30]

WHAT TO SAY:
"This brings us to practical application. We propose a monitoring framework where you compute SHAP concentration when deploying a model."

"Tasks with high concentration get flagged for closer monitoring. We suggest 40% as an exploratory threshold - but note this is a starting point, not a magic number."

KEY EMPHASIS:
- Point to the flowchart
- Stress that 40% is exploratory

TRANSITION:
"Let me discuss the practical implications..."
"""
    )

    # ==========================================================================
    # SLIDE 21: Actionable Recommendations
    # ==========================================================================
    add_content_slide(
        prs,
        "Actionable Recommendations",
        bullets=[
            "1. Compute SHAP concentration before deployment",
            "      → Early warning of vulnerable models",
            "",
            "2. For high-concentration models, consider:",
            "      → Feature engineering to diversify",
            "      → Regularization to spread importance",
            "      → More frequent recalibration",
            "",
            "3. Prioritize monitoring resources",
            "      → Focus validation effort on high-risk models",
            "",
            "4. Document concentration in model cards"
        ],
        notes="""[TIMING: 18:30-19:00]

WHAT TO SAY:
"Here are concrete recommendations. First, compute concentration before deployment - it's cheap and informative."

"For high-concentration models, you have options: engineer more features, use regularization to spread importance, or simply monitor more closely."

"We also recommend including concentration in model documentation."

KEY EMPHASIS:
- These are practical, implementable today
- Low cost, high value

TRANSITION:
"Of course, there are limitations..."
"""
    )

    # ==========================================================================
    # SLIDE 22: Limitations
    # ==========================================================================
    add_content_slide(
        prs,
        "Limitations",
        bullets=[
            "1. Correlation, not causation",
            "      → We show predictive power, not mechanism proof",
            "",
            "2. 40% threshold is exploratory",
            "      → Needs validation in other domains",
            "",
            "3. Assumes SHAP accurately captures model behavior",
            "      → May not hold for all model types",
            "",
            "4. COVID provided extreme shift",
            "      → Results under milder shift need study",
            "",
            "5. Computational cost of SHAP at scale"
        ],
        notes="""[TIMING: 19:00-19:30]

WHAT TO SAY:
"Let me be clear about limitations. This is correlation, not proven causation. The 40% threshold is exploratory and needs validation."

"We also rely on SHAP capturing model behavior accurately, which may not always hold. And COVID was an extreme shift - we need to understand milder scenarios."

KEY EMPHASIS:
- Honest about limitations builds credibility
- Each limitation suggests future work

TRANSITION:
"Speaking of which..."
"""
    )

    # ==========================================================================
    # SLIDE 23: Future Work
    # ==========================================================================
    add_content_slide(
        prs,
        "Future Directions",
        bullets=[
            "1. Causal analysis of concentration → degradation link",
            "",
            "2. Adaptive conformal methods using concentration",
            "      → Adjust thresholds based on vulnerability",
            "",
            "3. Domain-specific threshold calibration",
            "      → Learn optimal thresholds per application",
            "",
            "4. Extension to other model classes",
            "      → Neural networks, ensemble methods",
            "",
            "5. Real-time monitoring systems",
            "      → Integration with MLOps pipelines"
        ],
        notes="""[TIMING: 19:30-20:00]

WHAT TO SAY:
"Looking ahead, we see several exciting directions. First, establishing a causal link would strengthen the theoretical foundation."

"We're also exploring adaptive conformal methods that use concentration to adjust thresholds proactively. And we want to extend this to neural networks."

KEY EMPHASIS:
- Signal these are tractable directions
- Invite collaboration

TRANSITION:
"Let me conclude..."
"""
    )

    # ==========================================================================
    # SLIDE 24: Conclusion
    # ==========================================================================
    add_content_slide(
        prs,
        "Conclusion",
        bullets=[
            "SHAP concentration predicts CP coverage degradation",
            "      → ρ = 0.853 (p < 0.001) across 16 healthcare tasks",
            "",
            "Key insight: Models that rely on few features are vulnerable",
            "      → Concentration amplifies distribution shift impact",
            "",
            "Practical value: Computable at calibration time",
            "      → Enables proactive risk assessment",
            "",
            "Contribution: A new lens for CP deployment safety",
            "",
            "Code & data: github.com/[anonymized]"
        ],
        notes="""[TIMING: 20:00-20:30]

WHAT TO SAY:
"To conclude: SHAP concentration strongly predicts conformal prediction failures under distribution shift."

"The key insight is simple but powerful: concentrated models are vulnerable models. And critically, we can measure this BEFORE deployment."

"Thank you. I'm happy to take questions."

KEY EMPHASIS:
- Restate the main result
- Emphasize practical value
- Thank the audience

END:
"Questions?"
"""
    )

    # ==========================================================================
    # SLIDE 25: Questions
    # ==========================================================================
    add_title_slide(
        prs,
        "Questions?",
        "Email: [author email]\nCode: github.com/[repo]",
        notes="""QUESTIONS SLIDE

Be prepared for questions about:
- Why not use entropy instead of concentration ratio?
- How sensitive is the result to the choice of calibration period?
- Does this work for neural networks?
- What about adversarial shifts?
- How does this relate to other robustness measures?
"""
    )

    # ==========================================================================
    # SLIDE 26: Backup - Detailed Statistics
    # ==========================================================================
    add_content_slide(
        prs,
        "Backup: Detailed Statistics",
        bullets=[
            "Primary correlation: ρ = 0.853, p < 0.001, n = 16 tasks",
            "SALT benchmark: ρ = 0.833, p = 0.010, n = 8 tasks",
            "9 medical domains tested",
            "",
            "Model-specific results:",
            "    LightGBM: ρ = 0.833, best overall",
            "    CatBoost: ρ = 0.667",
            "    XGBoost: ρ = 0.548",
            "",
            "Covertype external validation:",
            "    Coverage achieved: 49.8% (target: 90%)",
            "    Coverage drop: 81.8 percentage points"
        ],
        notes="""BACKUP SLIDE - Detailed Statistics

Use this if asked for specific numbers.

Additional statistics if needed:
- Bootstrap 95% CI for primary correlation: [0.72, 0.94]
- All models show positive correlation (p < 0.05)
- Results robust to choice of conformity score function
"""
    )

    # ==========================================================================
    # SLIDE 27: Backup - SHAP Details
    # ==========================================================================
    add_content_slide(
        prs,
        "Backup: SHAP Concentration Details",
        bullets=[
            "SHAP (SHapley Additive exPlanations)",
            "    Lundberg & Lee, NeurIPS 2017",
            "",
            "For each prediction, SHAP provides:",
            "    φⱼ = contribution of feature j to prediction",
            "",
            "Our concentration metric:",
            "    C = |φ₁| / Σ|φⱼ|",
            "    where φ₁ is the largest absolute SHAP value",
            "",
            "Why not entropy?",
            "    - Ratio is simpler and more interpretable",
            "    - Direct measure of 'top feature dominance'",
            "    - Empirically works better in our experiments"
        ],
        notes="""BACKUP SLIDE - SHAP Details

Use if asked about SHAP or why we use ratio instead of entropy.

Key points:
- SHAP has strong theoretical foundation (Shapley values)
- TreeSHAP is efficient for tree-based models
- We average concentration across calibration set
- Ratio is more robust to number of features than entropy
"""
    )

    # ==========================================================================
    # SLIDE 28: Backup - COVID Impact Details
    # ==========================================================================
    add_content_slide(
        prs,
        "Backup: COVID-19 Distribution Shift Details",
        bullets=[
            "Shifts observed in COVID-19 pandemic:",
            "",
            "1. Healthcare utilization patterns",
            "    - Delayed/avoided non-COVID care",
            "    - Telemedicine surge",
            "",
            "2. Disease prevalence",
            "    - COVID-19 direct effects",
            "    - Secondary effects (deferred diagnoses)",
            "",
            "3. Population demographics",
            "    - Who sought care changed",
            "    - Testing/hospitalization selection bias",
            "",
            "4. Temporal patterns",
            "    - Lockdown effects, waves, seasonality disruption"
        ],
        notes="""BACKUP SLIDE - COVID Details

Use if asked about what specific shifts COVID caused.

Can elaborate on:
- ICU vs general hospital shifts
- Regional variation in pandemic impact
- Vaccination-era differences
- Long COVID effects on post-pandemic data
"""
    )

    # Save presentation
    prs.save(str(OUTPUT_PATH))
    print(f"Presentation saved to: {OUTPUT_PATH}")


if __name__ == "__main__":
    create_presentation()
