import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWidgets import QOpenGLWidget
from PyQt5.QtCore import QTimer
from OpenGL.GL import *


class Viewport(QOpenGLWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.angle = 0

        # update loop (like a game engine)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update)
        self.timer.start(16)  # ~60 FPS

    # =========================
    # INIT
    # =========================
    def initializeGL(self):
        glEnable(GL_DEPTH_TEST)
        glClearColor(0.1, 0.1, 0.1, 1.0)

    # =========================
    # RESIZE
    # =========================
    def resizeGL(self, w, h):
        glViewport(0, 0, w, h)

    # =========================
    # DRAW
    # =========================
    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glLoadIdentity()
        glRotatef(self.angle, 0, 1, 0)

        # 🔺 simple triangle
        glBegin(GL_TRIANGLES)

        glColor3f(1, 0, 0)
        glVertex3f(-0.5, -0.5, 0)

        glColor3f(0, 1, 0)
        glVertex3f(0.5, -0.5, 0)

        glColor3f(0, 0, 1)
        glVertex3f(0, 0.5, 0)

        glEnd()

        self.angle += 1


# =========================
# MAIN WINDOW
# =========================
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("OpenGL Viewer")

        self.viewer = Viewport()
        self.setCentralWidget(self.viewer)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.resize(800, 600)
    window.show()

    sys.exit(app.exec_())