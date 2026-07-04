#!/usr/bin/env python3
"""Convert PDF slides to PPTX with speaker notes, preserving exact PDF styling."""

import subprocess
import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RgbColor
from pptx.enum.text import PP_ALIGN

# Paths
SLIDES_DIR = "/Users/i767700/Github/conformal-covid-uai2026/slides"
PDF_PATH = os.path.join(SLIDES_DIR, "main.pdf")
OUTPUT_PATH = os.path.join(SLIDES_DIR, "presentation_pdf_style.pptx")
IMAGES_DIR = os.path.join(SLIDES_DIR, "pdf_pages")

# Create images directory
os.makedirs(IMAGES_DIR, exist_ok=True)

# Convert PDF to images using sips (macOS built-in)
print("Converting PDF to images...")

# Use pdftoppm if available, otherwise use sips
try:
    # Check if pdftoppm is available
    result = subprocess.run(["which", "pdftoppm"], capture_output=True, text=True)
    if result.returncode == 0:
        subprocess.run([
            "pdftoppm", "-jpeg", "-r", "300", PDF_PATH,
            os.path.join(IMAGES_DIR, "slide")
        ], check=True)
        # pdftoppm creates slide-01.jpg, slide-02.jpg, etc.
        image_pattern = "slide-{:02d}.jpg"
    else:
        raise FileNotFoundError("pdftoppm not found")
except:
    # Fall back to using Preview via AppleScript or ImageMagick
    print("Using ImageMagick convert...")
    subprocess.run([
        "convert", "-density", "300", PDF_PATH,
        os.path.join(IMAGES_DIR, "slide-%02d.jpg")
    ], check=True)
    image_pattern = "slide-{:02d}.jpg"

# Count number of pages
page_files = sorted([f for f in os.listdir(IMAGES_DIR) if f.startswith("slide") and f.endswith(".jpg")])
num_pages = len(page_files)
print(f"Found {num_pages} slides")

