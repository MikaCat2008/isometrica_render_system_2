import os

from pygame.image import load as pg_load
from pygame.surface import Surface

from kit import Manager


class TexturesManager(Manager, init=False):
    textures: dict[str, Surface]

    def __init__(self) -> None:
        super().__init__()

        self.textures = {
            file.rsplit(".", 1)[0]: self.load_texture(file)
            for file in os.listdir("assets")
        }

    def load_texture(self, path: str) -> Surface:
        return pg_load("assets/" + path).convert_alpha()

    def get_texture(self, texture_name: str) -> Surface:
        return self.textures[texture_name]
