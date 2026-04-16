import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import style , prefrenece 
from dataclasses import dataclass
from FileExplorer import FileExplorer

@dataclass
class DefoldProject : 
    project_path = None




class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.project = DefoldProject()
        self.setWindowTitle("Blender Style PyQt App")
        self.showMaximized()
        self._create_menu()
        self._create_main_layout()

    def _create_menu(self):
        menubar = self.menuBar()
        # FILE
        file_menu = menubar.addMenu("File")
        open_action = QAction("Open", self)
        file_menu.addAction(open_action)
        open_action.setShortcut(QKeySequence.Open)
        open_action.triggered.connect(self.open_project)

    def _create_main_layout(self) : 
        self.fileExplorer = FileExplorer(self)
        self.fileExplorer.set_rootPath(".")
        self.fileExplorer.setSizePolicy(
            QSizePolicy.Preferred, QSizePolicy.Expanding
        )
        self.assests_outline = QFrame(self)
        self.assests_outline.setSizePolicy(
            QSizePolicy.Preferred, QSizePolicy.Expanding
        )
        self.middle_zone = QFrame(self)
        self.middle_zone.setSizePolicy(
            QSizePolicy.Expanding, QSizePolicy.Expanding
        )
        # main splitter 
        self.main_split = QSplitter(Qt.Horizontal)
        self.main_split.addWidget(self.fileExplorer)
        self.main_split.addWidget(self.middle_zone)
        self.main_split.addWidget(self.assests_outline)
        self.main_split.setStretchFactor(0, 0)
        self.main_split.setStretchFactor(1, 1)
        self.main_split.setStretchFactor(2, 0)
        # =========================
        # SET CENTRAL
        # =========================
        container = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.main_split)
        container.setLayout(layout)
        self.setCentralWidget(container)


    def open_project(self):
        folder = QFileDialog.getExistingDirectory(
            self,
            "Select Folder",
            prefrenece.PROJECTS_FOLDER,
            QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks | QFileDialog.DontUseNativeDialog
        )

        if folder:
            print("Selected folder:", folder)





# =========================
# 🚀 MAIN
# =========================
if __name__ == "__main__":
    app = QApplication(sys.argv)

    # # APPLY STYLE
    app.setStyleSheet(style.BLENDER_STYLE)

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())