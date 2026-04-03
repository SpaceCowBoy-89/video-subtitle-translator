"""Settings dialog for API key and preferences."""

from __future__ import annotations

from PySide6.QtWidgets import (
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QFileDialog,
    QFormLayout,
    QHBoxLayout,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
)

from app.config import Config
from app.languages import WHISPER_MODELS, TRANSLATION_SERVICES


class SettingsDialog(QDialog):
    def __init__(self, config: Config, parent=None) -> None:
        super().__init__(parent)
        self._config = config
        self.setWindowTitle("Settings")
        self._init_ui()
        self._load_settings()

    def _init_ui(self) -> None:
        layout = QVBoxLayout(self)

        form = QFormLayout()

        # Translation Service
        self.service_combo = QComboBox()
        self.service_combo.addItems(TRANSLATION_SERVICES.keys())
        self.service_combo.currentTextChanged.connect(self._on_service_changed)
        form.addRow("Translation Service:", self.service_combo)

        # API Key
        self.api_key_edit = QLineEdit()
        self.api_key_edit.setEchoMode(QLineEdit.Password)
        self.api_key_edit.setPlaceholderText("Enter your DeepL API key")
        form.addRow("API Key:", self.api_key_edit)

        # Whisper Model
        self.whisper_combo = QComboBox()
        self.whisper_combo.addItems(WHISPER_MODELS)
        form.addRow("Whisper Model:", self.whisper_combo)

        # Output Directory
        dir_layout = QHBoxLayout()
        self.output_dir_edit = QLineEdit()
        self.output_dir_edit.setPlaceholderText("Same as input file")
        dir_layout.addWidget(self.output_dir_edit)
        self.browse_btn = QPushButton("Browse...")
        self.browse_btn.clicked.connect(self._browse_directory)
        dir_layout.addWidget(self.browse_btn)
        form.addRow("Output Directory:", dir_layout)

        layout.addLayout(form)

        # Buttons
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def _load_settings(self) -> None:
        # Find and set translation service
        service_code = self._config.translation_service
        for display_name, code in TRANSLATION_SERVICES.items():
            if code == service_code:
                self.service_combo.setCurrentText(display_name)
                break

        self.api_key_edit.setText(self._config.deepl_api_key)
        self.whisper_combo.setCurrentText(self._config.whisper_model)
        self.output_dir_edit.setText(self._config.output_directory)
        self._on_service_changed(self.service_combo.currentText())

    def _on_service_changed(self, service_name: str) -> None:
        """Update UI based on selected service."""
        service_code = TRANSLATION_SERVICES.get(service_name, "deepl")

        if service_code == "google":
            self.api_key_edit.setEnabled(False)
            self.api_key_edit.setPlaceholderText("No API key needed for Google Translate")
        else:
            self.api_key_edit.setEnabled(True)
            self.api_key_edit.setPlaceholderText("Enter your DeepL API key")

    def _browse_directory(self) -> None:
        directory = QFileDialog.getExistingDirectory(self, "Select Output Directory")
        if directory:
            self.output_dir_edit.setText(directory)

    def accept(self) -> None:
        service_name = self.service_combo.currentText()
        self._config.translation_service = TRANSLATION_SERVICES[service_name]
        self._config.deepl_api_key = self.api_key_edit.text()
        self._config.whisper_model = self.whisper_combo.currentText()
        self._config.output_directory = self.output_dir_edit.text()
        super().accept()
