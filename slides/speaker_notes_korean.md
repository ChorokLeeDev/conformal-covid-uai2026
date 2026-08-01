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

먼저 Conformal Prediction이 뭔지, 왜 중요한지 말씀드리겠습니다.

머신러닝 모델이 예측을 할 때, 보통은 "이 환자는 당뇨병입니다"처럼 하나의 답만 줍니다. 하지만 실제로는 "당뇨병일 수도 있고, 고혈압일 수도 있다"처럼 불확실성이 있죠.

Conformal Prediction은 이 불확실성을 정량화하는 프레임워크입니다. 하나의 답 대신 "가능한 답들의 집합"을 줍니다. 예를 들어 "이 환자는 {당뇨병, 고혈압} 중 하나입니다"라고 알려주는 거죠.

세 가지 핵심 장점이 있습니다.

첫째, distribution-free입니다. 데이터가 정규분포를 따른다, 이런 가정이 필요 없습니다. 오직 "calibration 데이터와 test 데이터가 같은 분포에서 나왔다"는 가정만 필요합니다. 이걸 교환가능성이라고 부릅니다.

둘째, 어떤 모델과도 작동합니다. LightGBM이든, 딥러닝이든, 심지어 블랙박스 API여도 됩니다. 모델 위에 얹는 wrapper 같은 거라고 생각하시면 됩니다.

셋째, 유한 샘플에서도 보장이 정확합니다. 보통 통계적 보장은 "샘플이 무한히 많으면 성립한다"는 점근적 보장인데요, conformal prediction은 샘플이 100개든 1000개든 exact하게 성립합니다. 왜냐하면 score의 절대값이 아니라 순위만 보기 때문입니다. n개 calibration 샘플이 있으면, test 샘플 포함 n+1개의 순서가 교환가능성 하에서 equally likely합니다. 순수하게 combinatorial한 argument로 보장이 나옵니다.

우리는 90% 커버리지를 목표로 합니다. 이 말은, "내가 주는 예측 집합 안에 정답이 90% 확률로 들어있다"는 뜻입니다.

하지만 여기엔 숨겨진 함정이 있습니다.

---

## 슬라이드 3: The Hidden Assumption (45초)

바로 교환가능성 가정입니다.

방금 말씀드렸듯이, conformal prediction이 작동하려면 calibration 데이터와 test 데이터가 같은 분포에서 나와야 합니다.

그런데 현실에서 이 가정이 깨지는 경우가 정말 많습니다. 이걸 distribution shift라고 부릅니다.

예를 들어볼게요. COVID-19가 터지기 전에 학습한 물류 예측 모델이 있다고 합시다. 팬데믹 이후에 소비 패턴이 완전히 바뀌었죠. 마스크, 손소독제 수요가 폭증하고, 여행 관련 상품은 급감했습니다. 이러면 calibration할 때 본 데이터와 실제 서비스할 때 보는 데이터가 완전히 다릅니다.

다른 예로, 서울에서 학습한 모델을 부산에 배포하면 지역 특성 때문에 분포가 다를 수 있고, 젊은 사용자로 학습했는데 노년층 사용자가 유입되면 또 다릅니다.

이렇게 distribution shift가 발생하면, conformal prediction의 90% 커버리지 보장이 깨집니다. 심하면 커버리지가 10%까지 떨어질 수 있습니다.

---

## 슬라이드 4: The Research Gap (1분)

그러면 기존에 distribution shift를 탐지하는 방법은 없었을까요? 있습니다. MMD, C2ST, PSI 같은 방법들이요.

MMD는 Maximum Mean Discrepancy의 약자로, 두 분포가 다른지 kernel 기반으로 테스트합니다. C2ST는 Classifier Two-Sample Test로, classifier가 두 데이터를 구분할 수 있으면 분포가 다르다고 판단합니다.

문제는, 이 방법들이 shift를 탐지는 하는데, 그게 얼마나 심각한지는 모릅니다.

비유를 들어볼게요. 의사가 "당신 몸에 이상이 있습니다"라고만 말하고, 그게 감기인지 암인지는 안 알려주는 거예요. 모든 환자한테 "이상 있음"이라고만 하면, 누구를 먼저 치료해야 할지 모르잖아요.

