from dataclasses import dataclass, field
from enum import IntEnum
from typing import List
from pydefoldsdk import sdk
import os , sys , json 
from google.protobuf.json_format import MessageToJson
from google.protobuf.text_format import MessageToString, Parse
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from pathlib import Path



class PrimitiveType(IntEnum):
    PRIMITIVE_LINES = 1
    PRIMITIVE_TRIANGLES = 4
    PRIMITIVE_TRIANGLE_STRIP = 5


@dataclass
class MeshDesc:
    material: str = ""
    vertices: str = ""
    textures: List[str] = field(default_factory=list)  # ✅ FIX
    primitive_type: PrimitiveType = PrimitiveType.PRIMITIVE_TRIANGLES
    position_stream: str = "position"
    normal_stream: str = "normal"



class QMeshDescWidget(QWidget) : 
    def __init__(self,parent = None,project = None):
        super().__init__(parent=parent)
        self.project = project
        self.layout = QVBoxLayout(self)
        self.data = MeshDesc()

    def CreationUI(self) : 
        self.setWindowTitle("New Mesh")
        self.center_on_screen()
        form = QFormLayout()
        self.name = QLineEdit()
        self.location = QComboBox()
        self.location.addItems(self.project.get_all_folders())
        form.addRow("Name:", self.name)
        form.addRow("Location:", self.location)
        self.layout.addLayout(form)
        self.buildDataUi()
        btn_layout = QHBoxLayout()
        self.ok_btn = QPushButton("OK")
        self.cancel_btn = QPushButton("Cancel")
        btn_layout.addWidget(self.ok_btn)
        btn_layout.addWidget(self.cancel_btn)
        self.layout.addLayout(btn_layout)
        self.ok_btn.clicked.connect(self.on_ok)
        self.cancel_btn.clicked.connect(self.on_cancel)

    def buildDataUi(self) : 
        group_inputs = QGroupBox("Mesh")
        form_layout = QFormLayout()
        #######################################
        ## Material : 
        self.material = QComboBox()
        self.material.setCurrentIndex(-1)
        self.material.setPlaceholderText("Select Material...")
        self.material.currentIndexChanged.connect(self.on_material_changed)
        materials = self.project.find_by_ext(ext = ".material")
        [self.material.addItems(materials)]
        form_layout.addRow("Material :" , self.material)
        self.material_inputs = QGroupBox("Material Data")
        self.material_inputs.hide()
        self.material_inputs_form = QFormLayout()
        self.material_inputs.setLayout(self.material_inputs_form)
        form_layout.addRow( self.material_inputs)
        ## buffer :
        self.vertices = QComboBox()
        self.vertices.setCurrentIndex(-1)
        self.vertices.setPlaceholderText("Select buffer...")
        self.vertices.addItems(self.project.find_by_ext(ext = ".buffer"))
        self.vertices.currentIndexChanged.connect(self.on_buffer_changed)
        form_layout.addRow("Vertices :" , self.vertices)
        ## Positions : 
        self.position_stream = QComboBox()  
        self.position_stream.setCurrentIndex(-1)
        self.position_stream.setPlaceholderText("Select Position...")
        form_layout.addRow("Position Stream", self.position_stream)
        ## Normals : 
        self.normal_stream = QComboBox() 
        self.normal_stream.setCurrentIndex(-1)
        self.normal_stream.setPlaceholderText("Select Normal...")
        form_layout.addRow("Normal Stream", self.normal_stream)
        ## primitive type 
        self.primitive = QComboBox()
        [self.primitive.addItem(p.name, p) for p in PrimitiveType]
        form_layout.addRow("Primtive Type :" , self.primitive)
        #######################################
        group_inputs.setLayout(form_layout)
        self.layout.addWidget(group_inputs)

    def on_material_changed(self,index) : 
        material_path = os.path.join(self.project.project_path ,self.material.itemText(index))
        self.material_inputs.hide()
        file = open(material_path)
        content = file.read()
        mat = sdk.MaterialDesc()
        self.Material_samplers = dict()
        samplers = list()
        self.clear_form(self.material_inputs_form)
        try : 
            Parse(content.encode('utf-8'), mat)
            if len(mat.samplers) > 0  : 
                self.material_inputs.show()
            for sam in mat.samplers : 
                self.Material_samplers[sam.name] = QComboBox()
                self.Material_samplers[sam.name].setCurrentIndex(-1)
                self.Material_samplers[sam.name].setPlaceholderText(" ...")
                self.Material_samplers[sam.name].addItems(self.project.get_all_samplers())
                self.material_inputs_form.addRow(sam.name , self.Material_samplers[sam.name])
            
        except Exception as err  : 
            msg = f"File Matrial {self.material.itemText(index)} is corrupted . "
            self.project.LogError(msg)




    def on_buffer_changed(self,index) : 
        self.position_stream.clear()
        self.position_stream.setCurrentIndex(-1)
        self.position_stream.setPlaceholderText("Select Position...")
        self.normal_stream.clear()
        self.normal_stream.setCurrentIndex(-1)
        self.normal_stream.setPlaceholderText("Select Normal...")
        buffer_path = os.path.join(self.project.project_path ,self.vertices.itemText(index))
        txt = Path(buffer_path).read_text()
        keys = list()
        try : 
            keys = sorted(i.get('name') for i in json.loads(txt))
        except Exception as err : 
            msg = f"File buffer ({buffer_path}) is not valid json . "
            print(msg)
        self.position_stream.addItems(keys)
        self.normal_stream.addItems(keys)

    def on_ok(self):
        self._result = self.get_value()
        self.close()

    def on_cancel(self):
        self._result = None
        self.close()

    def get_value(self):
        return {
            "name": self.name.text(),
            "location": self.location.currentText()
        }


    def exec_blocking(self):
        loop = QEventLoop()
        self._result = None
        self.show()

        self.destroyed.connect(loop.quit)
        loop.exec_()
        return self._result

    def clear_form(self,layout):
        if layout is None: return
        try:
            count = layout.count()
        except RuntimeError:
            return  # layout already deleted
        while layout.count():
            item = layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
            elif item.layout():
                self.clear_form(item.layout())

    def center_on_screen(self):
        screen = QGuiApplication.primaryScreen().geometry()
        window = self.geometry()

        x = (screen.width() - window.width()) // 2
        y = (screen.height() - window.height()) // 2

        self.move(x, y)