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
    ups: float
    fps: float
    ups_clock: Clock
    fps_clock: Clock

    ticks: TicksManager
    events: EventsManager
    scenes: ScenesManager

    screen: Surface

    max_ups: int
    max_fps: int

    _ups_interval: float
    _fps_interval: float

    def __init__(self, config: GameConfig) -> None:
        super().__init__()

        self.ups = 0
        self.fps = 0
        self.ups_clock = Clock()
        self.fps_clock = Clock()

        self.ticks = TicksManager()
        self.events = EventsManager()
        self.scenes = ScenesManager()

        self.screen = set_mode(
            size=config.screen_size, 
            flags=config.flags
        )

        self.max_ups = 60
        self.max_fps = 2400

        self._ups_interval = 1 / self.max_ups

    def update(self) -> None:
        self.ticks.update()

    def draw(self) -> None:
        flip()

    def run(self) -> None:
        last_ups_time = 0

        while 1:
            current_time = time.time()

            for event in get_events():
                self.events.broadcast(event)

            if current_time - last_ups_time >= self._ups_interval:
                self.update()

                last_ups_time = current_time

                self.ups = self.ups_clock.get_fps()
                self.ups_clock.tick(self.max_ups)

            self.draw()

            self.fps = self.fps_clock.get_fps()
            self.fps_clock.tick(self.max_fps)
