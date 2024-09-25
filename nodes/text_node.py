from functools import cache

from pygame.font import Font, SysFont

from kit import serialize_field, DrawableNode


@cache
def get_font(size: int) -> Font:
    return SysFont("Arial", size)


class TextNode(DrawableNode):
    _text: str = serialize_field(str, lambda: "", "text")

    def render(self) -> None:
        self.image = get_font(12).render(self.text, False, (255, 0, 0))

    @property
    def text(self) -> str:
        return self._text

    @text.setter
    def text(self, text: str) -> None:
        if self.text == text:
            return

        self._text = text
        self.render()
