from dataclasses import dataclass, field
from enum import IntEnum
from typing import List


# =========================
# ENUMS
# =========================
class ConstantType(IntEnum):
    CONSTANT_TYPE_USER = 0
    CONSTANT_TYPE_VIEWPROJ = 1
    CONSTANT_TYPE_WORLD = 2
    CONSTANT_TYPE_TEXTURE = 3
    CONSTANT_TYPE_VIEW = 4
    CONSTANT_TYPE_PROJECTION = 5
    CONSTANT_TYPE_NORMAL = 6
    CONSTANT_TYPE_WORLDVIEW = 7
    CONSTANT_TYPE_WORLDVIEWPROJ = 8
    CONSTANT_TYPE_USER_MATRIX4 = 9


class VertexSpace(IntEnum):
    VERTEX_SPACE_WORLD = 0
    VERTEX_SPACE_LOCAL = 1


class WrapMode(IntEnum):
    WRAP_MODE_REPEAT = 0
    WRAP_MODE_MIRRORED_REPEAT = 1
    WRAP_MODE_CLAMP_TO_EDGE = 2


class FilterModeMin(IntEnum):
    FILTER_MODE_MIN_NEAREST = 0
    FILTER_MODE_MIN_LINEAR = 1
    FILTER_MODE_MIN_NEAREST_MIPMAP_NEAREST = 2
    FILTER_MODE_MIN_NEAREST_MIPMAP_LINEAR = 3
    FILTER_MODE_MIN_LINEAR_MIPMAP_NEAREST = 4
    FILTER_MODE_MIN_LINEAR_MIPMAP_LINEAR = 5
    FILTER_MODE_MIN_DEFAULT = 6


class FilterModeMag(IntEnum):
    FILTER_MODE_MAG_NEAREST = 0
    FILTER_MODE_MAG_LINEAR = 1
    FILTER_MODE_MAG_DEFAULT = 2


# =========================
# NESTED TYPES
# =========================
@dataclass
class Constant:
    name: str = ""
    type: ConstantType = ConstantType.CONSTANT_TYPE_USER


@dataclass
class Sampler:
    name: str = ""
    wrap_u: WrapMode = WrapMode.WRAP_MODE_REPEAT
    wrap_v: WrapMode = WrapMode.WRAP_MODE_REPEAT
    min_filter: FilterModeMin = FilterModeMin.FILTER_MODE_MIN_LINEAR
    mag_filter: FilterModeMag = FilterModeMag.FILTER_MODE_MAG_LINEAR


@dataclass
class VertexAttribute:
    name: str = ""
    semantic: str = ""   # e.g. POSITION, NORMAL, TEXCOORD


@dataclass
class PbrParameters:
    roughness: float = 1.0
    metallic: float = 0.0


# =========================
# MAIN DATACLASS
# =========================
@dataclass
class MaterialDesc:
    name: str = ""
    tags: str = ""

    vertex_program: str = ""
    fragment_program: str = ""

    vertex_space: VertexSpace = VertexSpace.VERTEX_SPACE_LOCAL

    vertex_constants: List[Constant] = field(default_factory=list)
    fragment_constants: List[Constant] = field(default_factory=list)

    textures: List[str] = field(default_factory=list)
    samplers: List[Sampler] = field(default_factory=list)

    max_page_count: int = 0

    attributes: List[VertexAttribute] = field(default_factory=list)

    program: str = ""

    pbr_parameters: PbrParameters = field(default_factory=PbrParameters)

if __name__ == "__main__":
    mat = MaterialDesc(
        name="gold_material",
        vertex_program="/shaders/gold.vp",
        fragment_program="/shaders/gold.fp",
        textures=["/textures/gold.png"],
        vertex_space=VertexSpace.VERTEX_SPACE_WORLD,
        pbr_parameters=PbrParameters(roughness=0.2, metallic=1.0)
    )

    print(mat)