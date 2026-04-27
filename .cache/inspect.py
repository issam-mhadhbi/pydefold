"""
Proto Message Inspector
=======================
Pass any protobuf message CLASS or INSTANCE and get a full deep inspection:
  - All fields (name, number, type, label)
  - Nested message types (recursive)
  - Enums and their values
  - oneofs
  - Maps
  - Default values

Usage:
    from proto_inspector import inspect_proto, print_proto_tree

    # With a class
    inspect_proto(MyMessage)

    # With an instance
    msg = MyMessage(name="hello")
    inspect_proto(msg)
"""

import json
from typing import Any
import sys , os 
sys.path.extend([
    os.path.join(os.path.dirname(__file__) , 'pydefoldsdk')
])
try:
    from google.protobuf import descriptor as desc
    from google.protobuf.descriptor import (
        FieldDescriptor,
        Descriptor,
        EnumDescriptor,
        OneofDescriptor,
    )
    from google.protobuf.message import Message
except ImportError:
    raise ImportError("Install protobuf: pip install protobuf")


# ── Field type name mapping ────────────────────────────────────────────────────
FIELD_TYPE_NAMES = {
    FieldDescriptor.TYPE_DOUBLE:   "double",
    FieldDescriptor.TYPE_FLOAT:    "float",
    FieldDescriptor.TYPE_INT64:    "int64",
    FieldDescriptor.TYPE_UINT64:   "uint64",
    FieldDescriptor.TYPE_INT32:    "int32",
    FieldDescriptor.TYPE_FIXED64:  "fixed64",
    FieldDescriptor.TYPE_FIXED32:  "fixed32",
    FieldDescriptor.TYPE_BOOL:     "bool",
    FieldDescriptor.TYPE_STRING:   "string",
    FieldDescriptor.TYPE_GROUP:    "group",
    FieldDescriptor.TYPE_MESSAGE:  "message",
    FieldDescriptor.TYPE_BYTES:    "bytes",
    FieldDescriptor.TYPE_UINT32:   "uint32",
    FieldDescriptor.TYPE_ENUM:     "enum",
    FieldDescriptor.TYPE_SFIXED32: "sfixed32",
    FieldDescriptor.TYPE_SFIXED64: "sfixed64",
    FieldDescriptor.TYPE_SINT32:   "sint32",
    FieldDescriptor.TYPE_SINT64:   "sint64",
}

FIELD_LABEL_NAMES = {
    FieldDescriptor.LABEL_OPTIONAL: "optional",
    FieldDescriptor.LABEL_REQUIRED: "required",
    FieldDescriptor.LABEL_REPEATED: "repeated",
}


# ── Core inspection ────────────────────────────────────────────────────────────

def _inspect_enum(enum_desc: EnumDescriptor) -> dict:
    """Extract enum descriptor info."""
    return {
        "name": enum_desc.name,
        "full_name": enum_desc.full_name,
        "values": [
            {"name": v.name, "number": v.number}
            for v in enum_desc.values
        ],
    }


def _get_label(field) -> str:
    if getattr(field, "is_repeated", False):
        return "repeated"
    if getattr(field, "is_required", False):
        return "required"
    try:
        return FIELD_LABEL_NAMES.get(field.label, "optional")
    except AttributeError:
        return "optional"


