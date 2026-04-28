# PRD: Magic Square (4×4) — Dual-Track UI + Logic TDD (with MLOps)

| 항목 | 값 |
|------|-----|
| 문서 버전 | 0.2 |
| 상태 | Draft |
| 목적 | 경계(UI·I/O) 트랙과 도메인(로직) 트랙을 병렬 TDD로 고정하고, 선택적 MLOps 트랙으로 운영 규율을 둔다 |

---

# 1. Executive Summary

Magic Square (4×4) 프로젝트의 목표는 난이도 높은 알고리즘 구현이 아니라, 고정된 입력/출력 계약 위에서 불변조건을 명세하고 검증하는 TDD 역량을 훈련하는 것이다. 본 PRD는 **Track A — Boundary(UI·I/O 계약)**, **Track B — Domain(순수 로직·불변조건)**, **Track C — MLOps(선택: 데이터/모델·배포·모니터링 규율)** 을 구분하고, Concept → Rule → Use Case → Contract → Test → Component 추적성을 문서 수준에서 고정하여, 동일 입력에 대해 동일 결과를 재현 가능한 방식으로 검증한다. **정답·규칙의 단일 진실원천(SSOT)은 Track B**이며, Track C의 모델/추론은 **Domain 결과를 대체하지 않는다**.

# 2. Problem Statement (문제 정의)

이 프로젝트의 문제는 "마방진 하나를 만든다"가 아니라 "4×4 보드 상태가 도메인 불변조건을 만족하는지 검증 가능한 구조로 완성한다"이다. 입력/출력 계약이 모호하면 실패 원인을 분리할 수 없고 테스트의 합격 기준이 흔들리므로, 입력 제약(크기, 값 범위, 빈칸 수, 중복 금지)과 출력 제약(형식, 인덱스, 시도 순서)을 고정 계약으로 정의해야 한다. 고정 계약은 테스트의 SSOT이며, Track A와 Track B의 책임 분리를 가능하게 한다.

# 3. Framework: Dual-Track UI + Logic and MLOps (Track C)

## 3.1 핵심 원리

- **UI는 디자인(UX·I/O 계약)으로 RED를 만들고, 로직은 규칙으로 RED를 만든다 — GREEN과 REFACTOR는 항상 함께 간다.**
- **두 트랙(Track A / Track B)의 테스트는 서로 독립적이다**: Track A 테스트는 Domain 구현 상세를 알지 않고, Track B 테스트는 화면·CLI·API 포맷을 알지 않는다.
- **Track C**는 **배포·실험·모니터링**에 대한 규율이며, **FR-01~05의 비즈니스 판정을 ML이 대체하지 않는다**.

## 3.2 Track A — UX / I/O Contract (Boundary)

- **초점**: 외부에 노출되는 **입력 검증·오류 코드·출력 배열 형식** 등 I/O 계약(슬라이드의 "UX Contract"에 대응; GUI가 없으면 콘솔·`pytest`·API 응답이 그 계약의 구현체라고 본다).
- **FR 매핑**: **FR-01** 및 Domain 예외 → 표준 오류 코드 매핑, 출력 `int[6]`·1-index 등 **경계** 책임.

## 3.3 Track B — Logic Rule (Domain)

- **초점**: **허용/거부, 계산, 판정** — BR-01~12, **FR-02~05**.

## 3.4 Track C — MLOps (선택, 보조)

- **초점**: 모델·데이터 파이프라인이 **존재할 때만** — **아티팩트 버전**, **오프라인 eval 게이트**, **서빙 입출력 스키마**, **롤백/알람**, **추론 지연·처리량** SLI. **FR-01~05와 충돌 시 항상 Track B(및 Track A의 고정 오류 계약)가 우선**한다 (결정 D-05).

# 4. Target Users

