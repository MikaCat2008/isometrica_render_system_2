from typing import Optional

from pygame.image import load as pg_load
from pygame.surface import Surface
from pygame.transform import flip, scale, rotate

from ..manager import Manager
from ..animation import Animation


class ResourcesManager(Manager, init=False):
    textures: dict[str, Surface]
    animations: dict[str, list[str]]
    cached_textures: dict[tuple[str, float, bool, bool], Surface]

    def __init__(self):
        super().__init__()
        
        self.textures = {}
        self.animations = {}
        self.cached_textures = {}

    def load_texture(self, path: str, size: Optional[tuple[int, int]] = None) -> Surface:
        texture = pg_load("assets/" + path).convert_alpha()
        
        if size:
            return scale(texture, size)
        return texture

    def get_texture(
        self, 
        texture_name: str,
        rotation: float,
        flip_x: bool,
        flip_y: bool
    ) -> tuple[tuple[int, int], Surface]:
        data = texture_name, rotation, flip_x, flip_y

        if data in self.cached_textures:
            return self.textures[texture_name].get_size(), self.cached_textures[data]

        cached_texture = self.textures[texture_name]
        size = cached_texture.get_size()

        if rotation:
            cached_texture = rotate(cached_texture, rotation)
    
        if flip_x or flip_y:
            cached_texture = flip(cached_texture, flip_x, flip_y)

        self.cached_textures[data] = cached_texture

        return size, cached_texture
    
    def get_animation(self, animation_name: str) -> Animation:
        return self.animations[animation_name]
