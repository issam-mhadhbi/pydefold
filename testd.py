from pydefoldsdk import sdk
from google.protobuf.descriptor import FieldDescriptor


# ─────────────────────────────
# 🧠 Type + Label mapping
# ─────────────────────────────
TYPE_MAP = {
    FieldDescriptor.TYPE_DOUBLE: "double",
    FieldDescriptor.TYPE_FLOAT: "float",
    FieldDescriptor.TYPE_INT64: "int64",
    FieldDescriptor.TYPE_UINT64: "uint64",
    FieldDescriptor.TYPE_INT32: "int32",
    FieldDescriptor.TYPE_UINT32: "uint32",
    FieldDescriptor.TYPE_BOOL: "bool",
    FieldDescriptor.TYPE_STRING: "string",
    FieldDescriptor.TYPE_BYTES: "bytes",
    FieldDescriptor.TYPE_ENUM: "enum",
    FieldDescriptor.TYPE_MESSAGE: "message",
}

LABEL_MAP = {
    FieldDescriptor.LABEL_OPTIONAL: "optional",
    FieldDescriptor.LABEL_REPEATED: "repeated",
    FieldDescriptor.LABEL_REQUIRED: "required",
}


# ─────────────────────────────
# 🔍 Recursive inspector
# ─────────────────────────────
def inspect_message(msg, indent=0, path=None):
    if path is None:
        path = set()

    desc = msg.DESCRIPTOR
    pad = "  " * indent

    print(f"{pad}{desc.name} {{")

    # 🛑 prevent infinite recursion ONLY in current branch
    if desc.full_name in path:
        print(f"{pad}  ... (recursive reference)")
        print(f"{pad}}}")
        return

    # add to current path
    path.add(desc.full_name)

    for field in desc.fields:
        label = LABEL_MAP.get(field.label, "")
        field_type = TYPE_MAP.get(field.type, str(field.type))

        # ── Nested message
        if field.type == FieldDescriptor.TYPE_MESSAGE:
            print(f"{pad}  {label} {field.name} -> {field.message_type.name}")

            sub_msg = field.message_type._concrete_class()

            # 🔑 pass COPY of path (branch isolation)
            inspect_message(sub_msg, indent + 1, path.copy())

        # ── Enum
        elif field.type == FieldDescriptor.TYPE_ENUM:
            enum_vals = [v.name for v in field.enum_values]
            print(f"{pad}  {label} {field.name}: enum {enum_vals}")

        # ── Primitive
        else:
            print(f"{pad}  {label} {field.name}: {field_type}")

    print(f"{pad}}}")

# ─────────────────────────────
# 📦 Show current values (if set)
# ─────────────────────────────
def show_values(msg, indent=0):
    pad = "  " * indent

    for field, value in msg.ListFields():
        if field.type == FieldDescriptor.TYPE_MESSAGE:
            print(f"{pad}{field.name}:")
            show_values(value, indent + 1)
        else:
            print(f"{pad}{field.name}: {value}")


# ─────────────────────────────
# 🚀 MAIN
# ─────────────────────────────
if __name__ == "__main__":
    x = sdk.ModelDesc()

    print("\n=== 🧠 STRUCTURE ===\n")
    inspect_message(x)



    print("\n=== 📦 CURRENT VALUES (if any) ===\n")
    show_values(x)
