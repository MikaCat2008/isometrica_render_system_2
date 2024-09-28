import math
from typing import Optional

from kit import DrawableNode

import pygame as pg
from pygame.surface import Surface

from .tile import Tile
from .tile_chunk import TileChunk


class TileMapNode(DrawableNode):
    image: Surface
    tile_chunks: dict[tuple[int, int], TileChunk]
    inner_position: tuple[int, int]

    def __init__(self) -> None:
        super().__init__()

        self.image = Surface((512, 288), pg.SRCALPHA)
        self.tile_chunks = {}
        self.inner_position = 0, 0

    def create_chunk(self, position: tuple[int, int]) -> TileChunk:
        chunk = TileChunk(position)

        self.tile_chunks[position] = chunk

        return chunk

    def get_tile(self, position: tuple[int, int]) -> Optional[Tile]:
        x, y = position

        cx, incx = divmod(x, 8)
        cy, incy = divmod(y, 8)

        chunk = self.tile_chunks.get((cx, cy))

        if chunk is None:
            return None

        return chunk.get_tile((incx, incy))

    def get_render_tiles(self, position: tuple[int, int], size: tuple[int, int]) -> list[Tile]:
        w, h = size
        min_x, min_y = position

        max_x, max_y = min_x + w, min_y + h
        min_x, min_y = min_x // 16, min_y // 16
        max_x, max_y = math.ceil(max_x / 16), math.ceil(max_y / 16)

        return list(filter(bool, (
            self.get_tile((x, y))
            for x in range(min_x, max_x)
            for y in range(min_y, max_y)
        )))

    def update(self) -> bool:
        self.chunks = {
            position: chunk
            for position, chunk in self.tile_chunks.items()
            if chunk.update()
        }

        ix, iy = self.inner_position

        self.image.fill((0, 0, 0))
        self.image.fblits(
            (chunk.image, (ix + cx * 128, iy + cy * 128))
            for (cx, cy), chunk in self.tile_chunks.items()
        )

        return self.is_alive