from kit import DrawableNode

from .tile import Tile
from .tile_map_node import TileMapNode


class TileEntityNode(DrawableNode):
    tiles: list[Tile]
    tile_map: TileMapNode

    def __init__(self, tile_map: TileMapNode) -> None:
        self.tiles = []
        self.tile_map = tile_map

        super().__init__()

    def remove_tiles(self) -> None:
        for tile in self.tiles:
            tile.remove_node(self)

    def add_tiles(self) -> None:
        self.tiles = self.tile_map.get_render_tiles(
            self.render_position, self.image.get_size()
        )

        for tile in self.tiles:
            tile.add_node(self)

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