마찬가지로, 기존 방법들은 8개 태스크 모두에서 "shift 있음"이라고 알려주지만, 어떤 태스크가 90%에서 85%로 약간만 떨어지고, 어떤 태스크가 90%에서 10%로 catastrophic하게 실패할지 구분하지 못합니다.

우리의 연구 질문은 이겁니다: **배포하기 전에, 이 모델이 shift에 얼마나 취약한지 예측할 수 있을까?**

---

## 슬라이드 5: Conformal Prediction Primer (1분)

기술적인 내용을 좀 더 설명드리겠습니다. Conformal prediction이 어떻게 작동하는지요.

K개 클래스 분류 문제가 있다고 합시다. 예를 들어 7가지 산림 유형을 분류하는 문제요.

첫 번째 단계로, nonconformity score라는 걸 정의합니다. 직관적으로, "이 샘플이 얼마나 이상한가"를 숫자로 나타낸 겁니다. 우리가 쓰는 APS 방법에서는, 모델이 출력한 확률을 높은 순서대로 정렬한 다음, 정답 클래스까지의 누적 확률을 score로 씁니다. 정답에 높은 확률을 줬으면 score가 낮고, 정답을 뒤늦게 맞추면 score가 높습니다.

두 번째로, calibration set에서 이 score들을 다 계산하고, 90번째 percentile을 threshold로 잡습니다.

세 번째로, 새로운 test 샘플이 들어오면, 각 클래스를 정답이라고 가정하고 score를 계산합니다. Threshold보다 낮은 score를 가진 클래스들을 모아서 prediction set으로 출력합니다.

네 번째로, 데이터가 교환가능하면, 이 prediction set이 정답을 포함할 확률이 최소 90%임이 보장됩니다.

---

## 슬라이드 6: What Happens Under Distribution Shift? (45초)

그런데 distribution shift가 발생하면 어떻게 될까요?

여기 세 가지 시나리오가 있습니다.

Shift가 없으면 90.2% 커버리지로 타겟을 거의 정확히 달성합니다.

약한 shift가 있으면 85.1%로 약간 떨어집니다. 이 정도는 실무에서 감수할 수 있는 수준이죠.

하지만 심한 shift가 있으면 49.8%까지, 거의 절반으로 떨어집니다. 이건 catastrophic failure입니다. 90% 보장한다고 했는데 실제로 절반밖에 안 되면, 이 시스템을 믿고 의사결정을 내릴 수가 없잖아요.

핵심 관찰은 이겁니다: **shift의 크기만으로는 실패 정도를 예측할 수 없습니다.**

같은 COVID shift를 경험한 8개 태스크가 있는데, 어떤 건 robust하고 어떤 건 catastrophic하게 실패합니다. 왜 이런 차이가 날까요?

---

## 슬라이드 7: Conformal Prediction Pipeline (30초)

이 그림은 conformal prediction 파이프라인을 시각적으로 보여줍니다.

정상적인 상황에서는, calibration 데이터로 threshold를 정하고, 그 threshold가 test 데이터에서도 유효합니다.

하지만 distribution shift가 발생하면, calibration 때 정한 threshold가 test 데이터에는 맞지 않게 됩니다. 비유하자면, 서울 날씨로 calibration했는데 제주도 날씨를 예측하려는 거예요. 기준이 안 맞죠.

---

## 슬라이드 8: Our Key Insight (1분)

이제 우리의 핵심 통찰을 말씀드리겠습니다.

**Conformal prediction의 취약성은, 모델이 "변하는 feature"에 얼마나 의존하느냐에 따라 결정됩니다.**

슬라이드 왼쪽을 보시면, feature importance가 여러 feature에 골고루 분산되어 있습니다. 이런 모델은 일부 feature가 shift해도 전체적으로 안정적입니다.

오른쪽은 하나의 feature에 importance가 집중되어 있습니다. 이런 모델은 그 feature가 shift하면 크게 흔들립니다.

분산 투자 vs 몰빵 투자의 차이라고 보시면 됩니다.

우리는 이 집중도를 **SHAP Concentration**이라는 metric으로 측정합니다.

---

## 슬라이드 9: SHAP Concentration: The Metric (1분)

구체적인 계산 방법을 설명드리겠습니다.

