from typing import Optional

from kit import Node, GameManager
from tile_map import Sprite, TileMapNode


class EntityNode(Node):
    sprite: Sprite
    tile_map: Optional[TileMapNode]
    _find_tile_map_id: int

    def __init__(self) -> None:
        super().__init__()

        game = GameManager.get_instance()
        self._find_tile_map_id = game.ticks.register(1, self._find_tile_map)

        self.tile_map = None

    def _find_tile_map(self) -> None:
        self.tile_map = self.scene.root_node.get_node_by_tag("TileMap")

        if self.tile_map is None:
            return
        
        game = GameManager.get_instance()
        game.ticks.unregister(self._find_tile_map_id)
        
        self.tile_map.add_sprites([self.sprite])

    def destroy(self) -> None:
        self.is_alive = False
        self.sprite.is_alive = False
