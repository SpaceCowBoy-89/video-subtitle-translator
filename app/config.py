"""QSettings wrapper for application configuration."""

from __future__ import annotations

from PySide6.QtCore import QSettings


class Config:
    def __init__(self) -> None:
        self._settings = QSettings("VideoTranslator", "Translator")

    @property
    def deepl_api_key(self) -> str:
        return self._settings.value("deepl_api_key", "", type=str)

    @deepl_api_key.setter
    def deepl_api_key(self, value: str) -> None:
        self._settings.setValue("deepl_api_key", value)

    @property
    def whisper_model(self) -> str:
        return self._settings.value("whisper_model", "base", type=str)

    @whisper_model.setter
    def whisper_model(self, value: str) -> None:
        self._settings.setValue("whisper_model", value)

    @property
    def output_directory(self) -> str:
        return self._settings.value("output_directory", "", type=str)

    @output_directory.setter
    def output_directory(self, value: str) -> None:
        self._settings.setValue("output_directory", value)

    @property
    def last_source_language(self) -> str:
        return self._settings.value("last_source_language", "Auto-Detect", type=str)

    @last_source_language.setter
    def last_source_language(self, value: str) -> None:
        self._settings.setValue("last_source_language", value)

    @property
    def last_target_language(self) -> str:
        return self._settings.value("last_target_language", "English (American)", type=str)

    @last_target_language.setter
    def last_target_language(self, value: str) -> None:
        self._settings.setValue("last_target_language", value)

    @property
    def translation_service(self) -> str:
        return self._settings.value("translation_service", "deepl", type=str)

    @translation_service.setter
    def translation_service(self, value: str) -> None:
        self._settings.setValue("translation_service", value)
