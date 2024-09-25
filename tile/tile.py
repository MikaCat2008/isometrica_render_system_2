from __future__ import annotations

from typing import TYPE_CHECKING

from pygame.surface import Surface

from textures_manager import TexturesManager

if TYPE_CHECKING:
    from .tile_chunk import TileChunk
    from .tile_entity_sprite_node import TileEntitySpriteNode


class Tile:
    image: Surface
    chunk: TileChunk
    nodes: dict[tuple[int, int], list[TileEntitySpriteNode]]
    position: tuple[int, int]
    background_texture_name: str

    is_changed: bool
    is_render_required: bool

    def __init__(
        self, 
        chunk: TileChunk, 
        position: tuple[int, int], 
        background_texture_name: str
    ) -> None:
        self.image = Surface((1, 1))
        self.chunk = chunk
        self.nodes = {}
        self.position = position
        self.background_texture_name = background_texture_name

        self.is_alive = True
        self.is_changed = True
        self.is_render_required = True

    def add_node(self, node: TileEntitySpriteNode) -> None:
        position = self.get_inner_position(node.render_position)
        nodes = self.nodes.get(position)

        if nodes is None:
            self.nodes[position] = [node]
        else:
            nodes.append(node)

        self.is_changed = True
        self.is_render_required = True
        self.chunk.is_render_required = True

    def remove_node(self, node: TileEntitySpriteNode) -> None:
        position = self.get_inner_position(node.render_position)
        nodes = self.nodes[position]

        if len(nodes) == 1:
            del self.nodes[position]
        else:
            nodes.remove(node)
        
        self.is_changed = True
        self.is_render_required = True
        self.chunk.is_render_required = True

    def get_inner_position(self, position: tuple[int, int]) -> tuple[int, int]:
        x, y = position
        tx, ty = self.position
        cx, cy = self.chunk.position

        return x - tx * 16 - cx * 128, y - ty * 16 - cy * 128

    def get_is_changed(self) -> bool:
        if self.is_changed:
            self.is_changed = False
            
            return True
        
        return False

    def render(self) -> None:
        textures = TexturesManager.get_instance()

        self.image = textures.get_texture(self.background_texture_name).copy()
        self.image.fblits(
            ( node.image, position )
            for node, position in sorted((
                (node, position)
                for position, nodes in self.nodes.items()
                for node in nodes
            ), key=lambda pair: pair[0].position[1])
        )

    def update(self) -> bool:
        if self.is_render_required:
            self.render()

            self.is_render_required = False

        return self.is_alive
