"""Main application window — Cinematic Dark layout."""

from __future__ import annotations

import os
import shutil
import subprocess

from PySide6.QtCore import Qt, QThread
from PySide6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QDialog,
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QScrollArea,
    QSizePolicy,
    QSplitter,
    QStatusBar,
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
        self._ffmpeg_available = self._find_ffmpeg()

        self.setWindowTitle("Subtitle Translator")
        self.resize(980, 680)
        self.setMinimumSize(780, 540)

        self._init_ui()
        self._init_menu()
        self._restore_language_preferences()

        if not self._ffmpeg_available:
            self._status("ffmpeg not found — video burning disabled", error=True)

    # ── ffmpeg detection ────────────────────────────────────────────────────

    def _find_ffmpeg(self) -> bool:
        """Search PATH and common install locations for ffmpeg."""
        if shutil.which("ffmpeg"):
            return True
        common = [
            "/opt/homebrew/bin/ffmpeg",       # Apple Silicon Homebrew
            "/usr/local/bin/ffmpeg",           # Intel Homebrew / manual install
            "/usr/bin/ffmpeg",                 # Linux system
            "/snap/bin/ffmpeg",                # Snap
            os.path.expanduser("~/.local/bin/ffmpeg"),
        ]
        for path in common:
            if os.path.isfile(path) and os.access(path, os.X_OK):
                # Add its directory to PATH so ffmpeg-python and subprocesses find it
                bin_dir = os.path.dirname(path)
                os.environ["PATH"] = bin_dir + os.pathsep + os.environ.get("PATH", "")
                return True
        return False

    # ── Menu ────────────────────────────────────────────────────────────────

    def _init_menu(self) -> None:
        menu = self.menuBar()

        file_menu = menu.addMenu("File")
        file_menu.addAction("Add Files…", self._add_files)
        file_menu.addAction("Clear List", self.file_list.clear_all)
        file_menu.addSeparator()
        file_menu.addAction("Exit", self.close)

        settings_menu = menu.addMenu("Settings")
        settings_menu.addAction("Preferences…", self._open_settings)

        help_menu = menu.addMenu("Help")
        help_menu.addAction("About", self._show_about)

    # ── UI ──────────────────────────────────────────────────────────────────

    def _init_ui(self) -> None:
        root = QWidget()
        self.setCentralWidget(root)
        root_layout = QVBoxLayout(root)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(0)

        # ── Header strip ──
        header = self._make_header()
        root_layout.addWidget(header)

        # ── Body (splitter: sidebar | main) ──
        splitter = QSplitter(Qt.Horizontal)
        splitter.setChildrenCollapsible(False)

        sidebar = self._make_sidebar()
        splitter.addWidget(sidebar)

        main_pane = self._make_main_pane()
        splitter.addWidget(main_pane)

        splitter.setSizes([300, 680])
        splitter.setStretchFactor(0, 0)
        splitter.setStretchFactor(1, 1)
        root_layout.addWidget(splitter, 1)

        # ── Footer strip ──
        footer = self._make_footer()
        root_layout.addWidget(footer)

        # Status bar
        sb = QStatusBar()
        sb.setSizeGripEnabled(False)
        self.setStatusBar(sb)

    def _make_header(self) -> QWidget:
        w = QWidget()
        w.setFixedHeight(56)
        w.setStyleSheet("background-color: #080c14; border-bottom: 1px solid #141c2e;")
        h = QHBoxLayout(w)
        h.setContentsMargins(20, 0, 20, 0)

        title = QLabel("Subtitle Translator")
        title.setStyleSheet(
            "color: #d0d6e0; font-size: 16px; font-weight: 700; letter-spacing: -0.3px;"
            "background: transparent;"
        )
        h.addWidget(title)

        dot = QLabel("·")
        dot.setStyleSheet("color: #253152; font-size: 16px; background: transparent;")
        h.addWidget(dot)

        sub = QLabel("DeepL  &  Google Translate  +  Whisper")
        sub.setStyleSheet("color: #253152; font-size: 12px; background: transparent;")
        h.addWidget(sub)

        h.addStretch()

        settings_btn = QPushButton("⚙  Settings")
        settings_btn.setObjectName("iconBtn")
        settings_btn.clicked.connect(self._open_settings)
        h.addWidget(settings_btn)

        return w

    def _make_sidebar(self) -> QWidget:
        w = QWidget()
        w.setFixedWidth(300)
        w.setStyleSheet("background-color: #0a0e17; border-right: 1px solid #141c2e;")
        layout = QVBoxLayout(w)
        layout.setContentsMargins(18, 20, 18, 20)
        layout.setSpacing(0)

        # ── Language section ──
        layout.addWidget(_section_label("LANGUAGE"))
        layout.addSpacing(10)
        layout.addWidget(self._make_language_section())
        layout.addSpacing(24)

        # ── Options section ──
        layout.addWidget(_section_label("OPTIONS"))
        layout.addSpacing(10)

        # Subtitle source
        layout.addWidget(_field_label("Subtitle Source"))
        layout.addSpacing(5)
        self.subtitle_source_combo = QComboBox()
        self.subtitle_source_combo.addItems(["Auto", "Whisper", "Embedded"])
        self.subtitle_source_combo.setToolTip(
            "Auto: embedded subtitles first, then Whisper\n"
            "Whisper: speech recognition from audio\n"
            "Embedded: extract subtitles from video stream"
        )
        layout.addWidget(self.subtitle_source_combo)
        layout.addSpacing(12)

        # Output format
        layout.addWidget(_field_label("Output Format"))
        layout.addSpacing(5)
        self.format_combo = QComboBox()
        self.format_combo.addItems(["SRT", "VTT"])
        layout.addWidget(self.format_combo)
        layout.addSpacing(16)

        # Burn checkbox
        self.burn_checkbox = QCheckBox("Burn subtitles into video")
        self.burn_checkbox.setEnabled(self._ffmpeg_available)
        if not self._ffmpeg_available:
            self.burn_checkbox.setToolTip("Install ffmpeg to enable video burning")
        layout.addWidget(self.burn_checkbox)

        layout.addStretch()

        # ── Hint ──
        hint = QLabel("Drop video or subtitle files\ninto the panel on the right")
        hint.setStyleSheet(
            "color: #1e2d45; font-size: 11px; line-height: 1.5;"
            "background: transparent;"
        )
        hint.setAlignment(Qt.AlignCenter)
        layout.addWidget(hint)

        return w

    def _make_language_section(self) -> QWidget:
        self.language_selector = LanguageSelector()
        self.language_selector.setStyleSheet("background: transparent;")
        return self.language_selector

    def _make_main_pane(self) -> QWidget:
        w = QWidget()
        layout = QVBoxLayout(w)
        layout.setContentsMargins(20, 20, 20, 16)
        layout.setSpacing(10)

        # Toolbar row
        toolbar = QHBoxLayout()
        toolbar.setSpacing(8)

        count_label_text = "FILES"
        self.file_count_label = QLabel(count_label_text)
        self.file_count_label.setStyleSheet(
            "color: #4b5870; font-size: 10px; font-weight: 700;"
            "letter-spacing: 0.8px; background: transparent;"
        )
        toolbar.addWidget(self.file_count_label)
        toolbar.addStretch()

        add_btn = QPushButton("+ Add Files")
        add_btn.setObjectName("iconBtn")
        add_btn.clicked.connect(self._add_files)
        toolbar.addWidget(add_btn)

        remove_btn = QPushButton("Remove Selected")
        remove_btn.setObjectName("iconBtn")
        remove_btn.clicked.connect(self._remove_and_update)
        toolbar.addWidget(remove_btn)

        layout.addLayout(toolbar)

        # File list
        self.file_list = FileListWidget()
        self.file_list.model().rowsInserted.connect(self._update_file_count)
        self.file_list.model().rowsRemoved.connect(self._update_file_count)
        layout.addWidget(self.file_list, 1)

        return w

    def _make_footer(self) -> QWidget:
        w = QWidget()
        w.setFixedHeight(68)
        w.setStyleSheet("background-color: #080c14; border-top: 1px solid #141c2e;")
        h = QHBoxLayout(w)
        h.setContentsMargins(20, 0, 20, 0)
        h.setSpacing(16)

        # Progress (takes most space)
        self.progress_panel = ProgressPanel()
        h.addWidget(self.progress_panel, 1)

        # Buttons
        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.setObjectName("cancelBtn")
        self.cancel_btn.setFixedHeight(40)
        self.cancel_btn.setFixedWidth(100)
        self.cancel_btn.setEnabled(False)
        self.cancel_btn.clicked.connect(self._cancel_processing)
        h.addWidget(self.cancel_btn)

        self.start_btn = QPushButton("Translate")
        self.start_btn.setObjectName("primaryBtn")
        self.start_btn.setFixedHeight(40)
        self.start_btn.setFixedWidth(120)
        self.start_btn.clicked.connect(self._start_processing)
        h.addWidget(self.start_btn)

        return w

    # ── Helpers ─────────────────────────────────────────────────────────────

    def _restore_language_preferences(self) -> None:
        self.language_selector.set_source_language(self._config.last_source_language)
        self.language_selector.set_target_language(self._config.last_target_language)

    def _update_file_count(self) -> None:
        n = self.file_list.count()
        if n == 0:
            self.file_count_label.setText("FILES")
        else:
            self.file_count_label.setText(f"FILES  ·  {n}")

    def _remove_and_update(self) -> None:
        self.file_list.remove_selected()

    def _status(self, msg: str, error: bool = False) -> None:
        color = "#7f3535" if error else "#3d4f6a"
        self.statusBar().setStyleSheet(
            f"background-color: #080c14; color: {color};"
            "border-top: 1px solid #141c2e; font-size: 11px; padding: 0 8px;"
        )
        self.statusBar().showMessage(msg)

    # ── Actions ─────────────────────────────────────────────────────────────

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
        SettingsDialog(self._config, self).exec()

    def _show_about(self) -> None:
        QMessageBox.about(
            self,
            "Subtitle Translator",
            "Subtitle Translator\n\n"
            "Translate and burn subtitles into videos.\n\n"
            "Powered by DeepL, Google Translate,\n"
            "OpenAI Whisper, and ffmpeg.",
        )

    def _start_processing(self) -> None:
        files = self.file_list.get_files()
        if not files:
            QMessageBox.warning(self, "No Files", "Add at least one file to process.")
            return

        translation_service = self._config.translation_service
        api_key = self._config.deepl_api_key

        if translation_service == "deepl" and not api_key:
            QMessageBox.warning(
                self,
                "API Key Required",
                "Enter your DeepL API key in Settings,\nor switch to Google Translate (free).",
            )
            return

        self._config.last_source_language = self.language_selector.source_combo.currentText()
        self._config.last_target_language = self.language_selector.target_combo.currentText()

        configs = [
            JobConfig(
                input_path=f,
                target_lang=self.language_selector.get_target_language(),
                source_lang=self.language_selector.get_source_language(),
                subtitle_source=self.subtitle_source_combo.currentText().lower(),
                burn=self.burn_checkbox.isChecked(),
                output_format=self.format_combo.currentText().lower(),
                output_dir=self._config.output_directory,
                whisper_model=self._config.whisper_model,
            )
            for f in files
        ]

        self._thread = QThread()
        self._worker = BatchWorker(api_key, configs, self._config.whisper_model, translation_service)
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
        self._status("Processing…")

    def _cancel_processing(self) -> None:
        if self._worker:
            self._worker.cancel()
            self.progress_panel.set_status("Cancelling…")

    def _on_finished(self, result: dict) -> None:
        self._cleanup_thread()
        completed = result.get("completed", 0)
        failed = result.get("failed", 0)
        results = result.get("results", [])

        if completed == 0 and failed > 0:
            # All jobs failed — show the first error prominently
            first_error = next((r["error"] for r in results if not r["success"]), "Unknown error")
            self._status(f"Failed — {first_error}", error=True)
            QMessageBox.critical(self, "Translation Failed", f"{failed} file(s) failed.\n\n{first_error}")
            return

        self._status(f"Done — {completed} file(s) translated" + (f", {failed} failed" if failed else ""))
        _ResultsDialog(results, self).exec()

    def _on_error(self, error_msg: str) -> None:
        self._cleanup_thread()
        self.progress_panel.set_status(f"Error: {error_msg}")
        self._status(f"Error: {error_msg}", error=True)
        QMessageBox.critical(self, "Error", error_msg)

    def _cleanup_thread(self) -> None:
        if self._thread:
            self._thread.quit()
            self._thread.wait()
            self._thread = None
            self._worker = None
        self.start_btn.setEnabled(True)
        self.cancel_btn.setEnabled(False)
        self.progress_panel.reset()


