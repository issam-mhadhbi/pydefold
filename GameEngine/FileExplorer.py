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
        # set icons here 

        return super().data(index, role)

class FileExplorer(QTreeView):
    def __init__(self,parent = None):
        super().__init__(parent=parent)
        self.setMinimumWidth(250)
        
        


    def on_double_click(self, index):
        path = self.model.filePath(index)
        self.selected_index= index 
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

    def on_single_click(self,position):
        index = self.indexAt(position)

        if not index.isValid():
            return
        self.selected_index= index 
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
        self.selected_index = None 
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

        # Double click open
        self.doubleClicked.connect(self.on_double_click)
        self.clicked.connect(self.on_single_click)
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.open_menu)
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