from pickle import dumps, loads
from typing import Any, Type, TypeVar, ClassVar

from .field import SerializeField

SerializableT = TypeVar("SerializableT", bound="Serializable")


class Serializable:
    serialize_fields: ClassVar[dict[str, SerializeField]] = {}

    _pre_initialized: bool = False

    def __init_subclass__(cls) -> None:
        cls.serialize_fields = cls.serialize_fields | {
            field_name: field
            for field_name, field in cls.__dict__.items()
            if isinstance(field, SerializeField)
        }

    def __pre_init__(self) -> None:
        cls = self.__class__
        self._pre_initialized = True

        for field_name in cls.serialize_fields.keys():
            setattr(self, field_name, None)

    def __init__(self) -> None:
        cls = self.__class__

        if not self._pre_initialized:
            self.__pre_init__()

        for field_name, field in cls.serialize_fields.items():
            if field.default and self.__dict__.get(field_name) is None:
                setattr(self, field_name if field.alias_name is None else field.alias_name, field.default())

    def serialize(self) -> bytes:
        return dumps(self)

    def update_fields(self: SerializableT, **fields: Any) -> SerializableT:
        for field, value in fields.items():
            setattr(self, field, value)
        
        return self

    def __getstate__(self) -> dict:
        cls = self.__class__

        return {
            (field_name if field.alias_name is None else field.alias_name): self.__dict__[field_name]
            for field_name, field in cls.serialize_fields.items()
        }
    
    def __setstate__(self, state: dict) -> None:
        cls = self.__class__

        self.__pre_init__()

        for field_name, field in cls.serialize_fields.items():
            field_name = field_name if field.alias_name is None else field.alias_name
            
            setattr(self, field_name, state[field_name])

        self.__init__()

    @classmethod
    def deserialize(cls: Type[SerializableT], serialized_data: bytes) -> SerializableT:
        serializable = loads(serialized_data)

        return serializable