먼저 SHAP이 뭔지 간단히 말씀드릴게요. SHAP은 각 feature가 예측에 얼마나 기여했는지를 측정하는 방법입니다. 게임 이론의 Shapley value에서 왔어요. 예를 들어, "이 환자가 당뇨병으로 예측된 이유의 40%는 혈당 수치 때문이고, 30%는 BMI 때문이다" 이런 식으로 알려줍니다.

Step 1에서, validation 데이터 전체에서 각 feature의 평균 SHAP 절댓값을 계산합니다.

Step 2에서, SHAP Concentration C를 계산합니다. 수식은 아주 간단합니다.

C = (1등 feature의 SHAP) / (전체 feature SHAP 합)

예를 들어 feature가 10개인데, 1등 feature가 전체의 50%를 차지하면 C = 0.5입니다. 10개가 균등하면 C = 0.1이겠죠.

해석도 간단합니다.

C가 40% 미만이면, importance가 여러 feature에 분산되어 있어서 shift에 robust합니다.
C가 40% 이상이면, 하나의 feature가 지배적이라 그 feature가 변하면 위험합니다.

핵심은, 이 metric을 **배포 전에** validation 데이터만으로 계산할 수 있다는 겁니다. Test 데이터를 안 봐도 됩니다.

---

## 슬라이드 10: Why Does Concentration Matter? (45초)

왜 concentration이 커버리지 실패와 연결될까요?

모델이 의존하는 feature가 shift하면 conformity score 분포가 변합니다.

여러 feature에 분산 의존하면, 개별 feature의 shift가 서로 평균화되어 score 분포가 안정적입니다.

한 feature에 집중 의존하면, 그 feature의 shift가 score 분포를 크게 흔듭니다.

Score 분포가 흔들리면 calibration threshold가 안 맞게 되고, 커버리지가 깨집니다.

즉, **Concentration = Fragility Amplifier**입니다.

---

## 슬라이드 11: Experimental Setup: SALT Benchmark (45초)

실험 설정을 말씀드리겠습니다.

SALT는 Supply chain ALlocaTion의 약자로, e-commerce 물류 분류를 위한 벤치마크입니다. 배송 조건, 결제 조건, 물류 센터 등 8개의 분류 태스크가 있습니다.

핵심은 **COVID-19 temporal split**입니다.

학습 데이터는 2020년 2월 이전, 즉 COVID 이전입니다.
테스트 데이터는 2020년 7월 이후, 즉 COVID 한창 때입니다.

팬데믹으로 인해 자연스러운 distribution shift가 발생했습니다. 소비 패턴, 물류 네트워크, 결제 방식 등이 다 바뀌었죠.

중요한 건, 8개 태스크가 **동일한** COVID shift를 경험했다는 겁니다. 같은 시간대, 같은 회사 데이터입니다. 그런데 결과는 태스크마다 완전히 다르게 나왔습니다.

---

## 슬라이드 12: Models and Methods (45초)

모델과 방법론입니다.

중요한 점을 먼저 말씀드리면, 우리의 diagnostic은 **GBM에 특화**되어 있습니다. GBM은 Gradient Boosting Machine의 약자로, LightGBM, XGBoost, CatBoost 같은 모델들이에요. 요즘 tabular 데이터에서 가장 많이 쓰이는 모델군입니다.

LightGBM에서 상관계수 rho가 0.833으로 가장 강했고, CatBoost와 XGBoost에서도 0.55에서 0.67 정도 나왔습니다.

반면 Random Forest와 MLP(다층 퍼셉트론)에서는 상관관계가 약했습니다. 이건 나중에 limitation에서 다시 설명드리겠습니다.

Conformal method로는 APS를 사용하고, 90% 커버리지를 타겟으로 합니다.

---

## 슬라이드 13: Experimental Setup (30초)

통계적으로 견고한 결과를 얻기 위해 철저하게 실험했습니다.

각 실험마다 50개의 random seed를 사용했습니다. 한 번 돌려서 운 좋게 나온 결과가 아니라, 50번 반복해도 일관된 결과인지 확인했습니다.

Spearman correlation을 계산하고, p-value로 통계적 유의성을 검증했습니다. Bootstrap으로 confidence interval도 구했습니다.