def _inspect_field(field: FieldDescriptor, visited: set) -> dict:
    """Extract field descriptor info, recursing into nested messages."""
    type_name  = FIELD_TYPE_NAMES.get(field.type, f"unknown({field.type})")
    label_name = _get_label(field)

    info: dict = {
        "name":        field.name,
        "number":      field.number,
        "type":        type_name,
        "label":       label_name,
        "is_map":      False,
        "is_oneof":    field.containing_oneof is not None,
        "oneof_name":  field.containing_oneof.name if field.containing_oneof else None,
        "default":     None,
    }

    # Default value
    try:
        if field.type != FieldDescriptor.TYPE_MESSAGE:
            info["default"] = field.default_value
    except Exception:
        pass

    # Enum fields
    if field.type == FieldDescriptor.TYPE_ENUM and field.enum_type:
        info["enum"] = _inspect_enum(field.enum_type)

    # Nested message fields
    if field.type == FieldDescriptor.TYPE_MESSAGE and field.message_type:
        nested = field.message_type
        # Detect map entries
        if nested.GetOptions().map_entry:
            info["is_map"] = True
            info["type"] = "map"
            key_field   = nested.fields_by_name.get("key")
            value_field = nested.fields_by_name.get("value")
            info["map_key_type"]   = FIELD_TYPE_NAMES.get(key_field.type,   "?") if key_field   else "?"
            info["map_value_type"] = FIELD_TYPE_NAMES.get(value_field.type, "?") if value_field else "?"
            if value_field and value_field.type == FieldDescriptor.TYPE_MESSAGE and value_field.message_type:
                info["map_value_message"] = value_field.message_type.full_name
        else:
            # Recurse only if not already visited (avoid infinite loops)
            if nested.full_name not in visited:
                info["nested_message"] = _inspect_message(nested, visited | {nested.full_name})
            else:
                info["nested_message"] = {"name": nested.name, "full_name": nested.full_name, "note": "(recursive ref)"}

    return info


def _inspect_message(msg_desc: Descriptor, visited: set = None) -> dict:
    """Recursively inspect a message descriptor."""
    if visited is None:
        visited = set()
    visited = visited | {msg_desc.full_name}

    # oneofs
    oneofs = [
        {
            "name": oo.name,
            "fields": [f.name for f in oo.fields],
        }
        for oo in msg_desc.oneofs
    ]

    # fields
    fields = [
        _inspect_field(f, visited)
        for f in msg_desc.fields
    ]

    # nested message types
    nested_types = [
        _inspect_message(nt, visited | {nt.full_name})
        for nt in msg_desc.nested_types
        if not nt.GetOptions().map_entry   # skip auto-generated map entries
    ]

    # enums
    enums = [
        _inspect_enum(e)
        for e in msg_desc.enum_types
    ]

    return {
        "name":         msg_desc.name,
        "full_name":    msg_desc.full_name,
        "fields":       fields,
        "oneofs":       oneofs,
        "nested_types": nested_types,
        "enums":        enums,
    }


def inspect_proto(msg: Any) -> dict:
    """
    Main entry point. Accepts:
      - A protobuf Message class  (e.g. MyMessage)
      - A protobuf Message instance (e.g. MyMessage())
    Returns a full inspection dict.
    """
    # Resolve to descriptor
    if isinstance(msg, type) and issubclass(msg, Message):
        descriptor = msg.DESCRIPTOR
    elif isinstance(msg, Message):
        descriptor = msg.DESCRIPTOR
    else:
        raise TypeError(f"Expected a protobuf Message class or instance, got {type(msg)}")

    return _inspect_message(descriptor)


# ── Pretty printer ─────────────────────────────────────────────────────────────

COLORS = {
    "reset":   "\033[0m",
    "bold":    "\033[1m",
    "blue":    "\033[94m",
    "cyan":    "\033[96m",
    "green":   "\033[92m",
    "yellow":  "\033[93m",
    "magenta": "\033[95m",
    "red":     "\033[91m",
    "gray":    "\033[90m",
}

def _c(text, color):
    return f"{COLORS.get(color,'')}{text}{COLORS['reset']}"


def _print_enum(enum: dict, indent: int):
    pad = "  " * indent
    print(f"{pad}{_c('enum', 'yellow')} {_c(enum['name'], 'bold')}  "
          f"{_c(enum['full_name'], 'gray')}")
    for v in enum["values"]:
        print(f"{pad}  {_c(v['name'], 'green')} = {_c(v['number'], 'cyan')}")


