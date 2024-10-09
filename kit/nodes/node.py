from __future__ import annotations

import time
from typing import TypeVar, Optional, Iterable, TYPE_CHECKING

from ..manager import Manager
from ..serialization import serialize_field, Serializable

if TYPE_CHECKING:
    from .scene import Scene
    from .component import Component
    from ..game_managers.scenes_manager import ScenesManager

NodeT = TypeVar("NodeT", bound="Node")


class Node(Serializable):
    tag: str = serialize_field(str, lambda: "Node")
    _nodes: list[Node] = serialize_field(list, lambda: [], "nodes")
    _components: list[Component] = serialize_field(list, lambda: [], "components")

    scene: Optional[Scene]
    parent: Optional[Node]
    is_alive: bool

    def __pre_init__(self) -> None:
        super().__pre_init__()

        self.scene = None
        self.parent = None
        self.is_alive = True

    def __init__(self) -> None:
        super().__init__()

        scenes_manager: ScenesManager = Manager.get_instance_by_name("ScenesManager")

        self.scene = scenes_manager.current_scene

    def add_nodes(self, nodes: Iterable[Node]) -> None:
        self.nodes.extend(
            node.update_fields(
                scene=self.scene, 
                parent=self
            ) 
            for node in nodes
        )

    def get_node_by_tag(self, tag: str) -> Optional[Node]:
        for node in self.nodes:
            if node.tag == tag:
                return node

            if subnode := node.get_node_by_tag(tag):
                return subnode

        return None

    def update(self) -> bool:
        if self.nodes:
            self.nodes = [
                node
                for node in self.nodes
                if node.update()
            ]

        return self.is_alive
    
    def destroy(self) -> None:
        self.is_alive = False

    @property
    def nodes(self) -> list[Node]:
        return self._nodes
    
    @nodes.setter
    def nodes(self, nodes: Iterable[Node]) -> None:
        self._nodes = [
            node.update_fields(
                scene=self.scene,
                parent=self
            )
            for node in nodes
        ]

    @property
    def components(self) -> list[Component]:
        return self._components
    
    @components.setter
    def components(self, components: Iterable[Component]) -> None:
        self._components = [
            component.update_fields(
                node=self
            )
            for component in components
        ]