External validation으로는 SALT 외에 UCI 데이터셋 8개를 추가로 사용했습니다. 총 9개 도메인, 16개 태스크에서 검증했고, 91.7% 정확도를 달성했습니다.

---

## 슬라이드 14: Main Result - Strong Correlation (1분)

이제 메인 결과입니다.

이 scatter plot을 보시면, x축이 SHAP concentration이고 y축이 coverage drop입니다. Coverage drop은 "목표 90%에서 실제 커버리지가 얼마나 떨어졌나"입니다.

점들이 우상향으로 쭉 늘어서 있죠? 이게 양의 상관관계입니다.

파란 점은 SALT COVID 태스크들이고, 주황 삼각형은 external validation 데이터셋들입니다.

Spearman rho가 0.853입니다. 1에 가까울수록 강한 상관관계인데, 0.853은 "매우 강함"에 해당합니다. p-value는 0.001 미만으로, 우연히 이런 상관관계가 나올 확률이 0.1% 미만이라는 뜻입니다.

9개 도메인에 걸친 16개 multiclass 태스크에서 이 결과를 얻었습니다.

이것이 primary finding입니다: **SHAP concentration이 높으면 커버리지 실패가 심하고, 낮으면 robust합니다.**

---

## 슬라이드 15: Within SALT COVID Tasks (45초)

SALT 내에서만 더 자세히 보겠습니다.

8개 태스크에서 rho 0.833, p-value 0.010입니다.

테이블을 보시면, concentration 순서대로 정렬되어 있습니다.

맨 위 s-payterms는 concentration이 54.2%로 가장 높습니다. 결제 조건을 예측하는 태스크인데, 하나의 feature에 절반 이상 의존하고 있어요. 결과적으로 커버리지가 13.7%까지 떨어졌습니다. 90%에서 77 percentage point나 떨어진 거죠. Catastrophic failure입니다.

반면 맨 아래 s-incoterms는 concentration이 23.7%로 낮습니다. 커버리지가 87%로 거의 유지됐습니다. 같은 COVID shift인데 robust했어요.

같은 시간대, 같은 회사, 같은 shift를 경험했는데 결과가 이렇게 다릅니다. 그 차이를 설명하는 게 SHAP concentration입니다.

---

## 슬라이드 16: Comparison with Standard Detectors (45초)

그러면 기존 shift detector들은 왜 이런 구분을 못 할까요?

표를 보시면, SHAP Concentration은 rho 0.853으로 strong입니다.
MMD는 rho 0.19, C2ST는 0.15, PSI는 0.12입니다. 거의 상관관계가 없어요.

왜 이런 차이가 날까요?

기존 방법들은 **marginal distribution shift**만 측정합니다. "전체 데이터 분포가 바뀌었는가?"만 보는 거예요. 8개 태스크 모두 COVID shift가 있으니까, 8개 모두 "shift 있음"이라고 나옵니다. 구분이 안 되죠.

우리 방법은 **model-relevant shift**를 측정합니다. "모델이 실제로 의존하는 feature가 바뀌었는가?"를 보는 거예요. 모델마다 의존하는 feature가 다르니까, 같은 shift라도 영향이 다르게 나타납니다.

---

## 슬라이드 17: External Validation - Covertype (45초)

External validation 중 가장 극적인 케이스를 보여드리겠습니다.

Covertype은 UCI에서 제공하는 유명한 데이터셋입니다. 산림 유형을 분류하는 문제로, 7개 클래스와 54개 feature가 있습니다. 고도, 경사, 토양 유형 같은 지형 정보로 어떤 나무가 자라는지 예측합니다.

우리는 geographic split을 적용했습니다. Wilderness Area 1, 2에서 학습하고, Area 4에서 테스트했습니다. 지역이 다르니까 지형 특성이 다르고, 자연스러운 distribution shift가 발생합니다.

결과를 보시면, SHAP Concentration이 49.8%로 높았습니다. 40% threshold를 넘었죠.

Target coverage는 90%였는데, actual coverage는 8.2%였습니다. **81.8 percentage point나 떨어진 catastrophic failure**입니다. 90% 보장한다고 했는데 실제로 10명 중 1명도 안 맞는 거예요.

