#!/usr/bin/env python3
"""Create PPTX from PDF pages with detailed speaker notes - read-as-is scripts."""

import os
from pptx import Presentation
from pptx.util import Inches

SLIDES_DIR = "/Users/i767700/Github/conformal-covid-uai2026/slides"
IMAGES_DIR = os.path.join(SLIDES_DIR, "pdf_pages")
OUTPUT_PATH = os.path.join(SLIDES_DIR, "presentation_pdf_style.pptx")

# Detailed speaker notes - complete scripts to read as-is
SPEAKER_NOTES = {
    1: """[TITLE SLIDE - 30초]

안녕하세요, 여러분. KAIST에서 온 이초록입니다.

오늘 발표할 내용은 "Distribution Shift 상황에서 Conformal Prediction 실패를 진단하는 방법"입니다.
COVID-19 팬데믹을 자연 실험으로 활용한 케이스 스터디입니다.

이 연구는 UAI 2026에 accept되었습니다.

---
[다음 슬라이드로]""",

    2: """[THE PROMISE OF CONFORMAL PREDICTION - 1분]

먼저 Conformal Prediction이 왜 매력적인지 말씀드리겠습니다.

Conformal Prediction은 세 가지 강력한 특성을 제공합니다.

첫째, Distribution-free 보장입니다.
데이터 분포에 대한 가정 없이도 coverage를 보장합니다.

둘째, 어떤 base model과도 함께 작동합니다.
Random Forest, Neural Network, XGBoost 등 무엇이든 가능합니다.

셋째, Exact finite-sample validity를 제공합니다.
점근적 보장이 아니라 유한 샘플에서도 정확한 보장을 제공합니다.

저희는 90% coverage를 목표로 합니다.
즉, true label이 prediction set에 최소 90% 확률로 포함됩니다.

하지만... 여기에 함정이 있습니다.

---
[다음 슬라이드로]""",

    3: """[THE HIDDEN ASSUMPTION - 1분]

그 함정은 바로 Exchangeability 가정입니다.

Conformal Prediction이 작동하려면 calibration 데이터와 test 데이터가
교환 가능해야 합니다. 쉽게 말해, 같은 분포에서 나와야 합니다.

그림을 보시면, Training과 Test 사이에 물음표가 있습니다.
실제로 이 둘이 같은 분포일까요?

현실 세계의 배포 환경에서는 Distribution Shift가 불가피합니다.

COVID-19 같은 temporal shift가 있을 수 있고,
새로운 지역으로 확장할 때 geographic shift가 있고,
새로운 사용자층이 유입되면 demographic shift가 생깁니다.

그렇다면 이 가정이 깨질 때 무슨 일이 일어날까요?

---
[다음 슬라이드로]""",

    4: """[THE RESEARCH GAP - 1분]

기존에도 Distribution Shift를 탐지하는 방법들이 있습니다.

MMD, Maximum Mean Discrepancy.
C2ST, Classifier Two-Sample Test.
PSI, Population Stability Index.

이들은 shift가 '발생했는지'는 탐지할 수 있습니다.

하지만 치명적인 한계가 있습니다.

이 지표들은 모든 task에서 비슷하게 shift를 탐지합니다.
Coverage failure와의 상관관계는 rho가 0.19 이하로 매우 약합니다.

즉, Robust한 결과와 Catastrophic failure를 구분하지 못합니다.

그래서 저희의 연구 질문은 이것입니다:

"Test 데이터를 관찰하기 전에, 어떤 모델이 실패할지 예측할 수 있을까요?"

---
[다음 슬라이드로]""",

    5: """[CONFORMAL PREDICTION: A BRIEF PRIMER - 1.5분]

Conformal Prediction에 익숙하지 않은 분들을 위해 간단히 설명드리겠습니다.

K개 클래스가 있는 분류 문제를 생각해봅시다.
Base model이 각 클래스에 대한 확률 pi를 출력합니다.

저희는 APS, Adaptive Prediction Sets를 사용합니다.

1단계: Nonconformity score를 정의합니다.
s(x,y)는 true class보다 높은 확률을 가진 클래스들의 확률 합입니다.
직관적으로, 모델이 true class를 얼마나 '놀랍게' 여기는지를 측정합니다.

2단계: Calibration set에서 threshold를 계산합니다.
q-hat은 calibration score들의 (1-alpha) quantile입니다.

3단계: Prediction set을 형성합니다.
Score가 threshold 이하인 모든 클래스를 포함합니다.

4단계: Coverage guarantee.
Exchangeability 하에서, true label이 prediction set에 포함될 확률이
최소 1-alpha, 즉 90%입니다.

저희 실험에서는 alpha=0.1, 즉 90% target coverage를 사용합니다.

---
[다음 슬라이드로]""",

    6: """[CONFORMAL PREDICTION PIPELINE - 30초]

이 그림이 Conformal Prediction의 전체 파이프라인을 보여줍니다.

왼쪽부터 보시면:
Training Data로 Base Model을 학습합니다.
Calibration Set으로 Nonconformity Score를 계산합니다.
Score 분포에서 quantile threshold를 구합니다.
새로운 입력에 대해 Prediction Set을 생성합니다.

아래 히스토그램이 중요합니다.
빨간 선이 quantile threshold입니다.
이 threshold가 90% coverage를 보장합니다.

하지만 Distribution Shift가 발생하면?
Calibration 때 계산한 threshold가 더 이상 유효하지 않습니다.
Coverage가 깨집니다.

---
[다음 슬라이드로]""",

    7: """[WHAT HAPPENS UNDER DISTRIBUTION SHIFT? - 1분]

실제로 무슨 일이 일어나는지 보여드리겠습니다.

왼쪽: Shift가 없는 경우.
Coverage가 target인 90% 근처를 유지합니다. 초록색 막대입니다.

가운데: 약한 Shift.
약간의 undercoverage가 발생합니다. 85% 정도.
주황색 막대입니다. 아직 사용 가능한 수준입니다.

오른쪽: 심한 Shift.
Catastrophic failure입니다. Coverage가 49.8%로 추락합니다.
빨간 막대입니다. 90%를 목표로 했는데 절반도 안 됩니다.

여기서 중요한 관찰이 있습니다.

Shift의 심각도만으로는 coverage failure를 예측할 수 없습니다.
중요한 것은 '어떤' feature가 shift하는지,
그리고 모델이 그 feature에 얼마나 '의존'하는지입니다.

---
[다음 슬라이드로]""",

    8: """[OUR KEY INSIGHT - 1분]

이것이 저희의 핵심 통찰입니다.

화면의 문장을 읽어드리겠습니다:

"Conformal Prediction의 취약성은
모델이 shifting feature에 얼마나 '집중적으로' 의존하는지에 의해 결정된다."

왼쪽 막대 그래프를 보세요. Low Concentration입니다.
Feature importance가 여러 feature에 고르게 분산되어 있습니다.
이런 모델은 Robust합니다.
한 feature가 shift해도 다른 feature들이 버텨줍니다.

오른쪽을 보세요. High Concentration입니다.
하나의 feature가 압도적으로 중요합니다.
이런 모델은 Vulnerable합니다.
그 feature가 shift하면 모델 전체가 무너집니다.

저희는 이것을 SHAP Concentration으로 측정합니다.

---
[다음 슬라이드로]""",

    9: """[SHAP CONCENTRATION: THE METRIC - 1분]

SHAP Concentration의 정의를 설명드리겠습니다.

매우 간단합니다.

1단계: Validation 데이터에서 각 feature의 mean absolute SHAP value를 계산합니다.
phi_j가 feature j의 평균 중요도입니다.

2단계: Concentration C를 계산합니다.

박스 안의 수식을 보세요:
C = phi_1 / sum of all phi_j

분자는 가장 중요한 feature의 importance입니다.
분모는 전체 feature importance의 합입니다.

즉, "top-1 feature가 전체의 몇 퍼센트를 차지하는가"입니다.

해석은 간단합니다:
C가 40% 미만이면: 모델이 shift에 Robust할 가능성이 높습니다.
C가 40% 이상이면: 모델이 Vulnerable합니다. 배포 전 조치가 필요합니다.

이 metric의 장점은:
단순하고, 해석 가능하고, 배포 전에 계산할 수 있습니다.

---
[다음 슬라이드로]""",

    10: """[EXPERIMENTAL SETUP: SALT BENCHMARK - 1분]

실험 설정을 말씀드리겠습니다.

저희는 Stanford의 SALT 벤치마크를 사용했습니다.
Supply chain ALlocaTion의 약자입니다.

8개의 e-commerce 분류 task가 있습니다.

핵심은 COVID-19 temporal split입니다.
Calibration: COVID 이전 데이터
Test: COVID 기간 데이터

이것이 왜 좋은 실험 설계인가?

모든 8개 task가 동일한 외부 충격을 경험합니다.
하지만 각 task의 SHAP Concentration profile은 다릅니다.

따라서 concentration과 coverage failure의 관계를
깔끔하게 분리해서 연구할 수 있습니다.

오른쪽 그림이 COVID-19로 인한 distribution shift를 보여줍니다.

---
[다음 슬라이드로]""",

    11: """[METHODOLOGY DETAILS - 45초]

방법론 세부사항입니다.

Models:
주로 LightGBM을 사용했습니다.
추가로 CatBoost, XGBoost, Random Forest도 테스트했습니다.

Conformal Method:
APS, Adaptive Prediction Sets.
Target coverage 90%, 즉 alpha = 0.1.

Statistical Robustness:
50개의 random seed로 실험을 반복했습니다.
Spearman correlation과 p-value를 보고합니다.

External Validation:
SALT 외에 8개 추가 데이터셋에서 검증했습니다.
총 9개 domain, 16개 task입니다.

---
[다음 슬라이드로]""",

    12: """[MAIN RESULT: STRONG CORRELATION - 1분]

이제 메인 결과입니다. 가장 중요한 슬라이드입니다.

그래프를 보세요.
X축이 SHAP Concentration,
Y축이 Coverage Deviation입니다.

16개 점이 있습니다.
파란 원이 SALT COVID task 8개,
주황 삼각형이 external validation 8개입니다.

회귀선과 confidence band가 보이시죠?

결과:
Spearman rho = 0.853
p-value < 0.001
n = 16 tasks across 9 domains

이것은 매우 강한 상관관계입니다.
SHAP Concentration이 높을수록 Coverage failure가 심합니다.

비교해보면:
기존 shift detector들의 rho는 0.19 이하입니다.
저희 metric은 0.853입니다.

---
[다음 슬라이드로]""",

    13: """[WITHIN SALT COVID TASKS - 45초]

SALT COVID task 내에서의 결과를 더 자세히 보겠습니다.

왼쪽 scatter plot:
8개 SALT task만 표시했습니다.
rho = 0.833, p = 0.010

오른쪽 테이블:
Task별로 Concentration과 Coverage를 보여줍니다.

패턴이 명확합니다:
Concentration이 낮은 task (0.21, 0.28)는 coverage가 88%, 85%로 양호합니다.
Concentration이 높은 task (0.67)는 coverage가 65%로 심하게 떨어집니다.

Bootstrap 95% CI는 [0.30, 1.00]입니다.

---
[다음 슬라이드로]""",

    14: """[COMPARISON: SHAP VS STANDARD DETECTORS - 1분]

기존 shift detector들과 비교해보겠습니다.

표를 보세요:

SHAP Concentration: rho = 0.853, Strong correlation.
MMD: rho = 0.19, Weak.
C2ST: rho = 0.15, Weak.
PSI: rho = 0.12, Negligible.

왜 기존 방법들이 실패할까요?

기존 방법들은 marginal distribution shift를 측정합니다.
"전체적으로 데이터가 얼마나 달라졌는가"를 봅니다.

하지만 coverage failure는 model-relevant feature의 shift에 달려있습니다.
모델이 의존하는 feature가 shift하면 실패하고,
모델이 무시하는 feature가 shift하면 괜찮습니다.

모든 task에서 MMD와 C2ST는 비슷한 값을 보여줍니다.
하지만 coverage outcome은 극단적으로 다릅니다.

---
[다음 슬라이드로]""",

    15: """[EXTERNAL VALIDATION: COVERTYPE - 1분]

External validation의 대표 사례로 Covertype 데이터셋을 보겠습니다.

Covertype은 forest cover type을 예측하는 task입니다.
7개 클래스, 54개 feature.

Geographic split을 사용했습니다:
Wilderness Area 1-2로 학습,
Area 4로 테스트.

결과를 보세요:

SHAP Concentration: 49.8%
저희 40% threshold를 초과합니다. Vulnerable로 예측됩니다.

실제 결과:
Target Coverage: 90%
Actual Coverage: 8.2%
Coverage Drop: 81.8 percentage points!

Catastrophic failure입니다.

그리고 이것은 10개 seed 모두에서 동일하게 발생했습니다.
Deterministic failure입니다.

저희 diagnostic이 이 실패를 정확히 예측했습니다.

---
[다음 슬라이드로]""",

    16: """[MODEL SENSITIVITY ANALYSIS - 45초]

이 diagnostic이 모든 모델에서 작동할까요?

테이블을 보세요:

LightGBM: rho = 0.833, 가장 강한 신호.
CatBoost: rho = 0.667, 좋음.
XGBoost: rho = 0.548, 보통.
Random Forest: rho = 0.300, 약함.

왜 이런 차이가 있을까요?

Gradient Boosting 계열에서 가장 잘 작동합니다.
Sequential training이 single-feature dependence를 강화하기 때문입니다.

Random Forest는 bagging이 feature importance를 분산시킵니다.
각 tree가 다른 feature subset을 보기 때문에
global concentration 신호가 희석됩니다.

따라서 이 diagnostic은 gradient boosting model에 가장 적합합니다.

---
[다음 슬라이드로]""",

    17: """[THEORETICAL FOUNDATION - 1분]

이론적 근거도 제공합니다.

Theorem 박스를 보세요:

H가 SHAP Concentration이고,
delta가 feature shift magnitude일 때,

Expected APS score deviation의 upper bound는
g(H) * ||delta||_2 에 비례합니다.

여기서 핵심은:
g(H)가 H에 대해 monotonically increasing합니다.

의미:
Concentration이 높을수록 → score perturbation bound가 커집니다.
Score perturbation이 크면 → coverage가 깨집니다.

Concentration은 일종의 "fragility amplifier" 역할을 합니다.
같은 크기의 shift라도 concentrated model에서 더 큰 피해를 줍니다.

자세한 증명은 논문 Appendix A에 있습니다.

---
[다음 슬라이드로]""",

    18: """[INTUITION BEHIND THE THEOREM - 1분]

직관적으로 설명드리겠습니다.

그림의 왼쪽: Low Concentration.
SHAP weight가 5개 feature에 균등하게 분포합니다.
아래 빨간 막대가 shift입니다.
일부 feature에 shift가 발생해도,
weighted impact가 평균화됩니다.
결과: Small perturbation.

그림의 오른쪽: High Concentration.
하나의 feature가 압도적인 SHAP weight를 가집니다.
그 feature에 shift가 발생하면?
Weighted impact가 엄청나게 큽니다.
결과: Large perturbation.

같은 양의 shift라도,
concentrated model에서 damage가 증폭됩니다.

이것이 concentration이 "fragility amplifier"인 이유입니다.

---
[다음 슬라이드로]""",

    19: """[OPERATIONAL FRAMEWORK: 3-STEP PROTOCOL - 1분]

실무에서 어떻게 적용할까요?

3단계 프로토콜을 제안합니다.

Step 1: Validation 데이터에서 Concentration C를 계산합니다.

Step 2: 40% threshold와 비교합니다.

C < 40%: 초록색 화살표.
"Deploy with CP" - Conformal Prediction과 함께 배포해도 됩니다.

C >= 40%: 빨간색 화살표.
"Mitigate first" - 배포 전에 조치가 필요합니다.

Step 3: 조치 후 재평가하거나, 다른 방법을 고려합니다.

40% threshold는 경험적으로 도출되었습니다.
SALT dataset에서 자연스러운 gap이 관찰되었습니다.

물론 domain에 따라 조정이 필요할 수 있습니다.

---
[다음 슬라이드로]""",

    20: """[MITIGATION STRATEGIES - 45초]

Concentration이 threshold를 초과하면 어떻게 할까요?

네 가지 전략을 제안합니다.

1. Feature Engineering
신호 소스를 다양화합니다.
Dominant feature에 대한 의존도를 줄입니다.

2. Model Regularization
Feature dropout을 적용합니다.
다양한 feature subset으로 ensemble합니다.

3. Monitoring
시간에 따른 concentration 변화를 추적합니다.
Threshold 위반 시 alert을 발생시킵니다.

오른쪽 그림이 monitoring framework을 보여줍니다.
Production pipeline과 병렬로 coverage tracker가 동작합니다.
Alert system이 traffic light처럼 상태를 표시합니다.

핵심 메시지:
실패가 발생한 후가 아니라, 배포 전에 concentration을 address하세요.

---
[다음 슬라이드로]""",

    21: """[LIMITATIONS - 1분]

정직하게 한계점을 말씀드리겠습니다.

첫째, Tabular data 중심입니다.
주로 tabular 데이터에서 테스트했습니다.
Image나 text로의 확장은 추가 연구가 필요합니다.

둘째, SHAP 계산 비용입니다.
TreeSHAP은 gradient boosting에서 효율적입니다.
하지만 deep learning에서 KernelSHAP은 느립니다.

셋째, Threshold calibration입니다.
40%는 경험적 값입니다.
n=8 SALT task에서 도출했습니다.
Domain에 따라 달라질 수 있습니다.

넷째, Model-specific입니다.
Tree ensemble에서 가장 잘 작동합니다.
Random Forest나 Neural Net에서는 약합니다.

마지막으로, 이것은 diagnostic tool이지 fix가 아닙니다.
Correlation이 causation을 의미하지는 않습니다.
하지만 이론이 mechanism을 지지합니다.

---
[다음 슬라이드로]""",

    22: """[FUTURE DIRECTIONS - 45초]

향후 연구 방향입니다.

세 가지 원으로 표시했습니다.

첫째, Extensions.
Deep learning으로 확장합니다.
Gradient-based explanation을 활용할 수 있습니다.

둘째, Automation.
자동 완화 기법을 개발합니다.
Concentration을 줄이는 feature engineering을 자동화합니다.

셋째, Theory.
더 tight한 bound를 도출합니다.
Distribution-specific 가정 하에서 더 정확한 예측이 가능할 것입니다.

열린 질문이 있습니다:
"본질적으로 low-concentration인 모델을 설계할 수 있을까요?"
"Adversarial robustness와의 관계는 무엇일까요?"

---
[다음 슬라이드로]""",

    23: """[CONCLUSION - 1분]

결론입니다.

SHAP Concentration은 Conformal Prediction 취약성을 위한
Pre-deployment diagnostic입니다.

Key contributions 세 가지:

첫째, Predictive metric.
SHAP concentration과 coverage failure의 상관관계: rho = 0.853.
16 tasks, 9 domains에서 검증되었습니다.

둘째, Theoretical grounding.
Score perturbation에 대한 monotonic bound를 증명했습니다.
Concentration이 fragility amplifier임을 보였습니다.

셋째, Practical protocol.
40% threshold를 기준으로 한 3단계 framework을 제안했습니다.

Impact:
취약한 배포를 실패가 발생하기 전에 사전 식별할 수 있습니다.
Proactive하게 대응할 수 있습니다.

코드와 데이터는 GitHub에 공개되어 있습니다.

감사합니다. 질문 받겠습니다.

---
[Q&A]""",

    24: """[BACKUP: QUESTIONS SLIDE]

예상되는 질문들:

Q: 왜 top-1 concentration을 사용하나요? Top-2나 entropy는?
A: sales-office task는 top-2/3 concentration이 높지만 coverage drop이 거의 없습니다.
   Top-1만이 유의미한 상관관계를 보여줍니다.

Q: 40% threshold는 어떻게 정했나요?
A: SALT dataset의 concentration 분포에서 자연스러운 gap이 관찰되었습니다.
   Low-concentration (24-29%)와 high-concentration (43-54%) 사이의 gap입니다.

Q: Neural network에서도 작동하나요?
A: MLP에서 rho = 0.43으로 약합니다.
   SHAP approximation 노이즈 때문입니다.
   Gradient boosting에서 가장 효과적입니다.""",

    25: """[BACKUP: FULL RESULTS TABLE]

전체 결과 테이블입니다.

SALT 8개 task:
- s-payterms: C=54.2%, Drop=77.1pp (Catastrophic)
- s-shipcond: C=50.7%, Drop=71.6pp (Catastrophic)
- i-shippoint: C=48.8%, Drop=18.5pp (High variance)
- s-group: C=47.3%, Drop=71.2pp (Catastrophic)
- s-office: C=42.6%, Drop=0.1pp (Robust - protective factor)
- i-incoterms: C=28.9%, Drop=11.3pp (Robust)
- i-plant: C=23.9%, Drop=10.6pp (Robust)
- s-incoterms: C=23.7%, Drop=8.5pp (Robust)

External validation 주요 케이스:
- Covertype: C=49.8%, Drop=81.8pp (Catastrophic)
- KDDCup99: C=21.1%, Drop=15.9pp (Intermediate, high variance)""",

    26: """[BACKUP: SHAP COMPUTATION DETAILS]

SHAP 계산 세부사항:

구현:
- SHAP library v0.42.1
- TreeExplainer for gradient boosting
- Exact SHAP values (not approximation)

계산 시간:
- 약 1초 per 1,000 samples
- 실용적으로 사용 가능한 수준

Aggregation:
- Class별, sample별 absolute SHAP의 평균
- Normalization하여 sum = 1

Robustness:
- Calibration set 크기 1K-10K에서 안정적
- Bootstrap CI 제공""",

    27: """[BACKUP: STATISTICAL ANALYSIS]

통계 분석 세부사항:

Spearman Correlation 선택 이유:
- Outlier에 robust
- Monotonic relationship 포착
- Ordinal pattern에 적합

결과:
- Overall: rho = 0.853, p < 0.001
- SALT only: rho = 0.833, p = 0.010
- 95% CI: [0.50, 0.96]

Multiple comparison correction:
- 5개 concentration variant 테스트
- Holm-Bonferroni correction 적용
- Top-1이 유일하게 유의미

ICC 분석:
- Task identity가 variance의 67.5% 설명
- Effective n = 11.7 > 8 tasks""",
}

# Create presentation
print("Creating PPTX with detailed speaker notes...")
prs = Presentation()
prs.slide_width = Inches(13.333)  # 16:9
prs.slide_height = Inches(7.5)

# Get sorted list of images
page_files = sorted([f for f in os.listdir(IMAGES_DIR) if f.startswith("slide") and f.endswith(".jpg")])
print(f"Found {len(page_files)} slides")

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
    print(f"  Added slide {i}/{len(page_files)}")

print(f"\nSaving to {OUTPUT_PATH}...")
prs.save(OUTPUT_PATH)
print(f"✓ Done! Created PPTX with {len(page_files)} slides")
print(f"  - Exact PDF styling preserved")
print(f"  - Detailed read-as-is speaker notes")
