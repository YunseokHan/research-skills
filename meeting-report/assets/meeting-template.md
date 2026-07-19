# 1. Summary

> 1. 핵심 실험 A
> 2. 핵심 실험 B
> 3. 현재 병목과 후속 계획

# 2. Baseline

- Data split 및 sample 수
- Frames, resolution, sampler, guidance
- Repetitions/seeds 및 uncertainty

| configuration / arm | 핵심 지표 A | 핵심 지표 B | 주요 guardrail / cost | 비고 |
| --- | ---: | ---: | ---: | --- |
| control | — | — | — | — |
| proposed | — | — | — | — |

- 핵심 baseline gap 또는 유지해야 할 성능

**의미.** 이 baseline은 이후 결과가 해결해야 하는 핵심 격차와 유지해야 하는 guardrail을 구분한다. 후속 실험은 이 기준에서 어떤 원인을 제거했는지 판단한다.

# 3. Major result

## 3.1. Protocol

- Data split, sample 수, seeds
- Training 또는 inference budget
- Control과 treatment의 matched 조건

**의미.** 이 protocol은 관찰된 차이를 treatment에 귀속할 수 있는 범위와 아직 남아 있는 confound를 규정한다. 결과 해석은 여기에서 고정한 비교 조건을 벗어나지 않는다.

## 3.2. Results

| Configuration | Metric A ↑ | Metric B ↓ | Guardrail | Status |
| --- | ---: | ---: | ---: | --- |
| Control | — | — | — | 완료 |
| Treatment | — | — | — | 완료 |

![Protocol-matched 정량 비교](../figures/mmdd_fig1.png)

- Primary result
- Trade-off
- Unsupported claim 또는 남은 uncertainty

**의미.** 이 결과는 treatment가 control 대비 바꾼 지표와 그 대가를 함께 보여준다. 다음 결정은 primary metric의 개선이 guardrail 저하 없이 유지되는지에 따라 달라진다.

## 3.3. Qualitative results

![동일 조건의 representative montage](../figures/mmdd_fig2.png)

- 반복적으로 관찰되는 visual difference
- Artifact, stasis, collapse 여부

**의미.** 정성 결과는 aggregate metric이 놓칠 수 있는 구조 붕괴, 정지, smoothing을 확인하기 위한 근거다. 수치와 영상의 판정이 충돌하면 원인을 분리하기 전까지 결론을 보류한다.

## 3.4. Conclusion

- 기각
  - Evidence bundle이 지지하는 범위
- 유지 가능한 주장
  - Control 대비 확인된 효과
- 미검증
  - 부족한 control 또는 protocol

**의미.** 이 결론은 현재 evidence bundle이 허용하는 채택·기각 범위를 명시한다. 미검증 항목은 다음 실험의 control과 완료 조건으로 직접 이어진다.

# 4. Active experiments

| Experiment | Status | Progress / ETA | Decision target |
| --- | --- | --- | --- |
| Experiment A | 진행 중 | — | — |
| Experiment B | 발표 자료 대기 | — | — |

- 완료 판정에 필요한 table, figure, montage

**의미.** 이 상태표는 진행률을 결과처럼 해석하지 않고, 각 작업이 어떤 decision bundle을 제공해야 하는지 추적하기 위한 장치다. ETA 변화보다 완료 근거의 착지가 우선이다.

# 5. Research plan

## 5.1. Component A

- PASS 조건
  - 다음 단계
- FAIL 조건
  - 중단 또는 대체 방향

**의미.** 이 분기는 Component A의 결과가 전체 연구 순서를 어떻게 바꾸는지 사전에 고정한다. PASS와 FAIL 모두 다음 행동을 정의해 사후적 해석 변경을 방지한다.

## 5.2. Component B

- Matched comparison
- Required evaluation bundle

**의미.** 이 비교는 Component B의 독립 효과를 다른 변경점과 분리하기 위한 계획이다. 동일 budget과 evaluation bundle이 충족될 때만 방향 결정을 내린다.

# 6. TODO

- [ ] Decision-grade experiment
- [ ] Quantitative plot
- [ ] Representative montage 및 full-video review
- [ ] 결과에 따른 living-document 갱신
