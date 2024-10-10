from __future__ import annotations

import time
from math import ceil
from typing import Union, Iterable, Generator, Optional
from threading import Lock
from collections import deque

import pygame as pg
from pygame.rect import Rect
from pygame.surface import Surface

from kit import DrawableNode
from textures_manager import TexturesManager


class Tile:
    is_new: bool
    sprites: deque[Sprite]
    position: tuple[int, int]
    requires_render: bool

    def __init__(self, position: tuple[int, int]) -> None:
        self.is_new = True
        self.sprites = deque()
        self.position = position
        self.requires_render = True

    def add_sprite(self, sprite: Sprite) -> None:
        sprite.tiles.append(self.position)
        self.sprites.append(sprite)

    def remove_sprite(self, sprite: Sprite) -> None:
        sprite.tiles.remove(self.position)
        self.sprites.remove(sprite)


class Sprite:
    size: tuple[int, int]
    image: Surface

    tiles: deque[tuple[int, int]]
    is_alive: bool
    render_position: tuple[int, int]

    requires_render: bool
    required_tiles_update: bool

    _required_image_update: bool
    _required_tiles_update: bool

    _flip_x: bool
    _flip_y: bool
    _position: tuple[int, int]
    _rotation: int
    _texture_name: str

    def __init__(
        self, 
        texture_name: str, 
        position: tuple[int, int] = (0, 0),
        rotation: float = 0.0,
        flip_x: bool = False,
        flip_y: bool = False,
    ) -> None:
        self.tiles = deque()
        self.is_alive = True

        self._required_image_update = True
        self._required_tiles_update = True

        self._flip_x = flip_x
        self._flip_y = flip_y
        self._position = position
        self._rotation = rotation
        self._texture_name = texture_name
        
        self.update()

    def update(self) -> bool:
        if self._required_image_update:
            textures = TexturesManager.get_instance()

            self.size, self.image = textures.get_texture(
                self._texture_name, self._rotation, self._flip_x, self._flip_y
            )
            
            self.requires_render = True
            self._required_image_update = False
        if self._required_tiles_update:
            x, y = self._position
            rw, rh = self.image.get_size()
        
            self.render_position = int(x - rw / 2), int(y - rh / 2 - self.size[1] / 2)

            self.requires_render = True
            self.required_tiles_update = True
            self._required_tiles_update = False

        return self.is_alive

    @property
    def position(self) -> tuple[int, int]:
        return self._position

    @position.setter
    def position(self, position: tuple[int, int]) -> None:
        if position == self._position:
            return

        self._position = position
        self._required_tiles_update = True

    @property
    def rotation(self) -> int:
        return self._rotation
    
    @rotation.setter
    def rotation(self, rotation: int) -> None:
        if rotation == self._rotation:
            return
        
        self._rotation = rotation
        self._required_image_update = True
        self._required_tiles_update = True

    @property
    def texture_name(self) -> str:
        return self._texture_name
    
    @texture_name.setter
    def texture_name(self, texture_name: str) -> None:
        if texture_name == self._texture_name:
            return

        self._texture_name = texture_name
        self._required_image_update = True
        self._required_tiles_update = True

    @property
    def flip_x(self) -> bool:
        return self._flip_x
    
    @flip_x.setter
    def flip_x(self, flip_x: bool) -> None:
        if flip_x == self._flip_x:
            return
        
        self._flip_x = flip_x
        self._required_image_update = True

    @property
    def flip_y(self) -> bool:
        return self._flip_y
    
    @flip_y.setter
    def flip_y(self, flip_y: bool) -> None:
        if flip_y == self._flip_y:
            return
        
        self._flip_y = flip_y
        self._required_image_update = True


class AnimatedSprite(Sprite):
    frame_i: int
    frame_rate: int
    frame_index: int

    animation: list[str]
    _animation_name: str

    def __init__(
        self, 
        animation_name: str,
        position: tuple[int, int] = (0, 0), 
        rotation: int = 0, 
        flip_x: bool = False, 
        flip_y: bool = False
    ):
        self.frame_i = 0
        self.frame_rate = 30
        self.frame_index = 0

        self._texture_name = ""
        self._animation_name = ""
        self.animation_name = animation_name

        super().__init__(self.animation[0], position, rotation, flip_x, flip_y)

    def update(self) -> bool:
        if self.frame_i % self.frame_rate == 0:
            self.frame_index = (self.frame_index + 1) % len(self.animation)
            self.texture_name = self.animation[self.frame_index]

        self.frame_i += 1

        return super().update()

    @property
    def animation_name(self) -> str:
        return self._animation_name

    @animation_name.setter
    def animation_name(self, animation_name: str) -> None:
        if self._animation_name == animation_name:
            return

        texture_manager = TexturesManager.get_instance()

        self.frame_i = 0
        self.animation = texture_manager.get_animation(animation_name)
        self._animation_name = animation_name


