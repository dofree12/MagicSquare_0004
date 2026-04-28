# Magic Square 4×4 — 테스트 케이스 명세

| 항목 | 내용 |
|------|------|
| **프로젝트명** | Magic Square 4×4 완성 시스템 |
| **대상 시스템** | Dual-Track TDD / ECB (Boundary · Control · Entity) |
| **단계** | 단위·시나리오 테스트 |
| **문서 상태** | PRD v0.2 (`docs/PRD_MagicSquare_4x4_DualTrack_TDD.md`) 정합 |
| **테스트 범위** | FR-01~05, TC-01~08, TD-01~07 |
| **버전** | 1.0 |

---

## 테스트환경

- **언어/런타임:** Python 3.x  
- **테스트:** `pytest` (`python -m pytest` / `pytest tests/ -v`)  
- **계측:** `pytest-cov` — PRD **NFR-01** (Domain ≥95%, Boundary ≥85% 라인 커버리지)  
- **OS/IDE:** (실행 머신에 맞게 기록, e.g. Windows 10+, Cursor / VS Code)  

---

## 전제 조건

- PRD·README에 정의된 **입출력 계약·오류 코드·TD 행렬**이 SSOT로 고정되어 있을 것.  
- 의존성 설치 후 **테스트 수집·실행이 오류 없이 동작**할 것.  
- Track A 테스트는 Domain 구현 세부를, Track B 테스트는 UI/CLI 포맷을 **가정하지 않을** 것( PRD §3.1 ).  

---

## 성공/실패 기준

| 구분 | 기준 |
|------|------|
| **성공** | 아래 표의 **예상 결과**와 실제 결과(반환값·`code`·예외 유형)가 일치한다. |
| **실패** | 하나라도 기대와 다르거나, PRD에 없는 오류 형태·책임 혼선(ECB 위반)이 드러난다. |

---

## 특별하게 필요한 절차

- 실행 후 **「결과」 열**에 Pass/Fail 및 실행일·커밋 해시를 기입한다.  
- 실패 시 **PRD TC/TD/AC ID**를 이슈·PR에 남기고, RED→GREEN 전환 시 동일 행을 갱신한다.  
- `TD-01`~`TD-07` 행렬을 변경하면 **본 표와 PRD §11**을 동시에 맞출 것.  

---

## 테스트 케이스 표

> **열:** TC ID → 기능 분류 → 테스트 항목 → 테스트 목적 → 입력값/전제조건 → 테스트 절차 (Given/When/Then) → 예상 결과 → 우선순위 → 결과 → 비고  
> **PRD 매핑:** 각 행 **비고**에 `PRD: TC-xx`, `TD-xx`를 표기한다.

