# UAI arXiv replacement: author review package

Status: prepared and locally validated; **not submitted to arXiv**. Public baseline is [2601.00908v2](https://arxiv.org/abs/2601.00908v2), retrieved 9 October 2026 KST. `v3` in filenames is a proposed next version, not an accepted version identifier. This corrects the preprint; it does not claim a publisher-issued correction.

## 내일 검토할 파일

- `UAI_2601.00908_v3_proposed.pdf`: 최종 24쪽 원고.
- `UAI_2601.00908_v3_proposed_source.zip`: 7개 파일, `main.tex`를 루트에서 pdfLaTeX로 컴파일. 참고문헌 `.bbl`과 `.bib`, 사용한 그림 3개, 클래스 파일 포함.
- `arxiv-change-comments.txt`: 변경 설명 초안.
- `arxiv-metadata.json`: 수정된 초록과 메타데이터 초안. 기존 공개 초록을 그대로 두면 정정 원고와 충돌하므로 함께 교체해야 함.
- [검증 기록](../../audit/2026-10-09/replacement/package-validation.json), [공개 v2 대비 소스 차이](../../audit/2026-10-09/replacement/public-to-final.diff), [초기 검토](../../audit/2026-10-09/replacement/independent-review-initial.md), [수정 후 재검토](../../audit/2026-10-09/replacement/independent-review-recheck.md).

이 파일들이 이번 리뷰 대상이다. `paper/main.pdf`, 기존 camera-ready ZIP, 10월 8일 PDF, 10월 9일의 이전 23쪽 PDF는 역사적 스냅샷이며 이번 업로드 파일이 아니다. 원본은 보존했다.

## 과학적으로 검토해야 할 변경

| 쟁점 | 공개 v2/원래 연구 | 수정본의 주장과 한계 |
|---|---|---|
| 집중도와 coverage 하락 | 양의 상관을 사전 배포 진단의 근거로 해석 | 16개·17개 과제의 상관은 반올림된 과거 요약 수치의 산술 재현이다. 별도 복구 후속 패널은 −0.238/−0.262이며 기존 양의 관계를 재현하지 않는다. 모집단 음의 관계나 동등성을 입증하는 것도 아니다. |
| 원래 실험과 후속 패널 | 원래 50시드 결과 | 원래 모델·예측·SHAP 원장은 미복구. 후속 연구는 8과제×3시드이고 표본 크기, 설정, 전처리, 클래스 어휘, 128행 SHAP 프로토콜이 다르다. 원래 실험의 정확한 재실행으로 부르지 않는다. |
| APS와 정리 | 서로 다른 집합 정의와 SHAP 기반 해석 | inclusive inversion/crossing sets를 구분한다. 정리는 명시적 가정의 확률 혼합 가중치에 관한 것이며, 관측 SHAP 집중도와 동일하지 않다. 작은 분위수 수준 차이가 작은 coverage 차이를 보장하지 않는다. |
| 통계적 추론 | ICC, 클래스 수, 여러 상관·시드 검정의 강한 해석 | 공유 데이터·과제 의존성, 선택·다중검정, 조건부 시드 변동성을 명시한다. 원래 검정/구간은 검증된 새 결과로 취급하지 않는다. |
| 조인과 COVID 설명 | 변화 원인을 팬데믹 기제로 해석 | 고정된 복구 스냅샷에서 날짜로 잘린 조인의 모든 테스트 ID 누락을 확인한 기록이 있다. 이것이 모든 과거 결과의 원인이었다고 단정하지 않는다. |
| 강건성과 배포 | 하이퍼파라미터 강건성, 40% 임계값, 운영 지침 | 실제 재학습 근거가 없는 강건성 표의 실증 해석과 배포 권고를 철회한다. 후속 연구가 이 주장을 복구하지 않는다. |

이번 최종 검토에서 SHAP bootstrap 안정성, COVID 인과 해석, null-shift 단정, WILDS 코드 미복구라는 모순, RAPS 원인 설명, 독립적으로 읽힐 때 과장되는 표 캡션을 추가 정정했다. 학습 어휘 밖의 라벨은 uncovered로 집계하며, 작은 coverage drop이 90% coverage 달성을 뜻하지 않는다는 점도 명시했다. 이전 최신본 대비 22개 표 본문·정리·증명·초록·그림 수치는 그대로다.

## What was verified in this session

1. Fresh official arXiv v2 source and PDF were downloaded. Its `main.tex` exactly matches the archived camera-ready ZIP. The earlier ZIP uses parent-directory figure paths; this new archive puts all required files under its own root.
2. Eight statistical checks and five deterministic quantile/confidence witnesses passed. Separate review recomputed rounded historical correlations, all six threshold rows, 620/40,320 exact-permutation arithmetic, model-family correlations and all 24 cells of the recovered-panel table.
3. The 24-model/528-array refit is an **earlier audit result**, not new training in this session. Private raw inputs/checkpoints were not replayed here. The source ZIP contains manuscript inputs, not a public end-to-end experiment package. Private recovery access remains necessary for raw replay; original 50-seed artifacts remain missing.
4. The exact final ZIP compiled in an isolated directory with three `pdflatex -no-shell-escape -interaction=nonstopmode -halt-on-error main.tex` passes. No undefined citations/references or overfull boxes. All 24 pages were visually inspected in rendered contact sheets. Local TeX Live 2023 verification does not certify arXiv's server build; an eventual upload still requires its PDF preview check.
5. Two separate AI reviewer passes (initial and targeted recheck) are retained. These are model-assisted checks with shared model/tool limitations, not independent human peer review or external empirical replication.

## Replacement description draft

Material post-publication correction. We distinguish unverified historical 50-seed experiments from a separate recovered eight-task, three-seed follow-up, which does not reproduce the original positive concentration–coverage-drop association. We correct APS conventions, theorem assumptions and statistical interpretations, document preprocessing/calibration and recovered-join limitations, and withdraw unsupported hyperparameter-robustness and deployment claims. Historical summaries remain explicitly labeled; missing original execution evidence is not supplied by the new follow-up.

No replacement page was opened or submitted. Linear must remain incomplete until a real arXiv receipt or announced version is available. Official packaging and change-comment guidance checked: https://info.arxiv.org/help/submit_tex.html and https://info.arxiv.org/help/replace.html.
