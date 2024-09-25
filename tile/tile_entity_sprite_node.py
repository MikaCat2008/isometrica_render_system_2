from nodes import SpriteNode

from .tile_entity_node import TileEntityNode


class TileEntitySpriteNode(SpriteNode, TileEntityNode):
    @property
    def texture_name(self) -> str:
        return super().texture_name

    @texture_name.setter
    def texture_name(self, texture_name: str) -> None:
        if self.texture_name == texture_name:
            return

        self.remove_tiles()

        super(TileEntitySpriteNode, TileEntitySpriteNode).texture_name.__set__(self, texture_name)
        
        self.add_tiles()
