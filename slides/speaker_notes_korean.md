# 발표 스크립트 (20분용)
## Diagnosing Conformal Prediction Failures Under Distribution Shift

**총 발표 시간: 20분**  
**코드 & 데이터:** github.com/ChorokLeeDev/conformal-covid-uai2026

---

## 슬라이드 1: 제목 (30초)

안녕하세요. KAIST의 이초록입니다.

오늘 발표 제목은 "Distribution Shift 환경에서 Conformal Prediction 실패 진단하기"입니다. COVID-19 팬데믹을 케이스 스터디로 활용했습니다.

---

## 슬라이드 2: The Promise of Conformal Prediction (45초)

먼저 Conformal Prediction이 왜 중요한지 말씀드리겠습니다.

Conformal Prediction은 머신러닝에서 불확실성을 정량화하는 강력한 프레임워크입니다. 세 가지 핵심 장점이 있는데요.

첫째, distribution-free 커버리지 보장을 제공합니다. 데이터 분포에 대한 가정 없이, 오직 교환가능성 가정만으로 작동합니다.

둘째, 어떤 베이스 모델과도 작동합니다. LightGBM이든, 신경망이든 상관없이 적용할 수 있습니다.

셋째, 유한 샘플에서도 정확한 보장을 제공합니다. 이게 핵심인데요, 왜 가능하냐면 score의 절대값이 아니라 순위만 보기 때문입니다. Calibration set에 n개 샘플이 있으면, test 샘플 포함 n+1개의 순서가 교환가능성 하에서 equally likely합니다. 그래서 test 샘플이 상위 90% 안에 들 확률이 combinatorial하게 보장됩니다. 점근적 보장이 아니라 exact finite-sample 보장이에요. 이게 Bayesian이나 frequentist 방법과 다른 핵심 강점입니다.

우리는 90% 커버리지를 목표로 합니다. 이 말은, 예측 집합 안에 실제 정답이 최소 90% 확률로 포함되어야 한다는 뜻입니다.

하지만 여기엔 숨겨진 함정이 있습니다.

---

## 슬라이드 3: The Hidden Assumption (45초)

바로 교환가능성 가정입니다.

Conformal prediction이 제대로 작동하려면, calibration 데이터와 test 데이터가 교환가능해야 합니다. 쉽게 말해서 같은 분포에서 나와야 한다는 겁니다.

문제는, 실제 배포 환경에서 distribution shift는 피할 수 없다는 겁니다.

예를 들어, COVID-19처럼 시간에 따라 데이터가 변하거나, 서비스를 새로운 지역으로 확장하거나, 새로운 사용자층이 유입되면 분포가 바뀝니다.

그렇다면 이런 상황에서 conformal prediction은 어떻게 될까요?

---

## 슬라이드 4: The Research Gap (1분)

기존에 distribution shift를 탐지하는 방법들이 있습니다. MMD, C2ST, PSI 같은 것들인데요.

이들의 문제점은, shift를 균일하게 탐지한다는 겁니다.

모든 태스크에서 "shift가 있다"고 알려주지만, 정작 중요한 건 구분하지 못합니다. 어떤 태스크가 shift에도 불구하고 robust하고, 어떤 태스크가 catastrophic하게 실패할지 구분하지 못한다는 거죠.

그래서 우리의 연구 질문은 이겁니다: Conformal prediction이 언제 실패할지, 배포하기 전에 미리 예측할 수 있을까?

---

## 슬라이드 5: Conformal Prediction Primer (1분)

간단히 conformal prediction을 복습하겠습니다.

K개 클래스 분류 문제가 있다고 합시다.

첫 번째 단계로, nonconformity score를 정의합니다. 우리가 사용하는 APS 방법에서는, true class까지의 누적 확률을 score로 씁니다.

두 번째로, calibration set에서 이 score들의 분포를 보고 threshold를 계산합니다. 90% 커버리지를 원하면 90번째 percentile을 threshold로 잡습니다.

세 번째로, 새로운 테스트 샘플이 들어오면 이 threshold를 기준으로 prediction set을 구성합니다.

네 번째로, 데이터가 교환가능하다면 커버리지가 보장됩니다.

우리는 알파 0.1, 즉 90% 커버리지를 타겟으로 합니다.

---

## 슬라이드 6: What Happens Under Distribution Shift? (45초)

그런데 distribution shift가 발생하면 어떻게 될까요?

여기 세 가지 시나리오가 있습니다.

Shift가 없으면 90.2% 커버리지로 타겟을 달성합니다. 약한 shift가 있으면 85.1%로 약간 떨어집니다. 하지만 심한 shift가 있으면 49.8%까지, 거의 절반으로 catastrophic하게 실패합니다.

핵심 관찰은 이겁니다. Shift의 심각도만으로는 커버리지 실패를 예측할 수 없습니다.

