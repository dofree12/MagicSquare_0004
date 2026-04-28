"""Minimal PyQt6 screen for validating and invoking Magic Square flows."""

from __future__ import annotations

import sys
from typing import List

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from magicsquare.boundary import BoundaryValidationError, validate
from magicsquare.constants import MATRIX_SIZE
from magicsquare.domain import DomainValidationError, find_blank_coords


class MainWindow(QMainWindow):
    """MVP screen: 4x4 input grid + Solve button + result label."""

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Magic Square 4x4")

        self._inputs: List[List[QLineEdit]] = []
        self._status_label = QLabel("Ready")
        self._result_label = QLabel("Result: -")

        central = QWidget()
        root = QVBoxLayout()
        grid = QGridLayout()

        for r in range(MATRIX_SIZE):
            row_widgets: List[QLineEdit] = []
            for c in range(MATRIX_SIZE):
                cell = QLineEdit("0")
                cell.setMaxLength(2)
                cell.setFixedWidth(56)
                cell.setAlignment(Qt.AlignmentFlag.AlignCenter)
                grid.addWidget(cell, r, c)
                row_widgets.append(cell)
            self._inputs.append(row_widgets)

        buttons = QHBoxLayout()
        solve_button = QPushButton("Solve")
        solve_button.clicked.connect(self._on_solve_clicked)
        buttons.addWidget(solve_button)

        root.addLayout(grid)
        root.addLayout(buttons)
        root.addWidget(self._result_label)
        root.addWidget(self._status_label)

        central.setLayout(root)
        self.setCentralWidget(central)

    def _read_matrix(self) -> list[list[int]]:
        matrix: list[list[int]] = []
        for row in self._inputs:
            out_row: list[int] = []
            for cell in row:
                text = cell.text().strip()
                if text == "":
                    raise ValueError("Use 0 for blank cells; do not leave fields empty.")
                try:
                    out_row.append(int(text))
                except ValueError as exc:
                    raise ValueError("All cells must be integers.") from exc
            matrix.append(out_row)
        return matrix

    def _on_solve_clicked(self) -> None:
        try:
            matrix = self._read_matrix()
            validate(matrix)
            blank1, blank2 = find_blank_coords(matrix)

            # Full solve is not implemented yet; keep output shape visible for MVP.
            preview_result = [blank1[0], blank1[1], 0, blank2[0], blank2[1], 0]
            self._result_label.setText(f"Result: {preview_result}")
            self._status_label.setText("Boundary validate + Domain blank scan OK")
        except (BoundaryValidationError, DomainValidationError, ValueError) as exc:
            self._status_label.setText("Error")
            QMessageBox.critical(self, "Validation Error", str(exc))


def run() -> int:
    """Start Qt app and return process exit code."""
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    return app.exec()

