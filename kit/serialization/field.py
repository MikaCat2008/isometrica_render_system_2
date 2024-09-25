from typing import TypeVar, Callable, Optional

T = TypeVar("T")


class SerializeField:
    default: Optional[Callable]
    alias_name: Optional[str]

    def __init__(self, default: Optional[Callable] = None, alias_name: Optional[str] = None) -> None:
        self.default = default
        self.alias_name = alias_name


def serialize_field(t: T, default: Optional[Callable] = None, alias_name: Optional[str] = None) -> T:
    return SerializeField(default, alias_name)
