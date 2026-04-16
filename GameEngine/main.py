import sys , os , json 
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from pathlib import Path
import style , prefrenece 
from dataclasses import dataclass
from FileExplorer import FileExplorer
from Viewport import Viewport
from CameraDesc import CameraDesc
from MeshDesc import MeshDesc



@dataclass
class DefoldProject:
    project_path = None

    def find_by_ext(self, ext):
        root = Path(self.project_path)
        return sorted([
            str(p.relative_to(root))
            for p in root.rglob(f"*{ext}")
        ])

    def get_all_folders(self):
        root = Path(self.project_path)

        folders = [root]  # include root

        folders += [p for p in root.rglob("*") if p.is_dir()]

        return sorted([
            str(p.relative_to(root)) if p != root else "."
            for p in folders
        ])





class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.project = DefoldProject()
        self.setWindowTitle("Defold Editor")
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
        edit_menu = menubar.addMenu("Edit")
        Add_menu = menubar.addMenu("Add")
        #---
        add_camera = QAction("Camera",self)
        add_camera.triggered.connect(self.addCamera)
        Add_menu.addAction(add_camera)
        add_mesh = QAction("Mesh",self)
        add_mesh.triggered.connect(self.addMesh)
        Add_menu.addAction(add_mesh)

    def _create_main_layout(self) : 
        self.fileExplorer = FileExplorer(self)
        self.fileExplorer.setSizePolicy(
            QSizePolicy.Preferred, QSizePolicy.Expanding
        )
        self.assests_outline = QFrame(self)
        self.assests_outline.setSizePolicy(
            QSizePolicy.Preferred, QSizePolicy.Expanding
        )
        self.middle_zone = QTabWidget(self)
        self.initQTabwidget()
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

    def initQTabwidget(self):
        win = Viewport(self)
        layout = QHBoxLayout(win)
        self.middle_zone.addTab(win, "Tab One")


    def open_project(self,project_path = None ):
        if not ( project_path is None) : 
            if os.path.exists(project_path) : 
                self.fileExplorer.set_rootPath(project_path)
                self.fileExplorer.on_double_click = self.on_fileExplorerItemDoubleClicked
                self.project.project_path = project_path
        else :     
            folder = QFileDialog.getExistingDirectory(
                self,
                "Select Folder",
                prefrenece.PROJECTS_FOLDER,
                QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks | QFileDialog.DontUseNativeDialog
            )
            if folder:
                self.fileExplorer.set_rootPath(folder)
                self.fileExplorer.on_double_click = self.on_fileExplorerItemDoubleClicked
                self.project.project_path = folder

    def addCamera(self) : 
        cam = CameraDesc.create_from_ui(self)
        if cam : 
            save_folder = self.fileExplorer.currentPathFolder()
            # cam.save2file(save_folder)

    def addMesh(self) : 
        save_folder = self.fileExplorer.currentPathFolder()
        mesh = MeshDesc.create_from_ui(self,project=self.project,save_folder = save_folder )
        if mesh : 
            mesh.save2file(save_folder)
    
    def on_fileExplorerItemDoubleClicked(self,path) : 
        if os.path.isdir(path) : return 
        ext = os.path.splitext(path)[1]
        print(ext)



# =========================
# 🚀 MAIN
# =========================
if __name__ == "__main__":
    app = QApplication(sys.argv)

    # # APPLY STYLE
    app.setStyleSheet(style.BLENDER_STYLE)

    window = MainWindow()
    window.open_project(os.path.join(prefrenece.PROJECTS_FOLDER , "Mobile-Game"))
    window.show()

    sys.exit(app.exec_())

