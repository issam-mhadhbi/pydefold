from PyQt5.QtCore import Qt
from PyQt5.QtGui import QStandardItemModel
from PyQt5.QtWidgets import QTreeView, QApplication


class TreeModel(QStandardItemModel):
    def __init__(self):
        super().__init__()
        self.setHorizontalHeaderLabels([
            " Name",           # ← leading space here
            " Type"
        ])


# Usage
app = QApplication([])

view = QTreeView()
model = TreeModel()
view.setModel(model)

view.show()
app.exec_()