- **TDD 학습자**: RED-GREEN-REFACTOR 사이클에서 계약 기반 테스트와 불변조건 중심 설계를 훈련한다.
- **코드 리뷰어/멘토**: 요구사항 누락, 계약 위반, 레이어 경계 위반을 테스트 기준으로 점검한다.
- **사용 환경**: 콘솔 또는 테스트 러너(`pytest`) 기반 실행 환경에서 입출력 계약을 검증한다(향후 GUI를 도입해도 **동일한 오류 코드·AC** 를 Track A에서 검증한다).

# 5. Scope

## 5.1 In-Scope

- 4×4 입력 행렬의 유효성 검증(Track A / Boundary)
- row-major 기준 빈칸(0) 두 좌표 탐색(Track B)
- 1~16 기준 누락 숫자 2개 탐색(Track B)
- 완성 보드의 마방진 판정(합 상수 34)(Track B)
- 두 조합 시도 후 정답 출력 형식으로 반환(Track B + Track A 포맷)
- **(선택)** MLOps: 모델/데이터가 있을 때 **버전·평가·배포·모니터링** 절차(Track C) — **도메인 규칙 대체 아님**

## 5.2 Out-of-Scope

- **본 PRD v0.2 기준**: 웹/모바일 **풀 GUI 제품**은 Out-of-Scope. 단, **Track A는 "I/O·경계"** 이므로 이후 GUI를 In-Scope로 올릴 때 **FR/AC/오류 코드는 변경하지 않고** 화면에서 동일 계약을 검증하는 것을 권장한다.
- DB 저장/조회 및 외부 인프라 연동(필수 아님; MLOps는 **선택**으로 5.1·§7·§3.4에 한정)
- N×N 일반화(확장 로드맵 항목으로만 관리)
- 마방진 완전 생성 알고리즘 문제
- **도메인 정답을 학습 모델 출력으로 대체**하는 것

# 6. UX Contract & Logic Rule Language — 시나리오 매핑

## 6.1 언어 사전

**UX / I/O Contract (Track A)** — 바이너리·가시성 중심:

- 보인다 / 안 보인다 · 가능하다 / 불가능하다 · 활성화 / 비활성화 · (오류/성공 메시지) 포함 / 미포함

**Logic Rule (Track B)** — 판정·상태 전이:

- 허용한다 / 거부한다 · 유지한다 / 중단한다 · 반환한다 / 차단한다 · 계산한다 (저장은 본 PRD 핵심 밖)

## 6.2 Magic Square 3단 매핑 (대표 시나리오)

| 시나리오 | UX / I/O Contract (Track A) | Logic Rule (Track B) |
|----------|----------------------------|----------------------|
| 합이 34가 아닌 완성 보드로 판정 | (해당 시) 실패/검증 결과가 계약대로 **표시·반환** | `isMagic` **거부**(`false`) |
| 빈칸 수 ≠ 2 (입력) | `E_UI_BLANK_COUNT` 등 **표시** | 경계에서 **차단** |
| 올바른 입력으로 해 완성 | 성공/해 **표시** (형식 `int[6]`) | `solve` **반환** |
| 잘못된 값(범위外) | 오류 **표시** | Track A에서 **차단** → `E_UI_VALUE_RANGE` |

## 6.3 테스트로 옮기는 To-Do 규칙

- **"보인다/거부한다/반환한다" 등 판단(Decision)이 있는 요구만** Track A/B 테스트로 변환한다. *작업 목록이 동사로만 끝나고 판단이 없으면* 테스트로 내리지 않는다(슬라이드 6.2 경고와 동일 취지).

# 7. Functional Requirements (기능 요구사항) — Track 매핑

- **Track A**: FR-01  
- **Track B**: FR-02, FR-03, FR-04, FR-05 (FR-05의 출력 좌표·`int[6]`은 Track A와의 **계약 경계**에도 걸침)

## FR-01 입력 검증 (Boundary) — **Track A**

