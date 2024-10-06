from __future__ import annotations

from typing import TYPE_CHECKING

from kit import DrawableNode

if TYPE_CHECKING:
    from .tile import ChunkTile
    from .chunk_map_node import ChunkMapNode


class ChunkEntityNode(DrawableNode):
    parent: ChunkMapNode

    tiles: dict[tuple[int, int], ChunkTile]
    is_require_render: bool
    is_require_last_render: bool

    def __init__(self) -> None:
        super().__init__()

        self.tiles = {}
        self.is_require_render = True
        self.is_require_last_render = False

    def add_tile(self, tile: ChunkTile) -> None:
        self.tiles[tile.position] = tile

    def remove_tile(self, tile: ChunkTile) -> None:
        del self.tiles[tile.position]

    def destroy(self) -> None:
        super().destroy()

        self.parent = None
        self.is_require_last_render = True

    @property
    def position(self) -> tuple[int, int]:
        return super().position

    @position.setter
    def position(self, position: tuple[int, int]) -> None:
        _super = super(ChunkEntityNode, ChunkEntityNode)
        _super.position.__set__(self, position)

        self.is_require_render = True
