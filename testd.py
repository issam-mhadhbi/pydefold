import os
import xml.etree.ElementTree as ET

class AnimationParser:
    def __init__(self, path):
        self.path = path
        self.ext = os.path.splitext(path)[1].lower()

        if self.ext not in [".gltf", ".glb", ".dae"]:
            raise ValueError("Unsupported format: use .gltf, .glb, or .dae")

    def get_animation_names(self):
        if self.ext in [".gltf", ".glb"]:
            return self._parse_gltf()
        elif self.ext == ".dae":
            return self._parse_dae()

    # ─────────────────────────────
    # 🟢 GLTF / GLB
    # ─────────────────────────────
    def _parse_gltf(self):
        try:
            from pygltflib import GLTF2
        except ImportError:
            raise ImportError("Install pygltflib: pip install pygltflib")

        gltf = GLTF2().load(self.path)

        names = []
        for i, anim in enumerate(gltf.animations):
            if anim.name:
                names.append(anim.name)
            else:
                names.append(f"animation_{i}")

        return names

    # ─────────────────────────────
    # 🔵 COLLADA (DAE)
    # ─────────────────────────────
    def _parse_dae(self):
        tree = ET.parse(self.path)
        root = tree.getroot()

        ns = {'c': 'http://www.collada.org/2005/11/COLLADASchema'}

        names = []

        for i, anim in enumerate(root.findall('.//c:animation', ns)):
            anim_id = anim.get('id')
            anim_name = anim.get('name')

            if anim_name:
                names.append(anim_name)
            elif anim_id:
                names.append(anim_id)
            else:
                names.append(f"animation_{i}")

        return names
        
        
parser = AnimationParser("/home/username/Desktop/dev.issam/Defold/test/Mobile-Game/builtins/assets/gltf/cube.gltf")
print(parser.get_animation_names())
