from dataclasses import dataclass, field
from enum import IntEnum
from typing import List
from pydefoldsdk import sdk


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