from typing import Callable 

from ..manager import Manager


class TicksManager(Manager, init=False):
    ticks: int
    listeners: list[tuple[int, Callable]]

    def __init__(self) -> None:
        super().__init__()

        self.ticks = 0
        self.listeners = []

    def update(self) -> None:
        self.ticks += 1

        for ticks, listener in self.listeners:
            if self.ticks % ticks == 0:
                listener()

    def register(self, ticks: int, listener: Callable) -> None:
        self.listeners.append((ticks, listener))

    def unregister(self, listener: Callable) -> None:
        self.listeners = [
            pair
            for pair in self.listeners
            if pair[1] != listener
        ]
