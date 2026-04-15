import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QSplitter, QFrame, QVBoxLayout,
    QTabWidget
)
from PyQt5.QtCore import Qt


# =========================
# 🧱 EMPTY PANEL
# =========================
def create_panel(name):
    panel = QFrame()
    panel.setObjectName(name)
    panel.setFrameShape(QFrame.NoFrame)
    return panel


# =========================
# 🧠 TAB CREATOR
# =========================
def create_tab(name):
    tab = QFrame()
    tab.setObjectName(name)
    return tab


# =========================
# 🖥️ MAIN WINDOW
# =========================
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Editor Layout with Tabs")
        self.resize(1200, 700)

        # =========================
        # PANELS
        # =========================
        self.left_panel = create_panel("left")
        self.right_panel = create_panel("right")
        self.terminal_panel = create_panel("terminal")

        # =========================
        # CENTER TABS 🔥
        # =========================
        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)

        # Add example tabs
        self.tabs.addTab(create_tab("scene"), "Scene")
        self.tabs.addTab(create_tab("code"), "Code")
        self.tabs.addTab(create_tab("preview"), "Preview")

        self.tabs.tabCloseRequested.connect(self.tabs.removeTab)

        # =========================
        # SIZE LIMITS
        # =========================
        self.left_panel.setMinimumWidth(120)
        self.left_panel.setMaximumWidth(300)

        self.right_panel.setMinimumWidth(120)
        self.right_panel.setMaximumWidth(300)

        self.terminal_panel.setMaximumHeight(200)

        # =========================
        # CENTER SPLIT (tabs + terminal)
        # =========================
        center_split = QSplitter(Qt.Vertical)
        center_split.addWidget(self.tabs)
        center_split.addWidget(self.terminal_panel)
        center_split.setSizes([500, 150])

        # =========================
        # MAIN SPLIT
        # =========================
        self.main_split = QSplitter(Qt.Horizontal)
        self.main_split.addWidget(self.left_panel)
        self.main_split.addWidget(center_split)
        self.main_split.addWidget(self.right_panel)

        self.main_split.setSizes([200, 800, 200])

        # =========================
        # SET CENTRAL
        # =========================
        container = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.main_split)
        container.setLayout(layout)

        self.setCentralWidget(container)

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
# 🚀 MAIN
# =========================
if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Simple dark style
    app.setStyleSheet("""
    #left { background: #2d2d2d; }
    #right { background: #2d2d2d; }
    #terminal { background: #111; }

    QTabWidget::pane {
        border: none;
        background: #1e1e1e;
    }

    QTabBar::tab {
        background: #3a3a3a;
        color: #ddd;
        padding: 6px 12px;
        margin-right: 2px;
    }

    QTabBar::tab:selected {
        background: #1e1e1e;
    }

    QSplitter::handle {
        background: #444;
    }
    """)

    win = MainWindow()
    win.show()

    sys.exit(app.exec_())