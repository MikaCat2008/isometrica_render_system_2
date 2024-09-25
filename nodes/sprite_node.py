from textures_manager import TexturesManager

from kit import serialize_field, DrawableNode


class SpriteNode(DrawableNode):
    _texture_name: str = serialize_field(str, alias_name="texture_name")

    def render(self) -> None:
        textures = TexturesManager.get_instance()

        self.image = textures.get_texture(self.texture_name)
        self.update_position()

    @property
    def texture_name(self) -> str:
        return self._texture_name

    @texture_name.setter
    def texture_name(self, texture_name: str) -> None:        
        self._texture_name = texture_name
        self.render()
