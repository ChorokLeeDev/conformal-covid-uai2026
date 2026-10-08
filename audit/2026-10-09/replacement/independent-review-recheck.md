# Independent UAI targeted recheck

Date: 2026-10-09 Asia/Seoul. Scope: compare current `paper/main.tex` against frozen commit `72132d32f8671fa099711211a5f54f0f55b22caf`; recheck only the findings in `uai-review-initial.md`. No manuscript edits or model refits were performed by this reviewer.

Reviewed manuscript SHA256: `61585b20caacdd4e7ab7b14f7ebcf0c4d8ecfb79335032e44a68ad0d9c540dc8`.

## Resolution

All six material residual findings from the initial review are addressed:

| Finding | Resolution |
|---|---|
| UAI-R1: unsupported SHAP stability / asserted power explanation | Historical bootstrap claim is now explicitly unverified; reduced sample size is described without claiming the cause of a p-value change. |
| UAI-R2: causal COVID explanation of per-feature shift | Both table notes now distinguish historical encoded-sample summaries from interpretable population shift; the unsupported pandemic explanation is removed. |
| UAI-R3: null-shift caption | Intended comparison conditions no longer assert absence of relevant shift or necessarily low concentration. |
| UAI-R4: WILDS provenance contradiction | Recovered candidate code is acknowledged separately from missing outputs/execution provenance. Section, caption and combined benchmark arithmetic are correctly labeled historical; no independent specificity is claimed. |
| UAI-R5: RAPS interpretation/ranking | Incorrect “most concentrated” claim is removed; the paired-test provenance gap and inability to identify a calibration mechanism are explicit. |
| UAI-R6: standalone claims | Main results, diagnostic comparison and baseline captions identify historical/unverified status; the SHAP footnote disclaims prospective validity. The unchanged n16 plot's caption already explicitly identifies its pre-deployment label/cutoff as historical. Added mechanism/feature-importance caption qualifications make their status clear. |

The added unknown-label sentence is consistent with a direct code inspection of `audit/2026-10-08/recovery/replay_recovered_evidence.py::metrics`: `hits` starts false for every record, and only `y >= 0` positions are assigned set membership. Unknown labels therefore remain uncovered regardless of threshold. The new sentence also correctly separates a small source-to-target drop from attainment of 90% target coverage.

## Change-integrity checks

- All 22 LaTeX `tabular` blocks are byte-identical to the frozen manuscript. No table cells, task means, correlation rows, interval values or threshold counts were changed.
- The theorem, proof and abstract are byte-identical to the frozen manuscript.
- All three included PDF figures are byte-identical to the frozen versions. Historical plot wording is handled through explicit captions, not presented as newly regenerated experimental evidence.
- Reviewed the complete `main.tex` diff: changes are qualifications, removal of unsupported interpretations, corrected provenance labels and the unknown-label estimand disclosure. No new empirical result or unsupported numerical claim was introduced.

## Judgment and remaining limits

No unresolved substantive issue from this targeted review prevents using the revised manuscript as a transparent correction of the earlier scientific claims. This is not validation of the original experiment or a prospective diagnostic. The original 50-seed model/prediction/SHAP ledgers remain missing; I checked saved aggregate arithmetic and receipts rather than independently rerunning the private raw follow-up payload. The follow-up is a different experiment and does not establish a population null, a recovered original mechanism, or restored target coverage.

The correction package's clean build, visual layout and arXiv upload readiness are handled by the root agent. This recheck does not establish arXiv acceptance/submission or authorize marking any issue complete.
