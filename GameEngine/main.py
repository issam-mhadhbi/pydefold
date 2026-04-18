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
from MeshDesc import  QMeshDescWidget
from PyQt5 import uic
HERE = os.path.dirname(__file__)
UI = Path(os.path.join(HERE , 'Ui'))


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

    def get_all_samplers(self):
        result = self.find_by_ext(".png")
        return sorted(result)

    def LogError(self,msg) :
        print("🚨📢🔔⚠️" , msg)
        self.MainWindow.statusBar().showMessage(f"🚨 {msg}")

    def Log(self,msg) :
        print(msg)
        self.MainWindow.statusBar().showMessage(f"📢 {msg}")
    def setMainWindow(self,mainwindow) :
        self.MainWindow   = mainwindow
        
    def fullPath(self,rel_path) : 
        return os.path.join(self.project_path,rel_path)

    def relativePath(self, abs_path):
        abs_path = Path(abs_path).resolve()
        project = Path(self.project_path).resolve()
        return str(abs_path.relative_to(project))




class DialogNewResource(QDialog) : 
    def __init__(self,parent = None,project = None ):
        super().__init__(parent=parent)
        self.project = project
        uic.loadUi(UI / "DialogNew.ui" , self)
        self.ext = None 
        self.accepted.connect(self.on_accepted)
        self.rejected.connect(self.on_rejected)
    def setExtension(self,ext) : 
        self.ext = ext 
        
    def LoadWidget(self,WidgetDesc,save_in_suggestion = None ) : 
        self.ItemWidget = QMeshDescWidget(project = self.project , parent = self )
        self.location.addItems(self.project.get_all_folders())
        if save_in_suggestion is not None : 
            self.location.setCurrentText(self.project.relativePath(save_in_suggestion))
        self.placeholder.addWidget(self.ItemWidget)
        self.setWindowTitle(self.ItemWidget.DialogTitle)

    def on_accepted(self):
        self.ItemWidget.deleteLater()
        saving_folder = self.location.currentText()
        name = self.name.text().strip()
        self.ItemWidget.save(folder = saving_folder , name = name )
        print("Dialog accepted:")

    def on_rejected(self):
        self.ItemWidget.deleteLater()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.project = DefoldProject()
        self.DialogNewResource = DialogNewResource(parent = self , project = self.project)
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
                self.project.setMainWindow(self)
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
                self.project.setMainWindow(self)

    def addCamera(self) :
        cam = CameraDesc.create_from_ui(self)
        if cam :
            save_folder = self.fileExplorer.currentPathFolder()
            # cam.save2file(save_folder)

    def addMesh(self) :
        save_folder = self.fileExplorer.currentPathFolder()
        print(self.fileExplorer.currentPathFolder())
        self.DialogNewResource.LoadWidget(WidgetDesc = QMeshDescWidget ,save_in_suggestion = self.fileExplorer.currentPathFolder())
        self.DialogNewResource.exec_()
        

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
    print("hhhhhhhhhh")
    window = MainWindow()
    window.open_project(os.path.join(prefrenece.PROJECTS_FOLDER , "Mobile-Game"))
    window.show()

    sys.exit(app.exec_())