중요한 건 어떤 feature가 shift하느냐, 그리고 모델이 그 feature에 얼마나 의존하느냐입니다.

---

## 슬라이드 7: Conformal Prediction Pipeline (30초)

이 그림은 conformal prediction 파이프라인을 보여줍니다.

정상적인 상황에서는 calibration된 threshold가 test 데이터에도 적용됩니다.

하지만 distribution shift가 발생하면, calibration된 threshold가 더 이상 유효하지 않게 되고, 결과적으로 커버리지 보장이 깨집니다.

---

## 슬라이드 8: Our Key Insight (1분)

이제 우리의 핵심 통찰을 말씀드리겠습니다.

Conformal prediction의 취약성은, 모델이 shifting feature에 얼마나 집중적으로 의존하는지에 의해 결정됩니다.

슬라이드 왼쪽을 보시면, feature importance가 여러 feature에 골고루 분산되어 있습니다. 이런 모델은 shift에 robust합니다.

오른쪽은 하나의 feature에 importance가 집중되어 있습니다. 이런 모델은 shift에 vulnerable합니다.

우리는 이 집중도를, top feature의 importance 비율로 측정합니다. 이걸 SHAP Concentration이라고 부릅니다.

---

## 슬라이드 9: SHAP Concentration: The Metric (1분)

구체적인 metric을 설명드리겠습니다.

Step 1에서, validation 데이터에서 각 feature의 mean absolute SHAP value를 계산합니다.

Step 2에서, SHAP Concentration C를 계산합니다. 수식은 간단합니다. Top feature의 importance를 전체 importance 합으로 나눕니다. 파이 1 나누기 시그마 파이 j입니다.

해석도 간단합니다.

C가 40% 미만이면, importance가 분산되어 있어서 shift에 robust합니다.
C가 40% 이상이면, 하나의 feature가 지배적이라 shift에 vulnerable합니다.

이 metric의 핵심 장점은, 배포 전에 validation 데이터만으로 계산할 수 있다는 겁니다.

---

## 슬라이드 10: Why Does Concentration Matter? (45초)

왜 concentration이 중요할까요?

직관은 이렇습니다.

모델이 소수의 feature에 의존하면, 그 feature들이 shift할 때 conformity score의 perturbation이 크게 발생합니다. 한 곳에 몰빵했는데 그게 무너지면 전체가 무너지는 거죠.

반면 다수의 feature에 의존하면, 개별 feature의 shift가 서로 평균화되어서 score distribution이 더 안정적입니다.

즉, Concentration은 fragility amplifier입니다. 집중도가 높을수록 취약해집니다.

---

## 슬라이드 11: Experimental Setup: SALT Benchmark (45초)

실험 설정을 말씀드리겠습니다.

SALT는 supply chain allocation의 약자로, e-commerce 물류 분류를 위한 벤치마크입니다. 8개의 분류 태스크가 있습니다.

핵심은 COVID-19 temporal split입니다.

Calibration 데이터는 COVID 이전, test 데이터는 COVID 기간 중입니다. 팬데믹으로 인해 자연스러운 distribution shift가 발생했고, 8개 태스크 모두 동일한 시간적 shift를 경험했습니다.

그런데 결과는 태스크마다 완전히 다르게 나왔습니다.

---

## 슬라이드 12: Models and Methods (45초)

모델과 방법론입니다.

중요한 점을 먼저 말씀드리면, 우리의 diagnostic은 GBM, 즉 gradient boosting model에 특화되어 있습니다.

LightGBM에서 rho 0.833으로 가장 강한 상관관계를 보였고, CatBoost와 XGBoost에서도 0.55에서 0.67 사이의 상관관계를 보였습니다.

반면 Random Forest와 MLP는 다른 failure mode를 가져서 이 diagnostic이 적용되지 않습니다. 이건 limitation 섹션에서 다시 말씀드리겠습니다.

Conformal method로는 APS를 사용하고, 90% 커버리지를 타겟으로 합니다.

---

## 슬라이드 13: Experimental Setup (30초)

통계적 robustness를 위해 철저하게 실험했습니다.

각 실험마다 50개의 random seed를 사용했고, Spearman correlation과 p-value를 계산했으며, bootstrap으로 confidence interval을 구했습니다.

External validation으로는 UCI 데이터셋 8개를 추가로 사용했고, 전체적으로 91.7% 정확도를 달성했습니다.

---

## 슬라이드 14: Main Result - Strong Correlation (1분)

이제 메인 결과입니다.

이 scatter plot을 보시면, x축이 SHAP concentration이고 y축이 coverage drop입니다.

SHAP concentration과 coverage deviation 사이에 강한 양의 상관관계가 있습니다.

Spearman rho가 0.853이고, p-value는 0.001 미만입니다. 9개 도메인에 걸친 16개 multiclass 태스크에서 이 결과를 얻었습니다.

