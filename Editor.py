import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QAction, QTextEdit, QFileDialog, QMessageBox
)
from PyQt5.QtGui import QKeySequence


# =========================
# 🎨 BLENDER STYLE (QSS)
# =========================
BLENDER_STYLE = """
QMainWindow {
    background-color: #2b2b2b;
}

QMenuBar {
    background-color: #3c3c3c;
    color: #dddddd;
}

QMenuBar::item {
    background: transparent;
    padding: 6px 12px;
}

QMenuBar::item:selected {
    background: #505050;
}

QMenu {
    background-color: #3c3c3c;
    color: #dddddd;
    border: 1px solid #222;
}

QMenu::item:selected {
    background-color: #5a5a5a;
}

QTextEdit {
    background-color: #1e1e1e;
    color: #dddddd;
    border: none;
    font-family: Consolas, monospace;
    font-size: 13px;
}

QScrollBar:vertical {
    background: #2b2b2b;
    width: 10px;
}

QScrollBar::handle:vertical {
    background: #555;
    border-radius: 4px;
}

QScrollBar::handle:vertical:hover {
    background: #777;
}

QStatusBar {
    background: #3c3c3c;
    color: #aaa;
}
"""


# =========================
# 🖥️ MAIN WINDOW
# =========================
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Blender Style PyQt App")
        self.resize(900, 600)

        # Editor
        self.editor = QTextEdit()
        self.setCentralWidget(self.editor)

        # Status bar
        self.statusBar().showMessage("Ready")

        self._create_menu()

    # =========================
    # MENU
    # =========================
    def _create_menu(self):
        menubar = self.menuBar()

        # FILE
        file_menu = menubar.addMenu("File")

        open_action = QAction("Open", self)
        open_action.setShortcut(QKeySequence.Open)
        open_action.triggered.connect(self.open_file)

        save_action = QAction("Save", self)
        save_action.setShortcut(QKeySequence.Save)
        save_action.triggered.connect(self.save_file)

        exit_action = QAction("Exit", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)

        file_menu.addAction(open_action)
        file_menu.addAction(save_action)
        file_menu.addSeparator()
        file_menu.addAction(exit_action)

        # EDIT
        edit_menu = menubar.addMenu("Edit")

        copy_action = QAction("Copy", self)
        copy_action.setShortcut(QKeySequence.Copy)
        copy_action.triggered.connect(self.editor.copy)

        paste_action = QAction("Paste", self)
        paste_action.setShortcut(QKeySequence.Paste)
        paste_action.triggered.connect(self.editor.paste)

        edit_menu.addAction(copy_action)
        edit_menu.addAction(paste_action)

        # HELP
        help_menu = menubar.addMenu("Help")

        about_action = QAction("About", self)
        about_action.triggered.connect(self.show_about)

        help_menu.addAction(about_action)

    # =========================
    # ACTIONS
    # =========================
    def open_file(self):
        path, _ = QFileDialog.getOpenFileName(self, "Open File", "", "All Files (*)")
        if path:
            with open(path, "r") as f:
                self.editor.setText(f.read())
            self.statusBar().showMessage(f"Opened: {path}")

    def save_file(self):
        path, _ = QFileDialog.getSaveFileName(self, "Save File", "", "All Files (*)")
        if path:
            with open(path, "w") as f:
                f.write(self.editor.toPlainText())
            self.statusBar().showMessage(f"Saved: {path}")

    def show_about(self):
        QMessageBox.about(self, "About", "Blender-style PyQt UI 🔥")


# =========================
# 🚀 MAIN
# =========================
if __name__ == "__main__":
    app = QApplication(sys.argv)

    # APPLY STYLE
    app.setStyleSheet(BLENDER_STYLE)

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())