"""Pure domain logic — no UI, DB, web, or PyQt (PRD Track B)."""

from __future__ import annotations

from magicsquare.constants import (
    BLANK_VALUE,
    EXPECTED_BLANK_COUNT,
    MATRIX_SIZE,
)


class DomainValidationError(Exception):
    """Raised when domain preconditions are violated (PRD FR-02, etc.)."""


def find_blank_coords(
    matrix: list[list[int]],
) -> tuple[tuple[int, int], tuple[int, int]]:
    """Return the two blank cells as 1-indexed ``(row, col)`` pairs in row-major order.

    L-RED-01 / FR-02 / BR-05: first blank is the first ``0`` in row-major scan.
    """
    found: list[tuple[int, int]] = []
    for r in range(MATRIX_SIZE):
        for c in range(MATRIX_SIZE):
            if matrix[r][c] == BLANK_VALUE:
                found.append((r + 1, c + 1))
    if len(found) != EXPECTED_BLANK_COUNT:
        raise DomainValidationError(
            f"expected exactly {EXPECTED_BLANK_COUNT} blank cells, found {len(found)}"
        )
    return (found[0], found[1])
