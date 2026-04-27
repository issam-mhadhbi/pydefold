from dataclasses import dataclass, field
from enum import IntEnum
from typing import List
import os, sys, json
sys.path.extend([
    os.path.join(os.path.dirname(__file__) , 'pydefoldsdk')
])
import  gamesys.model_ddf_pb2
import render.material_ddf_pb2
from google.protobuf.json_format import MessageToJson
from google.protobuf.text_format import MessageToString, Parse
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import uic
from pathlib import Path
import xml.etree.ElementTree as ET
HERE = os.path.dirname(__file__)
UI = Path(os.path.join(HERE , 'Ui'))


class QMaterialDescWidget(QWidget) :
    proto_field_changed = pyqtSignal(str)
    def __init__(self,parent = None,project = None ):
        super().__init__(parent=parent)
        self.project = project
        uic.loadUi(UI / "DialogNewModel.ui" , self)
        
class DialogNewResourceMaterialDesc(QDialog) :
    def __init__(self,parent = None,project = None ):
        super().__init__(parent=parent)
        self.project = project

    def LoadWidget(self,WidgetDesc,save_in_suggestion = None ) :
        self.ItemWidget = QMaterialDescWidget(project = self.project , parent = self )
        self.location.addItems(self.project.get_all_folders())
        if save_in_suggestion is not None :
            self.location.setCurrentText(self.project.relativePath(save_in_suggestion))
        self.placeholder.addWidget(self.ItemWidget)
        self.setWindowTitle(self.ItemWidget.DialogTitle)


def request_new(**kwargs) : ## called when add new item , shall return a dialog
    dialog  = DialogNewResourceMaterialDesc(parent = kwargs.get('parent') ,project = kwargs.get('project') )
    dialog.LoadWidget(WidgetDesc = QMaterialDescWidget ,save_in_suggestion = kwargs.get('location'))
    return dialog

def request_from_file(**kwargs) : ## called when file clicked from file explorer
    ext = ".mesh"
    prop_widget = QModelDescWidget(parent = kwargs.get('parent') ,project = kwargs.get('project'))
    prop_widget.from_file(file_path = kwargs.get('file_path'))
    prop_widget.proto_field_changed.connect(lambda  : prop_widget.save(kwargs.get('file_path')) )
    return prop_widget