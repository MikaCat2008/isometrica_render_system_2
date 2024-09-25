import pygame as pg
from pygame.surface import Surface

from .tile import Tile


class TileChunk:
    image: Surface
    tiles: list[Tile]
    position: tuple[int, int]

    is_alive: bool
    is_render_required: bool

    def __init__(self, position: tuple[int, int]) -> None:
        self.image = Surface((128, 128), pg.SRCALPHA)
        self.tiles = [
            Tile(self, (x, y), "grass-tile")
            for y in range(8)
            for x in range(8)
        ]
        self.position = position
        
        self.is_alive = True
        self.is_render_required = True

    def get_tile(self, position: tuple[int, int]) -> Tile:
        x, y = position

        return self.tiles[x + y * 8]

    def render(self) -> None:
        self.tiles = list(filter(Tile.update, self.tiles))
        self.image.fblits(
            ( tile.image, (i % 8 * 16, i // 8 * 16) )
            for i, tile in enumerate(self.tiles)
            if tile.get_is_changed()
        )

    def update(self) -> bool:
        if self.is_render_required:
            self.render()

            self.is_render_required = False

        return self.is_alive
