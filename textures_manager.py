from pygame.image import load as pg_load
from pygame.surface import Surface

from kit import Manager, Animation


class TexturesManager(Manager, init=False):
    textures: dict[str, Surface]

    def __init__(self) -> None:
        super().__init__()

        self.textures = {
            "": self.load_texture("unknown-entity.png"),

            "tree-0": self.load_texture("tree-0.png"),
            "tree-1": self.load_texture("tree-1.png"),

            "player-0-0": self.load_texture("player-0-0.png"),
            "player-0-1": self.load_texture("player-0-1.png"),
            "player-1": self.load_texture("player-1.png"),

            "grass-tile": self.load_texture("grass-tile.png"),
        }
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

    def load_texture(self, path: str) -> Surface:
        return pg_load("assets/" + path).convert_alpha()

    def get_texture(self, texture_name: str) -> Surface:
        return self.textures[texture_name]
    
    def get_animation(self, animation_name: str) -> Animation:
        return self.animations[animation_name]
