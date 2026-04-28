"""Safety net tests for refactor-only changes."""

from __future__ import annotations

import pytest

from magicsquare.boundary import (
    MSG_E_UI_MATRIX_SIZE,
    BoundaryValidationError,
    E_UI_MATRIX_SIZE,
    validate,
)
from magicsquare.domain import DomainValidationError, find_blank_coords


def test_find_blank_coords_raises_when_blank_count_not_two() -> None:
    matrix_with_one_blank = [
        [16, 2, 3, 13],
        [0, 5, 10, 8],
        [9, 7, 6, 12],
        [4, 14, 15, 1],
    ]

    with pytest.raises(
        DomainValidationError, match=r"expected exactly 2 blank cells, found 1"
    ):
        find_blank_coords(matrix_with_one_blank)


def test_validate_rejects_row_with_wrong_column_count() -> None:
    matrix_with_short_row = [
        [16, 2, 3, 13],
        [5, 11, 10],
        [9, 7, 6, 12],
        [4, 14, 15, 1],
    ]

    with pytest.raises(BoundaryValidationError) as excinfo:
        validate(matrix_with_short_row)
    assert excinfo.value.code == E_UI_MATRIX_SIZE
    assert excinfo.value.message == MSG_E_UI_MATRIX_SIZE
