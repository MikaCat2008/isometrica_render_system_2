from kit import Component, GameManager
from nodes import TextNode


class TileMapStatisticComponent(Component):
    node: TextNode
    _find_tile_map_id: int
    
    def __init__(self):
        super().__init__()

        self.game = GameManager.get_instance()
        self._find_tile_map_id = self.game.ticks.register(10, self._find_tile_map)
    
    def _find_tile_map(self) -> None:
        self.tile_map = self.node.scene.root_node.get_node_by_tag("TileMap")

        if self.tile_map is None:
            return
        
        self.game.ticks.unregister(self._find_tile_map_id)
        self.game.ticks.register(5, self.update_data)


class TileMapTilesComponent(TileMapStatisticComponent):
    def update_data(self) -> None:
        self.node.text = f"{len(self.tile_map.tile_map.tiles)} tiles"
        self.node.position = self.game.screen.get_width() - self.node.image.get_width(), 0


class TileMapChunksComponent(TileMapStatisticComponent):
    def update_data(self) -> None:
        self.node.text = f"{len(self.tile_map.tile_map.chunks)} chunks"
        self.node.position = self.game.screen.get_width() - self.node.image.get_width(), 14


class TileMapSpritesComponent(TileMapStatisticComponent):
    def update_data(self) -> None:
        self.node.text = f"{len(self.tile_map.sprites)} sprites"
        self.node.position = self.game.screen.get_width() - self.node.image.get_width(), 28
