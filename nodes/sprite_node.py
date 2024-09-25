from textures_manager import TexturesManager

from kit import serialize_field, DrawableNode


class SpriteNode(DrawableNode):
    texture_name: str = serialize_field(str)

    def set_texture(self, texture_name: str) -> None:        
        self.texture_name = texture_name
        self.render()

    def render(self) -> None:
        textures = TexturesManager.get_instance()

        self.image = textures.get_texture(self.texture_name)
