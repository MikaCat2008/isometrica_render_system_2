from .serialization import Serializable, serialize_field


class Animation(Serializable):
    frames: list[str] = serialize_field(list[str], lambda: [])
