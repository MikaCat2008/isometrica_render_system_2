from __future__ import annotations

from pygame.surface import Surface

from .node import Node
from ..serialization import serialize_field


class DrawableNode(Node):
    _position: tuple[int, int] = serialize_field(tuple[int, int], lambda: (0, 0), "position")

    image: Surface
    render_position: tuple[int, int]

    def __pre_init__(self) -> None:
        super().__pre_init__()

        self.image = Surface((1, 1))    
        
    def update_position(self) -> None:
        x, y = self.position
        w, h = self.image.get_size()

        self.render_position = int(x - w / 2), int(y - h)

    @property
    def position(self) -> tuple[int, int]:
        return self._position

    @position.setter
    def position(self, position: tuple[int, int]) -> None:
        self._position = position

        self.update_position()
