from pydefoldsdk import sdk 
from PyQt5.QtWidgets import *
from google.protobuf.descriptor import FieldDescriptor


class BaseElement : 
    pass 
class CameraDescUI(QDialog):
    def __init__(self):
        super().__init__()
        message_cls = sdk.CameraDesc
        self.setWindowTitle(f"{message_cls.__name__} Editor")
        
        self.msg = message_cls()
        self.layout = QFormLayout()
        self.widgets = {}

        for field in self.msg.DESCRIPTOR.fields:
            widget = self.create_widget(field)
            self.widgets[field.name] = widget
            self.layout.addRow(field.name, widget)

        # Submit button
        btn = QPushButton("Create")
        btn.clicked.connect(self.build_message)
        self.layout.addRow(btn)

        self.setLayout(self.layout)

class CameraDesc:
    def __init__(
        self,
        aspect_ratio: float = 1.0 ,
        fov: float = 0.7854 ,
        near_z: float = 0.1,
        far_z: float = 1000.0 ,
        auto_aspect_ratio: int = 0 ,
        orthographic_projection: int = 0 ,
        orthographic_zoom: float = 1.0 ,
        orthographic_mode: int = None ## this is from enum how to retireve name from the sdk.CameraDesc() class its values ?
    ):
        self.aspect_ratio = aspect_ratio
        self.fov = fov
        self.near_z = near_z
        self.far_z = far_z
        self.auto_aspect_ratio = auto_aspect_ratio
        self.orthographic_projection = orthographic_projection
        self.orthographic_zoom = orthographic_zoom
        self.orthographic_mode = orthographic_mode

    def ui(self) : 
        pass 

s = sdk.CameraDesc() --> this protobuff message
print(s)