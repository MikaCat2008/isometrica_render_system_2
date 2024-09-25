from __future__ import annotations

from typing import TypeVar, Optional, Generator, TYPE_CHECKING

from .manager import Manager
from .serialization import serialize_field, Serializable

if TYPE_CHECKING:
    from .scene import Scene
    from .component import Component
    from .game_managers.scenes_manager import ScenesManager

NodeT = TypeVar("NodeT", bound="Node")


class Node(Serializable):
    _nodes: list[Node] = serialize_field(list, lambda: [], "nodes")
    _components: list[Component] = serialize_field(list, lambda: [], "components")

    scene: Scene
    parent: Optional[Node] = None
    is_alive: bool = True

    def __init__(self) -> None:
        super().__init__()

        scenes_manager: ScenesManager = Manager.get_instance_by_name("ScenesManager")

        self.scene = scenes_manager.current_scene

    def add_nodes(self, *nodes: Node) -> None:
        self.nodes.extend(
            node.update_fields(
                scene=self.scene, 
                parent=self
            ) 
            for node in nodes
        )

    def remove_node(self, node: Node) -> None:
        node.parent = None
        self.nodes.remove(node)

    def get_nodes(self) -> Generator[Node]:
        yield self
        
        for node in self.nodes:
            yield from node.get_nodes()

    def update(self) -> bool:
        self.nodes = [
            node
            for node in self.nodes
            if node.update()
        ]

        return self.is_alive

    @property
    def nodes(self) -> list[Node]:
        return self._nodes
    
    @nodes.setter
    def nodes(self, nodes: list[Node]) -> None:
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
    def components(self, components: list[Component]) -> None:
        self._components = [
            component.update_fields(
                node=self
            )
            for component in components
        ]