| TC ID | 기능 분류 | 테스트 항목 | 테스트 목적 | 입력값 / 전제조건 | 테스트 절차 (Given / When / Then) | 예상 결과 | 우선순위 | 결과 | 비고 |
|------|-----------|-------------|---------------|-------------------|--------------------------------------|-----------|----------|------|------|
| TC-MS-A-001 | 입력 검증 (BoundaryInputValidator) / 크기 | 오류 — 행·열 길이 불일치 | AC-FR01-01: 4×4가 아니면 `E_UI_MATRIX_SIZE` | **TD-04:** `3×4` 또는 `4×3` 정수 배열 | **Given** 잘못된 크기의 `matrix`가 주어짐. **When** Boundary가 입력 검증을 수행함. **Then** 검증은 통과하지 않음. | 오류 객체 `code == E_UI_MATRIX_SIZE`, PRD §7 메시지 고정 문자열 | P1 | | PRD: **TC-04**, **TD-04** |
| TC-MS-A-002 | 입력 검증 (BoundaryInputValidator) / 범위 | 오류 — 1~16·0 외 값 | AC-FR01-03: 범위外 → `E_UI_VALUE_RANGE` | **TD-05:** 4×4 중 셀에 `17` 또는 `-1` 포함, 그 외는 계약 만족 | **Given** 범위外 값이 포함된 보드. **When** 입력 검증 수행. **Then** Domain으로 넘기지 않음. | `code == E_UI_VALUE_RANGE` | P1 | | PRD: **TC-05**, **TD-05** |
| TC-MS-A-003 | 입력 검증 (BoundaryInputValidator) / 빈칸 수 | 오류 — 0이 2개가 아님 | AC-FR01-02 → `E_UI_BLANK_COUNT` | **TD-07:** 0이 1개 또는 3개인 4×4 | **Given** 빈칸 개수가 2가 아님. **When** 입력 검증 수행. **Then** 차단. | `code == E_UI_BLANK_COUNT` | P1 | | PRD: **TC-06**, **TD-07** |
| TC-MS-A-004 | 입력 검증 (BoundaryInputValidator) / 중복 | 오류 — 0 제외 중복 | AC-FR01-04 → `E_UI_DUPLICATE` | **TD-06:** 0 제외 동일 숫자 2회 이상 | **Given** 중복이 있는 보드. **When** 입력 검증 수행. **Then** 차단. | `code == E_UI_DUPLICATE` | P1 | | PRD: **TC-07**, **TD-06** |
| TC-MS-A-005 | 출력·경계 (ResultFormatter) / 형식 | 방어 — `int[6]`·1-index 위반 시 | AC-FR05-03·BR-09, **TC-08** (경계 방어) | (테스트 더블 또는) 잘못된 내부 직렬화 결과가 Formatter에 전달되었다는 가정 | **Given** 길이≠6 이거나 좌표가 1~4 밖인 중간 데이터. **When** ResultFormatter가 경계 포맷을 강제함. **Then** 표준 오류로 수렴. | `E_UI_OUTPUT_FORMAT` (또는 PRD §7이 정한 동일 정책) | P2 | | PRD: **TC-08**, BR-09·10 |
| TC-MS-B-001 | 빈칸 탐색 (BlankPositionFinder) | 정상 — row-major 두 좌표 | AC-FR02-01·02 | **TD-01** 원본: `[[16,2,3,13],[0,0,10,8],[9,7,6,12],[4,14,15,1]]` (유효 입력으로 가정) | **Given** 위 보드. **When** `find`/`findBlankPositions` 등 FR-02 API 호출. **Then** 1-index로 `(2,1)`,`(2,2)` 순. | row-major: 첫 0·둘째 0 = (2,1),(2,2) (1-index) | P1 | | PRD: **TC-01** (일부), **TD-01**, BR-05 |
| TC-MS-B-002 | 누락 숫자 (MissingNumbersFinder) | 정상 — (small, large) | AC-FR03-01~03 | **TD-01** (동일) | **Given** 유효 보드. **When** 누락 쌍 계산. **Then** 1~16에서 0 제외 나머지 집합과 합. | `(5, 11)` (오름차순) | P1 | | **TD-01**, BR-06 |
| TC-MS-B-003 | 마방진 판정 (MagicSquareValidator.isMagic) | 정상 — 10개 합 34 | AC-FR04-01 | **TD-01** 해: 두 빈칸에 5,11을 시도1 규칙에 따라 채운 **완성** 보드 | **Given** 0이 없는 보드. **When** `isMagic` 호출. **Then** 합 34를 만족. | `True` | P1 | | **TC-01** 경로, BR-07 |
| TC-MS-B-004 | 마방진 판정 (MagicSquareValidator.isMagic) | 경계 — 일부 합 ≠ 34 | AC-FR04-02 | 임의 4×4: 한 행 합만 33/35로 깨뜨린 **완성(0 없음)** 보드 | **Given** 비마방진 완성 보드. **When** `isMagic`. **Then** false. | `False` | P2 | | AC-FR04-02 |
| TC-MS-B-005 | 마방진 판정 | 오류 — 0 잔존 | FR-04 Domain `DomainValidationError` | 0이 남은 4×4 | **Given** 미완성 보드. **When** `isMagic` (FR-04 전제 위반). **Then** 도메인 예외. | `DomainValidationError` (PRD §7 명칭 일치) | P2 | | PRD **FR-04** |
| TC-MS-B-006 | 해 찾기 (TwoAssignmentSolver) + 계약 | 시도1 성공 | AC-FR05-01, PI-01~04 | **TD-01** | **Given** 유효 보드. **When** `solve` (또는 Orchestrator 경로). **Then** 시도1이 성공하면 `[r1,c1,small,r2,c2,large]`. | 1-index `int[6]` = `[2,1,5,2,2,11]` ( **TD-01** 전제) | P1 | | **TC-01**, **TD-01**, **PI-01**~**PI-04** |
| TC-MS-B-007 | 해 찾기 (TwoAssignmentSolver) + 계약 | 시도2만 성공 | AC-FR05-02 | **TD-02:** `[[0,2,3,13],[5,11,10,8],[9,7,6,12],[4,14,15,0]]` (firstBlank 1-index (1,1), second (4,4), 누락 1·16) | **Given** **TD-02**. **When** `solve`. **Then** 시도1 실패·시도2 성공, `[r1,c1,large,r2,c2,small]`. | `int[6]` = `[1,1,16,4,4,1]` (1-index) | P1 | | **TC-02**, **TD-02** |
| TC-MS-B-008 | 해 찾기 / Control 매핑 | 해 없음 — SolveFailure | AC-FR05 (실패), **D-01** | **TD-03:** `[[16,2,4,13],[5,11,10,8],[9,7,6,12],[0,14,15,0]]` | **Given** **TD-03**. **When** `solve` 후 실패를 Boundary/Control이 노출. **Then** Domain `SolveFailure` → `E_DOMAIN_NO_SOLUTION`. | `E_DOMAIN_NO_SOLUTION` (I/O 경계) | P1 | | **TC-03**, **TD-03**, D-01 |
| TC-MS-C-001 | 흐름 (SolverOrchestrator) / ECB | 정상 E2E — 유효 입력 | AC-FR01-05, NFR-05 | **TD-01** | **Given** 유효 `matrix`. **When** `boundary → control → entity` 경로로 solve 요청. **Then** 6요소·오류가 아닌 정상 응답. | `int[6]` 성공 형식, 입력 원본 **PI-05** 불변 | P1 | | **US-006**, **TC-01** |
| TC-MS-C-002 | 흐름 / ECB | 입력 실패 시 Entity 미호출 | NFR-05, 짧은 경로 | **TD-04** (무효 크기) | **Given** 무효 입력. **When** Orchestrator 실행. **Then** Boundary에서 종료, solve·Entity **미호출** | 검증 실패 + Entity 호출 없음 | P2 | | PRD **§12**·README US-006 |

---

### 엑셀·슬라이드용: 우선순위 색 (참고)

- **P1:** 핵심 계약·회귀 (TC-01~07, 주요 AC)  
- **P2:** 경계2·부가 방어 (일부 isMagic, TC-08, E2E 짧은 경로)  
- **P3:** (미사용 시 생략; 팀에서 부하/성능 **NFR-04** 스모크 등에 지정 가능)  

---

*행렬·오류코드·`int[6]`·예외명은* `docs/PRD_MagicSquare_4x4_DualTrack_TDD.md` *가 정본이며, 본 표의 TC-MS-xxx ID는 문서·강의용 권고명이다. PRD `TC-01`~`TC-08`과 1:1이 아닌 점(세분)은 비고·PRD 열로 추적한다.*
