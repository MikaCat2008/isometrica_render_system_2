from .serialization import serialize_field, Serializable


class GameConfig(Serializable):
    flags: int = serialize_field(int, lambda: 0)
    screen_size: tuple[int, int] = serialize_field(tuple[int, int], lambda: (0, 0))
