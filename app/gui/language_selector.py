"""Language selector with source → target arrow layout."""

from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QComboBox, QHBoxLayout, QLabel, QVBoxLayout, QWidget

from app.languages import DEEPL_SOURCE_LANGUAGES, DEEPL_TARGET_LANGUAGES


class LanguageSelector(QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self._init_ui()

    def _init_ui(self) -> None:
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Source
        src_col = QVBoxLayout()
        src_col.setSpacing(5)
        src_label = QLabel("SOURCE")
        src_label.setProperty("class", "section-title")
        src_col.addWidget(src_label)

        self.source_combo = QComboBox()
        self.source_combo.addItems(sorted(DEEPL_SOURCE_LANGUAGES.keys()))
        self.source_combo.setCurrentText("Auto-Detect")
        src_col.addWidget(self.source_combo)
        layout.addLayout(src_col)

        # Arrow
        arrow = QLabel("→")
        arrow.setAlignment(Qt.AlignCenter)
        arrow.setFixedWidth(44)
        arrow.setStyleSheet(
            "color: #253152; font-size: 20px; font-weight: 300;"
            "padding-top: 18px; background: transparent;"
        )
        layout.addWidget(arrow)

        # Target
        tgt_col = QVBoxLayout()
        tgt_col.setSpacing(5)
        tgt_label = QLabel("TARGET")
        tgt_label.setProperty("class", "section-title")
        tgt_col.addWidget(tgt_label)

        self.target_combo = QComboBox()
        self.target_combo.addItems(sorted(DEEPL_TARGET_LANGUAGES.keys()))
        tgt_col.addWidget(self.target_combo)
        layout.addLayout(tgt_col)

        layout.addStretch()

    def get_source_language(self) -> str:
        return DEEPL_SOURCE_LANGUAGES[self.source_combo.currentText()]

    def get_target_language(self) -> str:
        return DEEPL_TARGET_LANGUAGES[self.target_combo.currentText()]

    def set_source_language(self, display_name: str) -> None:
        idx = self.source_combo.findText(display_name)
        if idx >= 0:
            self.source_combo.setCurrentIndex(idx)

    def set_target_language(self, display_name: str) -> None:
        idx = self.target_combo.findText(display_name)
        if idx >= 0:
            self.target_combo.setCurrentIndex(idx)


class _VBox(QWidget):
    pass
