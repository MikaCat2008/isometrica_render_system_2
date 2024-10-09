from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .chunk import Chunk
    from .entity_node import ChunkEntityNode


class ChunkTile:
    chunk: Chunk
    nodes: list[ChunkEntityNode]
    position: tuple[int, int]
    texture_name: str
    render_position: tuple[int, int]
    is_require_render: bool

    def __init__(self, chunk: Chunk, position: tuple[int, int]) -> None:
        x, y = position
        
        self.chunk = chunk
        self.nodes = []
        self.position = position
        self.texture_name = "grass-tile"
        self.render_position = x * 16, y * 16
        self.is_require_render = True

    def add_node(self, node: ChunkEntityNode) -> None:
        self.nodes.append(node)

    def remove_node(self, node: ChunkEntityNode) -> None:
        self.nodes.remove(node)

    def update_nodes(self) -> None:
        for node in self.nodes:
            node.is_require_render = True
