# 연구 레포 구조 리팩토링 지시문

아래 내용을 새 Codex/Claude Code 세션에 그대로 붙여 넣고 대괄호 부분만 채운다.

```text
$refactor-research-repo를 사용해 [TARGET_REPOSITORY_PATH]를 지속 가능한 연구 레포 구조로 리팩토링해줘.

목표는 현재 동작을 보존하면서 다음 책임을 명확히 분리하는 것이다.

1. active codebase: 프로젝트의 실제 package 이름을 유지하고 models/data/eval/training·inference 등 책임별로
   정리한다. import 가능한 핵심 로직과 실행/orchestration 로직을 분리하고, 검증된 비활성 코드는 삭제하지
   말고 active import closure 밖의 archive로 이동한다.
2. documents: docs/METHOD.md는 현재 방법·recipe·evaluation contract, docs/ROADMAP.md는 미래 계획만,
   docs/LESSON.md는 pointer-only index, docs/lessons/는 주제별 verdict·negative result·risk·reopen 조건,
   docs/CODE_STRUCTURE.md는 실제 코드 배치와 entrypoint, docs/meetings/는 날짜별 연구 delta,
   docs/surveys/는 검증된 prior art를 담당하게 한다. 같은 사실의 authoritative owner를 하나로 정하고
   코드·방법·결과·계획 변경 시 관련 living docs를 같은 변경에서 갱신하도록 AGENTS.md/CLAUDE.md에 규칙을 둔다.
3. execution: scripts/에 공통 dispatcher, train/infer/eval wrapper, experiment orchestrator, watcher,
   report builder, archive를 구분한다. 장기 작업은 preflight, manifest, DONE/FAILED, external watcher,
   idempotent retry/transition 규칙을 가져야 한다.
4. supporting structure: configs/, tests/, .env.example, ignored cache/logs/outputs 경계를 정리한다. secret,
   machine-specific path, dataset, checkpoint, cache, generated binary를 소스 트리에 섞거나 커밋하지 않는다.
5. writing: 실제 논문/submission artifact가 이미 있을 때만 docs/writing/을 만든다. FACTS.md와 STATUS.md를
   두고 sections/tables/figs/bibliography와 venue-provided template을 분리하여 특정 학회에 종속되지 않게 한다.
   기존 학회 style/class 파일은 수정하지 않는다.
6. Codex–Claude 역할: Codex는 Claude Code의 대화 문맥·주장·변경·실행 결과를 독립 감사하는 supervisor,
   Claude는 shared policy 아래의 bounded implementation/GPU operator로 정의한다. Claude의 write/GPU 요청이
   현재 목적·최신 사용자 정정·living docs·protocol·resource/provenance/watcher/docs gate와 일치하면 Codex가
   매번 사용자 승인을 다시 묻지 않고 즉시 실행·검증·후속 queue 전환할 수 있게 한다. destructive data,
   credential/access, 외부 게시, 타인 자원, 모호한 연구 방향 변경은 자동 권한에서 제외한다. Claude 보고는
   항상 직전 사용자–Claude 대화를 함께 읽어 wrong-task 응답, 정정 누락, experiment identity 혼동, 미이행
   follow-up을 감사하고, 상태 질문에는 node/job별 상태·근거 수준·병목·risk·ETA·다음 자동 작업을 줄글로
   설명하게 한다. transcript/report 위치는 ignored env로만 설정하고 개인 경로나 내용을 커밋하지 않는다.

작업 절차:
- 먼저 모든 repository instruction과 git status를 읽고, bundled audit로 code/docs/scripts/artifact inventory를
  만든다.
- reference 레포의 AGENTS.md/CLAUDE.md에 있는 모든 normative section을 훑고 `source rule → portable invariant
  → target parameter/evidence → target owner → excluded literal` policy-transfer ledger를 만든다. 문서 규율,
  lesson-first ideation, primary-source novelty check, code/archive ownership, env/secret, test/preflight,
  shared-compute ownership·watcher·reclamation, held-out matched evaluation, 결과 bundle, paper sync, honesty/rebuttal
  규율은 target에 적용 가능한 형태로 이식한다.
- current path → target path → consumer/import/command → docs owner → risk 형식의 migration map을 제시한다.
- 사용자 변경을 보존하고, 구조 변경과 알고리즘 변경을 섞지 않는다. 불확실한 active/dead 판정이나
  breaking command 변경만 질문한다.
- 작은 dependency-safe 단위로 이동하면서 imports, entrypoints, configs, tests, README, CODE_STRUCTURE를
  함께 갱신한다. 기존 파일을 대량 삭제하거나 결과를 새로 해석하지 않는다.
- 최종적으로 tests/import smoke/command dry-run/docs link/audit를 실행하고, 변경된 트리, 호환 shim,
  archive 항목, 외부·generated 상태, 남은 blocker를 보고한다. AGENTS.md와 CLAUDE.md의 supervisor/operator
  역할, autonomous validity gate, conversational-context audit 규칙이 서로 일치하는지도 검증한다.

[REFERENCE_REPOSITORY_PATH]는 구조와 운영 규율의 참고 자료일 뿐이다. 여기의 프로젝트명, 방법론, GPU 서버,
metric, 데이터 경로, 학회 템플릿을 target에 그대로 복사하지 마라. 폴더명보다 문서 ownership, evidence
discipline, reproducible execution, history preservation을 우선하라. 단, project-specific literal을 제외한다는
이유로 일반적인 규율까지 누락하지 말고, target evidence로 parameterize할 수 없는 항목은 명시적 placeholder와
blocker로 남겨라.
```
