from dataclasses import dataclass
from enum import IntEnum
from typing import Optional
from pydefoldsdk import sdk
from PyQt5.QtWidgets import *
from google.protobuf.text_format import MessageToString, Parse
import os 

class OrthographicMode(IntEnum):
    ORTHO_MODE_FIXED = 0
    ORTHO_MODE_AUTO_FIT = 1
    ORTHO_MODE_AUTO_COVER = 2 


@dataclass
class CameraDesc:
    NAME: str = None
    aspect_ratio: float = 1.0
    fov: float = 0.7854
    near_z: float = 0.1
    far_z: float = 1000.0
    auto_aspect_ratio: int = 0
    orthographic_projection: int = 0
    orthographic_zoom: float = 1.0
    orthographic_mode: Optional[OrthographicMode] = None

    # =========================
    # 🧱 NESTED EDITOR WIDGET
    # =========================
    class EditorWidget:
        def __init__(self, parent=None, data=None):
            self.widget = QWidget(parent)
            self.data = data or CameraDesc()

            main_layout = QVBoxLayout(self.widget)

            # =========================
            # 📦 PERSPECTIVE GROUP
            # =========================
            persp_group = QGroupBox("Perspective")
            persp_layout = QFormLayout()

            self.aspect = QDoubleSpinBox()
            self.aspect.setRange(0.1, 10.0)
            self.aspect.setValue(self.data.aspect_ratio)

            self.fov = QDoubleSpinBox()
            self.fov.setRange(0.01, 3.14)
            self.fov.setValue(self.data.fov)

            self.near_z = QDoubleSpinBox()
            self.near_z.setRange(0.001, 1000)
            self.near_z.setValue(self.data.near_z)

            self.far_z = QDoubleSpinBox()
            self.far_z.setRange(1, 10000)
            self.far_z.setValue(self.data.far_z)

            self.auto_aspect = QCheckBox()
            self.auto_aspect.setChecked(bool(self.data.auto_aspect_ratio))

            persp_layout.addRow("Aspect Ratio", self.aspect)
            persp_layout.addRow("FOV", self.fov)
            persp_layout.addRow("Near Z", self.near_z)
            persp_layout.addRow("Far Z", self.far_z)
            persp_layout.addRow("Auto Aspect", self.auto_aspect)

            persp_group.setLayout(persp_layout)

            # =========================
            # 📦 ORTHOGRAPHIC GROUP
            # =========================
            ortho_group = QGroupBox("Orthographic")
            ortho_layout = QFormLayout()

            self.ortho_proj = QCheckBox()
            self.ortho_proj.setChecked(bool(self.data.orthographic_projection))

            self.ortho_zoom = QDoubleSpinBox()
            self.ortho_zoom.setRange(0.01, 100)
            self.ortho_zoom.setValue(self.data.orthographic_zoom)

            self.ortho_mode = QComboBox()
            self.ortho_mode.addItem("None", None)
            for mode in OrthographicMode:
                self.ortho_mode.addItem(mode.name, mode)

            if self.data.orthographic_mode is not None:
                idx = self.ortho_mode.findData(self.data.orthographic_mode)
                if idx >= 0:
                    self.ortho_mode.setCurrentIndex(idx)

            ortho_layout.addRow("Enable Ortho", self.ortho_proj)
            ortho_layout.addRow("Zoom", self.ortho_zoom)
            ortho_layout.addRow("Mode", self.ortho_mode)

            ortho_group.setLayout(ortho_layout)

            # =========================
            # ADD GROUPS
            # =========================
            main_layout.addWidget(persp_group)
            main_layout.addWidget(ortho_group)

        # =========================
        # 🔁 EXTRACT DATA
        # =========================
        def get_value(self) -> "CameraDesc":
            return CameraDesc(
                aspect_ratio=self.aspect.value(),
                fov=self.fov.value(),
                near_z=self.near_z.value(),
                far_z=self.far_z.value(),
                auto_aspect_ratio=int(self.auto_aspect.isChecked()),
                orthographic_projection=int(self.ortho_proj.isChecked()),
                orthographic_zoom=self.ortho_zoom.value(),
                orthographic_mode=self.ortho_mode.currentData(),
            )

    # =========================
    # 🪟 DIALOG FACTORY
    # =========================

    @classmethod
    def create_from_ui(cls, parent):
        from PyQt5.QtWidgets import (
            QDialog, QVBoxLayout, QDialogButtonBox,
            QLineEdit, QLabel, QHBoxLayout, QMessageBox
        )

        dialog = QDialog(parent=parent)
        dialog.setWindowTitle("New Camera")
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
    
    def save2file(self,path) : 
        file = open(os.path.join(path , f'{self.NAME}.cam'),"w")
        file.write(MessageToString(self.to_proto()))


    def to_proto(self) -> sdk.CameraDesc:
        msg = sdk.CameraDesc()
        msg.aspect_ratio = self.aspect_ratio
        msg.fov = self.fov
        msg.near_z = self.near_z
        msg.far_z = self.far_z
        msg.auto_aspect_ratio = self.auto_aspect_ratio
        msg.orthographic_projection = self.orthographic_projection
        msg.orthographic_zoom = self.orthographic_zoom

        if self.orthographic_mode is not None:
            msg.orthographic_mode = int(self.orthographic_mode)

        return msg

    @classmethod
    def from_proto(cls, msg: sdk.CameraDesc):
        mode = None
        try:
            mode = OrthographicMode(msg.orthographic_mode)
        except ValueError:
            pass

        return cls(
            aspect_ratio=msg.aspect_ratio,
            fov=msg.fov,
            near_z=msg.near_z,
            far_z=msg.far_z,
            auto_aspect_ratio=msg.auto_aspect_ratio,
            orthographic_projection=msg.orthographic_projection,
            orthographic_zoom=msg.orthographic_zoom,
            orthographic_mode=mode,
        )


# =========================
# 🚀 Demo
# =========================
if __name__ == "__main__":
    cam = CameraDesc(
        aspect_ratio=1.77,
        fov=0.9,
        orthographic_mode=OrthographicMode.ORTHO_MODE_FIXED
    )

    print("Dataclass:")
    print(cam)

    proto = cam.to_proto()
    print("\nProtobuf:")
    print(proto)

    back = CameraDesc.from_proto(proto)
    print("\nBack to dataclass:")
    print(back)