이 실패를 우리 방법이 **배포 전에** 정확히 예측했습니다. 10개 seed 모두에서 deterministic하게요.

---

## 슬라이드 18: Model Sensitivity Analysis (45초)

모델별로 우리 diagnostic이 얼마나 잘 작동하는지 분석했습니다.

LightGBM은 rho 0.833으로 잘 작동합니다.
CatBoost는 0.667, XGBoost는 0.548로 역시 유의미합니다.
하지만 Random Forest는 0.300, MLP는 0.430으로 상관관계가 약합니다.

왜 이런 차이가 날까요?

GBM 계열은 sequential boosting을 합니다. 앞의 tree가 틀린 부분을 다음 tree가 집중적으로 학습해요. 이 과정에서 특정 feature에 concentrated dependence가 만들어집니다.

Random Forest는 bagging을 합니다. 여러 tree가 서로 다른 feature subset을 랜덤하게 보기 때문에, single-feature reliance가 자연스럽게 희석됩니다.

MLP는 아예 다른 메커니즘으로 실패합니다. Concentrated dependence가 아니라, 여러 feature가 coordinated하게 영향을 미쳐서 실패해요. 이건 우리 diagnostic이 포착하지 못합니다.

---

## 슬라이드 19: Theoretical Foundation (1분)

지금까지 경험적 결과를 보여드렸는데, 이론적으로도 뒷받침됩니다.

우리 논문에서 Theorem을 증명했습니다.

간단히 말씀드리면, SHAP concentration이 높을수록 APS score의 expected deviation bound가 커집니다. 그리고 이 bound는 concentration에 대해 단조 증가합니다.

수식적으로는, score perturbation의 upper bound가 concentration의 함수로 표현되는데, 이 함수가 monotonically increasing합니다.

핵심 함의는 세 가지입니다.

첫째, 높은 concentration → 큰 score perturbation bound
둘째, score perturbation → calibration threshold 불일치 → coverage deviation
셋째, 따라서 concentration은 **fragility amplifier**로 작용합니다.

자세한 증명은 paper Appendix에 있습니다. 관심 있으신 분들은 참고해주세요.

---

## 슬라이드 20: Intuition Behind the Theorem (45초)

이론의 직관을 그림으로 설명드리겠습니다.

왼쪽은 Low Concentration 케이스입니다. Feature importance가 여러 feature에 골고루 분포되어 있습니다. Feature 1이 shift해도, 전체 importance에서 차지하는 비중이 작으니까 score perturbation이 작습니다.

오른쪽은 High Concentration 케이스입니다. Feature 1 하나가 importance의 대부분을 차지합니다. Feature 1이 shift하면, 그게 곧 전체 score의 shift로 이어집니다.

---

## 슬라이드 21: Operational Framework (1분)

실용적으로 어떻게 쓰면 되는지, 3-Step Protocol을 제안합니다.

**Step 1**: C를 계산합니다. 모델을 학습한 후, validation 데이터에서 SHAP을 계산하고, top feature의 비율을 구합니다.

**Step 2**: 40% threshold와 비교합니다.

**Step 3**: 결정을 내립니다.
- C < 40%: 낮은 위험으로 판단하고 배포합니다.
- C ≥ 40%: 취약하다고 판단하고 mitigation을 고려합니다.

40% threshold는 우리 데이터에서 경험적으로 도출한 값입니다. Catastrophic failure가 발생한 태스크와 robust한 태스크 사이에 natural gap이 40% 근처에 있었어요.

단, 이 threshold는 exploratory합니다. SALT 8개 태스크에서 도출했기 때문에, 다른 도메인에서는 prospective validation이 필요합니다.

---

## 슬라이드 22: Mitigation Strategies (45초)

C가 40%를 넘어서 취약하다고 판단되면 어떻게 해야 할까요?

세 가지 mitigation 전략을 제안합니다.

첫째, **Feature Engineering**입니다. Dominant feature에 대한 의존도를 줄이기 위해 새로운 feature를 추가하거나, 기존 feature를 transform합니다. 예를 들어, 하나의 강력한 feature를 여러 개의 약한 feature로 분해할 수 있습니다.

둘째, **Model Regularization**입니다. Feature dropout을 적용하거나, diverse subset으로 ensemble을 구성합니다. 모델이 특정 feature에 과도하게 의존하지 않도록 강제하는 거죠.

