import sys
import math

from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import Qt
from PyQt5.QtOpenGL import QGLWidget

from OpenGL.GL import *
from OpenGL.GLU import *


# =========================
# 🧠 3D VIEWER
# =========================
class GLViewer(QGLWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.last_x = 0
        self.last_y = 0

        # Camera orbit
        self.rot_x = 20
        self.rot_y = -30
        self.distance = 5.0

    # =========================
    # INIT
    # =========================
    def initializeGL(self):
        glEnable(GL_DEPTH_TEST)

        # Lighting
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)

        glLightfv(GL_LIGHT0, GL_POSITION, [5, 5, 5, 1])
        glLightfv(GL_LIGHT0, GL_DIFFUSE, [1, 1, 1, 1])

        glEnable(GL_COLOR_MATERIAL)

        glClearColor(0.1, 0.1, 0.1, 1)

    # =========================
    # RESIZE
    # =========================
    def resizeGL(self, w, h):
        glViewport(0, 0, w, h)

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()

        gluPerspective(45, w / max(h, 1), 0.1, 100)

        glMatrixMode(GL_MODELVIEW)

    # =========================
    # DRAW
    # =========================
    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glLoadIdentity()

        # Camera
        gluLookAt(
            0, 0, self.distance,
            0, 0, 0,
            0, 1, 0
        )

        # Orbit rotation
        glRotatef(self.rot_x, 1, 0, 0)
        glRotatef(self.rot_y, 0, 1, 0)

        # Draw grid
        self.draw_grid()

        # Draw cube
        self.draw_cube()

    # =========================
    # GRID
    # =========================
    def draw_grid(self):
        glDisable(GL_LIGHTING)
        glColor3f(0.3, 0.3, 0.3)

        glBegin(GL_LINES)
        for i in range(-10, 11):
            glVertex3f(i, 0, -10)
            glVertex3f(i, 0, 10)

            glVertex3f(-10, 0, i)
            glVertex3f(10, 0, i)
        glEnd()

        glEnable(GL_LIGHTING)

    # =========================
    # CUBE
    # =========================
    def draw_cube(self):
        glColor3f(0.8, 0.7, 0.2)

        glBegin(GL_QUADS)

        # Front
        glNormal3f(0, 0, 1)
        glVertex3f(-1, -1, 1)
        glVertex3f(1, -1, 1)
        glVertex3f(1, 1, 1)
        glVertex3f(-1, 1, 1)

        # Back
        glNormal3f(0, 0, -1)
        glVertex3f(-1, -1, -1)
        glVertex3f(-1, 1, -1)
        glVertex3f(1, 1, -1)
        glVertex3f(1, -1, -1)

        # Left
        glNormal3f(-1, 0, 0)
        glVertex3f(-1, -1, -1)
        glVertex3f(-1, -1, 1)
        glVertex3f(-1, 1, 1)
        glVertex3f(-1, 1, -1)

        # Right
        glNormal3f(1, 0, 0)
        glVertex3f(1, -1, -1)
        glVertex3f(1, 1, -1)
        glVertex3f(1, 1, 1)
        glVertex3f(1, -1, 1)

        # Top
        glNormal3f(0, 1, 0)
        glVertex3f(-1, 1, -1)
        glVertex3f(-1, 1, 1)
        glVertex3f(1, 1, 1)
        glVertex3f(1, 1, -1)

        # Bottom
        glNormal3f(0, -1, 0)
        glVertex3f(-1, -1, -1)
        glVertex3f(1, -1, -1)
        glVertex3f(1, -1, 1)
        glVertex3f(-1, -1, 1)

        glEnd()

    # =========================
    # MOUSE
    # =========================
    def mousePressEvent(self, event):
        self.last_x = event.x()
        self.last_y = event.y()

    def mouseMoveEvent(self, event):
        dx = event.x() - self.last_x
        dy = event.y() - self.last_y

        if event.buttons() & Qt.LeftButton:
            self.rot_x += dy * 0.5
            self.rot_y += dx * 0.5

        self.last_x = event.x()
        self.last_y = event.y()
        self.update()

    def wheelEvent(self, event):
        delta = event.angleDelta().y()
        self.distance -= delta * 0.01
        self.distance = max(1.0, min(50.0, self.distance))
        self.update()


# =========================
# 🖥️ MAIN WINDOW
# =========================
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("3D Viewer (Blender Style Base)")
        self.resize(900, 600)

        self.viewer = GLViewer(self)
        self.setCentralWidget(self.viewer)


# =========================
# 🚀 MAIN
# =========================
if __name__ == "__main__":
    app = QApplication(sys.argv)

    win = MainWindow()
    win.show()

    sys.exit(app.exec_())