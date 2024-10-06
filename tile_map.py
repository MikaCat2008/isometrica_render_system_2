import pygame as pg
from pygame.surface import Surface

from kit import DrawableNode, serialize_field


class Tile:
    i: int
    image: Surface
    is_require_render: bool

    def __init__(self, i: int) -> None:
        self.i = i
        self.is_require_render = True


class TileMapNode(DrawableNode):
    _size: tuple[int, int] = serialize_field(tuple[int, int], lambda: (1, 1), "size")
    _tile_size: int = serialize_field(int, lambda: 32, "tile_size")

    tiles: list[Tile]

    def __init__(self) -> None:
        super().__init__()

        self.tiles = []

    def update(self) -> bool:
        self.image.fblits(
            (
                tile.image
            )
            for tile in self.tiles
            if tile.is_require_render
        )
        
        return super().update()

    def update_sizes(self) -> None:
        if self._size is None or self._tile_size is None:
            return

        w, h = self._size
        tile_size = self._tile_size

        self.image = Surface((w * tile_size, h * tile_size), pg.SRCALPHA)
        self.tiles = [
            Tile(i) for i in range(w * h)
        ]

    @property
    def size(self) -> tuple[int, int]:
        return self._size
    
    @size.setter
    def size(self, size: tuple[int, int]) -> None:
        self._size = size
        self.update_sizes()

    @property
    def tile_size(self) -> int:
        return self._tile_size

    @tile_size.setter
    def tile_size(self, tile_size: int) -> None:
        self._tile_size = tile_size
        self.update_sizes()