def _print_field(field: dict, indent: int):
    pad = "  " * indent
    parts = []

    # label
    label = field["label"]
    if label == "repeated":
        parts.append(_c("repeated", "magenta"))
    elif label == "required":
        parts.append(_c("required", "red"))

    # type
    if field["is_map"]:
        kv = f"map<{_c(field['map_key_type'], 'cyan')}, {_c(field['map_value_type'], 'cyan')}>"
        parts.append(kv)
    else:
        parts.append(_c(field["type"], "cyan"))

    # name + number
    parts.append(_c(field["name"], "bold"))
    parts.append(_c(f"= {field['number']}", "gray"))

    # oneof hint
    if field["is_oneof"]:
        parts.append(_c(f"[oneof: {field['oneof_name']}]", "yellow"))

    # default
    if field.get("default") not in (None, "", 0, False, []):
        parts.append(_c(f"(default: {field['default']})", "gray"))

    print(f"{pad}{'  '.join(parts)}")

    # enum values inline
    if "enum" in field:
        _print_enum(field["enum"], indent + 1)

    # nested message inline
    if "nested_message" in field:
        nm = field["nested_message"]
        if nm.get("note"):
            print(f"{'  '*(indent+1)}{_c('→ ' + nm['full_name'], 'gray')} {_c(nm['note'], 'red')}")
        else:
            _print_message(nm, indent + 1, is_nested_field=True)


def _print_message(msg: dict, indent: int = 0, is_nested_field: bool = False):
    pad = "  " * indent
    label = "nested message" if is_nested_field else "message"
    print(f"\n{pad}{_c(label, 'blue')} {_c(msg['name'], 'bold')}  "
          f"{_c(msg['full_name'], 'gray')}")
    print(f"{pad}{'─' * (50 - indent*2)}")

    # oneofs summary
    if msg["oneofs"]:
        for oo in msg["oneofs"]:
            fields_str = ", ".join(_c(f, "bold") for f in oo["fields"])
            print(f"{pad}  {_c('oneof', 'yellow')} {_c(oo['name'], 'bold')} "
                  f"{{ {fields_str} }}")
        print()

    # fields
    if msg["fields"]:
        for field in msg["fields"]:
            _print_field(field, indent + 1)
    else:
        print(f"{pad}  {_c('(no fields)', 'gray')}")

    # enums defined in this message
    if msg["enums"]:
        print()
        for enum in msg["enums"]:
            _print_enum(enum, indent + 1)

    # nested types
    if msg["nested_types"]:
        for nt in msg["nested_types"]:
            _print_message(nt, indent + 1)


def print_proto_tree(msg: Any):
    """Pretty-print the full proto tree to terminal."""
    result = inspect_proto(msg)
    print(_c("\n══ Proto Inspector ══════════════════════════════════", "bold"))
    _print_message(result)
    print(_c("\n══ Summary ══════════════════════════════════════════", "bold"))
    _summarize(result)


def _summarize(msg: dict, counts: dict = None, top: bool = True):
    if counts is None:
        counts = {"messages": 0, "fields": 0, "enums": 0, "maps": 0, "oneofs": 0}
    counts["messages"] += 1
    counts["fields"]   += len(msg["fields"])
    counts["enums"]    += len(msg["enums"])
    counts["oneofs"]   += len(msg["oneofs"])
    counts["maps"]     += sum(1 for f in msg["fields"] if f.get("is_map"))
    for nt in msg.get("nested_types", []):
        _summarize(nt, counts, top=False)
    if top:
        for k, v in counts.items():
            print(f"  {_c(k.capitalize(), 'cyan')}: {_c(v, 'bold')}")


def to_json(msg: Any, indent: int = 2) -> str:
    """Return inspection result as a JSON string."""
    return json.dumps(inspect_proto(msg), indent=indent, default=str)


# ── Demo ───────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    import gamesys.model_ddf_pb2
    print_proto_tree(gamesys.model_ddf_pb2.ModelDesc)