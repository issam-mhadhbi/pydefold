from PyQt5.QtWidgets import QApplication, QMainWindow, QTreeView, QVBoxLayout, QWidget
from PyQt5.QtGui import QStandardItemModel, QStandardItem


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QTreeView Example")

        # Central widget and layout
        central = QWidget()
        layout = QVBoxLayout()
        central.setLayout(layout)
        self.setCentralWidget(central)

        # Create tree view
        tree = QTreeView()
        layout.addWidget(tree)

        # Create model and set header
        model = QStandardItemModel()
        model.setHorizontalHeaderLabels(["Name", "Type"])

        # Top‑level item
        parent1 = QStandardItem("Documents")
        parent1.appendRow([QStandardItem("report.txt"), QStandardItem("file")])
        parent1.appendRow([QStandardItem("notes.md"), QStandardItem("file")])

        # Second branch
        parent2 = QStandardItem("Images")
        parent2.appendRow([QStandardItem("photo.jpg"), QStandardItem("image")])
        parent2.appendRow([QStandardItem("logo.png"), QStandardItem("image")])

        model.appendRow(parent1)
        model.appendRow(parent2)

        # Attach model to tree
        tree.setModel(model)

        # Optional: expand all nodes
        tree.expandAll()


app = QApplication([])
window = MainWindow()
window.resize(400, 300)
window.show()
app.exec_()