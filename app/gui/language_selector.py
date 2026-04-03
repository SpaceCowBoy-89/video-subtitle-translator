"""Language selector widgets for source and target languages."""

from __future__ import annotations

from PySide6.QtWidgets import QComboBox, QHBoxLayout, QLabel, QWidget

from app.languages import DEEPL_SOURCE_LANGUAGES, DEEPL_TARGET_LANGUAGES


class LanguageSelector(QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self._init_ui()

    def _init_ui(self) -> None:
        layout = QHBoxLayout(self)

        layout.addWidget(QLabel("Source Language:"))
        self.source_combo = QComboBox()
        self.source_combo.addItems(sorted(DEEPL_SOURCE_LANGUAGES.keys()))
        self.source_combo.setCurrentText("Auto-Detect")
        layout.addWidget(self.source_combo)

        layout.addWidget(QLabel("Target Language:"))
        self.target_combo = QComboBox()
        self.target_combo.addItems(sorted(DEEPL_TARGET_LANGUAGES.keys()))
        layout.addWidget(self.target_combo)

        layout.addStretch()

    def get_source_language(self) -> str:
        """Get DeepL source language code."""
        return DEEPL_SOURCE_LANGUAGES[self.source_combo.currentText()]

    def get_target_language(self) -> str:
        """Get DeepL target language code."""
        return DEEPL_TARGET_LANGUAGES[self.target_combo.currentText()]

    def set_source_language(self, display_name: str) -> None:
        """Set source language by display name."""
        idx = self.source_combo.findText(display_name)
        if idx >= 0:
            self.source_combo.setCurrentIndex(idx)

    def set_target_language(self, display_name: str) -> None:
        """Set target language by display name."""
        idx = self.target_combo.findText(display_name)
        if idx >= 0:
            self.target_combo.setCurrentIndex(idx)