# Speaker notes for each slide (based on the LaTeX content)
SPEAKER_NOTES = {
    1: """[TITLE - 30 seconds]
Welcome everyone. I'm Chorok Lee from KAIST.
Today I'll present our work on diagnosing conformal prediction failures under distribution shift, using COVID-19 as a natural case study.
This is joint work accepted at UAI 2026.""",

    2: """[MOTIVATION - 1 minute]
Let me start with what makes conformal prediction attractive.
It provides distribution-free coverage guarantees - meaning we can be confident the true label is in our prediction set at least 90% of the time.
This works with ANY base model, and gives exact finite-sample validity.
But there's a catch...""",

    3: """[HIDDEN ASSUMPTION - 1 minute]
The catch is the exchangeability assumption.
Conformal prediction requires that calibration and test data come from the same distribution.
In real deployments, distribution shift is INEVITABLE - temporal shifts like COVID, geographic shifts, demographic changes.
So the question becomes: what happens when this assumption breaks?""",

    4: """[RESEARCH GAP - 1 minute]
Standard shift detectors like MMD, C2ST, and PSI can detect THAT shift occurred.
But they show rho less than 0.2 correlation with coverage failure.
They cannot distinguish between robust outcomes where coverage is maintained, and catastrophic failures where coverage drops to 50% or below.
Our research question: can we PREDICT which models will fail BEFORE we observe test data?""",

    5: """[CP PRIMER - 1.5 minutes]
Quick primer on conformal prediction for those less familiar.
We use Adaptive Prediction Sets - APS.
Step 1: Define a nonconformity score - for APS, this is the sum of probabilities of classes ranked above the true class.
Step 2: Calibrate a threshold from our calibration set.
Step 3: Form prediction sets by including classes until we exceed the threshold.
Step 4: This gives us the coverage guarantee - under exchangeability.
We use alpha=0.1 throughout, meaning 90% target coverage.""",

    6: """[CP PIPELINE - 30 seconds]
This figure shows the conformal prediction pipeline.
Training data to base model, calibration set to compute scores, then prediction sets.
The key insight: when distribution shift occurs, the calibrated threshold becomes invalid, and coverage breaks.""",

    7: """[WHAT HAPPENS UNDER SHIFT - 1 minute]
Here's what happens in practice.
No shift: coverage stays at target, around 90%.
Mild shift: slight undercoverage, maybe 85%.
Severe shift: CATASTROPHIC failure - coverage can drop to 50% or below.
Key observation: shift severity alone doesn't predict coverage failure.
What matters is HOW features shift relative to model reliance.""",

    8: """[KEY INSIGHT - 1 minute]
This is our key insight.
The vulnerability of conformal prediction is determined by how CONCENTRATED the model's reliance is on shifting features.
Low concentration - importance spread across features - leads to robust coverage.
High concentration - single feature dominates - leads to vulnerability.
We measure this using SHAP concentration.""",

    9: """[SHAP CONCENTRATION - 1 minute]
Here's our metric: SHAP Concentration.
Step 1: Compute mean absolute SHAP values on validation data.
Step 2: Concentration C equals the top feature importance divided by total importance.
Simple, interpretable, computed BEFORE deployment.
Below 40%: model is likely robust to shift.
40% or above: model is vulnerable - flag for intervention.""",

    10: """[EXPERIMENTAL SETUP - 1 minute]
Our experimental setup uses the SALT benchmark from Stanford.
8 e-commerce classification tasks with COVID-19 temporal split.
Training on pre-COVID data, testing during COVID.
This gives us a natural experiment where all tasks experience the same external shock, but have different concentration profiles.""",

    11: """[METHODOLOGY - 45 seconds]
Methodology details:
Primary model is LightGBM, but we also test CatBoost, XGBoost, and Random Forest.
Conformal method is APS with 90% target coverage.
50 random seeds for statistical robustness.
External validation on 8 additional datasets across 9 domains total.""",

    12: """[MAIN RESULT - 1 minute]
Here's our main result - the scatter plot you've been waiting for.
SHAP concentration on x-axis, coverage deviation on y-axis.
Spearman rho = 0.853, p < 0.001, across 16 tasks in 9 domains.
This is a STRONG correlation - concentration predicts failure severity.
Compare to standard detectors which show rho ≤ 0.19.""",

    13: """[SALT RESULTS - 45 seconds]
Within the SALT COVID tasks specifically:
rho = 0.833, p = 0.010 with n=8 tasks.
Same pattern - high concentration tasks fail catastrophically, low concentration tasks maintain coverage.
Bootstrap 95% CI is 0.30 to 1.00.""",

    14: """[COMPARISON - 1 minute]
How does our diagnostic compare to standard shift detectors?
SHAP Concentration: rho = 0.853 - STRONG correlation.
MMD: rho = 0.19 - weak.
C2ST: rho = 0.15 - weak.
PSI: rho = 0.12 - negligible.
Standard detectors detect shift uniformly across all tasks but CANNOT distinguish which will actually fail.""",

    15: """[COVERTYPE - 1 minute]
External validation on Covertype dataset - geographic shift.
SHAP Concentration: 49.8% - above our 40% threshold.
Result: CATASTROPHIC failure. Target 90%, actual 8.2%. That's an 81.8 percentage point drop.
10 out of 10 seeds showed this failure - completely deterministic.
Our diagnostic correctly predicted this vulnerability.""",

    16: """[MODEL SENSITIVITY - 45 seconds]
Is the diagnostic specific to model type?
LightGBM: rho = 0.833 - strongest signal.
CatBoost: rho = 0.667 - good.
XGBoost: rho = 0.548 - moderate.
Random Forest: rho = 0.300 - weak.
The diagnostic works best for gradient boosting methods where sequential training reinforces single-feature dependence.""",

    17: """[THEORY - 1.5 minutes]
We also provide theoretical grounding.
Our theorem shows that under concentration, APS score bounds worsen monotonically.
Higher concentration leads to larger score perturbation bounds.
Score perturbation leads to coverage deviation through quantile shift.
Concentration acts as a 'fragility amplifier'.""",

    18: """[INTUITION - 1 minute]
Intuition for the theorem:
Low concentration - SHAP weights spread uniformly. When shift hits, the weighted impact averages out.
High concentration - one feature dominates. When shift hits THAT feature, the weighted impact is huge.
Same shift magnitude, but concentrated models amplify the damage.""",

    19: """[FRAMEWORK - 1 minute]
Practical framework - 3 steps.
Step 1: Compute concentration C on validation data.
Step 2: Check against 40% threshold.
Below 40%: deploy with confidence.
Above 40%: flag for mitigation before deployment.
The key is to catch vulnerable models BEFORE they fail in production.""",

    20: """[MITIGATION - 45 seconds]
When concentration exceeds threshold:
Feature engineering - diversify signal sources.
Model regularization - feature dropout, ensemble with diverse subsets.
Monitoring - track concentration over time, alert on threshold violations.
Key message: address concentration BEFORE deployment, not after failure.""",

    21: """[LIMITATIONS - 1 minute]
Honest limitations:
Tabular focus - tested primarily on tabular data.
SHAP cost - TreeSHAP is efficient for GBMs, but KernelSHAP is slower for deep learning.
Threshold calibration - 40% is empirical from n=8 SALT tasks, may vary by domain.
Model-specific - works best with tree ensembles, weaker for RF and neural nets.""",

    22: """[FUTURE WORK - 45 seconds]
Future directions:
Extensions to deep learning with gradient-based explanations.
Automatic mitigation - feature engineering to reduce concentration.
Tighter theoretical bounds under distribution-specific assumptions.
Open question: can we design models that are intrinsically low-concentration?""",

    23: """[CONCLUSION - 1 minute]
To conclude:
SHAP Concentration is a pre-deployment diagnostic for conformal prediction vulnerability.
Strong correlation: rho = 0.853 across 16 tasks.
Theoretical grounding with monotonic score bound.
Practical 3-step protocol with 40% threshold.
Impact: enables PROACTIVE identification of vulnerable deployments BEFORE failures occur.
Thank you. I'm happy to take questions.""",

    24: """[BACKUP - QUESTIONS]
This is the Q&A slide.
Common questions I expect:
- Why top-1 concentration vs entropy? Because sales-office has high top-2/3 but near-zero drop.
- Why 40% threshold? Natural gap in the concentration distribution.
- Does this work for neural nets? Weaker - MLP rho = 0.43.""",
}

# Create presentation
print("Creating PPTX...")
prs = Presentation()
prs.slide_width = Inches(13.333)  # 16:9
prs.slide_height = Inches(7.5)

# Add slides with images and notes
for i, page_file in enumerate(page_files, 1):
    slide_layout = prs.slide_layouts[6]  # Blank layout
    slide = prs.slides.add_slide(slide_layout)

    # Add full-page image
    img_path = os.path.join(IMAGES_DIR, page_file)
    slide.shapes.add_picture(
        img_path,
        Inches(0), Inches(0),
        width=prs.slide_width,
        height=prs.slide_height
    )

    # Add speaker notes
    if i in SPEAKER_NOTES:
        notes_slide = slide.notes_slide
        notes_slide.notes_text_frame.text = SPEAKER_NOTES[i]

print(f"Saving to {OUTPUT_PATH}...")
prs.save(OUTPUT_PATH)
print(f"Done! Created {OUTPUT_PATH} with {num_pages} slides and speaker notes.")

# Clean up
import shutil
shutil.rmtree(IMAGES_DIR)
print("Cleaned up temporary files.")
