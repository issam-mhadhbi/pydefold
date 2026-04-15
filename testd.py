import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QTextEdit,
    QTreeWidget, QTreeWidgetItem, QVBoxLayout,
    QSplitter, QPushButton, QSizePolicy
)
from PyQt5.QtCore import Qt


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Editor Layout (Defold Style)")
        self.resize(1200, 700)

        # =========================
        # LEFT SIDEBAR (Assets)
        # =========================
        self.left_panel = QTreeWidget()
        self.left_panel.setHeaderHidden(True)

        root = QTreeWidgetItem(["assets"])
        root.addChild(QTreeWidgetItem(["models"]))
        root.addChild(QTreeWidgetItem(["textures"]))
        self.left_panel.addTopLevelItem(root)
        root.setExpanded(True)

        # 🔒 limit size
        self.left_panel.setMaximumWidth(300)
        self.left_panel.setMinimumWidth(150)

        # =========================
        # RIGHT SIDEBAR (Inspector)
        # =========================
        self.right_panel = QTextEdit("Inspector")
        self.right_panel.setMaximumWidth(300)
        self.right_panel.setMinimumWidth(150)

        # =========================
        # CENTER VIEW
        # =========================
        self.center_view = QTextEdit("3D View / Scene")

        # =========================
        # TERMINAL
        # =========================
        self.terminal = QTextEdit("Console output...")
        self.terminal.setMaximumHeight(200)

        # =========================
        # CENTER SPLITTER (vertical)
        # =========================
        center_split = QSplitter(Qt.Vertical)
        center_split.addWidget(self.center_view)
        center_split.addWidget(self.terminal)

        center_split.setSizes([500, 150])

        # =========================
        # MAIN SPLITTER (horizontal)
        # =========================
        main_split = QSplitter(Qt.Horizontal)

        main_split.addWidget(self.left_panel)
        main_split.addWidget(center_split)
        main_split.addWidget(self.right_panel)

        main_split.setSizes([200, 800, 200])

        # =========================
        # COLLAPSE BUTTONS
        # =========================
        self.toggle_left_btn = QPushButton("⮜")
        self.toggle_left_btn.setFixedWidth(20)
        self.toggle_left_btn.clicked.connect(self.toggle_left)

        self.toggle_right_btn = QPushButton("⮞")
        self.toggle_right_btn.setFixedWidth(20)
        self.toggle_right_btn.clicked.connect(self.toggle_right)

        # wrap in layout
        container = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        layout.addWidget(main_split)

        container.setLayout(layout)
        self.setCentralWidget(container)

        self.main_split = main_split

    # =========================
    # COLLAPSE LEFT
    # =========================
    def toggle_left(self):
        sizes = self.main_split.sizes()

        if sizes[0] > 0:
            self.main_split.setSizes([0, sizes[1] + sizes[0], sizes[2]])
        else:
            self.main_split.setSizes([200, sizes[1] - 200, sizes[2]])

    # =========================
    # COLLAPSE RIGHT
    # =========================
    def toggle_right(self):
        sizes = self.main_split.sizes()

        if sizes[2] > 0:
            self.main_split.setSizes([sizes[0], sizes[1] + sizes[2], 0])
        else:
            self.main_split.setSizes([sizes[0], sizes[1] - 200, 200])


# =========================
# MAIN
# =========================
if __name__ == "__main__":
    app = QApplication(sys.argv)

    win = MainWindow()
    win.show()

    sys.exit(app.exec_())