# 1. Intro

지난 미팅 이후 바뀐 핵심 연구 상태를 2–4개 bullet로 요약.

- **핵심 진척**: 이전 상태 → 현재 상태.
- **현재 병목**: 검증된 증거와 남은 불확실성.
- **이번 미팅의 결정**: 결과가 요구하는 다음 선택.

---

# 2. Method / Architecture

## 2.1. Motivation

현재 설계가 해결하려는 구체적 문제.

## 2.2. Changed component

필요한 경우에만 수식 또는 실행 흐름을 추가.

⇒ 이전 미팅 대비 달라진 방법론적 의미.

---

# 3. Results

프로젝트 규칙에 맞는 정확한 protocol: data split, sample 수, repetitions/seeds, budget, evaluation setting.

| configuration / arm | 핵심 지표 A | 핵심 지표 B | 주요 guardrail / cost | 비고 |
| --- | ---: | ---: | ---: | --- |
| control | — | — | — | — |
| proposed | — | — | — | — |

![정량 비교](../figures/mmdd_fig1.png)

![동일 조건 정성 비교](../figures/mmdd_fig2.png)

⇒ 수치와 시각 결과가 함께 지지하는 범위의 결론만 작성.

---

# 4. Current Bottleneck

- **Verified**: 직접 확인된 현상.
- **Unknown**: 아직 분리되지 않은 원인.
- **Decision gate**: 다음 실험이 어느 방향을 선택하게 하는지.

---

## TODO

1. 다음 decision-grade 실험과 판정 기준.
2. 필요한 평가/정성 자료.
3. 결과에 따른 분기.