# ── Utility widgets ──────────────────────────────────────────────────────────

def _section_label(text: str) -> QLabel:
    lbl = QLabel(text)
    lbl.setStyleSheet(
        "color: #4b5870; font-size: 10px; font-weight: 700;"
        "letter-spacing: 0.8px; background: transparent;"
    )
    return lbl


def _field_label(text: str) -> QLabel:
    lbl = QLabel(text)
    lbl.setStyleSheet(
        "color: #6b7280; font-size: 12px; font-weight: 500; background: transparent;"
    )
    return lbl


# ── Results dialog ───────────────────────────────────────────────────────────

class _ResultsDialog(QDialog):
    """Shows per-file outcomes with output paths and a Reveal in Finder button."""

    def __init__(self, results: list[dict], parent=None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Translation Complete")
        self.setMinimumWidth(520)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        self._build(results)

    def _build(self, results: list[dict]) -> None:
        root = QVBoxLayout(self)
        root.setContentsMargins(24, 24, 24, 20)
        root.setSpacing(0)

        ok = [r for r in results if r["success"]]
        bad = [r for r in results if not r["success"]]

        # Header
        title = QLabel(f"{len(ok)} file(s) translated" + (f", {len(bad)} failed" if bad else ""))
        title.setStyleSheet(
            "color: #d0d6e0; font-size: 16px; font-weight: 700; background: transparent;"
        )
        root.addWidget(title)
        root.addSpacing(16)

        # Scroll area for results
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QScrollArea.NoFrame)
        scroll.setMaximumHeight(300)

        inner = QWidget()
        inner_layout = QVBoxLayout(inner)
        inner_layout.setContentsMargins(0, 0, 0, 0)
        inner_layout.setSpacing(8)

        for r in results:
            inner_layout.addWidget(self._make_row(r))

        inner_layout.addStretch()
        scroll.setWidget(inner)
        root.addWidget(scroll)
        root.addSpacing(20)

        # Close button
        btn_row = QHBoxLayout()
        btn_row.addStretch()
        close_btn = QPushButton("Close")
        close_btn.setObjectName("primaryBtn")
        close_btn.setMinimumWidth(90)
        close_btn.setFixedHeight(36)
        close_btn.clicked.connect(self.accept)
        btn_row.addWidget(close_btn)
        root.addLayout(btn_row)

    def _make_row(self, r: dict) -> QWidget:
        row = QWidget()
        row.setStyleSheet(
            "background-color: #0f1520; border-radius: 8px; border: 1px solid #1c2840;"
        )
        h = QHBoxLayout(row)
        h.setContentsMargins(12, 10, 12, 10)
        h.setSpacing(10)

        if r["success"]:
            dot = QLabel("●")
            dot.setStyleSheet("color: #10b981; font-size: 10px; background: transparent;")
            dot.setFixedWidth(14)
            h.addWidget(dot)

            out_path = r.get("subtitle_path") or r.get("video_path", "")
            name = os.path.basename(out_path) if out_path else os.path.basename(r["input"])
            lbl = QLabel(name)
            lbl.setStyleSheet(
                "color: #c0c8d8; font-size: 13px; font-weight: 600; background: transparent;"
            )
            h.addWidget(lbl, 1)

            if out_path and os.path.exists(out_path):
                reveal_btn = QPushButton("Reveal")
                reveal_btn.setObjectName("iconBtn")
                reveal_btn.setFixedWidth(64)
                reveal_btn.setFixedHeight(28)
                _path = out_path
                reveal_btn.clicked.connect(lambda _, p=_path: subprocess.run(["open", "-R", p]))
                h.addWidget(reveal_btn)
        else:
            dot = QLabel("●")
            dot.setStyleSheet("color: #ef4444; font-size: 10px; background: transparent;")
            dot.setFixedWidth(14)
            h.addWidget(dot)

            name = os.path.basename(r["input"])
            col = QVBoxLayout()
            col.setSpacing(2)
            name_lbl = QLabel(name)
            name_lbl.setStyleSheet(
                "color: #c0c8d8; font-size: 13px; font-weight: 600; background: transparent;"
            )
            col.addWidget(name_lbl)
            err_lbl = QLabel(r["error"])
            err_lbl.setStyleSheet(
                "color: #7f3535; font-size: 11px; background: transparent;"
            )
            err_lbl.setWordWrap(True)
            col.addWidget(err_lbl)
            h.addLayout(col)

        return row