- **Feature ID**: FR-01
- **설명**: 외부 입력이 고정 계약을 만족하는지 검사하고, 위반 시 표준 오류를 반환한다.
- **입력**: `int[][] matrix`
- **처리 규칙(불변조건 포함)**:
  - 행 개수는 4여야 한다.
  - 각 행 길이는 4여야 한다.
  - 모든 셀 값은 `0` 또는 `1..16`이어야 한다.
  - `0`의 개수는 정확히 2개여야 한다.
  - `0`을 제외한 숫자는 중복되면 안 된다.
- **출력**: 유효 입력이면 검증 통과 상태, 아니면 표준 오류 객체
- **승인 기준(AC)**:
  - AC-FR01-01: 4×4가 아닌 입력은 반드시 `E_UI_MATRIX_SIZE`를 반환해야 한다.
  - AC-FR01-02: 0 개수가 2가 아니면 반드시 `E_UI_BLANK_COUNT`를 반환해야 한다.
  - AC-FR01-03: 범위 외 값이 존재하면 반드시 `E_UI_VALUE_RANGE`를 반환해야 한다.
  - AC-FR01-04: 0 제외 중복이 있으면 반드시 `E_UI_DUPLICATE`를 반환해야 한다.
  - AC-FR01-05: 유효 입력은 Domain 호출로 진행되어야 한다.
- **관련 오류/예외 정책**:
  - 오류 형식: `{ code, message, details? }`
  - 메시지는 고정 문자열 비교 테스트를 통과해야 한다.

## FR-02 빈칸 탐색 — **Track B**

- **Feature ID**: FR-02
- **설명**: Domain에서 빈칸(0) 두 위치를 row-major 순서로 식별한다.
- **입력**: 유효한 4×4 행렬
- **처리 규칙(불변조건 포함)**:
  - 스캔 순서는 `(1,1) -> (1,4) -> (2,1) ... -> (4,4)`이다.
  - 첫 번째 빈칸은 row-major 스캔에서 먼저 발견된 0이다.
  - 빈칸 좌표는 내부적으로 0-index를 사용해도, 출력 계약에서는 1-index로 변환한다.
- **출력**: `[blank1, blank2]` (row-major 기준)
- **승인 기준(AC)**:
  - AC-FR02-01: 빈칸 2개 입력에서 반드시 두 좌표를 row-major 순으로 반환해야 한다.
  - AC-FR02-02: 빈칸 순서는 동일 입력에서 항상 동일해야 한다.
- **관련 오류/예외 정책**:
  - 빈칸 수 불일치가 발견되면 `DomainValidationError`를 발생시켜야 한다.

## FR-03 누락 숫자 탐색 — **Track B**

- **Feature ID**: FR-03
- **설명**: `1..16` 전체 집합에서 현재 보드 값(0 제외)을 제거하여 누락 숫자 두 개를 계산한다.
- **입력**: 유효한 4×4 행렬
- **처리 규칙(불변조건 포함)**:
  - 비교 기준 집합은 정확히 `{1..16}`이다.
  - 누락 숫자 결과는 `(small, large)` 오름차순으로 정규화한다.
- **출력**: `(small, large)`
- **승인 기준(AC)**:
  - AC-FR03-01: 정상 입력에서 누락 숫자를 정확히 2개 반환해야 한다.
  - AC-FR03-02: 반환 숫자는 `1..16` 범위여야 한다.
  - AC-FR03-03: 반환 순서는 항상 오름차순이어야 한다.
- **관련 오류/예외 정책**:
  - 유효 범위/중복 전제 위반 시 `DomainValidationError`를 발생시켜야 한다.

## FR-04 마방진 판정 — **Track B**

- **Feature ID**: FR-04
- **설명**: 완성된 4×4 보드가 마방진 상수 34를 만족하는지 판정한다.
- **입력**: 0이 없는 완성 4×4 보드
- **처리 규칙(불변조건 포함)**:
  - 4개 행 합, 4개 열 합, 주대각선/부대각선 합을 계산한다.
  - 10개 합이 모두 34일 때만 `true`이다.
