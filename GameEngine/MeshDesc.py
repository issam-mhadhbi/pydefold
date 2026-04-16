from dataclasses import dataclass, field
from enum import IntEnum
from typing import List
from pydefoldsdk import sdk
import os , sys 
from google.protobuf.text_format import MessageToString, Parse


class PrimitiveType(IntEnum):
    PRIMITIVE_LINES = 1
    PRIMITIVE_TRIANGLES = 4
    PRIMITIVE_TRIANGLE_STRIP = 5


@dataclass
class MeshDesc:
    NAME : str = None
    EXTENSION : str = ".mesh"
    material: str = ""
    vertices: str = ""
    textures: List[str] = field(default_factory=list)  # ✅ FIX
    primitive_type: PrimitiveType = PrimitiveType.PRIMITIVE_TRIANGLES
    position_stream: str = "position"
    normal_stream: str = "normal"
    # =========================
    # 🧱 NESTED UI EDITOR
    # =========================
    class EditorWidget:
        def __init__(self, parent=None, data=None):
            from PyQt5.QtWidgets import (
                QWidget, QVBoxLayout, QFormLayout,
                QLineEdit, QComboBox, QGroupBox
            )

            self.widget = QWidget(parent)
            self.data = data or MeshDesc()

            main = QVBoxLayout(self.widget)

            # =========================
            # 📦 MESH GROUP
            # =========================
            mesh_group = QGroupBox("Mesh")
            mesh_layout = QFormLayout()

            self.material = QLineEdit(self.data.material)
            self.vertices = QLineEdit(self.data.vertices)

            mesh_layout.addRow("Material", self.material)
            mesh_layout.addRow("Vertices Buffer", self.vertices)

            mesh_group.setLayout(mesh_layout)

            # =========================
            # 📦 STREAMS GROUP
            # =========================
            stream_group = QGroupBox("Streams")
            stream_layout = QFormLayout()

            self.position_stream = QLineEdit(self.data.position_stream)
            self.normal_stream = QLineEdit(self.data.normal_stream)

            stream_layout.addRow("Position Stream", self.position_stream)
            stream_layout.addRow("Normal Stream", self.normal_stream)

            stream_group.setLayout(stream_layout)

            # =========================
            # 📦 PRIMITIVE TYPE
            # =========================
            prim_group = QGroupBox("Primitive")
            prim_layout = QFormLayout()

            self.primitive = QComboBox()
            for p in PrimitiveType:
                self.primitive.addItem(p.name, p)

            idx = self.primitive.findData(self.data.primitive_type)
            if idx >= 0:
                self.primitive.setCurrentIndex(idx)

            prim_layout.addRow("Type", self.primitive)
            prim_group.setLayout(prim_layout)

            # =========================
            # ADD ALL GROUPS
            # =========================
            main.addWidget(mesh_group)
            main.addWidget(stream_group)
            main.addWidget(prim_group)

        # =========================
        # 🔁 EXTRACT DATA
        # =========================
        def get_value(self) -> "MeshDesc":
            return MeshDesc(
                material=self.material.text().strip(),
                vertices=self.vertices.text().strip(),
                primitive_type=self.primitive.currentData(),
                position_stream=self.position_stream.text().strip(),
                normal_stream=self.normal_stream.text().strip(),
            )

    # =========================
    # 🪟 FACTORY UI
    # =========================
    @classmethod
    def create_from_ui(cls, parent):
        from PyQt5.QtWidgets import (
            QDialog, QVBoxLayout, QDialogButtonBox,
            QLineEdit, QLabel, QHBoxLayout, QMessageBox
        )

        dialog = QDialog(parent=parent)
        dialog.setWindowTitle("New Mesh")

        layout = QVBoxLayout(dialog)

        # =========================
        # 🔤 NAME FIELD (TOP)
        # =========================
        name_layout = QHBoxLayout()
        name_label = QLabel("Name:")
        name_edit = QLineEdit()

        name_layout.addWidget(name_label)
        name_layout.addWidget(name_edit)

        layout.addLayout(name_layout)

        # =========================
        # EDITOR
        # =========================
        editor = cls.EditorWidget(dialog)
        layout.addWidget(editor.widget)

        # =========================
        # BUTTONS
        # =========================
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        layout.addWidget(buttons)

        # =========================
        # VALIDATION
        # =========================
        def on_accept():
            if not name_edit.text().strip():
                QMessageBox.warning(dialog, "Error", "Name must not be empty")
                return
            dialog.accept()

        buttons.accepted.connect(on_accept)
        buttons.rejected.connect(dialog.reject)

        # =========================
        # EXEC
        # =========================
        if dialog.exec_() == QDialog.Accepted:
            cam = editor.get_value()
            cam.NAME = name_edit.text().strip()   # 🔥 attach name dynamically
            return cam

        return None
    def to_proto(self) -> sdk.MeshDesc:
        msg = sdk.MeshDesc()
        msg.material = self.material
        msg.vertices = self.vertices

        # ✅ FIX: repeated field
        msg.textures.extend(self.textures)

        msg.primitive_type = int(self.primitive_type)
        msg.position_stream = self.position_stream
        msg.normal_stream = self.normal_stream
        return msg

    @classmethod
    def from_proto(cls, msg: sdk.MeshDesc):
        try:
            prim = PrimitiveType(msg.primitive_type)
        except ValueError:
            prim = PrimitiveType.PRIMITIVE_TRIANGLES

        return cls(
            material=msg.material,
            vertices=msg.vertices,
            textures=list(msg.textures),  # ✅ FIX
            primitive_type=prim,
            position_stream=msg.position_stream,
            normal_stream=msg.normal_stream,
        )

    def save2file(self,path) : 
        file = open(os.path.join(path , f'{self.NAME}.{self.EXTENSION}'),"w")
        file.write(MessageToString(self.to_proto()))
