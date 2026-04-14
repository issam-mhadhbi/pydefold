from dataclasses import dataclass
from enum import IntEnum
from typing import Optional
from pydefoldsdk import sdk



class OrthographicMode(IntEnum):
    ORTHO_MODE_FIXED = 0
    ORTHO_MODE_AUTO_FIT = 1
    ORTHO_MODE_AUTO_COVER = 2 


@dataclass
class CameraDesc:
    aspect_ratio: float = 1.0
    fov: float = 0.7854
    near_z: float = 0.1
    far_z: float = 1000.0
    auto_aspect_ratio: int = 0
    orthographic_projection: int = 0
    orthographic_zoom: float = 1.0
    orthographic_mode: Optional[OrthographicMode] = None

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