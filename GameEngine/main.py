import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import style , prefrenece 
from dataclasses import dataclass


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
        self.left_panel = QTreeWidget()
        self.left_panel.setHeaderHidden(False)

    def _create_menu(self):
        menubar = self.menuBar()
        # FILE
        file_menu = menubar.addMenu("File")
        open_action = QAction("Open", self)
        file_menu.addAction(open_action)
        open_action.setShortcut(QKeySequence.Open)
        open_action.triggered.connect(self.open_project)




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