class TileMap:
    tiles: dict[tuple[int, int], Tile]
    tile_size: int
    
    def __init__(self, tile_size: int) -> None:
        self.tiles = {}
        self.tile_size = tile_size

    def create_tile(self, position: tuple[int, int]) -> Tile:
        return Tile(position)

    def get_covered_tiles(self, sprite: Sprite) -> set[tuple[int, int]]:
        w, h = sprite.image.get_size()
        x, y = sprite.render_position

        min_x = x // self.tile_size
        min_y = y // self.tile_size

        max_x = ceil((x + w) / self.tile_size)
        max_y = ceil((y + h) / self.tile_size)
        
        return {
            (tx, ty)
            for tx in range(min_x, max_x)
            for ty in range(min_y, max_y)
        }

    def add_sprites(self, sprites: Iterable[Sprite]) -> None:
        for sprite in sprites:
            covered_tiles = self.get_covered_tiles(sprite)

            self.tiles |= {
                position: self.create_tile(position)
                for position in covered_tiles
                if position not in self.tiles
            }

            for position in covered_tiles:
                tile = self.tiles[position]
                tile.add_sprite(sprite)

    def update_sprites(self, sprites: Iterable[Sprite]) -> None:
        for sprite in sprites:
            sprite.requires_render = False

            tiles = set(sprite.tiles)

            if sprite.required_tiles_update:
                covered_tiles = self.get_covered_tiles(sprite)
                sprite.required_tiles_update = False

                self.tiles |= {
                    position: self.create_tile(position)
                    for position in covered_tiles
                    if position not in self.tiles
                }

                for position in covered_tiles:
                    if position in tiles:
                        continue

                    tile = self.tiles[position]
                    tile.add_sprite(sprite)
                    tile.requires_render = True

            for position in tiles:
                tile = self.tiles[position]
                tile.requires_render = True

                if position in covered_tiles:
                    continue

                tile.remove_sprite(sprite)
                tile.requires_render = True

    def remove_sprites(self, sprites: Iterable[Sprite]) -> None:
        for sprite in sprites:
            for position in list(sprite.tiles):
                tile = self.tiles[position]
                tile.remove_sprite(sprite)
                tile.requires_render = True

    def update_tiles(self) -> None:
        self.tiles = {
            position: tile
            for position, tile in self.tiles.items()
            if tile.sprites
        }


class TSTileMap(TileMap):
    lock: Lock

    def __init__(self, tile_size: int) -> None:
        super().__init__(tile_size)

        self.lock = Lock()

    def add_sprites(self, sprites: Iterable[Sprite]) -> None:
        with self.lock:
            super().add_sprites(sprites)

    def update_sprites(self, sprites: Iterable[Sprite]) -> None:
        with self.lock:
            return super().update_sprites(sprites)

    def remove_sprites(self, sprites: Iterable[Sprite]) -> None:
        with self.lock:
            return super().remove_sprites(sprites)

    def update_tiles(self) -> None:
        with self.lock:
            super().update_tiles()


class Chunk:
    tiles: int
    image: Surface
    tile_map: ChunkedTileMap
    position: tuple[int, int]
    background: Surface
    render_position: tuple[int, int]

    def __init__(self, tile_map: ChunkedTileMap, position: tuple[int, int]) -> None:
        self.tiles = 1
        self.image = Surface((
            tile_map.chunk_size * tile_map.tile_size, 
            tile_map.chunk_size * tile_map.tile_size
        ))
        self.tile_map = tile_map
        self.position = position
        self.background = Surface((tile_map.tile_size, tile_map.tile_size))
        self.render_position = (
            position[0] * tile_map.tile_size * tile_map.chunk_size, 
            position[1] * tile_map.tile_size * tile_map.chunk_size
        )

    def draw_tiles(self, tiles: deque[ChunkedTile]) -> None:
        self.image.blits((
            render_data
            for tile in tiles
            for render_data in self.get_render_data(tile)
        ), 0)

    def get_render_data(
        self, tile: Tile
    ) -> Generator[
        Union[
            tuple[Surface, tuple[int, int]],
            tuple[Surface, tuple[int, int], tuple[int, int, int, int]]
        ],
        None, 
        None
    ]:
        x, y = tile.position
        arx, ary = x * self.tile_map.tile_size, y * self.tile_map.tile_size
        relative_render_position = (
            x % self.tile_map.chunk_size * self.tile_map.tile_size, 
            y % self.tile_map.chunk_size * self.tile_map.tile_size
        )

        yield self.background, relative_render_position

        for sprite in sorted(tile.sprites, key=lambda s: s.position[1]):
            yield (
                sprite.image,
                relative_render_position,
                (
                    arx - sprite.render_position[0],
                    ary - sprite.render_position[1],
                    self.tile_map.tile_size, self.tile_map.tile_size
                )
            )


