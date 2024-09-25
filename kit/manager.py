from __future__ import annotations

from typing import Type, TypeVar, ClassVar

ManagerT = TypeVar("ManagerT", bound="Manager")


class Manager:
    instance: Manager
    instances: ClassVar[dict[str, Manager]] = {}

    def __init_subclass__(cls, init: bool = True) -> None:
        if init:
            cls()

    def __init__(self) -> None:   
        for cls in self.__class__.__mro__:
            if cls is not Manager and Manager in cls.__mro__:
                cls.set_instance(self)


    @classmethod
    def set_instance(cls, instance: Manager) -> None:
        cls.instance = instance
        cls.instances[cls.__name__] = instance

    @classmethod
    def get_instance(cls: Type[ManagerT]) -> ManagerT:
        return cls.instance

    @classmethod
    def get_instance_by_name(cls, name: str) -> Manager:
        return cls.instances[name]
