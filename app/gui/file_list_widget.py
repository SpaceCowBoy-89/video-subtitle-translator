"""Drag-and-drop file list with custom item rendering and empty-state paint."""

from __future__ import annotations

from pathlib import Path

import math

from PySide6.QtCore import Qt, QSize, QTimer, Signal
from PySide6.QtGui import QColor, QFont, QPainter, QPen, QRadialGradient
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
VIDEO_EXTENSIONS    = {".mp4", ".mkv", ".avi", ".mov", ".webm", ".flv", ".wmv"}
SUBTITLE_EXTENSIONS = {".srt", ".vtt"}

_TYPE_BADGE = {
    ".mp4":  ("MP4",  "#0ea5e9"),
    ".mkv":  ("MKV",  "#0ea5e9"),
    ".avi":  ("AVI",  "#0ea5e9"),
    ".mov":  ("MOV",  "#0ea5e9"),
    ".webm": ("WEBM", "#0ea5e9"),
    ".flv":  ("FLV",  "#0ea5e9"),
    ".wmv":  ("WMV",  "#0ea5e9"),
    ".srt":  ("SRT",  "#10b981"),
    ".vtt":  ("VTT",  "#10b981"),
}


class _FileItemWidget(QWidget):
    def __init__(self, file_path: str, parent=None) -> None:
        super().__init__(parent)
        p = Path(file_path)
        ext = p.suffix.lower()
        label_text, color = _TYPE_BADGE.get(ext, (ext.upper().lstrip("."), "#6b7280"))

        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 8, 10, 8)
        layout.setSpacing(10)

        badge = QLabel(label_text)
        badge.setFixedSize(42, 20)
        badge.setAlignment(Qt.AlignCenter)
        badge.setStyleSheet(
            f"background-color: {color}22; color: {color}; border: 1px solid {color}55;"
            "border-radius: 4px; font-size: 10px; font-weight: 700; letter-spacing: 0.5px;"
        )
        layout.addWidget(badge)

        text_col = QVBoxLayout()
        text_col.setSpacing(1)

        name_label = QLabel(p.name)
        name_label.setStyleSheet(
            "color: #c8d0e0; font-size: 13px; font-weight: 600; background: transparent;"
        )
        text_col.addWidget(name_label)

        dir_label = QLabel(str(p.parent))
        dir_label.setStyleSheet("color: #2d3f58; font-size: 11px; background: transparent;")
        dir_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        text_col.addWidget(dir_label)

        layout.addLayout(text_col)
        layout.addStretch()


