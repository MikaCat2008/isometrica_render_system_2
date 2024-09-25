import time

from pygame.time import Clock
from pygame.event import get as get_events
from pygame.surface import Surface
from pygame.display import flip, set_mode

from ..manager import Manager
from ..game_config import GameConfig

from .ticks_manager import TicksManager
from .events_manager import EventsManager
from .scenes_manager import ScenesManager


class GameManager(Manager, init=False):
    fps: float
    clock: Clock
    ticks: TicksManager
    events: EventsManager
    scenes: ScenesManager

    screen: Surface

    _draw_interval: float
    _update_interval: float

    def __init__(self, config: GameConfig) -> None:
        super().__init__()

        self.fps = 0
        self.clock = Clock()
        self.ticks = TicksManager()
        self.events = EventsManager()
        self.scenes = ScenesManager()

        self.screen = set_mode(
            size=config.screen_size, 
            flags=config.flags
        )

        self._draw_interval = 1 / 2400
        self._update_interval = 1 / 60

    def update(self) -> None:
        self.ticks.update()

    def draw(self) -> None:
        flip()

    def run(self) -> None:
        last_draw_time = 0
        last_update_time = 0

        while 1:
            current_time = time.time()

            for event in get_events():
                self.events.broadcast(event)

            if current_time - last_update_time > self._update_interval:
                self.update()

                last_update_time = current_time

            if current_time - last_draw_time > self._draw_interval:
                self.draw()

                last_draw_time = current_time

            self.fps = self.clock.get_fps()
            self.clock.tick(2400)
