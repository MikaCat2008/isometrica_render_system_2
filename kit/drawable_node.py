from __future__ import annotations

from pygame.surface import Surface

from .node import Node
from .serialization import serialize_field



class DrawableNode(Node):
    image: Surface
    position: tuple[int, int] = serialize_field(tuple[int, int], lambda: (0, 0))

    def __init__(self) -> None:
        super().__init__()
        
        self.image = Surface((1, 1))

    def update(self) -> bool:
        super().update()

        return self.is_alive
