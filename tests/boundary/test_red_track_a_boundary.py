"""Track A (UI / Boundary) RED — Report/10 UI-A-01~06.

시나리오·계약: Report/10.MagicSquare_DualTrack_RED_TestDesign_Export_Report_2026-04-28.md
구현 없음; pytest 수집 시 의도적 실패(RED).
"""

import pytest


class TestUIRedTrackA:
    """PRD FR-01 / Boundary — 입력·출력 계약 RED."""

    def test_ui_a_01_rejects_non_4x4_matrix(self) -> None:
        pytest.fail("RED: UI-A-01 — E_UI_MATRIX_SIZE (TD-04)")

    def test_ui_a_02_rejects_blank_count_not_two(self) -> None:
        pytest.fail("RED: UI-A-02 — E_UI_BLANK_COUNT (TD-07)")

    def test_ui_a_03_rejects_value_out_of_range(self) -> None:
        pytest.fail("RED: UI-A-03 — E_UI_VALUE_RANGE (TD-05)")

    def test_ui_a_04_rejects_duplicate_nonzero(self) -> None:
        pytest.fail("RED: UI-A-04 — E_UI_DUPLICATE (TD-06)")

    def test_ui_a_05_success_result_length_six(self) -> None:
        pytest.fail("RED: UI-A-05 — int[6] (TD-01)")

    def test_ui_a_06_success_coords_one_indexed(self) -> None:
        pytest.fail("RED: UI-A-06 — 1..4 (TD-01)")
