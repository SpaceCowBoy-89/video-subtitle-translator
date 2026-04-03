"""Entry point for Video Subtitle Translator."""

import sys

from PySide6.QtWidgets import QApplication

from app.gui.main_window import MainWindow


def main() -> None:
    app = QApplication(sys.argv)
    app.setApplicationName("Video Subtitle Translator")
    app.setOrganizationName("VideoTranslator")

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
