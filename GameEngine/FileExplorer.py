import sys , os 
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import  * 
import Prefrenece , subprocess , os 
from pathlib import Path 

from pathlib import Path 


class LineNumberArea(QWidget):
    def __init__(self, editor):
        super().__init__(editor)
        self.editor = editor

    def sizeHint(self):
        return QSize(self.editor.lineNumberAreaWidth(), 0)

    def paintEvent(self, event):
        self.editor.lineNumberAreaPaintEvent(event)


class TextFileViewer(QPlainTextEdit):
    def __init__(self):
        super().__init__()

        self.setReadOnly(True)  # ✅ make it read-only

        self.lineNumberArea = LineNumberArea(self)
        self.blockCountChanged.connect(self.updateLineNumberAreaWidth)
        self.updateRequest.connect(self.updateLineNumberArea)
        self.cursorPositionChanged.connect(self.highlightCurrentLine)

        self.updateLineNumberAreaWidth(0)
        self.highlightCurrentLine()

    def lineNumberAreaWidth(self):
        digits = len(str(max(1, self.blockCount())))
        return 10 + self.fontMetrics().horizontalAdvance('9') * digits

    def updateLineNumberAreaWidth(self, _):
        self.setViewportMargins(self.lineNumberAreaWidth(), 0, 0, 0)

    def updateLineNumberArea(self, rect, dy):
        if dy:
            self.lineNumberArea.scroll(0, dy)
        else:
            self.lineNumberArea.update(0, rect.y(), self.lineNumberArea.width(), rect.height())
        if rect.contains(self.viewport().rect()):
            self.updateLineNumberAreaWidth(0)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        cr = self.contentsRect()
        self.lineNumberArea.setGeometry(
            QRect(cr.left(), cr.top(), self.lineNumberAreaWidth(), cr.height())
        )

    def lineNumberAreaPaintEvent(self, event):
        painter = QPainter(self.lineNumberArea)
        painter.fillRect(event.rect(), QColor(30, 30, 30))

        block = self.firstVisibleBlock()
        blockNumber = block.blockNumber()

        top = int(self.blockBoundingGeometry(block).translated(self.contentOffset()).top())
        bottom = top + int(self.blockBoundingRect(block).height())

        while block.isValid() and top <= event.rect().bottom():
            if block.isVisible() and bottom >= event.rect().top():
                painter.setPen(Qt.white)
                painter.drawText(
                    0, top,
                    self.lineNumberArea.width() - 5,
                    self.fontMetrics().height(),
                    Qt.AlignRight,
                    str(blockNumber + 1)
                )

            block = block.next()
            top = bottom
            bottom = top + int(self.blockBoundingRect(block).height())
            blockNumber += 1

    def highlightCurrentLine(self):
        selection = QTextEdit.ExtraSelection()
        selection.format.setBackground(QColor(50, 50, 50))
        selection.format.setProperty(QTextFormat.FullWidthSelection, True)

        selection.cursor = self.textCursor()
        selection.cursor.clearSelection()

        self.setExtraSelections([selection])




# ✅ Dialog wrapper
class ViewerDialog(QDialog):
    def __init__(self, file_path=None, text=None, parent=None):
        super().__init__(parent)

        self.setWindowTitle("File Viewer")
        self.resize(800, 600)

        layout = QVBoxLayout(self)

        self.viewer = TextFileViewer()
        layout.addWidget(self.viewer)

        if file_path:
            self.viewer.open_file(file_path)
        elif text:
            self.viewer.setPlainText(text)

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
        open_file_manager_action = QAction("Reveal in File Manager", self)
        open_defold = QAction("Open Defold", self)
        open_as_text = QAction("Open as text", self)
        open_terminal_here = QAction("Open Treminal Here ...", self)
        menu.addAction(open_action)
        menu.addSeparator()
        menu.addAction(rename_action)
        menu.addAction(delete_action)
        menu.addSeparator()
        menu.addAction(open_file_manager_action)
        menu.addSeparator()
        menu.addAction(open_defold)
        menu.addSeparator()
        menu.addAction(open_as_text)
        menu.addSeparator()
        menu.addAction(open_terminal_here)
        action = menu.exec_(self.viewport().mapToGlobal(position))

        # =========================
        # ACTIONS
        # =========================

        if action == open_action:
            self.open_as_text(path)

        if action == open_terminal_here:
            self.open_terminal_here(path)
        elif action == open_as_text:
            self.open_as_text(path)
        elif action == delete_action:
            self.delete_item(path)

        elif action == rename_action:
            self.edit(index)  # built-in rename

        elif action == open_file_manager_action :
            self.exec_open_file_manager_action(path)  # built-in rename
        elif action == open_defold :
            self.open_defold(path)  # built-in rename          
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
        
    def exec_open_file_manager_action(self,path) : 
        open_path = path if  Path(path).is_dir() else Path(path).parent
        proc = subprocess.Popen(
            [Prefrenece.FILE_MANAGER_BIN, open_path],
            stdin=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            start_new_session=True
        )

    def open_defold(self,path) : 
        if self.model is None : return 
        game_project = os.path.join(self.model.rootPath() , "game.project")
        if not Path(game_project).exists() : return 
        proc = subprocess.Popen(
            [Prefrenece.DEFOLD_BIN, game_project],
            stdin=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            start_new_session=True
        )

    def open_as_text(self,path) : 
        if self.model is None : return 
        path_file = Path(path)
        if not path_file.exists():return
        if not path_file.is_file(): return
        ViewerDialog(text=path_file.read_text(), parent=self).exec_()
        
    def open_terminal_here(self,path) : 
        if self.model is None : return 
        open_path = path if  Path(path).is_dir() else Path(path).parent
        proc = subprocess.Popen(
            [Prefrenece.TERMINAL_BIN],
            stdin=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            start_new_session=True , 
            cwd = str(open_path)
        )  
        
        
        
        
        





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