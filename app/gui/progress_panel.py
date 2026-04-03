"""Slim progress panel — no GroupBox chrome."""

from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QHBoxLayout, QLabel, QProgressBar, QVBoxLayout, QWidget


class ProgressPanel(QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self._init_ui()

    def _init_ui(self) -> None:
        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(6)

        # Status row
        status_row = QHBoxLayout()
        status_row.setContentsMargins(0, 0, 0, 0)

        self.status_label = QLabel("Ready")
        self.status_label.setStyleSheet(
            "color: #4b5870; font-size: 12px; background: transparent;"
        )
        status_row.addWidget(self.status_label)

        status_row.addStretch()

        self.pct_label = QLabel("")
        self.pct_label.setStyleSheet(
            "color: #253152; font-size: 11px; font-weight: 600;"
            "background: transparent; "
        )
        self.pct_label.setAlignment(Qt.AlignRight)
        status_row.addWidget(self.pct_label)

        outer.addLayout(status_row)

        # Overall bar
        self.overall_progress = QProgressBar()
        self.overall_progress.setRange(0, 100)
        self.overall_progress.setValue(0)
        self.overall_progress.setFixedHeight(5)
        self.overall_progress.setTextVisible(False)
        outer.addWidget(self.overall_progress)

    def set_overall_progress(self, value: float) -> None:
        pct = int(value * 100)
        self.overall_progress.setValue(pct)
        if pct > 0:
            self.pct_label.setText(f"{pct}%")
            self.pct_label.setStyleSheet(
                "color: #0ea5e9; font-size: 11px; font-weight: 600;"
                "background: transparent; "
            )

    def set_file_progress(self, value: float) -> None:
        pass  # Folded into overall for the slim layout

    def set_status(self, message: str) -> None:
        self.status_label.setText(message)

    def reset(self) -> None:
        self.overall_progress.setValue(0)
        self.status_label.setText("Ready")
        self.pct_label.setText("")
        self.pct_label.setStyleSheet(
            "color: #253152; font-size: 11px; font-weight: 600;"
            "background: transparent;"
        )
