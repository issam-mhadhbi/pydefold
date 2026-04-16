import sys , os 
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QDir, Qt



class FileExplorerFileSystemModel(QFileSystemModel):

    def __init__(self, parent=None,icons = dict()):
        super().__init__(parent)


    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            if section == 0:
                return "File Explorer"
        return super().headerData(section, orientation, role)


    def data(self, index, role=Qt.DisplayRole):
        # if role == Qt.DecorationRole:
        #     if index.column() == 0:
        #         path = self.filePath(index)

        #         if self.isDir(index):
        #             return self.icons["folder"]

        #         ext = os.path.splitext(path)[1].lower()

        #         if ext == ".lua":
        #             return self.icons["lua"]
        #         elif ext == ".png":
        #             return self.icons["png"]
        #         elif ext == ".mesh":
        #             return self.icons["mesh"]

        #         return self.icons["default"]

        return super().data(index, role)

class FileExplorer(QTreeView):
    def __init__(self,parent = None):
        super().__init__(parent=parent)
        self.setMinimumWidth(250)
        
        


    def on_double_clicked(self, index):
        path = self.model.filePath(index)
        self.currentPath = self.model.filePath(index)
        self.on_double_click(path)

    # =========================
    # RIGHT CLICK MENU
    # =========================
    def open_menu(self, position):
        index = self.indexAt(position)

        if not index.isValid():
            return

        path = self.model.filePath(index)
        self.selected_index= index 
        menu = QMenu()

        open_action = QAction("Open", self)
        delete_action = QAction("Delete", self)
        rename_action = QAction("Rename", self)

        menu.addAction(open_action)
        menu.addSeparator()
        menu.addAction(rename_action)
        menu.addAction(delete_action)

        action = menu.exec_(self.viewport().mapToGlobal(position))

        # =========================
        # ACTIONS
        # =========================
        if action == open_action:
            print("Open:", path)

        elif action == delete_action:
            self.delete_item(path)

        elif action == rename_action:
            self.edit(index)  # built-in rename

    def on_single_click(self,index):
        if not index.isValid():
            return
        self.currentPath = self.model.filePath(index)
        path = self.model.filePath(index)
        self.on_click(path)

    def on_click(self,path) : 
        pass 

    def on_double_click(self,path) : 
        pass 

    def set_rootPath(self,path) : 
        
        if not os.path.exists(os.path.abspath(path=path)) : 
            self.model = None 
            return
        # =========================
        # MODEL
        # =========================
        root_path = os.path.abspath(path=path)
        self.setRootIsDecorated(True)
        self.model = FileExplorerFileSystemModel(parent=self)
        self.model.setRootPath(root_path)
        self.model.setHeaderData(0, Qt.Horizontal, "File Explorer")
        self.currentPath = self.model.rootPath()
        # Filters (optional)
        self.model.setFilter(QDir.AllDirs | QDir.Files | QDir.NoDotAndDotDot)
        # =========================
        # VIEW
        # =========================
        self.setModel(self.model)
        self.setRootIndex(self.model.index(root_path))
        # Hide extra columns (keep only name)
        self.hideColumn(1)  # Size
        self.hideColumn(2)  # Type
        self.hideColumn(3)  # Date
        # Enable nice UX
        self.setAnimated(True)
        self.setIndentation(18)
        self.setSortingEnabled(True)
        self.setSortingEnabled(True)
        self.sortByColumn(0, Qt.AscendingOrder)
        header = self.header()
        header.setSectionsClickable(False)
        header.setSortIndicatorShown(False)
        header.setHighlightSections(False)
        # Double click open
        self.doubleClicked.connect(self.on_double_clicked)
        self.clicked.connect(self.on_single_click)
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.open_menu)

    def currentPathFolder(self) : 
        if not os.path.exists(self.currentPath) : 
            self.currentPath = self.model.rootPath()
        if os.path.isfile(self.currentPath) : 
            return os.path.dirname(self.currentPath)
        return self.currentPath
# =========================
# RUN
# =========================
if __name__ == "__main__":
    app = QApplication(sys.argv)
    here = os.path.dirname(__file__)
    test_folder = os.path.join(here,"..","test")

    win  = FileExplorer()
    win.set_rootPath(test_folder)
    win.show()

    sys.exit(app.exec_())