- **출력**: `boolean isMagic`
- **승인 기준(AC)**:
  - AC-FR04-01: 10개 합이 모두 34인 보드는 `true`를 반환해야 한다.
  - AC-FR04-02: 10개 중 하나라도 34가 아니면 `false`를 반환해야 한다.
- **관련 오류/예외 정책**:
  - 입력 보드에 0이 남아 있으면 `DomainValidationError`를 발생시켜야 한다.

## FR-05 해 찾기(solution): 두 조합 시도 및 반환 — **Track B** (출력 **Track A** 계약)

- **Feature ID**: FR-05
- **설명**: 빈칸 2개와 누락 숫자 2개를 이용해 두 조합을 순차 시도하고 계약된 출력을 반환한다.
- **입력**: 유효한 4×4 행렬
- **처리 규칙(불변조건 포함)**:
  - 시도 1: `small -> firstBlank`, `large -> secondBlank`
  - 시도 2: 시도 1 실패 시 `large -> firstBlank`, `small -> secondBlank`
  - 첫 성공 시점의 배치를 그대로 반환하고 추가 시도는 하지 않는다.
  - 출력 좌표는 1-index를 사용한다.
- **출력**: `int[6] = [r1, c1, n1, r2, c2, n2]`
- **승인 기준(AC)**:
  - AC-FR05-01: 시도 1이 성공하면 `[r1,c1,small,r2,c2,large]`를 반환해야 한다.
  - AC-FR05-02: 시도 1 실패/시도 2 성공이면 `[r1,c1,large,r2,c2,small]`를 반환해야 한다.
  - AC-FR05-03: 반환 배열 길이는 항상 6이어야 한다.
  - AC-FR05-04: 반환 좌표 `(r1,c1),(r2,c2)`는 항상 `1..4` 범위여야 한다.
  - AC-FR05-05: 함수 호출 전후 입력 행렬 원본은 깊은 비교 시 동일해야 한다.
- **관련 오류/예외 정책**:
  - 두 시도 모두 실패하면 `SolveFailure`를 발생시키고 Boundary는 `E_DOMAIN_NO_SOLUTION`(HTTP/CLI 공통 의미의 Unprocessable 상태)로 매핑해야 한다.

# 8. Business Rules (도메인 규칙) — **Track B**

- **BR-01**: 보드 크기는 항상 4×4여야 한다.
- **BR-02**: 셀 값은 `0` 또는 `1..16`만 허용한다.
- **BR-03**: 값 `0`은 정확히 2개여야 한다.
- **BR-04**: `0`을 제외한 숫자는 중복되면 안 된다.
- **BR-05**: 첫 번째 빈칸은 row-major 스캔에서 먼저 발견된 0으로 정의한다.
- **BR-06**: 누락 숫자 결과는 항상 오름차순 `(small, large)`로 정규화한다.
- **BR-07**: 마방진 판정은 행 4개, 열 4개, 대각선 2개의 합이 모두 34일 때만 참이다.
- **BR-08**: 해 탐색은 시도 1 후 실패 시 시도 2를 수행하며, 성공 즉시 종료한다.
- **BR-09**: 출력은 항상 길이 6의 `int[6]` 형식 `[r1,c1,n1,r2,c2,n2]`여야 한다.
- **BR-10**: 출력 좌표는 항상 1-index(`1..4`)여야 한다.
- **BR-11**: 동일 입력은 항상 동일 출력 또는 동일 오류 코드를 반환해야 한다.
- **BR-12**: Domain은 입력 행렬 원본을 변경하면 안 된다(불변 입력 정책).

# 9. Non-Functional Requirements

- **NFR-01 테스트 커버리지**:
  - Domain Logic: 95% 이상
  - Boundary Validation: 85% 이상
