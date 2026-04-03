"""Entry point for Video Subtitle Translator."""

import sys

from PySide6.QtWidgets import QApplication

from app.gui.main_window import MainWindow
from app.gui.theme import STYLESHEET


def main() -> None:
    app = QApplication(sys.argv)
    app.setApplicationName("Video Subtitle Translator")
    app.setOrganizationName("VideoTranslator")
    # Apply at app level so dropdown popups (top-level windows) also get the theme
    app.setStyleSheet(STYLESHEET)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
