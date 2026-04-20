import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPlainTextEdit, QTextEdit, QDialog, QVBoxLayout
from PyQt5.QtGui import QColor, QPainter, QTextFormat
from PyQt5.QtCore import QRect, QSize, Qt
from pathlib import Path 


class LineNumberArea(QWidget):
    def __init__(self, editor):
        super().__init__(editor)
        self.editor = editor

    def sizeHint(self):
        return QSize(self.editor.lineNumberAreaWidth(), 0)

    def paintEvent(self, event):
        self.editor.lineNumberAreaPaintEvent(event)


class TextFileViewer(QPlainTextEdit):
    def __init__(self):
        super().__init__()

        self.setReadOnly(True)  # ✅ make it read-only

        self.lineNumberArea = LineNumberArea(self)
        self.blockCountChanged.connect(self.updateLineNumberAreaWidth)
        self.updateRequest.connect(self.updateLineNumberArea)
        self.cursorPositionChanged.connect(self.highlightCurrentLine)

        self.updateLineNumberAreaWidth(0)
        self.highlightCurrentLine()

    def lineNumberAreaWidth(self):
        digits = len(str(max(1, self.blockCount())))
        return 10 + self.fontMetrics().horizontalAdvance('9') * digits

    def updateLineNumberAreaWidth(self, _):
        self.setViewportMargins(self.lineNumberAreaWidth(), 0, 0, 0)

    def updateLineNumberArea(self, rect, dy):
        if dy:
            self.lineNumberArea.scroll(0, dy)
        else:
            self.lineNumberArea.update(0, rect.y(), self.lineNumberArea.width(), rect.height())
        if rect.contains(self.viewport().rect()):
            self.updateLineNumberAreaWidth(0)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        cr = self.contentsRect()
        self.lineNumberArea.setGeometry(
            QRect(cr.left(), cr.top(), self.lineNumberAreaWidth(), cr.height())
        )

    def lineNumberAreaPaintEvent(self, event):
        painter = QPainter(self.lineNumberArea)
        painter.fillRect(event.rect(), QColor(30, 30, 30))

        block = self.firstVisibleBlock()
        blockNumber = block.blockNumber()

        top = int(self.blockBoundingGeometry(block).translated(self.contentOffset()).top())
        bottom = top + int(self.blockBoundingRect(block).height())

        while block.isValid() and top <= event.rect().bottom():
            if block.isVisible() and bottom >= event.rect().top():
                painter.setPen(Qt.white)
                painter.drawText(
                    0, top,
                    self.lineNumberArea.width() - 5,
                    self.fontMetrics().height(),
                    Qt.AlignRight,
                    str(blockNumber + 1)
                )

            block = block.next()
            top = bottom
            bottom = top + int(self.blockBoundingRect(block).height())
            blockNumber += 1

    def highlightCurrentLine(self):
        selection = QTextEdit.ExtraSelection()
        selection.format.setBackground(QColor(50, 50, 50))
        selection.format.setProperty(QTextFormat.FullWidthSelection, True)

        selection.cursor = self.textCursor()
        selection.cursor.clearSelection()

        self.setExtraSelections([selection])

    def open_file(self, file_path):
        path_file = Path(file_path)

        if not path_file.exists():
            self.setPlainText(f"🚨 : cannot open {path_file} (does not exist)")
            return

        if not path_file.is_file():
            self.setPlainText(f"🚨 : cannot open {path_file} (not a file)")
            return

        self.setPlainText(path_file.read_text())


# ✅ Dialog wrapper
class ViewerDialog(QDialog):
    def __init__(self, file_path=None, text=None, parent=None):
        super().__init__(parent)

        self.setWindowTitle("File Viewer")
        self.resize(800, 600)

        layout = QVBoxLayout(self)

        self.viewer = TextFileViewer()
        layout.addWidget(self.viewer)

        if file_path:
            self.viewer.open_file(file_path)
        elif text:
            self.viewer.setPlainText(text)


# ✅ Run example
if __name__ == "__main__":
    app = QApplication(sys.argv)

    dialog = ViewerDialog(text="Hello\nThis is a read-only viewer\nWith line numbers")
    dialog.exec_()

    sys.exit(app.exec_())