- **NFR-02 결정론**: 동일 입력은 항상 동일 출력/오류를 반환해야 한다. (ML 추론이 끼면 **Track C**에서 시드/버전 고정으로 **재현성**을 명시한다 — 선택 항목.)
- **NFR-03 부작용 금지**: 입력 `int[][]` 원본은 함수 호출 전후 동일해야 한다(깊은 비교 테스트로 검증).
- **NFR-04 성능 기준**: 4×4 단일 요청은 표준 개발 머신에서 50ms 이내 처리되어야 한다(1000회 반복 평균 기준). (선택) 추론 경로가 있으면 **Track C** SLI(예: P95 지연)로 별도 측정.
- **NFR-05 레이어 경계 준수**: `boundary -> control -> entity` 의존 방향을 위반하면 빌드/리뷰에서 실패로 처리한다. **Track C** 파이프라인은 **제품의 Domain·Boundary에 역주입(역의존)** 하지 않는다.
- **NFR-06 (선택) MLOps 품질 게이트**: Track C를 쓰는 경우, **오프라인 eval** 최소 임계값·**모델 아티팩트 digest**·**롤백 기준**을 팀이 합의한 문서/CI 단계에 둔다(본 PRD v0.2는 수치를 강제하지 않음).

# 10. Dual-Track TDD Strategy (+ Track C)

## 10.1 Track A — Boundary (UX / I/O) TDD

- Contract-first 테스트 항목:
  - 입력 크기/형식 검증
  - 값 범위 검증
  - 빈칸 개수 검증
  - 0 제외 중복 검증
  - 출력 배열 길이/인덱스/순서 검증
  - Domain 예외의 오류 코드 매핑 검증
- 실패 정책(표준):
  - 예외 타입: `BoundaryValidationError`, `DomainMappedError`
  - 오류 코드: `E_UI_MATRIX_SIZE`, `E_UI_BLANK_COUNT`, `E_UI_VALUE_RANGE`, `E_UI_DUPLICATE`, `E_UI_OUTPUT_FORMAT`, `E_DOMAIN_NO_SOLUTION`
  - 메시지: 고정 문자열, 테스트에서 완전 일치 비교

## 10.2 Track B — Domain (Logic) TDD

- 메서드 단위 테스트 목록:
  - `findBlankPositions` row-major 순서 테스트
  - `findMissingNumbers` 정확성/오름차순 테스트
  - `isMagic` 참/거짓 판정 테스트
  - `solve` 시도1 성공 테스트
  - `solve` 시도1 실패 후 시도2 성공 테스트
  - `solve` 두 시도 실패 테스트
- 불변조건 테스트 목록:
  - 4×4 크기 위반
  - 값 범위 위반
  - 0 개수 위반
  - 0 제외 중복 위반
  - 입력 원본 불변성 위반 방지

## 10.3 병렬 진행 규칙 (Track A + B)

- 병렬 사이클 규칙: **I/O RED & Logic RED → I/O GREEN & Logic GREEN → REFACTOR**
- 금지 규칙: **Domain 전체 구현 완료 후 Boundary를 붙이는 방식 금지**
- 각 사이클 종료 조건:
  - 새 AC 대응 테스트가 RED에서 GREEN으로 전환
  - 기존 회귀 테스트 100% 통과
  - 리팩토링 후 동작 변화 없음

## 10.4 Track C — MLOps (선택, Domain과 비동기 가능)

- **역할**: 학습·재학습·배포·대시보드·알람은 **제품의 FR 합격과 독립된 리듬**으로 둘 수 있다. 다만 **배포된 모델이 "정답"을 스스로 정의해선 안 되며** D-05를 따른다.
- **최소 권장**: (해당 시) `model` 아티팩트 버전, `eval` 고정 셋, **프로덕션 점수 하락 시 롤백** 절차.

# 11. Test Plan (QA)

- **시나리오 기반 테스트 목록** (권장 Track 태그)
  - TC-01 정상 성공(시도 1 성공) — A+B
  - TC-02 역순 성공(시도 1 실패, 시도 2 성공) — A+B
  - TC-03 해 없음(두 시도 실패) — A+B
  - TC-04 입력 크기 오류 — **A**
  - TC-05 값 범위 오류 — **A**
  - TC-06 0 개수 오류 — **A**
  - TC-07 0 제외 중복 오류 — **A**
  - TC-08 출력 형식 오류(경계 계층 방어 테스트) — **A**