이것이 우리의 primary finding입니다. SHAP concentration이 coverage failure의 severity를 강하게 예측합니다.

---

## 슬라이드 15: Within SALT COVID Tasks (45초)

SALT 내에서만 보면 어떨까요?

8개 태스크에서 rho 0.833, p-value 0.010입니다.

테이블을 보시면, concentration이 높을수록 coverage가 낮습니다.

예를 들어 s-payterms는 concentration이 54.2%인데 coverage가 13.7%까지 떨어졌습니다. 77 percentage point나 떨어진 거죠.

반면 s-incoterms는 concentration이 23.7%인데 coverage가 87%로 거의 유지됐습니다.

같은 COVID shift를 경험했는데, 결과는 완전히 다릅니다. 그 차이를 설명하는 게 바로 SHAP concentration입니다.

---

## 슬라이드 16: Comparison with Standard Detectors (45초)

기존 shift detector들과 비교해보겠습니다.

SHAP Concentration은 rho 0.853으로 strong correlation입니다.
MMD는 rho 0.19로 weak합니다.
C2ST는 rho 0.15로 weak합니다.
PSI는 rho 0.12로 거의 없습니다.

왜 기존 detector들이 실패할까요?

이들은 marginal distribution shift만 측정하기 때문입니다. 전체 데이터의 분포가 바뀌었는지는 알려주지만, 모델이 실제로 의존하는 feature의 shift는 보지 못합니다.

우리의 방법은 model-relevant feature의 shift를 직접 측정합니다.

---

## 슬라이드 17: External Validation - Covertype (45초)

External validation 중 가장 극적인 케이스를 보여드리겠습니다.

Covertype 데이터셋입니다. 산림 유형을 분류하는 문제로, 7개 클래스와 54개 feature가 있습니다.

Geographic split을 적용했습니다. Areas 1과 2에서 학습하고, Area 4에서 테스트했습니다. 지역이 다르니까 자연스러운 distribution shift가 발생합니다.

결과를 보시면, SHAP Concentration이 49.8%로 높았습니다. Target coverage는 90%였는데, actual coverage는 8.2%였습니다. 81.8 percentage point나 떨어진 catastrophic failure입니다.

이 실패를 우리 방법이 정확히 예측했습니다. 10개 seed 모두에서 deterministic하게요.

---

## 슬라이드 18: Model Sensitivity Analysis (45초)

모델별 분석 결과입니다.

LightGBM은 rho 0.833으로 diagnostic이 잘 작동합니다.
CatBoost는 rho 0.667, XGBoost는 rho 0.548로 역시 작동합니다.
하지만 Random Forest는 rho 0.300, MLP는 rho 0.430으로 작동하지 않습니다.

왜 이런 차이가 날까요?

GBM은 sequential boosting을 하면서 특정 feature에 concentrated dependence를 만듭니다.
RF는 bagging을 해서 single-feature reliance를 희석시킵니다.
MLP는 아예 다른 메커니즘으로 실패합니다. Global sensitivity failure라고 부르는데, 이건 우리 diagnostic이 포착하지 못합니다.

---

## 슬라이드 19: Theoretical Foundation (1분)

이론적 기반을 간단히 설명드리겠습니다.

우리 논문에서 Theorem을 증명했습니다.

SHAP concentration이 높을수록, APS score deviation의 expected bound가 커집니다. 그리고 이 bound 함수 g of H는 H에 대해 단조 증가합니다.

핵심 함의는 세 가지입니다.

첫째, 높은 concentration은 큰 score perturbation bound로 이어집니다.
둘째, score perturbation은 coverage deviation으로 이어집니다.
셋째, 따라서 concentration은 fragility amplifier로 작용합니다.

자세한 증명은 paper Appendix에 있으니 관심 있으신 분들은 참고해주세요.

---

## 슬라이드 20: Operational Framework (1분)

실용적인 프레임워크를 제안합니다. 3-Step Protocol입니다.

Step 1에서 C를 계산합니다. Validation 데이터에서 SHAP concentration을 구합니다.

Step 2에서 40% threshold를 체크합니다.

Step 3에서 결정을 내립니다.
C가 40% 미만이면, 낮은 위험으로 판단하고 배포합니다.
C가 40% 이상이면, 취약하다고 판단하고 mitigation을 고려합니다.

이 40% threshold는 경험적으로 도출된 값입니다. SALT 8개 태스크에서 exploratory하게 도출했고, prospective validation이 필요합니다.

---

## 슬라이드 21: Limitations (45초)

한계점을 솔직히 말씀드리겠습니다.

첫째, tabular 데이터에 집중했습니다. 이미지나 텍스트로의 확장은 추가 연구가 필요합니다.

