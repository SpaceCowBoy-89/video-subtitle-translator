"""Base worker class for background tasks."""

from __future__ import annotations

from PySide6.QtCore import QObject, Signal


class BaseWorker(QObject):
    """Base worker with standard signals."""

    progress = Signal(float)  # 0.0 to 1.0
    status = Signal(str)  # Status message
    finished = Signal(dict)  # Result dictionary
    error = Signal(str)  # Error message
