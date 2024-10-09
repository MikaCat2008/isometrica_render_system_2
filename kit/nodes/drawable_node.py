from __future__ import annotations

from typing import Generator

from pygame.surface import Surface

from .node import Node
from ..serialization import serialize_field


class DrawableNode(Node):
    position: tuple[int, int] = serialize_field(tuple[int, int], lambda: (0, 0))

    image: Surface

    def __pre_init__(self) -> None:
        super().__pre_init__()

        self.image = Surface((1, 1))

    def get_render_nodes(self) -> Generator[DrawableNode, None, None]:
        for node in self.nodes:
            if isinstance(node, DrawableNode):
                yield from node.get_render_nodes()
        
        yield self