class ChunkedTile(Tile):
    chunk: Optional[Chunk]

    def __init__(self, position: tuple[int, int], chunk: Optional[Chunk] = None) -> None:
        super().__init__(position)

        self.chunk = chunk

    def __del__(self) -> None:
        self.chunk.tiles -= 1


class ChunkedTileMap(TileMap):
    tiles: dict[tuple[int, int], ChunkedTile]
    chunks: dict[tuple[int, int], Chunk]
    chunk_size: int

    def __init__(self, tile_size: int = 16, chunk_size: int = 8):
        super().__init__(tile_size)

        self.chunks = {}
        self.chunk_size = chunk_size

    def create_tile(self, position: tuple[int, int]) -> ChunkedTile:
        chunk_position = position[0] // self.chunk_size, position[1] // self.chunk_size

        if (chunk := self.chunks.get(chunk_position)):
            chunk.tiles += 1
        else:
            chunk = self.create_chunk(chunk_position)

        return ChunkedTile(position, chunk)

    def create_chunk(self, position: tuple[int, int]) -> Chunk:
        chunk = Chunk(self, position)
        
        self.chunks[position] = chunk
        
        return chunk

    def update(self, size: tuple[int, int], offset: tuple[int, int]) -> None:
        self.update_tiles(size, offset)
        self.update_chunks()

    def update_tiles(self, size: tuple[int, int], offset: tuple[int, int]) -> None:
        update_chunks: dict[tuple[int, int], deque[ChunkedTile]] = {}

        rect = Rect(
            offset[0] - self.tile_size, 
            offset[1] - self.tile_size, 
            size[0] + self.tile_size * 2,
            size[1] + self.tile_size * 2
        )

        for (x, y), tile in self.tiles.items():
            if not tile.requires_render:
                continue

            if not rect.contains(x * 16, y * 16, self.tile_size, self.tile_size):
                continue

            tile.requires_render = False
            
            chunk_position = tile.chunk.position

            if (tiles := update_chunks.get(chunk_position)) is None:
                update_chunks[chunk_position] = tiles = deque()

            tiles.append(tile)

        for position, tiles in update_chunks.items():
            self.chunks[position].draw_tiles(tiles)

        super().update_tiles()

    def update_chunks(self) -> None:
        self.chunks = {
            position: chunk
            for position, chunk in self.chunks.items()
            if chunk.tiles
        }


class TSChunkedTileMap(ChunkedTileMap, TSTileMap):
    def update_chunks(self) -> None:
        with self.lock:
            super().update_chunks()


class TileMapNode(DrawableNode):
    _offset: tuple[int, int]
    sprites: deque[Sprite]
    tile_map: TSChunkedTileMap

    def __init__(self) -> None:
        super().__init__()

        self.image = Surface(self.scene.game.screen.get_size(), pg.SRCALPHA)
        self.offset = 0, 0
        self.sprites = deque()
        self.tile_map = TSChunkedTileMap()

    def add_sprites(self, sprites: Iterable[Sprite]) -> None:
        sprites = list(sprites)
        
        self.sprites.extend(sprites)
        self.tile_map.add_sprites(sprites)

    def update(self) -> bool:
        self.tile_map.remove_sprites(
            sprite
            for sprite in self.sprites
            if not sprite.update()
        )

        self.tile_map.update_sprites(
            sprite 
            for sprite in self.sprites
            if sprite.is_alive and sprite.requires_render
        )

        self.tile_map.update(self.scene.game.screen.get_size(), self.offset)

        self.sprites = [
            sprite
            for sprite in self.sprites
            if sprite.is_alive
        ]

        ox, oy = self.offset

        self.image.fill((0, 0, 0))
        self.image.fblits(
            (
                chunk.image,
                (
                    chunk.render_position[0] - ox,
                    chunk.render_position[1] - oy
                )
            )
            for chunk in self.tile_map.chunks.values()
        )

        return self.is_alive
