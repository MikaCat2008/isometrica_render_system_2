from typing import Optional

from pygame.image import load as pg_load
from pygame.surface import Surface
from pygame.transform import flip, scale, rotate

from kit import Manager, Animation


class TexturesManager(Manager, init=False):
    cached_textures: dict[tuple[str, float, bool, bool], Surface]
    
    _textures: dict[str, Surface]

    def __init__(self) -> None:
        super().__init__()

        self._textures = {
            "tree-0": self.load_texture("tree-0.png"),
            "tree-1": self.load_texture("tree-1.png"),

            "player-0-0": self.load_texture("player-0-0.png"),
            "player-0-1": self.load_texture("player-0-1.png"),
            "player-1": self.load_texture("player-1.png"),

            "grass-tile": self.load_texture("grass-tile.png"),
        }
        self.cached_textures = {}
        self.animations = {
            "": Animation(),
            "player-0-stay": Animation().update_fields(
                frames=[
                    "player-0-0"
                ]
            ),
            "player-0-walk": Animation().update_fields(
                frames=[
                    "player-0-0",
                    "player-0-1"
                ]
            )
        }

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
            return self._textures[texture_name].get_size(), self.cached_textures[data]

        cached_texture = self._textures[texture_name]
        size = cached_texture.get_size()

        if rotation:
            cached_texture = rotate(cached_texture, rotation)
    
        if flip_x or flip_y:
            cached_texture = flip(cached_texture, flip_x, flip_y)

        self.cached_textures[data] = cached_texture

        return size, cached_texture
    
    def get_animation(self, animation_name: str) -> Animation:
        return self.animations[animation_name]
