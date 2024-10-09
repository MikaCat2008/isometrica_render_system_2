from __future__ import annotations

import time
from typing import Optional, TYPE_CHECKING
from collections import deque

from ..manager import Manager
from ..serialization import serialize_field, Serializable

from .node import Node
from .drawable_node import DrawableNode

if TYPE_CHECKING:
    from ..game_managers.game_manager import GameManager


class Scene(Serializable):
    root_node: DrawableNode = serialize_field(Node, lambda: DrawableNode())

    game: GameManager
    destroy_deque: deque[tuple[Node, float]]

    def __init__(self) -> None:
        super().__init__()

        self.game = Manager.get_instance_by_name("GameManager")
        self.game.ticks.register(1, self.update)
        self.destroy_deque = deque()

    def get_node_by_tag(self, tag: str) -> Optional[Node]:
        return self.root_node.get_node_by_tag(tag)

    def update(self) -> None:
        current_timestamp = time.time()

        for node, timestamp in self.destroy_deque:
            if timestamp <= current_timestamp:
                node.destroy()

        self.root_node.update()

    def destroy(self, node: Node, timeout: float) -> None:
        self.destroy_deque.append((node, time.time() + timeout))

    def draw(self) -> None:
        self.game.screen.fill((0, 0, 0))
        self.game.screen.fblits(
            (node.image, node.position)
            for node in self.root_node.get_render_nodes()
        )
