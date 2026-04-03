"""Drag-and-drop file list with custom item rendering."""

from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

SUPPORTED_EXTENSIONS = {".mp4", ".mkv", ".avi", ".mov", ".webm", ".flv", ".wmv", ".srt", ".vtt"}

VIDEO_EXTENSIONS = {".mp4", ".mkv", ".avi", ".mov", ".webm", ".flv", ".wmv"}
SUBTITLE_EXTENSIONS = {".srt", ".vtt"}

_TYPE_BADGE = {
    ".mp4": ("MP4", "#0ea5e9"),
    ".mkv": ("MKV", "#0ea5e9"),
    ".avi": ("AVI", "#0ea5e9"),
    ".mov": ("MOV", "#0ea5e9"),
    ".webm": ("WEBM", "#0ea5e9"),
    ".flv": ("FLV", "#0ea5e9"),
    ".wmv": ("WMV", "#0ea5e9"),
    ".srt": ("SRT", "#10b981"),
    ".vtt": ("VTT", "#10b981"),
}


class _FileItemWidget(QWidget):
    """Custom widget for a single file row."""

    def __init__(self, file_path: str, parent=None) -> None:
        super().__init__(parent)
        p = Path(file_path)
        ext = p.suffix.lower()
        label_text, color = _TYPE_BADGE.get(ext, (ext.upper().lstrip("."), "#6b7280"))

        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 8, 10, 8)
        layout.setSpacing(10)

        # Badge
        badge = QLabel(label_text)
        badge.setFixedSize(42, 20)
        badge.setAlignment(Qt.AlignCenter)
        badge.setStyleSheet(
            f"background-color: {color}22; color: {color}; border: 1px solid {color}55;"
            "border-radius: 4px; font-size: 10px; font-weight: 700; letter-spacing: 0.5px;"
        )
        layout.addWidget(badge)

        # Text
        text_col = QVBoxLayout()
        text_col.setSpacing(1)

        name_label = QLabel(p.name)
        name_label.setStyleSheet(
            "color: #c8d0e0; font-size: 13px; font-weight: 600; background: transparent;"
        )
        text_col.addWidget(name_label)

        dir_label = QLabel(str(p.parent))
        dir_label.setStyleSheet(
            "color: #3d4f6a; font-size: 11px; background: transparent;"
        )
        dir_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        text_col.addWidget(dir_label)

        layout.addLayout(text_col)
        layout.addStretch()


class FileListWidget(QListWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.setSelectionMode(QListWidget.ExtendedSelection)
        self.setSpacing(0)

    def _add_item(self, file_path: str) -> None:
        item = QListWidgetItem(self)
        item.setData(Qt.UserRole, file_path)
        item.setSizeHint(__import__("PySide6.QtCore", fromlist=["QSize"]).QSize(0, 52))
        self.addItem(item)
        widget = _FileItemWidget(file_path)
        self.setItemWidget(item, widget)

    def dragEnterEvent(self, event) -> None:
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dragMoveEvent(self, event) -> None:
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event) -> None:
        existing = self._existing_paths()
        for url in event.mimeData().urls():
            path = Path(url.toLocalFile())
            if path.is_file() and path.suffix.lower() in SUPPORTED_EXTENSIONS:
                if str(path) not in existing:
                    self._add_item(str(path))
                    existing.add(str(path))
        event.acceptProposedAction()

    def add_files(self, paths: list[str]) -> None:
        existing = self._existing_paths()
        for path in paths:
            p = Path(path)
            if p.is_file() and p.suffix.lower() in SUPPORTED_EXTENSIONS and str(p) not in existing:
                self._add_item(str(p))
                existing.add(str(p))

    def get_files(self) -> list[str]:
        return [self.item(i).data(Qt.UserRole) for i in range(self.count())]

    def remove_selected(self) -> None:
        for item in self.selectedItems():
            self.takeItem(self.row(item))

    def clear_all(self) -> None:
        self.clear()

    def _existing_paths(self) -> set[str]:
        return {self.item(i).data(Qt.UserRole) for i in range(self.count())}