class FileListWidget(QListWidget):
    # Emitted when the selected file changes; passes the file path (or "" for none)
    file_selected = Signal(str)

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.setSelectionMode(QListWidget.SingleSelection)
        self.setSpacing(0)
        self.currentItemChanged.connect(self._emit_selection)

        # Breathing animation for empty state
        self._anim_phase = 0.0
        self._anim_timer = QTimer(self)
        self._anim_timer.timeout.connect(self._tick_anim)
        self._anim_timer.start(40)  # 25 fps

    def _tick_anim(self) -> None:
        if self.count() == 0:
            self._anim_phase = (self._anim_phase + 0.03) % (2 * math.pi)
            self.viewport().update()

    # ── Empty-state painting ─────────────────────────────────────────────────

    def paintEvent(self, event) -> None:
        super().paintEvent(event)
        if self.count() > 0:
            return

        painter = QPainter(self.viewport())
        painter.setRenderHint(QPainter.Antialiasing)
        vp   = self.viewport().rect()
        inset = vp.adjusted(20, 20, -20, -20)
        cx, cy = vp.center().x(), vp.center().y()

        # ── Dot grid atmosphere ──────────────────────────────────────────────
        dot_alpha = int(25 + 8 * math.sin(self._anim_phase))
        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor(30, 50, 80, dot_alpha))
        spacing = 22
        for gx in range(inset.left(), inset.right(), spacing):
            for gy in range(inset.top(), inset.bottom(), spacing):
                painter.drawEllipse(gx, gy, 2, 2)

        # ── Breathing border ─────────────────────────────────────────────────
        t     = (math.sin(self._anim_phase) + 1) / 2          # 0-1
        alpha = int(35 + t * 55)                                # 35-90
        r, g, b = 14, 165, 233                                  # #0ea5e9 cyan
        border_color = QColor(r, g, b, alpha)

        pen = QPen(border_color, 1, Qt.DashLine)
        pen.setDashPattern([5, 5])
        painter.setPen(pen)
        painter.setBrush(Qt.NoBrush)
        painter.drawRoundedRect(inset, 12, 12)

        # ── Radial glow at center ────────────────────────────────────────────
        glow_alpha = int(12 + t * 18)
        grad = QRadialGradient(cx, cy, 120)
        grad.setColorAt(0.0, QColor(14, 165, 233, glow_alpha))
        grad.setColorAt(1.0, QColor(0, 0, 0, 0))
        painter.setBrush(grad)
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(cx - 120, cy - 120, 240, 240)

        # ── Upload icon ──────────────────────────────────────────────────────
        icon_alpha = int(80 + t * 60)
        icon_font = QFont("Helvetica Neue", 26)
        painter.setFont(icon_font)
        painter.setPen(QColor(14, 165, 233, icon_alpha))
        from PySide6.QtCore import QRect
        icon_rect = QRect(vp.left(), cy - 70, vp.width(), 50)
        painter.drawText(icon_rect, Qt.AlignHCenter | Qt.AlignVCenter, "↓")

        # ── Primary label ────────────────────────────────────────────────────
        pf = QFont("Helvetica Neue", 13)
        pf.setWeight(QFont.DemiBold)
        painter.setFont(pf)
        painter.setPen(QColor(50, 80, 120, 220))
        p_rect = QRect(vp.left(), cy - 10, vp.width(), 30)
        painter.drawText(p_rect, Qt.AlignHCenter | Qt.AlignVCenter, "Drop files here")

        # ── Secondary label ──────────────────────────────────────────────────
        sf = QFont("Helvetica Neue", 11)
        painter.setFont(sf)
        painter.setPen(QColor(35, 55, 85, 180))
        s_rect = QRect(vp.left(), cy + 20, vp.width(), 24)
        painter.drawText(s_rect, Qt.AlignHCenter | Qt.AlignVCenter,
                         "or click  + Add Files  above")

    # ── Drag and drop ────────────────────────────────────────────────────────

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

    # ── Public API ───────────────────────────────────────────────────────────

    def add_files(self, paths: list[str]) -> None:
        existing = self._existing_paths()
        for path in paths:
            p = Path(path)
            if (
                p.is_file()
                and p.suffix.lower() in SUPPORTED_EXTENSIONS
                and str(p) not in existing
            ):
                self._add_item(str(p))
                existing.add(str(p))
        # Auto-select first item if nothing is selected yet
        if self.count() > 0 and self.currentRow() < 0:
            self.setCurrentRow(0)

    def get_files(self) -> list[str]:
        return [self.item(i).data(Qt.UserRole) for i in range(self.count())]

    def remove_selected(self) -> None:
        for item in self.selectedItems():
            self.takeItem(self.row(item))

    def clear_all(self) -> None:
        self.clear()
        self.file_selected.emit("")

    # ── Private ──────────────────────────────────────────────────────────────

    def _add_item(self, file_path: str) -> None:
        item = QListWidgetItem(self)
        item.setData(Qt.UserRole, file_path)
        item.setSizeHint(QSize(0, 52))
        self.addItem(item)
        self.setItemWidget(item, _FileItemWidget(file_path))

    def _emit_selection(self, current, _previous) -> None:
        if current is not None:
            self.file_selected.emit(current.data(Qt.UserRole))
        else:
            self.file_selected.emit("")

    def _existing_paths(self) -> set[str]:
        return {self.item(i).data(Qt.UserRole) for i in range(self.count())}
