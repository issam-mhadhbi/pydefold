import sys
from PyQt5.QtWidgets import *

from PyQt5.QtCore import Qt


class FilePathEdit(QWidget):
    def __init__(self, parent=None, dialog_title="Select File", filter="All Files (*)"):
        super().__init__(parent)

        self.dialog_title = dialog_title
        self.filter = filter

        # =========================
        # BASE LINE EDIT
        # =========================
        self.line_edit = QLineEdit(self)

        # add right padding so text doesn't go under button
        self.line_edit.setStyleSheet("""
            QLineEdit {
                padding-right: 28px;
            }
        """)

        # =========================
        # OVERLAY BUTTON
        # =========================
        self.button = QPushButton("📁", self.line_edit)
        self.button.setCursor(Qt.PointingHandCursor)
        self.button.setFixedSize(24, 22)
        self.button.clicked.connect(self.open_dialog)

        # layout only holds line edit
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.line_edit)

    def resizeEvent(self, event):
        """Keep button glued to right side of QLineEdit"""
        super().resizeEvent(event)

        h = self.line_edit.height()
        self.button.move(
            self.line_edit.width() - self.button.width() - 2,
            (h - self.button.height()) // 2
        )

    def open_dialog(self):
        path, _ = QFileDialog.getOpenFileName(
            self,
            self.dialog_title,
            self.line_edit.text() or "",
            self.filter
        )
        if path:
            self.line_edit.setText(path)

    def text(self):
        return self.line_edit.text()

    def setText(self, value):
        self.line_edit.setText(value)

# =========================
# MAIN WINDOW DEMO
# =========================
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("FilePathEdit Demo")
        self.resize(600, 120)

        central = QWidget()
        layout = QVBoxLayout(central)

        layout.addWidget(QLabel("Select a file:"))

        self.file_picker = FilePathEdit(
            dialog_title="Choose a file",
            filter="All Files (*);;Images (*.png *.jpg)"
        )

        layout.addWidget(self.file_picker)

        self.setCentralWidget(central)


# =========================
# RUN
# =========================
if __name__ == "__main__":
    app = QApplication(sys.argv)

    win = MainWindow()
    win.show()

    sys.exit(app.exec_())