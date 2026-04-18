
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
        material_path = self.project.fullPath(self.material.currentText())
        self.project.Log(material_path)
        

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
        except Exception as e:
            import traceback
            self.project.LogError(f"[ERROR] on_vertices_changed crashed:\n{traceback.format_exc()}")

    def on_position_stream_changed(self, index):
        if index < 0: return
        self.msg.position_stream =  self.position_stream.currentText()

    def on_normal_stream_changed(self, index):
        if index < 0: return
        self.msg.normal_stream =  self.normal_stream.currentText()

    def on_primitive_type_changed(self, index):
        if index < 0: return
        self.msg.primitive_type =  self.primitive_modes.get(self.primitive_type.currentText() , None)   
        
    def save(self,folder , name) : 
        rel_path = os.path.join(folder,f"{name}.mesh")
        abs_path = self.project.fullPath(rel_path)
        print(MessageToString(self.msg))
        Path(abs_path).write_text(MessageToString(self.msg))
        
    def outlineModel(self) : 
        model = QStandardItemModel()
        model.setHorizontalHeaderLabels(["","Outliner"])
        return model 
        
    def fromFile(self,file_path) : 
        # update self.msg from the file 
        # update the ui from self.msg 
        pass 
        
    
        

        
    



if __name__ == "__main__": 
    pass 

























