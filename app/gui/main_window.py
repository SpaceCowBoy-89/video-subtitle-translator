"""Main application window."""

from __future__ import annotations

import shutil

from PySide6.QtCore import QThread
from PySide6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QFileDialog,
    QGroupBox,
    QHBoxLayout,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from app.config import Config
from app.core.pipeline import JobConfig
from app.gui.file_list_widget import FileListWidget
from app.gui.language_selector import LanguageSelector
from app.gui.progress_panel import ProgressPanel
from app.gui.settings_dialog import SettingsDialog
from app.workers.batch_worker import BatchWorker


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self._config = Config()
        self._worker = None
        self._thread = None
        self._ffmpeg_available = self._check_ffmpeg()

        self.setWindowTitle("Video Subtitle Translator")
        self.resize(800, 600)

        self._init_ui()
        self._init_menu()
        self._restore_language_preferences()

    def _check_ffmpeg(self) -> bool:
        """Check if ffmpeg is installed."""
        return shutil.which("ffmpeg") is not None

    def _init_menu(self) -> None:
        menu = self.menuBar()

        file_menu = menu.addMenu("&File")
        file_menu.addAction("Add Files...", self._add_files)
        file_menu.addAction("Clear List", self.file_list.clear_all)
        file_menu.addSeparator()
        file_menu.addAction("Exit", self.close)

        settings_menu = menu.addMenu("&Settings")
        settings_menu.addAction("Preferences...", self._open_settings)

        help_menu = menu.addMenu("&Help")
        help_menu.addAction("About", self._show_about)

    def _init_ui(self) -> None:
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)

        # Language selector
        self.language_selector = LanguageSelector()
        layout.addWidget(self.language_selector)

        # File list
        file_group = QGroupBox("Files")
        file_layout = QVBoxLayout(file_group)

        self.file_list = FileListWidget()
        file_layout.addWidget(self.file_list)

        btn_layout = QHBoxLayout()
        self.add_btn = QPushButton("Add Files...")
        self.add_btn.clicked.connect(self._add_files)
        btn_layout.addWidget(self.add_btn)

        self.remove_btn = QPushButton("Remove Selected")
        self.remove_btn.clicked.connect(self.file_list.remove_selected)
        btn_layout.addWidget(self.remove_btn)

        btn_layout.addStretch()
        file_layout.addLayout(btn_layout)
        layout.addWidget(file_group)

        # Options
        options_group = QGroupBox("Options")
        options_layout = QVBoxLayout(options_group)

        row1 = QHBoxLayout()
        row1.addWidget(QWidget().parent().findChild(QWidget, "label") or QWidget())  # placeholder
        self.subtitle_source_combo = QComboBox()
        self.subtitle_source_combo.addItems(["Auto", "Whisper", "Embedded"])
        row1.addWidget(QWidget())  # label placeholder
        options_layout.addLayout(row1)

        # Recreate options layout properly
        options_layout = QVBoxLayout(options_group)

        sub_layout = QHBoxLayout()
        from PySide6.QtWidgets import QLabel
        sub_layout.addWidget(QLabel("Subtitle Source:"))
        self.subtitle_source_combo = QComboBox()
        self.subtitle_source_combo.addItems(["Auto", "Whisper", "Embedded"])
        sub_layout.addWidget(self.subtitle_source_combo)
        sub_layout.addStretch()
        options_layout.addLayout(sub_layout)

        fmt_layout = QHBoxLayout()
        fmt_layout.addWidget(QLabel("Output Format:"))
        self.format_combo = QComboBox()
        self.format_combo.addItems(["SRT", "VTT"])
        fmt_layout.addWidget(self.format_combo)
        fmt_layout.addStretch()
        options_layout.addLayout(fmt_layout)

        self.burn_checkbox = QCheckBox("Burn subtitles into video")
        self.burn_checkbox.setEnabled(self._ffmpeg_available)
        if not self._ffmpeg_available:
            self.burn_checkbox.setToolTip("ffmpeg not found - video burning disabled")
        options_layout.addWidget(self.burn_checkbox)

        layout.addWidget(options_group)

        # Progress
        self.progress_panel = ProgressPanel()
        layout.addWidget(self.progress_panel)

        # Control buttons
        control_layout = QHBoxLayout()
        self.start_btn = QPushButton("Start")
        self.start_btn.clicked.connect(self._start_processing)
        control_layout.addWidget(self.start_btn)

        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.clicked.connect(self._cancel_processing)
        self.cancel_btn.setEnabled(False)
        control_layout.addWidget(self.cancel_btn)

        control_layout.addStretch()
        layout.addLayout(control_layout)

        if not self._ffmpeg_available:
            QMessageBox.warning(
                self,
                "ffmpeg Not Found",
                "ffmpeg is not installed or not in PATH. Video-related features will be disabled.",
            )

    def _restore_language_preferences(self) -> None:
        self.language_selector.set_source_language(self._config.last_source_language)
        self.language_selector.set_target_language(self._config.last_target_language)

    def _add_files(self) -> None:
        files, _ = QFileDialog.getOpenFileNames(
            self,
            "Select Files",
            "",
            "Supported Files (*.mp4 *.mkv *.avi *.mov *.webm *.srt *.vtt);;All Files (*)",
        )
        if files:
            self.file_list.add_files(files)

    def _open_settings(self) -> None:
        dialog = SettingsDialog(self._config, self)
        dialog.exec()

    def _show_about(self) -> None:
        QMessageBox.about(
            self,
            "About Video Subtitle Translator",
            "Video Subtitle Translator\n\n"
            "Translate and burn subtitles into videos using DeepL and Whisper.\n\n"
            "Built with PySide6, DeepL, OpenAI Whisper, and ffmpeg.",
        )

    def _start_processing(self) -> None:
        files = self.file_list.get_files()
        if not files:
            QMessageBox.warning(self, "No Files", "Please add files to process.")
            return

        # Check API key requirement based on service
        translation_service = self._config.translation_service
        api_key = self._config.deepl_api_key

        if translation_service == "deepl" and not api_key:
            QMessageBox.warning(
                self,
                "API Key Required",
                "Please configure your DeepL API key in Settings, or switch to Google Translate (free).",
            )
            return

        # Save language preferences
        src_display = self.language_selector.source_combo.currentText()
        tgt_display = self.language_selector.target_combo.currentText()
        self._config.last_source_language = src_display
        self._config.last_target_language = tgt_display

        # Build job configs
        configs = []
        for file_path in files:
            config = JobConfig(
                input_path=file_path,
                target_lang=self.language_selector.get_target_language(),
                source_lang=self.language_selector.get_source_language(),
                subtitle_source=self.subtitle_source_combo.currentText().lower(),
                burn=self.burn_checkbox.isChecked(),
                output_format=self.format_combo.currentText().lower(),
                output_dir=self._config.output_directory,
                whisper_model=self._config.whisper_model,
            )
            configs.append(config)

        # Start worker thread
        self._thread = QThread()
        self._worker = BatchWorker(
            api_key,
            configs,
            self._config.whisper_model,
            translation_service
        )
        self._worker.moveToThread(self._thread)

        self._worker.progress.connect(self.progress_panel.set_overall_progress)
        self._worker.status.connect(self.progress_panel.set_status)
        self._worker.finished.connect(self._on_finished)
        self._worker.error.connect(self._on_error)

        self._thread.started.connect(self._worker.run)
        self._thread.finished.connect(self._thread.deleteLater)

        self._thread.start()

        self.start_btn.setEnabled(False)
        self.cancel_btn.setEnabled(True)

    def _cancel_processing(self) -> None:
        if self._worker:
            self._worker.cancel()

    def _on_finished(self, result: dict) -> None:
        self._cleanup_thread()
        completed = result.get("completed", 0)
        QMessageBox.information(
            self,
            "Processing Complete",
            f"Completed {completed} file(s).",
        )

    def _on_error(self, error_msg: str) -> None:
        self.progress_panel.set_status(f"Error: {error_msg}")

    def _cleanup_thread(self) -> None:
        if self._thread:
            self._thread.quit()
            self._thread.wait()
            self._thread = None
            self._worker = None

        self.start_btn.setEnabled(True)
        self.cancel_btn.setEnabled(False)
        self.progress_panel.reset()
