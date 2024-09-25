from typing import Callable
from collections import defaultdict

from pygame.event import Event

from ..manager import Manager


class EventsManager(Manager, init=False):
    listeners: defaultdict[int, list[Callable]]

    def __init__(self) -> None:
        super().__init__()

        self.listeners = defaultdict(list)

    def broadcast(self, event: Event) -> None:
        for listener in self.listeners[event.type]:
            listener(event)

    def register(self, event: int, listener: Callable) -> None:
        self.listeners[event].append(listener)
