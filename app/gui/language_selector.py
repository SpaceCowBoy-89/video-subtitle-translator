"""Language selector — vertically stacked source/target combos for sidebar."""

from __future__ import annotations

from PySide6.QtWidgets import QComboBox, QLabel, QVBoxLayout, QWidget

from app.languages import DEEPL_SOURCE_LANGUAGES, DEEPL_TARGET_LANGUAGES


class LanguageSelector(QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self._init_ui()

    def _init_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)

        # Source
        src_label = QLabel("SOURCE")
        src_label.setStyleSheet(
            "color: #4b5870; font-size: 10px; font-weight: 700;"
            "letter-spacing: 0.8px; background: transparent;"
        )
        layout.addWidget(src_label)

        self.source_combo = QComboBox()
        self.source_combo.addItems(sorted(DEEPL_SOURCE_LANGUAGES.keys()))
        self.source_combo.setCurrentText("Auto-Detect")
        self.source_combo.setMinimumWidth(0)  # let it fill parent
        layout.addWidget(self.source_combo)

        layout.addSpacing(4)

        # Target
        tgt_label = QLabel("TARGET")
        tgt_label.setStyleSheet(
            "color: #4b5870; font-size: 10px; font-weight: 700;"
            "letter-spacing: 0.8px; background: transparent;"
        )
        layout.addWidget(tgt_label)

        self.target_combo = QComboBox()
        self.target_combo.addItems(sorted(DEEPL_TARGET_LANGUAGES.keys()))
        self.target_combo.setMinimumWidth(0)
        layout.addWidget(self.target_combo)

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