둘째, GBM에 특화된 diagnostic입니다. Random Forest는 rho 0.30, MLP는 rho 0.43으로 다른 failure mode를 가집니다.

셋째, K가 4 이상인 multiclass에서만 작동합니다. Binary나 ternary 분류에서는 APS prediction set이 structural ceiling을 가져서 concentration mechanism이 작동하지 않습니다.

넷째, 40% threshold는 n=8에서 exploratory하게 도출했습니다. Prospective validation이 필요합니다.

다섯째, 이건 diagnostic이지 solution이 아닙니다. 취약성을 표시해줄 뿐, 해결해주진 않습니다.

---

## 슬라이드 22: Future Directions (45초)

미래 연구 방향입니다.

Extensions로는, deep learning에 gradient-based explanation을 적용하는 연구가 가능합니다.

Automation으로는, C를 줄이기 위한 자동 feature engineering을 연구할 수 있습니다.

Theory로는, distribution-specific coverage bounds를 더 정교하게 도출할 수 있습니다.

Open questions도 있습니다. 본질적으로 low-concentration인 모델을 설계할 수 있을까요? 40% threshold의 prospective validation은 어떻게 할까요? Online conformal prediction에서 concentration monitoring은 어떻게 할까요?

---

## 슬라이드 23: Conclusion (1분)

결론입니다.

SHAP Concentration은 Conformal Prediction 취약성을 위한 Pre-Deployment Diagnostic입니다.

세 가지 기여를 했습니다.

첫째, predictive metric을 제안했습니다. rho 0.853, 95% confidence interval 0.50에서 0.96입니다. GBM classifier에서요.

둘째, validation을 철저히 했습니다. Leave-one-out CV에서 87.5%, external validation에서 91.7% 정확도입니다.

셋째, practical protocol을 제안했습니다. 40% threshold를 기준으로 한 3-step framework입니다.

Scope는 K가 4 이상인 multiclass GBM classifier입니다.

Impact는, 실패가 발생하기 전에 취약한 배포를 proactive하게 식별할 수 있다는 겁니다.

감사합니다. 질문 받겠습니다.

---

## Q&A 준비 (예상 질문과 답변)

**Q1: "왜 Random Forest나 MLP에는 작동하지 않나요?"**

Random Forest는 bagging을 해서 concentration을 희석시킵니다. 여러 tree가 서로 다른 feature subset을 보기 때문에, 전체적으로 single-feature reliance가 낮아집니다.

MLP는 global sensitivity failure mode를 가집니다. Concentrated dependence가 아니라, 여러 feature가 동시에 coordinated하게 영향을 미쳐서 실패합니다. 이건 우리 diagnostic이 포착하는 메커니즘과 다릅니다.

**Q2: "40% threshold는 어떻게 도출했나요?"**

SALT n=8에서 경험적으로 도출했습니다. Catastrophic failure가 발생한 태스크와 robust한 태스크를 구분하는 natural gap이 40% 근처에 있었습니다.

하지만 이건 exploratory한 값입니다. Prospective validation이 필요하고, 35%에서 45% 구간은 uncertainty band로 보고 추가 monitoring을 권장합니다.

**Q3: "Binary classification에는 적용 안 되나요?"**

네, K가 3 이하에서는 APS prediction set이 structural ceiling을 가집니다. Binary면 prediction set이 공집합, 클래스 0, 클래스 1, 또는 둘 다밖에 안 됩니다. 이 제한된 구조에서는 concentration mechanism이 작동할 공간이 없습니다.

K가 4 이상이어야 prediction set의 다양성이 충분해서 concentration의 영향이 나타납니다.

**Q4: "이미지나 텍스트 데이터에는 어떻게 확장하나요?"**

현재는 tabular에 집중했습니다. 이미지나 텍스트로 확장하려면 Deep SHAP 같은 방법을 써야 하는데, 몇 가지 도전이 있습니다.

첫째, feature 정의가 명확하지 않습니다. Pixel이 feature인지, superpixel인지, semantic region인지 정해야 합니다.
둘째, SHAP computation이 훨씬 비쌉니다.
셋째, GBM이 아니라 neural network이므로, 우리가 증명한 theoretical foundation이 직접 적용되지 않습니다.

Gradient-based explanation이 유망한 방향이라고 생각합니다.

**Q5: "Retraining이 도움이 되나요?"**

일부 도움이 됩니다. 우리 실험에서 평균 19 percentage point 개선을 보였고, unadjusted p-value는 0.036이었습니다.

하지만 Holm correction을 하면 p-value가 0.11로 올라가서 통계적으로 유의하지 않습니다. 또한 single seed 실험이라 variance가 큽니다.

결론적으로, retraining은 mechanism-dependent합니다. 모든 케이스에 효과적이진 않고, 어떤 종류의 shift인지에 따라 다릅니다.
