"""Drag-and-drop file list widget."""

from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QListWidget

SUPPORTED_EXTENSIONS = {".mp4", ".mkv", ".avi", ".mov", ".webm", ".flv", ".wmv", ".srt", ".vtt"}


class FileListWidget(QListWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.setSelectionMode(QListWidget.ExtendedSelection)

    def dragEnterEvent(self, event) -> None:
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dragMoveEvent(self, event) -> None:
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event) -> None:
        files = []
        for url in event.mimeData().urls():
            path = Path(url.toLocalFile())
            if path.is_file() and path.suffix.lower() in SUPPORTED_EXTENSIONS:
                files.append(str(path))

        # Add unique files only
        existing = {self.item(i).text() for i in range(self.count())}
        for file in files:
            if file not in existing:
                self.addItem(file)

        event.acceptProposedAction()

    def add_files(self, paths: list[str]) -> None:
        """Add files programmatically."""
        existing = {self.item(i).text() for i in range(self.count())}
        for path in paths:
            p = Path(path)
            if p.is_file() and p.suffix.lower() in SUPPORTED_EXTENSIONS and str(p) not in existing:
                self.addItem(str(p))

    def get_files(self) -> list[str]:
        """Get all file paths in the list."""
        return [self.item(i).text() for i in range(self.count())]

    def remove_selected(self) -> None:
        """Remove selected items from the list."""
        for item in self.selectedItems():
            self.takeItem(self.row(item))

    def clear_all(self) -> None:
        """Clear all items."""
        self.clear()
