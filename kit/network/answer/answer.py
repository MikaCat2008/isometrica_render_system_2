from typing import Any, Type, Self, TypeVar, Generic, Callable, Optional
from threading import Event

from pydantic import TypeAdapter

from .exception import NetworkException

T = TypeVar("T")


class Answer(Generic[T]):
    result: Any
    exception: Optional[NetworkException]

    event: Event
    adapter: TypeAdapter
    answer_id: int
    result_type: Type

    listeners: list[Callable]

    def __init__(self, answer_id: int, result_type: Type) -> None:
        super().__init__()
        
        self.result = None
        self.exception = None

        self.event = Event()
        self.adapter = TypeAdapter(result_type)
        self.answer_id = answer_id
        self.result_type = result_type

        self.listeners = []
    
    def set_result(self, result: Any) -> None:
        self.result = self.adapter.validate_python(result)
        self.event.set()

        for listener in self.listeners:
            listener(self.result)
    
    def set_exception(self, code: int) -> None:
        self.exception = NetworkException(code)
        self.event.set()

    def wait(self) -> T:
        if self.result_type is None:
            return None

        self.event.wait()

        if self.exception:
            raise self.exception

        if self.result:
            return self.result

    def on_result(self, listener: Callable) -> Self:
        self.listeners.append(listener)

        return self
