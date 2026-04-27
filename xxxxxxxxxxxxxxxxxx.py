from pydefoldsdk import sdk
import sys 
sys.path.extend([
    "/home/username/Desktop/dev.issam/Defold/GameEngine/pydefoldsdk"
])
from google.protobuf.text_format import MessageToString, Parse
import gamesys.model_ddf_pb2

model = sdk.ModelDesc()


x = MessageToString(model)
m = gamesys.model_ddf_pb2.Material() #sdk.Material()
m.name = "hhhhh"
model.materials.append(m)
print(model.materials)