from functools import cache

from pygame.font import Font, SysFont

from kit import serialize_field, DrawableNode


@cache
def get_font(size: int) -> Font:
    return SysFont("Arial", size)


class TextNode(DrawableNode):
    _text: str = serialize_field(str, lambda: "", "text")
    _color: tuple[int, int, int] = serialize_field(tuple[int, int, int], lambda: (0, 0, 0), "color")

    def __pre_init__(self):
        super().__pre_init__()

        self._text = None
        self._color = None

    def render(self) -> None:
        if self._text is None or self._color is None:
            return

        self.image = get_font(12).render(self._text, False, self._color)

    @property
    def text(self) -> str:
        return self._text

    @text.setter
    def text(self, text: str) -> None:
        if self._text == text:
            return

        self._text = text
        self.render()

    @property
    def color(self) -> tuple[int, int, int]:
        return self._color
    
    @color.setter
    def color(self, color: tuple[int, int, int]) -> None:
        if self._color == color:
            return

        self._color = color
        self.render()