- **회귀 테스트 정책**
  - 모든 FR별 AC에 최소 1개 이상의 회귀 테스트를 유지한다.
  - 오류 코드/메시지 변경 시 계약 버전과 테스트를 함께 갱신한다.
  - 테스트 삭제/약화는 PR 승인 기준에서 실패 처리한다.
  - **§6.3**: 판단 없는 To-Do는 테스트로 내리지 않는다.

- **대표 테스트 데이터(4×4 예시 행렬)**
  - TD-01 (정상/시도1 성공):
    - `[[16,2,3,13],[0,0,10,8],[9,7,6,12],[4,14,15,1]]`  
      (누락 숫자: 5,11 / firstBlank=(2,1), secondBlank=(2,2) / 시도1에서만 성공)
  - TD-02 (역순 성공):
    - `[[0,2,3,13],[5,11,10,8],[9,7,6,12],[4,14,15,0]]`  
      (누락 숫자: 1,16 / firstBlank=(1,1), secondBlank=(4,4) / 시도2에서만 성공)
  - TD-03 (해 없음):
    - `[[16,2,4,13],[5,11,10,8],[9,7,6,12],[0,14,15,0]]`  
      (누락 숫자: 1,3 / 두 시도 모두 행4 합이 33으로 실패)
  - TD-04 (입력 오류-크기):
    - `3x4`, `4x3`
  - TD-05 (입력 오류-범위):
    - 값 `17` 또는 `-1` 포함
  - TD-06 (입력 오류-중복):
    - 0 제외 동일 숫자 2회 이상
  - TD-07 (입력 오류-빈칸 수):
    - 0이 1개 또는 3개

- **Property/Invariant 기반 체크 항목**
  - PI-01: 유효 입력이면 반환 배열 길이는 항상 6
  - PI-02: 반환 좌표는 항상 1..4
  - PI-03: 반환 숫자 2개는 누락 숫자 집합과 정확히 동일
  - PI-04: 결과로 채운 보드는 `isMagic == true`
  - PI-05: 입력 원본은 호출 전후 깊은 동일성 유지

# 12. Architecture Overview (High-Level)

- **Boundary Layer (Track A)**
  - 책임: 입력 계약 검증, 출력 포맷 보장, 오류 코드 표준화
  - **금지**: Domain 규칙(예: `isMagic`·두 조합 로직)을 **중복 구현**하여 우회하는 것. **Control을 통한 Entity 사용은 Application 흐름에 따른다.** Boundary **모듈**이 **Entity/Domain** 을 **직접 import·호출** 하지 말 것(Control 경유).
- **Domain Layer (Track B)**
  - 책임: 빈칸 탐색, 누락 숫자 계산, 마방진 판정, 두 조합 해 탐색
  - 속성: 순수 함수 중심, 외부 I/O 없음
- **(선택) MLOps / Model Serving (Track C)**
  - 책임: **학습·평가·배포·모니터링** — **힌트/보조** 등 **비도메인-SSOT** 기능. Domain·Boundary **타입에 직접 결합하지 말고** 포트(인터페이스)로 주입.
- **책임 분리(SRP) 전략**
  - 입력 검증, 규칙 판정, 결과 직렬화를 분리된 컴포넌트로 분리
  - 컴포넌트 당 변경 이유를 1개로 제한
- **확장(OCP) 전략**
  - 검증 규칙/오류 매핑을 교체 가능한 정책으로 분리
  - N×N 확장은 별도 모듈/버전에서 추가하며 본 PRD 계약은 변경하지 않는다
- **의존성 방향**
  - `boundary -> control -> entity` ; (선택) `ml_pipeline -> (ports only)`; **entity는 ml_pipeline을 참조하지 않는다**.

