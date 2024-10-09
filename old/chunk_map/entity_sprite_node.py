from __future__ import annotations

from nodes import SpriteNode

from .entity_node import ChunkEntityNode


class ChunkEntitySpriteNode(SpriteNode, ChunkEntityNode):
    @property
    def texture_name(self) -> str:
        return super().texture_name

    @texture_name.setter
    def texture_name(self, texture_name: str) -> None:
        _super = super(ChunkEntitySpriteNode, ChunkEntitySpriteNode)
        _super.texture_name.__set__(self, texture_name)
        
        self.is_require_render = True
