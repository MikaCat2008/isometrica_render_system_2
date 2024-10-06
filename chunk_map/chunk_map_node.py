from __future__ import annotations

import math
from typing import Iterable, Optional, Generator, TYPE_CHECKING
from threading import Lock

import pygame as pg
from pygame.draw import rect as pg_draw_rect
from pygame.transform import flip
from pygame.surface import Surface

from textures_manager import TexturesManager

from kit import Node, DrawableNode

if TYPE_CHECKING:
    from .tile import ChunkTile
    from .chunk import Chunk
    from .entity_node import ChunkEntityNode


class ChunkMapNode(DrawableNode):
    nodes: list[ChunkEntityNode]
    chunks: dict[tuple[int, int], Chunk]
    render_offset: tuple[int, int]

    _lock: Lock

    def __init__(self) -> None:
        super().__init__()

        self.chunks = {}
        self.set_size(self.scene.game.screen.get_size())
        self.render_offset = 0, 0

        self._lock = Lock()

    def set_size(self, size: tuple[int, int]) -> None:
        self.image = Surface(size, pg.SRCALPHA)

    def add_nodes(self, nodes: Iterable[Node]) -> None:
        with self._lock:
            super().add_nodes(nodes)

    def add_chunk(self, chunk: Chunk) -> None:
        with self._lock:            
            self.chunks[chunk.position] = chunk

            x, y = chunk.position

            top_chunk = self.chunks.get((x, y - 1))
            bottom_chunk = self.chunks.get((x, y + 1))
            left_chunk = self.chunks.get((x - 1, y))
            right_chunk = self.chunks.get((x + 1, y))

            if top_chunk:
                top_chunk.update_bottom()
            if bottom_chunk:
                bottom_chunk.update_top()
            if left_chunk:
                left_chunk.update_right()
            if right_chunk:
                right_chunk.update_left()

    def remove_chunk(self, chunk: Chunk) -> None:
        cx, cy = position = chunk.position
        cx, cy = cx * 128, cy * 128

        for tile in chunk.tiles:
            for node in tile.nodes:
                node.remove_tile(tile)

        for node in self.nodes:
            x, y = node.position

            if cx <= x < cx + 128 and cy <= y < cy + 128:
                node.destroy()

        with self._lock:
            top_chunk = self.chunks.get((cx, cy - 1))
            bottom_chunk = self.chunks.get((cx, cy + 1))
            left_chunk = self.chunks.get((cx - 1, cy))
            right_chunk = self.chunks.get((cx + 1, cy))

            if top_chunk:
                top_chunk.update_bottom()
            if bottom_chunk:
                bottom_chunk.update_top()
            if left_chunk:
                left_chunk.update_right()
            if right_chunk:
                right_chunk.update_left()

            if position in self.chunks:
                del self.chunks[position]

    def get_tile(self, position: tuple[int, int]) -> Optional[ChunkTile]:
        x, y = position
        
        cx, tx = divmod(x, 8)
        cy, ty = divmod(y, 8)

        chunk = self.chunks.get((cx, cy))

        if chunk is not None:
            return chunk.tiles[tx + ty * 8]

    def get_covered_tiles(self, size: tuple[int, int], position: tuple[int, int]) -> Iterable[tuple[int, int]]:
        w, h = size
        x, y = position

        min_x = x // 16
        min_y = y // 16

        max_x = math.ceil((x + w) / 16)
        max_y = math.ceil((y + h) / 16)

        return (
            (tx, ty)
            for tx in range(min_x, max_x)
            for ty in range(min_y, max_y)
        )
    
    def get_render_nodes(self) -> Iterable[ChunkEntityNode]:
        return (
            node
            for node in self.nodes
            if node.is_require_render or node.is_require_last_render
        )
    
    def get_render_tiles(self) -> Iterable[ChunkTile]:
        return (
            tile
            for chunk in self.chunks.values()
            for tile in chunk.tiles
            if tile.is_require_render
        )

    def get_nodes(self) -> Generator[Node, None, None]:
        yield self

    def update(self) -> bool:
        cached_tiles: dict[tuple[int, int], ChunkTile] = {}

        with self._lock:
            self.nodes = [
                node
                for node in self.nodes
                if node.update() or node.is_require_last_render
            ]

            for i, node in enumerate(self.get_render_nodes()):
                if i == 64:
                    break

                tiles = node.tiles
                cached_tiles |= tiles
                tiles_set = set(tiles.keys())
                
                if node.is_alive:                    
                    covered_tiles = self.get_covered_tiles(
                        node.image.get_size(), node.render_position
                    )
                else:
                    node.is_require_last_render = False
                    covered_tiles = []

                covered_tiles_set = set(covered_tiles)

                for position in tiles_set | covered_tiles_set:
                    tile = cached_tiles.get(position)
                    
                    if tile is None:
                        tile = self.get_tile(position)

                        if tile is None:
                            continue

                        cached_tiles[position] = tile

                    if position in tiles_set and position in covered_tiles_set:
                        continue
                    elif position in tiles_set:
                        tile.remove_node(node)
                        node.remove_tile(tile)
                    else:
                        tile.add_node(node)
                        node.add_tile(tile)

                if node.tiles:
                    node.is_require_render = False

        for tile in cached_tiles.values():
            nodes_layer = tile.chunk.nodes_layer
            rtx, rty = tile.render_position

            pg_draw_rect(nodes_layer, (0, 0, 0, 0), (rtx % 128, rty % 128, 16, 16))

            nodes_layer.blits((
                (
                    flip(node.image, node.flip_x, node.flip_y), 
                    (rtx % 128, rty % 128), 
                    (
                        rtx - node.render_position[0],
                        rty - node.render_position[1],
                        16, 16
                    )
                )
                for node in sorted(
                    tile.nodes, 
                    key=lambda node: node.position[1]
                )
            ), 0)

        textures_manager = TexturesManager.get_instance()

        for i, tile in enumerate(self.get_render_tiles()):
            if i == 64:
                break

            rtx, rty = tile.render_position
            tile.chunk.background_layer.blit(
                textures_manager.get_texture(tile.texture_name),
                (rtx % 128, rty % 128)
            )
            tile.is_require_render = False

        ox, oy = self.render_offset

        self.image.fill((0, 0, 0))

        with self._lock:
            self.image.fblits(
                (chunk.background_layer, (ox + cx * 128, oy + cy * 128))
                for (cx, cy), chunk in self.chunks.items()
            )
            self.image.fblits(
                (chunk.nodes_layer, (ox + cx * 128, oy + cy * 128))
                for (cx, cy), chunk in self.chunks.items()
            )

        return self.is_alive

    def __getstate__(self) -> dict:
        state = super().__getstate__()

        state["nodes"] = []

        return state
