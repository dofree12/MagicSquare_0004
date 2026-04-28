"""Track A boundary — I/O contract validation (no Domain business rules, no Qt)."""

from __future__ import annotations

from magicsquare.constants import MATRIX_SIZE


class BoundaryValidationError(Exception):
    """Raised when external input violates the I/O contract (PRD §10.1)."""

    def __init__(self, code: str, message: str) -> None:
        self.code = code
        self.message = message
        super().__init__(message)


E_UI_MATRIX_SIZE = "E_UI_MATRIX_SIZE"
MSG_E_UI_MATRIX_SIZE = (
    f"Input matrix must be {MATRIX_SIZE} rows of {MATRIX_SIZE} integers each."
)


def _raise_matrix_size_error() -> None:
    raise BoundaryValidationError(E_UI_MATRIX_SIZE, MSG_E_UI_MATRIX_SIZE)


class BoundaryInputValidator:
    """FR-01 — validates external ``int[][]`` before Domain."""

    def validate_matrix_shape(self, matrix: list[list[int]]) -> None:
        """AC-FR01-01: reject non-4×4 boards (row/column lengths only)."""
        if not isinstance(matrix, list) or len(matrix) != MATRIX_SIZE:
            _raise_matrix_size_error()
        for row in matrix:
            if not isinstance(row, list) or len(row) != MATRIX_SIZE:
                _raise_matrix_size_error()


def validate(matrix: list[list[int]]) -> None:
    """U-RED-01 / public entry: ensure matrix dimensions are ``MATRIX_SIZE × MATRIX_SIZE``."""
    BoundaryInputValidator().validate_matrix_shape(matrix)
