BLENDER_STYLE = '''
* {
    background-color: #2b2b2b;
    color: #dddddd;
    border-color : : rgba(255, 255, 255, 0.05) ; 

}
'''
'''
/* ============================================================
   BLENDER THEME FOR PyQt5
   Inspired by Blender 3.x / 4.x dark UI theme
   ============================================================ */

/* ── GLOBAL ── */
* {
    font-family: "Inter", "Segoe UI", "Helvetica Neue", Arial, sans-serif;
    font-size: 11px;
    color: #D4D4D4;
    background-color: transparent;
    selection-color: #FFFFFF;
    selection-background-color: #2A6496;
    outline: none;
}

QWidget {
    background-color: #3A3A3A;
    color: #D4D4D4;
    border: none;
}

QMainWindow {
    background-color: #262626;
}

QMainWindow::separator {
    background-color: #1A1A1A;
    width: 2px;
    height: 2px;
}

/* ── WINDOW & DIALOGS ── */
QDialog {
    background-color: #3A3A3A;
    border: 1px solid #1A1A1A;
}

QMessageBox {
    background-color: #3A3A3A;
}

/* ── MENU BAR ── */
QMenuBar {
    background-color: #2A2A2A;
    color: #D4D4D4;
    border-bottom: 1px solid #1A1A1A;
    padding: 2px 0px;
    spacing: 2px;
}

QMenuBar::item {
    background-color: transparent;
    padding: 4px 10px;
    border-radius: 3px;
    color: #D4D4D4;
}

QMenuBar::item:selected,
QMenuBar::item:pressed {
    background-color: #4A7C6B;
    color: #FFFFFF;
}

/* ── MENUS ── */
QMenu {
    background-color: #252525;
    border: 1px solid #111111;
    padding: 4px 0px;
    border-radius: 4px;
}

QMenu::item {
    padding: 5px 30px 5px 16px;
    background-color: transparent;
    color: #D4D4D4;
    border-radius: 3px;
    margin: 1px 4px;
}

QMenu::item:selected {
    background-color: #4A7C6B;
    color: #FFFFFF;
}

QMenu::item:disabled {
    color: #666666;
}

QMenu::separator {
    height: 1px;
    background-color: #333333;
    margin: 4px 8px;
}

QMenu::indicator {
    width: 14px;
    height: 14px;
    left: 8px;
}

QMenu::indicator:checked {
    image: none;
    background-color: #4A7C6B;
    border-radius: 2px;
    border: 1px solid #5E9A88;
}

/* ── TOOLBARS ── */
QToolBar {
    background-color: #2A2A2A;
    border-bottom: 1px solid #1A1A1A;
    padding: 2px;
    spacing: 2px;
}

QToolBar::separator {
    background-color: #444444;
    width: 1px;
    height: 24px;
    margin: 3px 4px;
}

QToolButton {
    background-color: transparent;
    border: 1px solid transparent;
    border-radius: 4px;
    padding: 4px 6px;
    color: #D4D4D4;
    min-width: 22px;
    min-height: 22px;
}

QToolButton:hover {
    background-color: #4A4A4A;
    border-color: #5A5A5A;
}

QToolButton:pressed,
QToolButton:checked {
    background-color: #4A7C6B;
    border-color: #5E9A88;
    color: #FFFFFF;
}

QToolButton:disabled {
    color: #555555;
}

QToolButton::menu-indicator {
    image: none;
    width: 0px;
    height: 0px;
}

/* ── PUSH BUTTONS ── */
QPushButton {
    background-color: #555555;
    color: #D4D4D4;
    border: 1px solid #3A3A3A;
    border-radius: 4px;
    padding: 5px 14px;
    min-height: 22px;
    font-weight: 400;
}

QPushButton:hover {
    background-color: #606060;
    border-color: #4A7C6B;
    color: #FFFFFF;
}

QPushButton:pressed {
    background-color: #454545;
    border-color: #4A7C6B;
    padding-top: 6px;
    padding-bottom: 4px;
}

QPushButton:checked {
    background-color: #4A7C6B;
    border-color: #5E9A88;
    color: #FFFFFF;
}

QPushButton:disabled {
    background-color: #404040;
    color: #5A5A5A;
    border-color: #333333;
}

QPushButton:default {
    background-color: #4A7C6B;
    border-color: #5E9A88;
    color: #FFFFFF;
}

QPushButton:default:hover {
    background-color: #5E9A88;
}

/* ── LINE EDIT / TEXT INPUTS ── */
QLineEdit {
    background-color: #1D1D1D;
    color: #D4D4D4;
    border: 1px solid #333333;
    border-radius: 4px;
    padding: 4px 8px;
    selection-background-color: #2A6496;
    selection-color: #FFFFFF;
    min-height: 22px;
}

QLineEdit:hover {
    border-color: #555555;
}

QLineEdit:focus {
    border-color: #4A7C6B;
    background-color: #222222;
}

QLineEdit:disabled {
    background-color: #2A2A2A;
    color: #555555;
    border-color: #2A2A2A;
}

QLineEdit:read-only {
    background-color: #2C2C2C;
    color: #999999;
}

/* ── TEXT EDIT / PLAIN TEXT EDIT ── */
QTextEdit,
QPlainTextEdit {
    background-color: #1D1D1D;
    color: #D4D4D4;
    border: 1px solid #333333;
    border-radius: 4px;
    padding: 4px;
    selection-background-color: #2A6496;
}

QTextEdit:focus,
QPlainTextEdit:focus {
    border-color: #4A7C6B;
}

/* ── SPIN BOX / DOUBLE SPIN BOX ── */
QSpinBox,
QDoubleSpinBox {
    background-color: #1D1D1D;
    color: #D4D4D4;
    border: 1px solid #333333;
    border-radius: 4px;
    padding: 4px 6px;
    min-height: 22px;
}

QSpinBox:hover,
QDoubleSpinBox:hover {
    border-color: #555555;
}

QSpinBox:focus,
QDoubleSpinBox:focus {
    border-color: #4A7C6B;
}

QSpinBox::up-button,
QDoubleSpinBox::up-button {
    subcontrol-origin: border;
    subcontrol-position: top right;
    background-color: #3A3A3A;
    border-left: 1px solid #333333;
    border-top-right-radius: 4px;
    width: 18px;
    height: 12px;
}

QSpinBox::down-button,
QDoubleSpinBox::down-button {
    subcontrol-origin: border;
    subcontrol-position: bottom right;
    background-color: #3A3A3A;
    border-left: 1px solid #333333;
    border-bottom-right-radius: 4px;
    width: 18px;
    height: 12px;
}

QSpinBox::up-button:hover,
QDoubleSpinBox::up-button:hover,
QSpinBox::down-button:hover,
QDoubleSpinBox::down-button:hover {
    background-color: #4A7C6B;
}

QSpinBox::up-arrow,
QDoubleSpinBox::up-arrow {
    image: none;
    width: 0;
    height: 0;
    border-left: 4px solid transparent;
    border-right: 4px solid transparent;
    border-bottom: 5px solid #AAAAAA;
}

QSpinBox::down-arrow,
QDoubleSpinBox::down-arrow {
    image: none;
    width: 0;
    height: 0;
    border-left: 4px solid transparent;
    border-right: 4px solid transparent;
    border-top: 5px solid #AAAAAA;
}

/* ── COMBO BOX ── */
QComboBox {
    background-color: #555555;
    color: #D4D4D4;
    border: 1px solid #3A3A3A;
    border-radius: 4px;
    padding: 4px 8px;
    min-height: 22px;
    selection-background-color: #4A7C6B;
}

QComboBox:hover {
    background-color: #606060;
    border-color: #4A7C6B;
}

QComboBox:focus {
    border-color: #4A7C6B;
}

QComboBox:on {
    background-color: #454545;
    border-color: #4A7C6B;
}

QComboBox::drop-down {
    subcontrol-origin: padding;
    subcontrol-position: center right;
    width: 22px;
    border-left: 1px solid #3A3A3A;
    border-top-right-radius: 4px;
    border-bottom-right-radius: 4px;
    background-color: transparent;
}

QComboBox::down-arrow {
    image: none;
    width: 0;
    height: 0;
    border-left: 4px solid transparent;
    border-right: 4px solid transparent;
    border-top: 5px solid #AAAAAA;
}

QComboBox::down-arrow:on {
    border-top: none;
    border-bottom: 5px solid #AAAAAA;
}

QComboBox QAbstractItemView {
    background-color: #252525;
    color: #D4D4D4;
    border: 1px solid #111111;
    selection-background-color: #4A7C6B;
    selection-color: #FFFFFF;
    outline: none;
    padding: 2px;
}

QComboBox QAbstractItemView::item {
    padding: 4px 10px;
    min-height: 22px;
    border-radius: 3px;
    margin: 1px 3px;
}

QComboBox QAbstractItemView::item:hover {
    background-color: #3D3D3D;
}

QComboBox QAbstractItemView::item:selected {
    background-color: #4A7C6B;
}

/* ── CHECKBOXES ── */
QCheckBox {
    color: #D4D4D4;
    spacing: 8px;
    background-color: transparent;
}

QCheckBox:hover {
    color: #FFFFFF;
}

QCheckBox:disabled {
    color: #555555;
}

QCheckBox::indicator {
    width: 14px;
    height: 14px;
    border-radius: 3px;
    background-color: #1D1D1D;
    border: 1px solid #555555;
}

QCheckBox::indicator:hover {
    border-color: #4A7C6B;
}

QCheckBox::indicator:checked {
    background-color: #4A7C6B;
    border-color: #5E9A88;
}

QCheckBox::indicator:checked:hover {
    background-color: #5E9A88;
}

QCheckBox::indicator:disabled {
    background-color: #2A2A2A;
    border-color: #3A3A3A;
}

/* ── RADIO BUTTONS ── */
QRadioButton {
    color: #D4D4D4;
    spacing: 8px;
    background-color: transparent;
}

QRadioButton:hover {
    color: #FFFFFF;
}

QRadioButton:disabled {
    color: #555555;
}

QRadioButton::indicator {
    width: 14px;
    height: 14px;
    border-radius: 7px;
    background-color: #1D1D1D;
    border: 1px solid #555555;
}

QRadioButton::indicator:hover {
    border-color: #4A7C6B;
}

QRadioButton::indicator:checked {
    background-color: #4A7C6B;
    border-color: #5E9A88;
}

QRadioButton::indicator:checked:hover {
    background-color: #5E9A88;
}

/* ── SLIDER ── */
QSlider::groove:horizontal {
    background-color: #1D1D1D;
    height: 4px;
    border-radius: 2px;
    border: none;
}

QSlider::groove:vertical {
    background-color: #1D1D1D;
    width: 4px;
    border-radius: 2px;
    border: none;
}

QSlider::sub-page:horizontal {
    background-color: #4A7C6B;
    height: 4px;
    border-radius: 2px;
}

QSlider::add-page:horizontal {
    background-color: #1D1D1D;
    height: 4px;
    border-radius: 2px;
}

QSlider::add-page:vertical {
    background-color: #4A7C6B;
    width: 4px;
    border-radius: 2px;
}

QSlider::sub-page:vertical {
    background-color: #1D1D1D;
    width: 4px;
    border-radius: 2px;
}

QSlider::handle:horizontal {
    background-color: #B0B0B0;
    width: 14px;
    height: 14px;
    border-radius: 7px;
    margin: -5px 0;
    border: 1px solid #888888;
}

QSlider::handle:horizontal:hover {
    background-color: #FFFFFF;
    border-color: #4A7C6B;
}

QSlider::handle:vertical {
    background-color: #B0B0B0;
    width: 14px;
    height: 14px;
    border-radius: 7px;
    margin: 0 -5px;
    border: 1px solid #888888;
}

QSlider::handle:vertical:hover {
    background-color: #FFFFFF;
    border-color: #4A7C6B;
}

/* ── PROGRESS BAR ── */
QProgressBar {
    background-color: #1D1D1D;
    color: #D4D4D4;
    border: 1px solid #333333;
    border-radius: 4px;
    text-align: center;
    min-height: 16px;
    font-size: 10px;
}

QProgressBar::chunk {
    background-color: #4A7C6B;
    border-radius: 3px;
    margin: 1px;
}

/* ── TAB WIDGET / TAB BAR ── */
QTabWidget::pane {
    background-color: #3A3A3A;
    border: 1px solid #2A2A2A;
    border-top: none;
    border-radius: 0px 4px 4px 4px;
}

QTabWidget::tab-bar {
    alignment: left;
}

QTabBar {
    background-color: transparent;
}

QTabBar::tab {
    background-color: #2A2A2A;
    color: #999999;
    border: 1px solid #1A1A1A;
    border-bottom: none;
    padding: 5px 14px;
    margin-right: 2px;
    border-top-left-radius: 4px;
    border-top-right-radius: 4px;
    min-width: 70px;
}

QTabBar::tab:hover {
    background-color: #383838;
    color: #D4D4D4;
}

QTabBar::tab:selected {
    background-color: #3A3A3A;
    color: #D4D4D4;
    border-bottom: 1px solid #3A3A3A;
    font-weight: 500;
}

QTabBar::tab:!selected {
    margin-top: 2px;
}

QTabBar::close-button {
    subcontrol-position: right;
    padding: 2px;
}

/* ── GROUP BOX ── */
QGroupBox {
    background-color: #3A3A3A;
    border: 1px solid #2A2A2A;
    border-radius: 6px;
    margin-top: 12px;
    padding-top: 8px;
    font-weight: 500;
    color: #AAAAAA;
}

QGroupBox::title {
    subcontrol-origin: margin;
    subcontrol-position: top left;
    left: 10px;
    padding: 0 6px;
    background-color: #3A3A3A;
    color: #AAAAAA;
    font-size: 10px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

/* ── SCROLL BARS ── */
QScrollBar:vertical {
    background-color: #2A2A2A;
    width: 10px;
    border-radius: 5px;
    margin: 0px;
    border: none;
}

QScrollBar:horizontal {
    background-color: #2A2A2A;
    height: 10px;
    border-radius: 5px;
    margin: 0px;
    border: none;
}

QScrollBar::handle:vertical {
    background-color: #505050;
    min-height: 30px;
    border-radius: 5px;
    margin: 1px;
}

QScrollBar::handle:horizontal {
    background-color: #505050;
    min-width: 30px;
    border-radius: 5px;
    margin: 1px;
}

QScrollBar::handle:vertical:hover,
QScrollBar::handle:horizontal:hover {
    background-color: #686868;
}

QScrollBar::handle:vertical:pressed,
QScrollBar::handle:horizontal:pressed {
    background-color: #4A7C6B;
}

QScrollBar::add-line,
QScrollBar::sub-line {
    height: 0px;
    width: 0px;
}

QScrollBar::add-page,
QScrollBar::sub-page {
    background-color: transparent;
}

/* ── SCROLL AREA ── */
QScrollArea {
    background-color: transparent;
    border: none;
}

QScrollArea > QWidget > QWidget {
    background-color: transparent;
}

/* ── LIST / TREE / TABLE VIEWS ── */
QListView,
QTreeView,
QTableView,
QListWidget,
QTreeWidget,
QTableWidget {
    background-color: #2A2A2A;
    alternate-background-color: #2F2F2F;
    color: #D4D4D4;
    border: 1px solid #222222;
    border-radius: 4px;
    selection-background-color: #3D6B5D;
    selection-color: #FFFFFF;
    gridline-color: #333333;
    outline: none;
}

QListView::item,
QTreeView::item,
QTableView::item,
QListWidget::item,
QTreeWidget::item,
QTableWidget::item {
    padding: 3px 6px;
    border-radius: 3px;
    min-height: 22px;
    border: none;
}

QListView::item:hover,
QTreeView::item:hover,
QTableView::item:hover,
QListWidget::item:hover,
QTreeWidget::item:hover,
QTableWidget::item:hover {
    background-color: #3A3A3A;
}

QListView::item:selected,
QTreeView::item:selected,
QTableView::item:selected,
QListWidget::item:selected,
QTreeWidget::item:selected,
QTableWidget::item:selected {
    background-color: #3D6B5D;
    color: #FFFFFF;
}

QListView::item:selected:!active,
QTreeView::item:selected:!active {
    background-color: #344F48;
}

/* Tree branch arrows */
QTreeView::branch {
    background-color: transparent;
    color: #777777;
}

QTreeView::branch:has-children:!has-siblings:closed,
QTreeView::branch:closed:has-children:has-siblings {
    image: none;
    border: none;
}

QTreeView::branch:open:has-children:!has-siblings,
QTreeView::branch:open:has-children:has-siblings {
    image: none;
    border: none;
}

/* ── HEADER VIEW (Tables/Trees) ── */
QHeaderView {
    background-color: #2A2A2A;
    color: #AAAAAA;
    border: none;
    font-size: 10px;
    font-weight: 500;
    text-transform: uppercase;
}

QHeaderView::section {
    background-color: #252525;
    color: #999999;
    padding: 5px 8px;
    border: none;
    border-right: 1px solid #1A1A1A;
    border-bottom: 1px solid #1A1A1A;
}

QHeaderView::section:hover {
    background-color: #303030;
    color: #D4D4D4;
}

QHeaderView::section:checked {
    background-color: #3D6B5D;
    color: #FFFFFF;
}

QHeaderView::section:first {
    border-top-left-radius: 4px;
}

QHeaderView::section:last {
    border-right: none;
    border-top-right-radius: 4px;
}

/* ── SPLITTERS ── */
QSplitter::handle {
    background-color: #1A1A1A;
}

QSplitter::handle:horizontal {
    width: 3px;
}

QSplitter::handle:vertical {
    height: 3px;
}

QSplitter::handle:hover {
    background-color: #4A7C6B;
}

/* ── DOCK WIDGETS ── */
QDockWidget {
    titlebar-close-icon: none;
    titlebar-normal-icon: none;
    color: #D4D4D4;
}

QDockWidget::title {
    background-color: #252525;
    color: #AAAAAA;
    padding: 5px 8px;
    border-bottom: 1px solid #1A1A1A;
    font-size: 10px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    font-weight: 500;
}

QDockWidget::close-button,
QDockWidget::float-button {
    background-color: transparent;
    border: none;
    padding: 2px;
    border-radius: 3px;
}

QDockWidget::close-button:hover,
QDockWidget::float-button:hover {
    background-color: #4A4A4A;
}

/* ── STATUS BAR ── */
QStatusBar {
    background-color: #222222;
    color: #888888;
    border-top: 1px solid #1A1A1A;
    font-size: 10px;
}

QStatusBar::item {
    border: none;
}

QStatusBar QLabel {
    color: #888888;
}

/* ── LABELS ── */
QLabel {
    color: #D4D4D4;
    background-color: transparent;
    padding: 0px 2px;
}

QLabel:disabled {
    color: #555555;
}

/* ── TOOLTIPS ── */
QToolTip {
    background-color: #1A1A1A;
    color: #D4D4D4;
    border: 1px solid #333333;
    border-radius: 4px;
    padding: 5px 8px;
    font-size: 11px;
    opacity: 240;
}

/* ── FRAME ── */
QFrame {
    background-color: transparent;
    border: none;
}

QFrame[frameShape="4"],  /* HLine */
QFrame[frameShape="5"] { /* VLine */
    color: #2A2A2A;
    background-color: #2A2A2A;
    border: none;
    max-height: 1px;
}

QFrame[frameShape="5"] {
    max-width: 1px;
    max-height: none;
}

/* ── STACK / PAGES ── */
QStackedWidget {
    background-color: transparent;
}

/* ── CALENDAR ── */
QCalendarWidget {
    background-color: #2A2A2A;
    color: #D4D4D4;
}

QCalendarWidget QTableView {
    background-color: #2A2A2A;
    selection-background-color: #4A7C6B;
    selection-color: #FFFFFF;
}

QCalendarWidget QWidget#qt_calendar_navigationbar {
    background-color: #252525;
}

QCalendarWidget QToolButton {
    background-color: transparent;
    color: #D4D4D4;
    border-radius: 3px;
    padding: 4px;
}

QCalendarWidget QToolButton:hover {
    background-color: #4A7C6B;
}

/* ── INPUT DIALOG ── */
QInputDialog {
    background-color: #3A3A3A;
}

/* ── COLOR DIALOG ── */
QColorDialog {
    background-color: #3A3A3A;
}

/* ── FILE DIALOG ── */
QFileDialog {
    background-color: #3A3A3A;
}

QFileDialog QPushButton {
    min-width: 80px;
}

/* ── FONT COMBO BOX ── */
QFontComboBox {
    background-color: #555555;
    color: #D4D4D4;
    border: 1px solid #3A3A3A;
    border-radius: 4px;
    padding: 4px 8px;
    min-height: 22px;
}

QFontComboBox:hover {
    border-color: #4A7C6B;
}

/* ── DATE / TIME EDIT ── */
QDateEdit,
QTimeEdit,
QDateTimeEdit {
    background-color: #1D1D1D;
    color: #D4D4D4;
    border: 1px solid #333333;
    border-radius: 4px;
    padding: 4px 8px;
    min-height: 22px;
}

QDateEdit:focus,
QTimeEdit:focus,
QDateTimeEdit:focus {
    border-color: #4A7C6B;
}

QDateEdit::drop-down,
QTimeEdit::drop-down,
QDateTimeEdit::drop-down {
    width: 20px;
    background-color: #3A3A3A;
    border-left: 1px solid #333333;
    border-top-right-radius: 4px;
    border-bottom-right-radius: 4px;
}

/* ── LCD NUMBER ── */
QLCDNumber {
    background-color: #111111;
    color: #4A7C6B;
    border: 1px solid #222222;
    border-radius: 4px;
    padding: 4px;
}

/* ── RUBBER BAND (selection rectangle) ── */
QRubberBand {
    background-color: rgba(74, 124, 107, 0.25);
    border: 1px solid #4A7C6B;
    border-radius: 2px;
}

/* ── ABSTRACT ITEM VIEW (shared) ── */
QAbstractItemView {
    background-color: #2A2A2A;
    alternate-background-color: #2F2F2F;
    color: #D4D4D4;
    border: 1px solid #222222;
    selection-background-color: #3D6B5D;
    selection-color: #FFFFFF;
    outline: none;
}

QAbstractItemView:disabled {
    color: #555555;
}

QAbstractScrollArea {
    background-color: transparent;
}

/* ── BLENDER ACCENT COLOR HELPERS ──
   Apply these as dynamic properties:
   widget.setProperty("accent", "orange")  →  uses Blender orange
   widget.setProperty("accent", "blue")    →  uses Blender blue
   widget.setProperty("accent", "red")     →  uses warning red
   ── */

QPushButton[accent="orange"] {
    background-color: #B05B20;
    border-color: #CC6E2A;
    color: #FFFFFF;
}

QPushButton[accent="orange"]:hover {
    background-color: #CC6E2A;
}

QPushButton[accent="blue"] {
    background-color: #2B6095;
    border-color: #3A7AB8;
    color: #FFFFFF;
}

QPushButton[accent="blue"]:hover {
    background-color: #3A7AB8;
}

QPushButton[accent="red"] {
    background-color: #8B2020;
    border-color: #AA2828;
    color: #FFFFFF;
}

QPushButton[accent="red"]:hover {
    background-color: #AA2828;
}

/* Blender-style number field (draggable number input) */
QLabel[blender_field="true"] {
    background-color: #3D3D3D;
    color: #D4D4D4;
    border: 1px solid #282828;
    border-radius: 4px;
    padding: 4px 8px;
    min-height: 22px;
}

QLabel[blender_field="true"]:hover {
    background-color: #4A4A4A;
    border-color: #4A7C6B;
}

/* ── PANEL HEADERS (like Blender's property panel sections) ── */
QWidget[panel_header="true"] {
    background-color: #272727;
    border-bottom: 1px solid #1A1A1A;
}

/* ── OPERATOR SEARCH / NODE SEARCH style popup ── */
QListWidget[search_popup="true"] {
    background-color: #1D1D1D;
    border: 1px solid #111111;
    border-radius: 6px;
    padding: 4px;
    font-size: 12px;
}

QListWidget[search_popup="true"]::item {
    padding: 5px 10px;
    border-radius: 4px;
    min-height: 24px;
}

QListWidget[search_popup="true"]::item:selected {
    background-color: #4A7C6B;
    color: #FFFFFF;
}

'''