셋째, **Monitoring**입니다. C를 지속적으로 추적하고, threshold를 넘으면 alert을 발생시킵니다. 모델이 재학습되면 C도 다시 계산해야 합니다.

핵심은, **배포 후 문제가 터진 다음에 대응하는 게 아니라, 배포 전에 취약성을 파악하고 선제 대응**하는 겁니다.

---

## 슬라이드 23: Limitations (45초)

한계점을 솔직히 말씀드리겠습니다.

첫째, **tabular 데이터에 집중**했습니다. 이미지나 텍스트에서는 "feature"의 정의 자체가 달라지기 때문에, 추가 연구가 필요합니다.

둘째, **GBM에 특화**되어 있습니다. Random Forest는 rho 0.30, MLP는 0.43으로 상관관계가 약합니다. 이 모델들은 다른 failure mode를 가져서 우리 diagnostic이 맞지 않습니다.

셋째, **K가 4 이상인 multiclass에서만 작동**합니다. Binary 분류에서는 prediction set이 {0}, {1}, {0,1} 세 가지밖에 없어서 concentration mechanism이 작동할 공간이 없습니다.

넷째, **40% threshold는 exploratory**합니다. n=8에서 도출했기 때문에, prospective validation이 필요합니다.

다섯째, 이건 **diagnostic이지 solution이 아닙니다**. "당신 모델 취약해요"라고 알려줄 뿐, 자동으로 고쳐주진 않습니다.

---

## 슬라이드 24: Future Directions (45초)

미래 연구 방향입니다.

**Extensions**로는, deep learning에 적용할 수 있는 gradient-based explanation 연구가 가능합니다. SHAP 대신 Integrated Gradients 같은 방법을 쓰면 어떨지요.

**Automation**으로는, C를 낮추기 위한 자동 feature engineering을 연구할 수 있습니다. "이 feature를 이렇게 transform하면 concentration이 낮아집니다" 같은 추천을 해주는 거죠.

**Theory**로는, distribution-specific coverage bounds를 더 정교하게 도출할 수 있습니다. "이런 종류의 shift에서는 이만큼 떨어진다" 같은 더 구체적인 예측이요.

Open questions도 있습니다. 본질적으로 low-concentration인 모델을 설계할 수 있을까요? Online setting에서 concentration을 실시간 monitoring하려면 어떻게 해야 할까요?

---

## 슬라이드 25: Conclusion (1분)

결론입니다.

**SHAP Concentration**은 Conformal Prediction 취약성을 위한 **Pre-Deployment Diagnostic**입니다.

세 가지 기여를 했습니다.

첫째, **predictive metric**을 제안했습니다. Spearman rho 0.853, 95% CI [0.50, 0.96]입니다. GBM classifier에서요.

둘째, **validation**을 철저히 했습니다. Leave-one-out CV에서 87.5%, 9개 도메인 external validation에서 91.7% 정확도입니다.

셋째, **practical protocol**을 제안했습니다. 40% threshold를 기준으로 한 3-step framework입니다.

**Scope**는 K ≥ 4인 multiclass GBM classifier입니다.

**Impact**는, 실패가 발생하기 **전에** 취약한 배포를 proactive하게 식별할 수 있다는 겁니다. 배포하고 나서 "왜 안 되지?" 하는 게 아니라, 배포 전에 "이 모델은 위험하니까 조심하자"를 알 수 있습니다.

감사합니다. 질문 받겠습니다.

---

## Backup 슬라이드 (26-28)

### 슬라이드 26: Full Results Table
- 8 SALT + 8 external = 16 multiclass tasks
- 9 domains: SALT(COVID), Covertype, KDDCup99, PAMAP2, Gas Sensor, Shuttle, Pendigits, Satimage, Avila
- Covertype가 가장 극적인 external case (81.8pp drop)

### 슬라이드 27: SHAP Computation Details
- TreeSHAP 사용, 정확한 SHAP 값 (근사치 아님)
- Validation 데이터에서만 계산 (pre-deployment)

### 슬라이드 28: Statistical Analysis
- Spearman correlation: rank 기반, outlier에 robust
- Baseline 비교: MMD, C2ST, PSI 모두 ρ < 0.2로 실패 심각도 예측 못함

