import sys
from PyQt5.QtWidgets import QApplication, QPushButton, QWidget, QVBoxLayout
from PyQt5.QtGui import QIcon, QPixmap, QPainter, QColor
from PyQt5.QtCore import Qt


def text_icon(text, size=48, bg="#444", fg="white"):
    pixmap = QPixmap(size, size)
    pixmap.fill(Qt.transparent)

    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.Antialiasing)

    painter.setBrush(QColor(bg))
    painter.setPen(Qt.NoPen)
    painter.drawRoundedRect(0, 0, size, size, 8, 8)

    painter.setPen(QColor(fg))
    painter.drawText(pixmap.rect(), Qt.AlignCenter, text)

    painter.end()

    return QIcon(pixmap)


class Window(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)

        btn1 = QPushButton("Lua File")
        btn1.setIcon(text_icon("LUA"))

        btn2 = QPushButton("Mesh File")
        btn2.setIcon(text_icon("M"))

        btn3 = QPushButton("Texture")
        btn3.setIcon(text_icon("PNG", bg="#2a2a2a", fg="#00ffcc"))

        layout.addWidget(btn1)
        layout.addWidget(btn2)
        layout.addWidget(btn3)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = Window()
    w.show()
    sys.exit(app.exec_())