# 13. Risks & Ambiguities

- **결정 항목 D-01 (두 시도 모두 실패 정책)**:
  - 결정: Domain은 `SolveFailure`를 반환하고, Boundary는 `E_DOMAIN_NO_SOLUTION`으로 매핑한다.
- **결정 항목 D-02 (1-index 규칙)**:
  - 결정: 내부 인덱스와 무관하게 외부 계약 출력은 항상 1-index를 강제한다.
- **결정 항목 D-03 (row-major 첫 빈칸)**:
  - 결정: 첫 빈칸 정의는 row-major 고정이며, 다른 순회 방식은 허용하지 않는다.
- **결정 항목 D-04 (입력 변경 여부)**:
  - 결정: 입력 행렬은 절대 변경하지 않으며, 필요한 경우 복사본으로 계산한다.
- **결정 항목 D-05 (ML·추론 vs Domain SSOT)**:
  - 결정: Track C(모델/추론) 출력이 **FR-01~05·BR과 충돌**하면 **Track B(및 Track A의 오류/출력 계약)가 항상 우선**한다. UI/API에 노출하는 "해"는 **Domain이 계약에 따라 산출한 것**이어야 한다.
- **자주 실수하는 포인트**
  - 1-index/0-index 혼동
  - 빈칸 순서와 누락 숫자 매핑 순서 혼동
  - 시도 1 실패 후 시도 2를 생략하는 오류
  - 출력 길이 6 또는 타입 검증 누락
  - "UI"를 **Track A(경계)**와 **풀 GUI 제품(§5.2)** 를 혼동하는 것

# 14. Traceability Matrix (필수)

| Track | Concept/Invariant | Business Rule | Feature(FR) | Acceptance Criteria | Test Case | Component |
|-------|------------------|---------------|-------------|---------------------|-----------|-----------|
| A | 4×4 고정 크기 | BR-01 | FR-01 | AC-FR01-01 | TC-04 | BoundaryInputValidator |
| A | 값 범위 `0 or 1..16` | BR-02 | FR-01 | AC-FR01-03 | TC-05 | BoundaryInputValidator |
| A,B | 빈칸 정확히 2개 | BR-03 | FR-01, FR-02 | AC-FR01-02, AC-FR02-01 | TC-07 | BoundaryInputValidator, BlankPositionFinder |
| A,B | 0 제외 중복 금지 | BR-04 | FR-01, FR-03 | AC-FR01-04, AC-FR03-01 | TC-06 | BoundaryInputValidator, MissingNumbersFinder |
| B | row-major 첫 빈칸 정의 | BR-05 | FR-02 | AC-FR02-01, AC-FR02-02 | TC-01, TC-02 | BlankPositionFinder |
| B | 누락 숫자 오름차순 정규화 | BR-06 | FR-03 | AC-FR03-03 | TC-01 | MissingNumbersFinder |
| B | 합 상수 34 규칙 | BR-07 | FR-04 | AC-FR04-01, AC-FR04-02 | TC-01, TC-02, TC-03 | MagicSquareValidator |
| A,B | 두 조합 순차 시도 | BR-08 | FR-05 | AC-FR05-01, AC-FR05-02 | TC-01, TC-02 | TwoAssignmentSolver |
| A,B | 출력 형식 `int[6]` | BR-09 | FR-05 | AC-FR05-03 | TC-08 | ResultFormatter |
| A,B | 출력 좌표 1-index | BR-10 | FR-05 | AC-FR05-04 | TC-01, TC-02 | ResultFormatter |
| B | 결정론 보장 | BR-11 | FR-02~FR-05 | AC-FR02-02 | TC-01 재실행 비교 | SolverOrchestrator |
| B | 입력 불변성 | BR-12 | FR-05 | AC-FR05-05 | PI-05 | SolverOrchestrator |

(Track C를 도입하며 MLOps 전용 AC를 추가하는 경우, 본 테이블에 `C` 행을 **별도** 추가한다.)