# =========================
# 🚀 Demo
# =========================
if __name__ == "__main__":
    mesh = MeshDesc(
        material="/builtins/materials/model.material",
        vertices="/monkey.buffer",
        textures=["/captivating-yellow-texture-background-om4bll54o53qo9p5.jpg"],
        primitive_type=PrimitiveType.PRIMITIVE_TRIANGLES,
        position_stream="position",
        normal_stream="normal"
    )

    print("Dataclass:")
    print(mesh)

    proto = mesh.to_proto()
    print("\nProtobuf:")
    print(proto)

    back = MeshDesc.from_proto(proto)
    print("\nBack to dataclass:")
    print(back)

## buffer are json data : 
'''

This example contains a game object with a mesh component in the shape of a triangle. The triangle is defined in `triangle.buffer` as the three points of the triangle in the `position` stream. The triangle also defines the colors at each point. The colors get mixed automatically when the triangle is drawn by the shader.

```
[
    {
        "name": "position",
        "type": "float32",
        "count": 3,
        "data": [
            -0.5, -0.5, 0,
            0.5, -0.5, 0,
            0.0, 0.5, 0
        ]
    },
    {
        "name": "color0",
        "type": "float32",
        "count": 4,
        "data": [
            0, 1, 0, 1,
            1, 0, 0, 1,
            0, 0, 1, 1
        ]
    }
]
```

#### Scripts

mesh.fp

```
varying mediump vec4 var_color;

void main()
{
    gl_FragColor = var_color;
}
```

mesh.vp

```
uniform mediump mat4 mtx_worldview;
uniform mediump mat4 mtx_proj;

attribute mediump vec4 position;
attribute mediump vec4 color0;

varying mediump vec4 var_color;

void main()
{
    gl_Position = mtx_proj * mtx_worldview * vec4(position.xyz, 1.0);
    var_color = color0;
}
```'''