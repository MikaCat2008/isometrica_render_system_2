import pygame as pg
from pygame.surface import Surface

from .tile import ChunkTile


class Chunk:
    nodes_layer: Surface
    background_layer: Surface

    tiles: list[ChunkTile]
    position: tuple[int, int]
    
    def __init__(self, position: tuple[int, int]) -> None:
        cx, cy = position
        
        self.nodes_layer = Surface((128, 128), pg.SRCALPHA)
        self.background_layer = Surface((128, 128), pg.SRCALPHA)
        
        self.tiles = [
            ChunkTile(self, (x + cx * 8, y + cy * 8)) 
            for y in range(8)
            for x in range(8)
        ]
        self.position = position

    def update_top(self) -> None:
        for tile in self.tiles[:8]:
            tile.update_nodes()

    def update_bottom(self) -> None:
        for tile in self.tiles[56:]:
            tile.update_nodes()

    def update_left(self) -> None:
        for tile in self.tiles[::8]:
            tile.update_nodes()

    def update_right(self) -> None:
        for tile in self.tiles[7::8]:
            tile.update_nodes()
