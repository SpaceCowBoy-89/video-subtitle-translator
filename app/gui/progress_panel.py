"""Progress display panel."""

from __future__ import annotations

from PySide6.QtWidgets import QGroupBox, QLabel, QProgressBar, QVBoxLayout


class ProgressPanel(QGroupBox):
    def __init__(self, parent=None) -> None:
        super().__init__("Progress", parent)
        self._init_ui()

    def _init_ui(self) -> None:
        layout = QVBoxLayout(self)

        layout.addWidget(QLabel("Overall:"))
        self.overall_progress = QProgressBar()
        self.overall_progress.setRange(0, 100)
        layout.addWidget(self.overall_progress)

        layout.addWidget(QLabel("Current File:"))
        self.file_progress = QProgressBar()
        self.file_progress.setRange(0, 100)
        layout.addWidget(self.file_progress)

        self.status_label = QLabel("Ready")
        layout.addWidget(self.status_label)

    def set_overall_progress(self, value: float) -> None:
        """Set overall progress (0.0 to 1.0)."""
        self.overall_progress.setValue(int(value * 100))

    def set_file_progress(self, value: float) -> None:
        """Set current file progress (0.0 to 1.0)."""
        self.file_progress.setValue(int(value * 100))

    def set_status(self, message: str) -> None:
        """Set status message."""
        self.status_label.setText(message)

    def reset(self) -> None:
        """Reset all progress indicators."""
        self.overall_progress.setValue(0)
        self.file_progress.setValue(0)
        self.status_label.setText("Ready")
