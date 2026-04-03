"""Settings dialog — clean modal with section headers."""

from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QComboBox,
    QDialog,
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from app.config import Config
from app.languages import WHISPER_MODELS, TRANSLATION_SERVICES


def _section(title: str) -> QLabel:
    lbl = QLabel(title)
    lbl.setStyleSheet(
        "color: #4b5870; font-size: 10px; font-weight: 700; letter-spacing: 0.8px;"
        "background: transparent; padding-top: 8px;"
    )
    return lbl


def _field_label(text: str) -> QLabel:
    lbl = QLabel(text)
    lbl.setStyleSheet("color: #8b95a8; font-size: 12px; background: transparent;")
    return lbl


class SettingsDialog(QDialog):
    def __init__(self, config: Config, parent=None) -> None:
        super().__init__(parent)
        self._config = config
        self.setWindowTitle("Preferences")
        self.setMinimumWidth(440)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        self._init_ui()
        self._load_settings()

    def _init_ui(self) -> None:
        root = QVBoxLayout(self)
        root.setContentsMargins(24, 24, 24, 20)
        root.setSpacing(0)

        # Header
        header = QLabel("Preferences")
        header.setStyleSheet(
            "color: #d0d6e0; font-size: 17px; font-weight: 700; background: transparent;"
        )
        root.addWidget(header)
        root.addSpacing(4)
        sub = QLabel("Configure translation service and output options")
        sub.setStyleSheet("color: #3d4f6a; font-size: 12px; background: transparent;")
        root.addWidget(sub)
        root.addSpacing(20)

        # Divider
        root.addWidget(_divider())
        root.addSpacing(16)

        # ── Translation ──
        root.addWidget(_section("TRANSLATION"))
        root.addSpacing(10)
        root.addLayout(_row(_field_label("Service"), self._make_service_combo()))
        root.addSpacing(10)
        self.api_key_edit = QLineEdit()
        self.api_key_edit.setEchoMode(QLineEdit.Password)
        self.api_key_edit.setPlaceholderText("Enter your DeepL API key")
        root.addLayout(_row(_field_label("API Key"), self.api_key_edit))
        root.addSpacing(20)

        # Divider
        root.addWidget(_divider())
        root.addSpacing(16)

        # ── Transcription ──
        root.addWidget(_section("TRANSCRIPTION"))
        root.addSpacing(10)
        self.whisper_combo = QComboBox()
        self.whisper_combo.addItems(WHISPER_MODELS)
        hint = QLabel("Larger models are slower but more accurate")
        hint.setStyleSheet("color: #2d3f58; font-size: 11px; background: transparent;")
        root.addLayout(_row(_field_label("Whisper Model"), self.whisper_combo))
        root.addSpacing(4)
        root.addWidget(hint)
        root.addSpacing(20)

        # Divider
        root.addWidget(_divider())
        root.addSpacing(16)

        # ── Output ──
        root.addWidget(_section("OUTPUT"))
        root.addSpacing(10)
        dir_row = QHBoxLayout()
        dir_row.setSpacing(8)
        self.output_dir_edit = QLineEdit()
        self.output_dir_edit.setPlaceholderText("Same folder as input file")
        dir_row.addWidget(self.output_dir_edit)
        self.browse_btn = QPushButton("Browse")
        self.browse_btn.setObjectName("iconBtn")
        self.browse_btn.setFixedWidth(72)
        self.browse_btn.clicked.connect(self._browse_directory)
        dir_row.addWidget(self.browse_btn)
        root.addLayout(_row(_field_label("Output Folder"), dir_row))
        root.addSpacing(24)

        # ── Action buttons ──
        btn_row = QHBoxLayout()
        btn_row.setSpacing(8)
        btn_row.addStretch()

        cancel_btn = QPushButton("Cancel")
        cancel_btn.setObjectName("iconBtn")
        cancel_btn.setFixedWidth(90)
        cancel_btn.clicked.connect(self.reject)
        btn_row.addWidget(cancel_btn)

        save_btn = QPushButton("Save")
        save_btn.setObjectName("primaryBtn")
        save_btn.setFixedWidth(90)
        save_btn.setFixedHeight(36)
        save_btn.clicked.connect(self.accept)
        btn_row.addWidget(save_btn)

        root.addLayout(btn_row)

    def _make_service_combo(self) -> QComboBox:
        self.service_combo = QComboBox()
        self.service_combo.addItems(TRANSLATION_SERVICES.keys())
        self.service_combo.currentTextChanged.connect(self._on_service_changed)
        return self.service_combo

    def _load_settings(self) -> None:
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
        service_code = TRANSLATION_SERVICES.get(service_name, "deepl")
        if service_code == "google":
            self.api_key_edit.setEnabled(False)
            self.api_key_edit.setPlaceholderText("Not required for Google Translate")
        else:
            self.api_key_edit.setEnabled(True)
            self.api_key_edit.setPlaceholderText("Enter your DeepL API key")

    def _browse_directory(self) -> None:
        directory = QFileDialog.getExistingDirectory(self, "Select Output Folder")
        if directory:
            self.output_dir_edit.setText(directory)

    def accept(self) -> None:
        service_name = self.service_combo.currentText()
        self._config.translation_service = TRANSLATION_SERVICES[service_name]
        self._config.deepl_api_key = self.api_key_edit.text()
        self._config.whisper_model = self.whisper_combo.currentText()
        self._config.output_directory = self.output_dir_edit.text()
        super().accept()


def _divider() -> QWidget:
    line = QWidget()
    line.setFixedHeight(1)
    line.setStyleSheet("background-color: #141c2e;")
    return line


def _row(label: QWidget, field) -> QHBoxLayout:
    h = QHBoxLayout()
    h.setSpacing(12)
    label.setFixedWidth(110)
    h.addWidget(label)
    if isinstance(field, QHBoxLayout):
        h.addLayout(field)
    else:
        h.addWidget(field)
    return h