---

## Q&A 준비 (예상 질문과 답변)

**Q1: "왜 Random Forest나 MLP에는 작동하지 않나요?"**

Random Forest는 bagging을 해서 concentration을 희석시킵니다. 여러 tree가 서로 다른 feature subset을 보기 때문에, 전체적으로 single-feature reliance가 낮아집니다. 그래서 concentration이 높아도 실제로는 분산되어 있어서 robust할 수 있어요.

MLP는 다른 failure mode를 가집니다. MLP에서 SHAP을 계산하면 local approximation이라서 정확하지 않고, 무엇보다 MLP의 failure는 concentrated dependence가 아니라 여러 feature가 coordinated하게 영향을 미쳐서 발생합니다. 이걸 global sensitivity failure라고 부르는데, 우리 metric은 이걸 포착하지 못합니다.

**Q2: "40% threshold는 어떻게 도출했나요?"**

SALT n=8에서 경험적으로 도출했습니다. Catastrophic failure가 발생한 태스크들(coverage < 50%)과 robust한 태스크들(coverage > 80%) 사이에 natural gap이 40% 근처에 있었습니다.

하지만 이건 exploratory한 값입니다. n=8은 작은 샘플이고, 이 threshold가 다른 도메인에서도 일반화되는지는 prospective validation이 필요합니다. 35%에서 45% 구간은 uncertainty band로 보고, 이 구간에 있으면 추가 monitoring을 권장합니다.

**Q3: "Binary classification에는 적용 안 되나요?"**

네, K ≤ 3에서는 작동하지 않습니다. APS prediction set을 생각해보세요. Binary면 가능한 prediction set이 {}, {0}, {1}, {0,1} 네 가지뿐입니다. 3-class면 조금 더 많지만 여전히 제한적이에요.

Prediction set의 다양성이 충분해야 concentration의 영향이 나타나는데, K가 작으면 structural ceiling 때문에 이 mechanism이 작동하지 않습니다. K ≥ 4여야 prediction set 구성의 자유도가 충분합니다.

**Q4: "이미지나 텍스트 데이터에는 어떻게 확장하나요?"**

현재는 tabular에 집중했습니다. 이미지나 텍스트로 확장하려면 몇 가지 도전이 있습니다.

첫째, "feature"의 정의가 명확하지 않습니다. 이미지에서 feature가 pixel인지, superpixel인지, object인지 정해야 합니다.

둘째, SHAP computation이 훨씬 비쌉니다. ImageNet 모델에 SHAP 돌리면 하루가 걸릴 수도 있어요.

셋째, GBM이 아니라 neural network이므로, 우리가 증명한 theoretical foundation이 직접 적용되지 않습니다.

Gradient-based explanation (Integrated Gradients, GradCAM)이 유망한 방향이라고 생각합니다.

**Q5: "Retraining이 도움이 되나요?"**

일부 도움이 됩니다. 우리 실험에서 평균 19 percentage point 개선을 보였고, unadjusted p-value는 0.036이었습니다.

하지만 Holm correction을 하면 p-value가 0.11로 올라가서 통계적으로 유의하지 않습니다. 또한 single seed 실험이라 variance가 큽니다.

결론적으로, retraining은 mechanism-dependent합니다. Shift의 종류에 따라 효과가 다르고, 모든 케이스에 효과적이진 않습니다.

**Q6: "Conformal Prediction이 Bayesian 방법과 뭐가 다른가요?"**

결이 다릅니다.

Bayesian 방법은 "내 믿음(prior)을 데이터로 업데이트한 결과"를 줍니다. "이 파라미터가 진짜일 확률이 95%입니다" 같은 posterior 확률이요. 하지만 prior가 틀리면 posterior도 틀립니다.

Conformal Prediction은 "100번 하면 90번은 정답이 이 집합 안에 있습니다"라는 frequentist guarantee를 줍니다. 분포 가정 없이, 오직 교환가능성만 있으면 됩니다. 그리고 이 보장은 finite sample에서도 exact합니다.

Bayesian credible interval은 coverage를 보장하지 않지만, conformal prediction set은 보장합니다. 대신 informativensss(집합 크기)와 trade-off가 있습니다.
