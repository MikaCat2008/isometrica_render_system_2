from __future__ import annotations

from typing import Any, Type, ClassVar, Callable
from threading import Thread

from pydantic import BaseModel


class Model(BaseModel):
    _models: ClassVar[dict[str, Type[Model]]] = {}

    def __init_subclass__(cls, **kwargs: Any) -> None:
        super().__init_subclass__(**kwargs)

        Model._models[cls.__name__] = cls

    @classmethod
    def parse(cls, data: dict) -> Model:
        model_type: str = data["type"]
        model_dict: dict = data["data"]

        return cls._models[model_type](**model_dict)


class Method(Model):
    return_type: ClassVar[Any] = None


class Update(Model):
    ...


class Runnable:
    def _run(self) -> None:
        ...

    def run(self) -> None:
        self._thread = Thread(target=self._run)
        self._thread.start()


class Sender(Runnable):
    ...


class Dispatcher(Runnable):
    sender: Sender
    handlers: dict[Type[Model], Callable]
    
    def __init__(self, sender: Sender) -> None:
        self.sender = sender
        self.handlers = {}

    def process(self, model: Model) -> Any:
        handler = self.handlers.get(type(model))

        if handler:
            return handler(model)

    def register(self, model: Type[Model], handler: Callable) -> None:
        self.handlers[model] = handler
