import time
from typing import Callable 

from ..manager import Manager


class TicksManager(Manager, init=False):
    ticks: int
    listeners: dict[int, dict[int, Callable]]
    unregister_set: set[int]
    next_listener_id: int

    def __init__(self) -> None:
        super().__init__()

        self.ticks = 0
        self.listeners = {}
        self.unregister_set = set()
        self.next_listener_id = 0

    def update(self) -> None:
        self.ticks += 1

        for ticks, listeners in list(self.listeners.items()):
            if self.ticks % ticks == 0:
                for listener in list(listeners.values()):
                    listener()

        for ticks, listeners in self.listeners.items():
            self.listeners[ticks] = {
                _listener_id: listener
                for _listener_id, listener in listeners.items()
                if _listener_id not in self.unregister_set
            }

        self.listeners = {
            ticks: listeners
            for ticks, listeners in self.listeners.items()
            if listeners
        }

        self.unregister_set = set()

    def register(self, ticks: int, listener: Callable) -> int:
        listener_id = self.next_listener_id
        self.next_listener_id += 1

        if ticks not in self.listeners:
            self.listeners[ticks] = {}

        self.listeners[ticks][listener_id] = listener

        return listener_id

    def unregister(self, listener_id: int) -> None:
        self.unregister_set.add(listener_id)
