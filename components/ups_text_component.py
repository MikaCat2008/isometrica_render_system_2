from __future__ import annotations

import math
from typing import TYPE_CHECKING

from kit import Component, GameManager

if TYPE_CHECKING:
    from nodes import TextNode


class UpsTextComponent(Component):
    node: TextNode
    game: GameManager

    def __init__(self) -> None:
        super().__init__()

        self.game = GameManager.get_instance()
        self.game.ticks.register(1, self.update_fps)

    def update_fps(self) -> None:
        ups = self.game.ups

        if math.isfinite(ups):
            ups = int(ups)

        self.node.text = f"{ups} ups"
