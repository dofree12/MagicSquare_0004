"""Pure domain logic — no UI, DB, web, or PyQt (PRD Track B)."""

from __future__ import annotations

from dataclasses import dataclass

from magicsquare.constants import (
    BLANK_VALUE,
    EXPECTED_BLANK_COUNT,
    MATRIX_SIZE,
)


class DomainValidationError(Exception):
    """Raised when domain preconditions are violated (PRD FR-02, etc.)."""


@dataclass(frozen=True)
class Coordinate:
    """1-indexed matrix coordinate value object."""

    row: int
    col: int

    def as_tuple(self) -> tuple[int, int]:
        return (self.row, self.col)


def _validate_expected_blank_count(found: list[Coordinate]) -> None:
    if len(found) != EXPECTED_BLANK_COUNT:
        raise DomainValidationError(
            f"expected exactly {EXPECTED_BLANK_COUNT} blank cells, found {len(found)}"
        )


def find_blank_coords(
    matrix: list[list[int]],
) -> tuple[tuple[int, int], tuple[int, int]]:
    """Return the two blank cells as 1-indexed ``(row, col)`` pairs in row-major order.

    L-RED-01 / FR-02 / BR-05: first blank is the first ``0`` in row-major scan.
    """
    found: list[Coordinate] = []
    for r in range(MATRIX_SIZE):
        for c in range(MATRIX_SIZE):
            if matrix[r][c] == BLANK_VALUE:
                found.append(Coordinate(r + 1, c + 1))
    _validate_expected_blank_count(found)
    return (found[0].as_tuple(), found[1].as_tuple())
