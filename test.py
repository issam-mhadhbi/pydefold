from pydefoldsdk import sdk

s = sdk.CameraDesc()

# Access enum descriptor
field = s.DESCRIPTOR.fields_by_name['orthographic_mode']
enum_desc = field.enum_type

# Build mapping (number -> name)
enum_map = {v.number: v.name for v in enum_desc.values}

# Current value → name
value = s.orthographic_mode
name = enum_desc.values_by_number.get(value).name if value in enum_desc.values_by_number else None

print("Enum mapping:", enum_map)
print("Current value:", value)
print("Resolved name:", name)