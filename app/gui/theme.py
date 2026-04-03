"""Application-wide Qt stylesheet — Cinematic Dark theme."""

STYLESHEET = """
/* ── Base ── */
* {
    font-family: "Helvetica Neue", Arial;
    font-size: 13px;
}
QWidget {
    background-color: #0d1117;
    color: #d0d6e0;
}

/* ── Main Window ── */
QMainWindow {
    background-color: #0d1117;
}

/* ── Menu Bar ── */
QMenuBar {
    background-color: #0d1117;
    color: #6b7280;
    border-bottom: 1px solid #1c2333;
    padding: 2px 8px;
    spacing: 2px;
}
QMenuBar::item {
    padding: 5px 10px;
    border-radius: 5px;
    background: transparent;
}
QMenuBar::item:selected {
    background-color: #1c2333;
    color: #d0d6e0;
}
QMenu {
    background-color: #141c2e;
    border: 1px solid #253152;
    border-radius: 8px;
    padding: 5px;
}
QMenu::item {
    padding: 7px 28px 7px 12px;
    border-radius: 5px;
    color: #c0c8d8;
}
QMenu::item:selected {
    background-color: #1c2c4a;
    color: #38bdf8;
}
QMenu::separator {
    height: 1px;
    background-color: #1c2333;
    margin: 4px 8px;
}

/* ── Group Box ── */
QGroupBox {
    border: 1px solid #1c2333;
    border-radius: 10px;
    margin-top: 12px;
    padding: 14px 14px 10px 14px;
    font-size: 10px;
    font-weight: 700;
    color: #4b5870;
    letter-spacing: 0.8px;
    text-transform: uppercase;
}
QGroupBox::title {
    subcontrol-origin: margin;
    subcontrol-position: top left;
    left: 14px;
    padding: 0 6px;
    background-color: #0d1117;
}

/* ── Labels ── */
QLabel {
    background: transparent;
    color: #6b7280;
    font-size: 12px;
}
QLabel[class="section-title"] {
    color: #4b5870;
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 0.8px;
}
QLabel[class="field-label"] {
    color: #8b95a8;
    font-size: 12px;
    font-weight: 500;
}

/* ── Combo Box ── */
QComboBox {
    background-color: #141c2e;
    border: 1px solid #253152;
    border-radius: 7px;
    padding: 7px 30px 7px 11px;
    color: #d0d6e0;
    font-size: 13px;
    selection-background-color: transparent;
}
QComboBox:hover {
    border-color: #344268;
    background-color: #172038;
}
QComboBox:focus {
    border-color: #38bdf8;
    outline: none;
}
QComboBox::drop-down {
    border: none;
    width: 28px;
    subcontrol-position: right center;
}
QComboBox::down-arrow {
    border-left: 4px solid transparent;
    border-right: 4px solid transparent;
    border-top: 5px solid #4b5870;
    margin-right: 10px;
    width: 0;
    height: 0;
}
QComboBox QAbstractItemView {
    background-color: #141c2e;
    border: 1px solid #253152;
    border-radius: 7px;
    selection-background-color: #1c2c4a;
    selection-color: #38bdf8;
    padding: 4px;
    outline: none;
}
QComboBox QAbstractItemView::item {
    padding: 7px 12px;
    border-radius: 5px;
    min-height: 22px;
    color: #c0c8d8;
}
QComboBox QAbstractItemView::item:hover {
    background-color: #1a2644;
    color: #d8e0f0;
}

/* ── Line Edit ── */
QLineEdit {
    background-color: #141c2e;
    border: 1px solid #253152;
    border-radius: 7px;
    padding: 8px 11px;
    color: #d0d6e0;
    font-size: 13px;
    selection-background-color: #1c3a5e;
}
QLineEdit:hover {
    border-color: #344268;
}
QLineEdit:focus {
    border-color: #38bdf8;
    background-color: #111927;
    outline: none;
}
QLineEdit:disabled {
    color: #374151;
    background-color: #0f151f;
    border-color: #1a2030;
}

/* ── Buttons ── */
QPushButton {
    background-color: #141c2e;
    border: 1px solid #253152;
    border-radius: 7px;
    padding: 7px 15px;
    color: #a0aab8;
    font-size: 13px;
    font-weight: 500;
}
QPushButton:hover {
    background-color: #1a2540;
    border-color: #344268;
    color: #d0d6e0;
}
QPushButton:pressed {
    background-color: #111927;
    border-color: #253152;
}
QPushButton:disabled {
    color: #2c3748;
    border-color: #141c2e;
    background-color: #0f141e;
}

QPushButton#primaryBtn {
    background-color: #0ea5e9;
    border: none;
    color: #03080f;
    font-weight: 700;
    font-size: 14px;
    letter-spacing: 0.3px;
    border-radius: 8px;
    padding: 10px 36px;
}
QPushButton#primaryBtn:hover {
    background-color: #38bdf8;
}
QPushButton#primaryBtn:pressed {
    background-color: #0284c7;
}
QPushButton#primaryBtn:disabled {
    background-color: #0f1e2e;
    color: #1e3040;
}

QPushButton#cancelBtn {
    background-color: transparent;
    border: 1px solid #2a1e1e;
    color: #7f3535;
    border-radius: 8px;
    padding: 10px 24px;
    font-size: 13px;
}
QPushButton#cancelBtn:hover {
    background-color: #1e1010;
    border-color: #c53030;
    color: #fc8181;
}
QPushButton#cancelBtn:pressed {
    background-color: #180d0d;
}
QPushButton#cancelBtn:disabled {
    color: #2a1e1e;
    border-color: #1a1212;
    background-color: transparent;
}

QPushButton#iconBtn {
    background-color: transparent;
    border: 1px solid #1c2333;
    border-radius: 6px;
    padding: 6px 12px;
    color: #6b7280;
    font-size: 12px;
}
QPushButton#iconBtn:hover {
    background-color: #141c2e;
    color: #a0aab8;
    border-color: #253152;
}

/* ── Check Box ── */
QCheckBox {
    color: #a0aab8;
    font-size: 13px;
    spacing: 8px;
    background: transparent;
}
QCheckBox::indicator {
    width: 16px;
    height: 16px;
    border-radius: 4px;
    border: 1.5px solid #344268;
    background-color: #141c2e;
}
QCheckBox::indicator:checked {
    background-color: #0ea5e9;
    border-color: #0ea5e9;
}
QCheckBox::indicator:hover {
    border-color: #38bdf8;
}
QCheckBox:disabled {
    color: #2c3748;
}
QCheckBox::indicator:disabled {
    border-color: #1c2333;
    background-color: #0f141e;
}

/* ── List Widget ── */
QListWidget {
    background-color: #0a0e17;
    border: 1px solid #1c2333;
    border-radius: 10px;
    padding: 6px;
    outline: none;
    show-decoration-selected: 1;
}
QListWidget::item {
    border-radius: 7px;
    padding: 0;
    border: none;
    color: #c0c8d8;
    margin: 2px 0;
}
QListWidget::item:selected {
    background-color: #132040;
    color: #e8eaf0;
}
QListWidget::item:hover:!selected {
    background-color: #111927;
}

/* ── Progress Bar ── */
QProgressBar {
    border: none;
    border-radius: 3px;
    background-color: #141c2e;
    height: 5px;
    text-align: center;
    color: transparent;
}
QProgressBar::chunk {
    background-color: qlineargradient(
        x1:0, y1:0, x2:1, y2:0,
        stop:0 #0369a1,
        stop:0.6 #0ea5e9,
        stop:1 #38bdf8
    );
    border-radius: 3px;
}

/* ── Scroll Bar ── */
QScrollBar:vertical {
    background: transparent;
    width: 7px;
    margin: 6px 2px;
}
QScrollBar::handle:vertical {
    background-color: #1c2840;
    border-radius: 3px;
    min-height: 28px;
}
QScrollBar::handle:vertical:hover {
    background-color: #253152;
}
QScrollBar::add-line:vertical,
QScrollBar::sub-line:vertical { height: 0; }
QScrollBar::add-page:vertical,
QScrollBar::sub-page:vertical { background: none; }

/* ── Tooltip ── */
QToolTip {
    background-color: #141c2e;
    border: 1px solid #253152;
    border-radius: 5px;
    color: #c0c8d8;
    padding: 5px 9px;
    font-size: 12px;
}

/* ── Dialog ── */
QDialog {
    background-color: #0d1117;
}
QDialogButtonBox QPushButton {
    min-width: 90px;
}

/* ── Status Bar ── */
QStatusBar {
    background-color: #080c14;
    color: #374151;
    border-top: 1px solid #141c2e;
    font-size: 11px;
    padding: 0 8px;
}

/* ── Splitter ── */
QSplitter::handle {
    background-color: #1c2333;
}
QSplitter::handle:horizontal {
    width: 1px;
}
"""
