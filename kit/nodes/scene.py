from __future__ import annotations

from typing import Optional, TYPE_CHECKING

from ..manager import Manager
from ..serialization import serialize_field, Serializable

from .node import Node
from .drawable_node import DrawableNode

if TYPE_CHECKING:
    from ..game_managers.game_manager import GameManager


class Scene(Serializable):
    root_node: Node = serialize_field(Node, lambda: Node())

    game: GameManager

    def __init__(self) -> None:
        super().__init__()

        self.game = Manager.get_instance_by_name("GameManager")
        self.game.ticks.register(1, self.update)

    def get_node_by_tag(self, tag: str) -> Optional[Node]:
        return self.root_node.get_node_by_tag(tag)

    def update(self) -> None:
        self.root_node.update()

    def draw(self) -> None:
        self.game.screen.fill((0, 0, 0))
        self.game.screen.fblits(
            (node.image, node.position)
            for node in self.root_node.get_nodes()
            if isinstance(node, DrawableNode)
        )

