from __future__ import annotations

from nodes import AnimatedSpriteNode

from .entity_sprite_node import ChunkEntitySpriteNode


class ChunkEntityAnimatedSpriteNode(AnimatedSpriteNode, ChunkEntitySpriteNode):
    ...