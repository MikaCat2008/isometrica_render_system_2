from typing import Optional

from kit import DrawableNode

from .tile import Tile
from .tile_map_node import TileMapNode


class TileEntityNode(DrawableNode):
    tiles: list[Tile]
    _tile_map: Optional[TileMapNode] = None

    def __init__(self) -> None:
        super().__init__()

        self.tiles = []
        self.tile_map = None

    def remove_tiles(self) -> None:
        if self.tile_map is None:
            return

        for tile in self.tiles:
            tile.remove_node(self)

    def add_tiles(self) -> None:
        if self.tile_map is None:
            return

        self.tiles = self.tile_map.get_render_tiles(
            self.render_position, self.image.get_size()
        )

        for tile in self.tiles:
            tile.add_node(self)

    @property
    def tile_map(self) -> Optional[TileMapNode]:
        return self._tile_map
    
    @tile_map.setter
    def tile_map(self, tile_map: TileMapNode) -> None:
        self.remove_tiles()

        self._tile_map = tile_map
        
        self.add_tiles()

    @property
    def position(self) -> tuple[int, int]:
        return super().position
    
    @position.setter
    def position(self, position: tuple[int, int]) -> None:
        if self.position == position:
            return
        
        self.remove_tiles()

        super(TileEntityNode, TileEntityNode).position.__set__(self, position)

        self.add_tiles()
