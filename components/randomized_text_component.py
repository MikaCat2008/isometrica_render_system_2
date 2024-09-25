from __future__ import annotations

import random
from typing import TYPE_CHECKING

from kit import Component, GameManager

if TYPE_CHECKING:
    from nodes import TextNode


class RandomizedTextComponent(Component):
    node: TextNode
    game: GameManager

    def update_value(self) -> None:
        self.node.text = str(random.randint(100_000, 999_999))

    def __init__(self) -> None:
        self.game = GameManager.get_instance()
        self.game.ticks.register(1, self.update_value)
