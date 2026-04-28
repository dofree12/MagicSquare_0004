"""Track A (UI / Boundary) — Report/10 UI-A-01~06.

시나리오·계약: Report/10.MagicSquare_DualTrack_RED_TestDesign_Export_Report_2026-04-28.md
UI-A-01만 GREEN(크기 검증). 나머지는 RED.
"""

import pytest

from magicsquare.boundary import (
    MSG_E_UI_MATRIX_SIZE,
    BoundaryValidationError,
    E_UI_MATRIX_SIZE,
    validate,
)


class TestUIRedTrackA:
    """PRD FR-01 / Boundary — 입력·출력 계약 (UI-A-01 GREEN, 그 외 RED)."""

    def test_ui_a_01_rejects_non_4x4_matrix(self) -> None:
        """TD-04: 3×4 — AC-FR01-01 ``E_UI_MATRIX_SIZE``."""
        matrix_3x4 = [[1, 2, 3, 4], [1, 2, 3, 4], [1, 2, 3, 4]]
        with pytest.raises(BoundaryValidationError) as excinfo:
            validate(matrix_3x4)
        assert excinfo.value.code == E_UI_MATRIX_SIZE
        assert excinfo.value.message == MSG_E_UI_MATRIX_SIZE

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
