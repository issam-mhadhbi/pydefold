from dataclasses import dataclass, field
from enum import IntEnum
from typing import List
import sys , os 
sys.path.extend([
    os.path.join(os.path.dirname(__file__) , 'pydefoldsdk')
])
import  gamesys.model_ddf_pb2
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

class QModelDescWidget(QWidget) :
    proto_field_changed = pyqtSignal(str)
    def __init__(self,parent = None,project = None ):
        super().__init__(parent=parent)
        self.DialogTitle = "New Model"
        self.project = project
        self.msg = gamesys.model_ddf_pb2.ModelDesc()
        uic.loadUi(UI / "ModelDescOutliner.ui" , self)
        self.mesh.addItems(self.project.get_mesh_models())
        self.skeleton.addItems(self.project.get_mesh_models())
        self.animations.addItems(self.project.get_mesh_models())
        self.default_animation.addItems(self.project.get_mesh_models())
        self.materials.addItems(self.project.find_by_ext(ext = ".material"))
        self.materials.currentIndexChanged.connect(self.on_materials_changed)
        self.mesh.currentIndexChanged.connect(self.on_mesh_changed)
        self.skeleton.currentIndexChanged.connect(self.on_skeleton_changed)
        self.default_animation.currentIndexChanged.connect(self.on_default_animation_changed)
        self.animations.currentIndexChanged.connect(self.on_animations_changed)
        self.create_go_bones.stateChanged.connect(self.on_create_go_bones_changed)
        self.name.textChanged.connect(self.on_name_changed)

    def on_create_go_bones_changed(self,state):
        self.msg.create_go_bones = self.create_go_bones.isChecked()
        self.proto_field_changed.emit("create_go_bones")
        
    def on_animations_changed(self,index):
        if index < 0: return
        self.msg.animations = self.animations.currentText()  
        self.proto_field_changed.emit("animations")


    def on_name_changed(self,text):
        name = self.name.text().strip()
        if len(name) > 0 : 
            self.msg.name = name 
            self.proto_field_changed.emit("name")



    def on_default_animation_changed(self, index):
        if index < 0: return
        self.msg.default_animation = self.default_animation.currentText()  
        self.proto_field_changed.emit("default_animation")

    def on_skeleton_changed(self, index):
        if index < 0: return
        self.msg.skeleton = self.skeleton.currentText()  
        self.proto_field_changed.emit("skeleton")

    def on_mesh_changed(self, index):
        if index < 0: return
        self.msg.mesh = self.mesh.currentText()  
        self.proto_field_changed.emit("mesh")
        
    def on_materials_changed(self, index):
        if index < 0: return
        self.msg.materials.clear()
        self.msg.materials.append(gamesys.model_ddf_pb2.Material(name = "default" ))
        self.msg.materials[0].material = self.materials.currentText()
        self.msg.materials[0].textures.clear()
        samplers = self.getMaterialSamplers(self.msg.materials[0].material)
        self.msg.materials[0].textures.extend(["" for sam in samplers])
        
        

        mat_widget = self.buildMaterialWidget(self.msg.materials[0].material)
        self.proto_field_changed.emit("materials")
        
    def getMaterialSamplers(self,rel_mat_file_path) :
        mat_file_path = self.project.fullPath(rel_mat_file_path)
        material = sdk.MaterialDesc()
        Parse(Path(mat_file_path).read_text().encode('utf-8'), material)
        return material.samplers

    def buildMaterialWidget(self, rel_mat_file_path):
        self.clearMaterialWidget()
        samplers = self.getMaterialSamplers(rel_mat_file_path)
        self.msg.textures.clear()
        self.msg.textures.extend(["" for sam in samplers])
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

    def save(self,file_path) :
        Path(file_path).write_text(MessageToString(self.msg))

    def from_file(self,file_path) :
        Parse(Path(file_path).read_text().encode('utf-8'), self.msg)
        self.name.setText(self.msg.name)
        self.mesh.setCurrentText(self.msg.mesh)
        self.skeleton.setCurrentText(self.msg.skeleton)
        self.create_go_bones.setChecked(self.msg.create_go_bones)
        self.animations.setCurrentText(self.msg.animations)
        self.default_animation.setCurrentText(self.msg.default_animation)
        self.material.setCurrentText(self.msg.materials.material)
        self.buildMaterialWidget(self.msg.materials.material)
        self.buildOutlineModel(file_path)

    def buildOutlineModel(self,file_path) :
        self.outlineModel = QStandardItemModel()
        self.outlineModel.setHorizontalHeaderLabels(["\t\t\t\tOutliner"])
        child1 = QStandardItem(os.path.basename(file_path))
        child1.setEditable(False)
        self.outlineModel.appendRow(child1)
        
class DialogNewResourceModel(QDialog) :
    def __init__(self,parent = None,project = None ):
        super().__init__(parent=parent)
        self.project = project
        uic.loadUi(UI / "DialogNewModel.ui" , self)
        self.ext = None
        self.accepted.connect(self.on_accepted)
        self.rejected.connect(self.on_rejected)
        


    def LoadWidget(self,WidgetDesc,save_in_suggestion = None ) :
        self.ItemWidget = WidgetDesc(project = self.project , parent = self )
        self.location.addItems(self.project.get_all_folders())
        if save_in_suggestion is not None :
            self.location.setCurrentText(self.project.relativePath(save_in_suggestion))
        self.placeholder.addWidget(self.ItemWidget)
        self.setWindowTitle(self.ItemWidget.DialogTitle)
        self.name.textChanged.connect(self.on_name_changed)

    def on_accepted(self):
        file_path = os.path.join(self.project.fullPath(self.location.currentText()),f'{self.name.text().strip()}.model')
        self.ItemWidget.save(file_path = file_path )
        self.ItemWidget.deleteLater()

    def on_name_changed(self,text):
        file_path = os.path.join(self.project.fullPath(self.location.currentText()),f'{self.name.text().strip()}.model')
        self.ItemWidget.name.setText(text)


    def on_rejected(self):
        self.ItemWidget.deleteLater()









def request_new(**kwargs) : ## called when add new item , shall return a dialog
    dialog  = DialogNewResourceModel(parent = kwargs.get('parent') ,project = kwargs.get('project') )
    dialog.LoadWidget(WidgetDesc = QModelDescWidget ,save_in_suggestion = kwargs.get('location'))
    return dialog

def request_from_file(**kwargs) : ## called when file clicked from file explorer
    ext = ".mesh"
    prop_widget = QModelDescWidget(parent = kwargs.get('parent') ,project = kwargs.get('project'))
    prop_widget.from_file(file_path = kwargs.get('file_path'))
    prop_widget.proto_field_changed.connect(lambda  : prop_widget.save(kwargs.get('file_path')) )
    return prop_widget