# Magic Square 4×4 완성 시스템

부분적으로 비어 있는 4×4 마방진(빈칸 `0` 두 칸)을 **도메인 규칙**에 따라 완성하거나, 유효하지 않으면 **표준 오류**로 거부하는 시스템입니다. 본 프로젝트는 **Dual-Track TDD**(경계·도메인 분리)와 **ECB(Entity / Control / Boundary)** 를 전제로 합니다.

---

## 문서 기준 (Single Source of Truth)

| 구분 | 문서 | 용도 |
|------|------|------|
| **본문·완료 조건·검증 기준** | [`docs/PRD_MagicSquare_4x4_DualTrack_TDD.md`](docs/PRD_MagicSquare_4x4_DualTrack_TDD.md) | FR/AC/BR/TC·TD·PI·테스트 플랜·오류 코드·NFR·아키텍처·추적 표 (PRD v0.2) |
| **에픽·사용자 여정·스토리** (보조) | [`Report/05.MagicSquare_UserJourney_EpicToTechnical_Report_2026-04-27.md`](Report/05.MagicSquare_UserJourney_EpicToTechnical_Report_2026-04-27.md) | 비즈니스 목표, 페르소나, Journey 단계, User Story 서술 |

상세 수치·예외 메시지·행렬 예시(TD)·오류 코드 문자열은 **항상 PRD**를 따릅니다. Report의 성공 지표·서술이 PRD와 겹치면 **PRD의 NFR·AC**가 우선합니다.

---

## Epic (Report 보조, 완료는 PRD)

**Epic (Report/05):** *Invariant(불변조건) 기반 사고 훈련 시스템 구축*

4×4 Magic Square를 통해 다음을 연습하는 것이 목표입니다 (Report/05 Level 1).

- Invariant 중심 설계 사고
- Dual-Track TDD
- 입·출력 계약 명확화
- 설계 → 테스트 → 구현 → 리팩터 흐름 체화

