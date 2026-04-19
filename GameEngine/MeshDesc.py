
from dataclasses import dataclass, field
from enum import IntEnum
from typing import List
from pydefoldsdk import sdk
import os, sys, json
from google.protobuf.json_format import MessageToJson
from google.protobuf.text_format import MessageToString, Parse
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import uic
from pathlib import Path
HERE = os.path.dirname(__file__)
UI = Path(os.path.join(HERE , 'Ui'))


class QMeshDescWidget(QWidget) :
    proto_field_changed = pyqtSignal(str)
    def __init__(self,parent = None,project = None ):
        super().__init__(parent=parent)
        self.DialogTitle = "New Mesh"
        self.project = project
        self.primitive_modes = {
            1: "PRIMITIVE_LINES",
            4: "PRIMITIVE_TRIANGLES",
            5: "PRIMITIVE_TRIANGLE_STRIP",
        }
        self.msg = sdk.MeshDesc()
        self.samplers_textures = list()
        uic.loadUi(UI / "MeshDescOutliner.ui" , self)
        self.vertices.addItems(self.project.find_by_ext(ext = ".buffer"))
        self.material.addItems(self.project.find_by_ext(ext = ".material"))
        self.material.currentIndexChanged.connect(self.on_material_changed)
        self.vertices.currentIndexChanged.connect(self.on_buffer_changed)
        self.position_stream.currentIndexChanged.connect(self.on_position_stream_changed)
        self.normal_stream.currentIndexChanged.connect(self.on_normal_stream_changed)
        self.primitive_type.currentIndexChanged.connect(self.on_primitive_type_changed)


    def on_material_changed(self, index):
        if index < 0: return
        self.msg.material = self.material.currentText()
        samplers = self.getMaterialSamplers(self.msg.material)
        self.msg.textures.extend(["" for sam in self.getMaterialSamplers(self.msg.material)])
        mat_widget = self.buildMaterialWidget(self.msg.material)
        self.proto_field_changed.emit("material")

    def buildMaterialWidget(self, rel_mat_file_path):
        self.clearMaterialWidget()
        samplers = self.getMaterialSamplers(rel_mat_file_path)
        self.msg.textures.extend(["" for sam in self.getMaterialSamplers(rel_mat_file_path)])
        widget  , vhbox  , form = QWidget(self) , QVBoxLayout() ,  QFormLayout()
        vhbox.addLayout(form)
        widget.setLayout(vhbox)
        for index , sampler in enumerate(samplers) :
            combo = QComboBox()
            combo.setObjectName(sampler.name)   # set object name
            combo.setCurrentIndex(-1)
            combo.setPlaceholderText(f"Select {sampler.name}...")
            combo.addItems(self.project.get_all_samplers())
            if self.msg.textures[index] != "" :
                print("-----------------" , self.msg.textures[index])
                combo.setCurrentText(self.msg.textures[index])
            combo.currentIndexChanged.connect(self.on_sampler_changed)
            form.addRow(sampler.name , combo)

        self.placeholder.addWidget(widget)


    def on_sampler_changed(self,index) :
        if index < 0 : return
        sampler_index = [sam.name for sam in self.getMaterialSamplers(self.msg.material)].index(self.sender().objectName())
        self.msg.textures[sampler_index] = self.sender().currentText()
        self.proto_field_changed.emit("textures")

    def clearMaterialWidget(self) :
        itm = self.placeholder.takeAt(0)
        if itm :
            widget = itm.widget()
            if widget :
                widget.deleteLater()



    def on_buffer_changed(self, index):
        if index < 0: return
        self.position_stream.clear()
        self.normal_stream.clear()
        buffer_path = self.project.fullPath(self.vertices.currentText())
        self.msg.vertices = self.vertices.currentText()
        print(self.msg.vertices)
        txt = Path(buffer_path).read_text()

        try:
            data = json.loads(txt)
            keys = sorted(i.get('name') for i in data)
            self.position_stream.addItems(keys)
            self.normal_stream.addItems(keys)
            self.proto_field_changed.emit("vertices")
        except Exception as e:
            import traceback
            self.project.LogError(f"[ERROR] on_vertices_changed crashed:\n{traceback.format_exc()}")

    def on_position_stream_changed(self, index):
        if index < 0: return
        self.msg.position_stream =  self.position_stream.currentText()
        self.proto_field_changed.emit("position_stream")

    def on_normal_stream_changed(self, index):
        if index < 0: return
        self.msg.normal_stream =  self.normal_stream.currentText()
        self.proto_field_changed.emit("normal_stream")

    def on_primitive_type_changed(self, index):
        if index < 0: return
        self.msg.primitive_type =  index + 1
        self.proto_field_changed.emit("primitive_type")


    def save(self,file_path) :
        Path(file_path).write_text(MessageToString(self.msg))

    def buildOutlineModel(self,file_path) :
        self.outlineModel = QStandardItemModel()
        self.outlineModel.setHorizontalHeaderLabels(["\t\t\t\tOutliner"])
        child1 = QStandardItem(os.path.basename(file_path))
        child1.setEditable(False)
        self.outlineModel.appendRow(child1)
        

    def getMaterialSamplers(self,rel_mat_file_path) :
        mat_file_path = self.project.fullPath(rel_mat_file_path)
        material = sdk.MaterialDesc()
        Parse(Path(mat_file_path).read_text().encode('utf-8'), material)
        return material.samplers



    def from_file(self,file_path) :
        Parse(Path(file_path).read_text().encode('utf-8'), self.msg)
        self.material.setCurrentText(self.msg.material)
        self.vertices.setCurrentText(self.msg.vertices)
        self.position_stream.setCurrentText(self.msg.position_stream)
        self.normal_stream.setCurrentText(self.msg.normal_stream)
        self.primitive_type.setCurrentText(self.primitive_modes.get(self.msg.primitive_type)  )
        self.buildMaterialWidget(self.msg.material)
        self.buildOutlineModel(file_path)




class DialogNewResourceMesh(QDialog) :
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
        file_path = os.path.join(self.project.fullPath(self.location.currentText()),f'{self.name.text().strip()}.mesh')
        self.ItemWidget.save(file_path = file_path )
        self.ItemWidget.deleteLater()


    def on_rejected(self):
        self.ItemWidget.deleteLater()



def request_new(**kwargs) : ## called when add new item , shall return a dialog
    dialog  = DialogNewResourceMesh(parent = kwargs.get('parent') ,project = kwargs.get('project') )
    dialog.LoadWidget(WidgetDesc = QMeshDescWidget ,save_in_suggestion = kwargs.get('location'))
    return dialog

def request_from_file(**kwargs) : ## called when file clicked from file explorer
    ext = ".mesh"
    prop_widget = QMeshDescWidget(parent = kwargs.get('parent') ,project = kwargs.get('project'))
    prop_widget.from_file(file_path = kwargs.get('file_path'))
    prop_widget.proto_field_changed.connect(lambda  : prop_widget.save(kwargs.get('file_path')) )
    return prop_widget






if __name__ == "__main__":
    pass
