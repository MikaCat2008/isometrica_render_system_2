from typing import Any, Type, TypeVar, Generic, Callable
from threading import Event

from pydantic import TypeAdapter

T = TypeVar("T")


class Answer(Generic[T]):
    event: Event
    result: Any
    adapter: TypeAdapter
    answer_id: int
    listeners: list[Callable]
    result_type: Type
    
    def __init__(self, answer_id: int, result_type: Type) -> None:
        super().__init__()
        
        self.event = Event()
        self.result = None
        self.adapter = TypeAdapter(result_type)
        self.answer_id = answer_id
        self.listeners = []
        self.result_type = result_type
    
    def set(self, result: Any) -> None:
        self.result = self.adapter.validate_python(result)
        self.event.set()

        for listener in self.listeners:
            listener(self.result)
    
    def wait(self) -> T:
        if self.result_type is None:
            return None

        self.event.wait()
        
        return self.result

    def on_result(self, listener: Callable) -> None:
        self.listeners.append(listener)