**PRD 기준 정량·검증 완료:** 아래 [검증 기준 (PRD)](#검증-기준-prd)의 **FR/AC·TC·PI·NFR-01**을 충족할 것. Report에 언급된 “Domain 95%·계약 테스트 100%” 등은 **NFR-01 및 FR-01 AC**와 정합되도록 해석합니다.

---

## 사용자 여정 (User Journey, Report 보조)

**페르소나 (Report/05):** 소프트웨어 개발 학습자, TDD·Clean Architecture를 익히는 중.

| 단계 | 여정 (요지) | PRD·기술 대응 |
|------|-------------|----------------|
| 1. 문제 인식 | “알고리즘 하나”가 아니라 **불변조건·계약**으로 본다 | PRD §2 Problem Statement |
| 2. 계약 정의 | 입력/출력 스키마, 예외·오류 코드 | **Track A**, FR-01 |
| 3. Domain 분리 | 빈칸·누락 숫자·마방진 판정·두 조합 해 | **Track B**, FR-02~05, Report의 BlankFinder 등 |
| 4. Dual-Track | I/O RED ∥ Logic RED → GREEN → REFACTOR | PRD §10.3 |
| 5. 회귀 보호 | 엣지·입력 오류·조합 실패 | PRD §11 TC-01~08, TD-01~07 |

---

## User Story (Report 서술 + PRD ID)

| ID | As a… / I want… (Report 요지) | PRD | 승인·검증 (PRD가 정본) |
|----|--------------------------------|-----|-------------------------|
| **US-1** | 입력이 4×4·빈칸 2·범위·중복 규칙을 만족하길 원한다 | FR-01 | AC-FR01-01~05, TC-04~07 |
| **US-2** | `0`의 위치를 row-major로 알고 싶다 | FR-02 | AC-FR02-01,02, TC-01~03 |
| **US-3** | 1~16 중 누락된 두 수를 (small, large)로 얻고 싶다 | FR-03 | AC-FR03-01~03 |
| **US-4** | 완성 보드가 마방진(합 34)인지 판정하고 싶다 | FR-04 | AC-FR04-01,02 |
| **US-5** | 두 조합 시도로 해를 찾거나, 불가 시 표준 실패로 돌리고 싶다 | FR-05 | AC-FR05-01~05, TC-01~03, D-01 |
| **US-6** | 경계는 I/O만, Control이 흐름을 조율하고 Entity는 규칙만 | PRD §12 | NFR-05 `boundary → control → entity` |

**C2C 섹션 ID:** 아래 **「C2C Traceability: To-Do → 시나리오 → 테스트 → 코드」** 절의 `US-001`~`US-007` — 위 표 `US-1`~`US-6`과 같은 요구 축이며, 품질·추적을 **`US-007`**, Control·오케스트레이션을 **`US-006`**로 세분한 것이다.

---

## 도메인 규칙 (요약, 상세는 PRD BR-01~12)

- 보드는 **4×4**이고, 셀 값은 **`0` 또는 1~16**만 허용한다.  
- **`0`은 정확히 2칸**(빈칸)이다.  
- **0을 제외한 중복**은 허용하지 않는다.  
- 완성 시 **행 4 + 열 4 + 대각선 2, 총 10개 합**이 모두 **34**이어야 한다 (FR-04, BR-07).  
- 유효하지 않은 **외부 입력**은 **Track A**에서 거부; Domain 전제 위반은 **Domain** 예외 (`DomainValidationError`, `SolveFailure` 등, PRD §7).  
- **도메인 SSOT는 Track B**; Track C(MLOps)는 PRD **D-05**에 따라 **FR·BR을 대체하지 않는다**.

---

## 아키텍처 (ECB, PRD §12·§14)

- **Entity (Track B, Domain):** 순수 로직 — 빈칸·누락 숫자·`isMagic`·`solve` 등, 외부 I/O 없음.  
- **Boundary (Track A):** 입·출력 계약, 오류 코드·메시지, 출력 형식. **Entity를 직접 import·호출하지 않는다** (Control 경유).  
- **Control:** 검증 통과 후 Entity 호출, Domain 예외 → 경계 오류 코드 매핑, 흐름 조율.  
- **의존성:** `boundary → control → entity` (NFR-05).

**PRD §14 컴포넌트명(참고):** `BoundaryInputValidator`, `BlankPositionFinder`, `MissingNumbersFinder`, `MagicSquareValidator`, `TwoAssignmentSolver`, `ResultFormatter`, `SolverOrchestrator`.

### 시나리오 레벨 (C2C·테스트 설계)

| 레벨 | 의미 |
|------|------|
| **L0** | 기능 개요 |
| **L1** | 정상 흐름 |
| **L2** | 경계 상황 |
| **L3** | 실패·오류 상황 |

---

## 검증 기준 (PRD)

### 기능 요구(FR)와 승인 기준(AC)

- **FR-01 (Track A, Boundary):** 4×4, 셀 `0` 또는 `1..16`, `0` 정확히 2개, 0 제외 중복 금지.  
  - **AC-FR01-01** `E_UI_MATRIX_SIZE` · **AC-FR01-02** `E_UI_BLANK_COUNT` · **AC-FR01-03** `E_UI_VALUE_RANGE` · **AC-FR01-04** `E_UI_DUPLICATE` · **AC-FR01-05** 유효 시 Domain(Control 경유)으로 진행.  
  - 오류 형식: `{ code, message, details? }` (PRD FR-01).

- **FR-02~05 (Track B, Domain):**  
  - **FR-02** 빈칸 row-major, **AC-FR02-01,02**  
  - **FR-03** 누락 2개 `(small, large)`, **AC-FR03-01~03**  
  - **FR-04** 10개 합 모두 34일 때만 `isMagic` 참, 0 잔존 시 `DomainValidationError`, **AC-FR04-01,02**  
  - **FR-05** 시도1·시도2 순서, 성공 시 `int[6]`·1-index, 실패 시 `SolveFailure` → 경계 `E_DOMAIN_NO_SOLUTION`, **AC-FR05-01~05** · **BR-12** 입력 비변조.

### 시나리오 테스트 (PRD §11)

| ID | 내용 | Track |
|----|------|--------|
| TC-01 | 정상(시도 1 성공) | A+B |
| TC-02 | 시도 1 실패·시도 2 성공 | A+B |
| TC-03 | 해 없음(두 시도 실패) | A+B |
| TC-04 | 입력 크기 오류 | A |
| TC-05 | 값 범위 오류 | A |
| TC-06 | 0 개수 오류 | A |
| TC-07 | 0 제외 중복 오류 | A |
| TC-08 | 출력 형식(경계 방어) | A |

대표 행렬·입력 실패 케이스는 PRD **TD-01~TD-07**을 사용한다.

### Property / Invariant (PI-01~05, PRD §11)

- **PI-01** 유효 입력이면 반환 배열 길이 6 · **PI-02** 좌표 `1..4` · **PI-03** 반환 두 숫자 = 누락 집합  
- **PI-04** 채운 보드 `isMagic == true` · **PI-05** 입력 원본 호출 전후 동일(깊은 동등, NFR-03)

### 비기능 (NFR)

- **NFR-01** Domain **≥95%**, Boundary **≥85%** (라인 커버리지)  
- **NFR-02** 결정론(동일 입력 → 동일 출력/오류)  
- **NFR-03** 입력 `int[][]` 변이 금지  
- **NFR-04** 4×4 단일 요청, 1000회 평균 **50ms** 이내(개발 머신, PRD)  
- **NFR-05** ECB 의존 방향 준수 · **NFR-06** Track C 선택 시 팀 합의( PRD)

---

## C2C Traceability: To-Do → 시나리오 → 테스트 → 코드

아래 구조는 **슬라이드 예시(1.5 Magic Square — 완성 To-Do 구조)**와 동일하게 **To-Do → 시나리오(레벨) → 테스트 → 코드**를 한 번에 추적하도록 썼다.  
**이름·책임·수치·완료 조건**은 PRD가 정본이다. (슬라이드에 `SquareValidator`를 Control에 둔 예는, 본 프로젝트에선 **FR-01은 `BoundaryInputValidator` `<<boundary>>`**, 도메인 판정은 `MagicSquareValidator` `<<entity>>` 등 [PRD §12·§14](docs/PRD_MagicSquare_4x4_DualTrack_TDD.md)에 맞춘다.)

### Epic-001: Magic Square 4×4 완성 시스템

- **범위:** 부분 보드(0 두 칸) 완성 또는 표준 오류.  
- **Report/05 정렬:** Invariant·Dual-Track·계약 명확화 **학습 목표** — 검증 수치는 아래 **REQ = PRD FR** 열.

---

#### US-001: 보드 표현·입력 유효성 (REQ-001 = FR-01, Track A)

- [ ] **TASK-001** `Board` / `MagicSquareBoard` 정의 `<<entity>>` (4×4 격자·불변/복사, **NFR-03·BR-12** 방향)  
  - **→ Test:** `test_board_entity_creation` (또는 동일 의미) · **Scenario:** L0~L1  
  - **→ Code:** Entity 모듈  

- [ ] **TASK-002** `BoundaryInputValidator` — 외부 `int[][]` 계약 검증 `<<boundary>>` (Domain 규칙 **복제·우회 금지**, PRD §12)  
  - [ ] **TASK-002-1 [RED]** `test_matrix_size_returns_e_ui_matrix_size` — **AC-FR01-01**, **TC-04**, **TD-04** · *L3 실패*  
  - [ ] **TASK-002-2 [RED]** `test_blank_count_returns_e_ui_blank_count` — **AC-FR01-02**, **TC-06**, **TD-07** · *L3*  
  - [ ] **TASK-002-3 [RED]** `test_value_range_returns_e_ui_value_range` — **AC-FR01-03**, **TC-05**, **TD-05** · *L3*  
  - [ ] **TASK-002-4 [RED]** `test_duplicate_returns_e_ui_duplicate` — **AC-FR01-04**, **TC-07**, **TD-06** · *L3*  
  - [ ] **TASK-002-5 [GREEN]** 위 실패 테스트가 기대 오류 `{ code, message, … }`로 **통과**하도록 최소 구현 (PRD FR-01)  
  - [ ] **TASK-002-6 [REFACTOR]** 타입 힌트·검증 순서·고정 메시지 정리 (PRD §7, §10.1)  
  - **Checkpoint:** **AC-FR01-01~04** 대응 RED→GREEN 전환 후, `test_valid_input_proceeds_to_control` — **AC-FR01-05** · *L1* 를 추가·통과한 뒤 US-002 진행  

---

#### US-002: 빈칸 위치 탐색 (REQ-002 = FR-02, Track B)

- [ ] **TASK-003** `BlankPositionFinder.findBlankPositions` (또는 팀 네이밍) `<<entity>>`  
  - [ ] **TASK-003-1 [RED]** `test_blanks_row_major_order` — **AC-FR02-01**, **TC-01/02** / **TD-01,02** · *L1*  
  - [ ] **TASK-003-2 [RED]** `test_blanks_deterministic_same_input` — **AC-FR02-02**, **NFR-02** · *L2*  
  - [ ] **TASK-003-3 [RED]** `test_domain_validation_when_blank_mismatch` — `DomainValidationError` (PRD FR-02) · *L3 실패*  
  - [ ] **TASK-003-4 [GREEN]** row-major 스캔 **최소 구현**  
  - [ ] **TASK-003-5 [REFACTOR]** 가독성·이름 PRD `BlankPositionFinder`와 [§14](docs/PRD_MagicSquare_4x4_DualTrack_TDD.md#14-traceability-matrix-필수) 정렬  
  - *슬라이드 참고:* "백트래킹 최적화" 메모는 **본 PRD의 4×4·두 시도 `solve` 모델(§7 FR-05)과는 별개**이며, 4×4는 전수 스캔으로 충분하다(필요 시 성능은 **NFR-04 50ms**·PRD §9).  
  - **Checkpoint:** `TASK-003-1` 통과 확인 후 US-003 진행 · (선택) **NFR-04** 스모크 · Domain 커버리지는 **NFR-01 ≥95%**  

---

#### US-003: 누락 숫자 (REQ-003 = FR-03, Track B)

- [ ] **TASK-004** `MissingNumbersFinder` `<<entity>>`  
  - [ ] [RED] `test_missing_pair_sorted` — **AC-FR03-01,03**, **TC-01** / **TD-01**  
  - [ ] [RED] `test_missing_values_in_range` — **AC-FR03-02**  
  - [ ] [RED] *L3* 전제 위반 → `DomainValidationError` (PRD FR-03)  
  - [ ] [GREEN] [REFACTOR] (PRD BR-06 `(small, large)`)  
  - **Checkpoint:** **PI-03** (유효 해에 대해 반환 숫자 = 누락 집합) 를 **US-005** 품질 단계에서 재검  

---

#### US-004: 마방진 판정 (REQ-004 = FR-04, Track B)

- [ ] **TASK-005** `MagicSquareValidator.isMagic` `<<entity>>`  
  - [ ] [RED] *L1* 10개 합 모두 34 → `true` — **AC-FR04-01**  
  - [ ] [RED] *L2* 일부 합 ≠34 → `false` — **AC-FR04-02**  
  - [ ] [RED] *L3* 0 잔존 → `DomainValidationError` (PRD FR-04)  
  - [ ] [GREEN] [REFACTOR]  

---

#### US-005: 두 조합 해(solve)·출력 계약 (REQ-005 = FR-05, Track B + 출력 경계)

- [ ] **TASK-006** `TwoAssignmentSolver.solve` `<<entity>>`  
  - [ ] [RED] 시도1 성공 — **AC-FR05-01**, **TC-01** / **TD-01** · *L1*  
  - [ ] [RED] 시도1 실패·시도2 성공 — **AC-FR05-02**, **TC-02** / **TD-02** · *L1*  
  - [ ] [RED] 두 시도 실패 `SolveFailure` — **TC-03** / **TD-03** · *L3*  
  - [ ] [RED] 입력 불변 **PI-05** / **AC-FR05-05** · *L1*  
  - [ ] [GREEN] [REFACTOR] **BR-08, BR-12**  
- [ ] **TASK-007** `ResultFormatter` `<<boundary>>` — `int[6]`, 1-index **AC-FR05-03,04**, **TC-08**, **PI-01,02**  
  - [ ] [RED] [GREEN] [REFACTOR]  

---

#### US-006: 흐름 조율·Domain 예외 매핑 (REQ-006 = PRD §12, NFR-05)

- [ ] **TASK-008** `SolverOrchestrator` `<<control>>`  
  - [ ] [RED] `boundary → control → entity` 경로 **AC-FR01-05** 후 solve  
  - [ ] [RED] `SolveFailure` → **`E_DOMAIN_NO_SOLUTION`** (Boundary 매핑) — **D-01**, **TC-03**  
  - [ ] [GREEN] [REFACTOR] 경로 실패 시 Entity **미호출** (짧은 경로) 회귀  

---

#### US-007: 품질·추적 (REQ-007 = PRD §9·11·14)

- [ ] **TASK-009** `pytest --cov` 게이트 — **NFR-01** (Domain **≥95%**, Boundary **≥85%**; 슬라이드의 “80%”·“100ms” **아님**)  
- [ ] **TASK-010** **NFR-02** 재현성, **NFR-04** (선택) 50ms 스모크  
- [ ] **TASK-011** PRD **§14** Traceability Matrix 1:1 점검 (FR/AC/TC ↔ 테스트·모듈)  

**Dual-Track (PRD §10.3)**  
- [ ] **D-1** I/O RED & Logic RED를 **동일 주기**에 둘 수 있게 쪼갬 · Domain 전부 완성 후에만 Boundary 붙이기 **금지**  

**판단 없는 작업**만의 To-Do는 PRD **§6.3**에 따라 테스트로 내리지 않는다.  

---

### 부록: Phase별 빠른 색인 (C2C와 동일 PRD)

| Phase | 키워드 | C2C |
|--------|--------|-----|
| P0 기반 | 저장소, `pytest`, `TASK-001` | US-001 |
| Track B | `TASK-003`~`006` | US-002~005 |
| Track A | `BoundaryInputValidator`, `ResultFormatter` | US-001, US-005~006 |
| Control | `SolverOrchestrator` | US-006 |
| 품질 | `TASK-009`~`011`, **D-1** | US-007 |

---

## 개발 환경

- **언어/런타임:** Python 3.x  
- **테스트:** `pytest` (예: `python -m pytest` 또는 `pytest tests/ -v --cov=...`)  
- **Cursor/규칙:** 저장소에 `.cursor` 규칙·`AGENTS`가 있으면 동일 팀 컨벤션에 맞게 참고 (경로는 프로젝트에 따라 조정).

---

## 관련 경로

| 경로 | 설명 |
|------|------|
| [`docs/PRD_MagicSquare_4x4_DualTrack_TDD.md`](docs/PRD_MagicSquare_4x4_DualTrack_TDD.md) | 제품 요구·AC·TC·TD·PI·NFR (본 README의 **정본**) |
| [`Report/05.MagicSquare_UserJourney_EpicToTechnical_Report_2026-04-27.md`](Report/05.MagicSquare_UserJourney_EpicToTechnical_Report_2026-04-27.md) | 에픽·여정·스토리 **보조** |
| `Report/`, `Prompting/` | 분석·프롬프트 산출물 |

---

*이 README의 본문·To-Do·검증 기준은 [`docs/PRD_MagicSquare_4x4_DualTrack_TDD.md`](docs/PRD_MagicSquare_4x4_DualTrack_TDD.md)를 따르며, Epic·User Journey·Story의 **서술·학습자 관점**은 [`Report/05...UserJourney...`](Report/05.MagicSquare_UserJourney_EpicToTechnical_Report_2026-04-27.md)를 보조로 인용한다.*
