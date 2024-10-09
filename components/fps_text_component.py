from __future__ import annotations

import math
from typing import TYPE_CHECKING

from kit import Component, GameManager

if TYPE_CHECKING:
    from nodes import TextNode


class FpsTextComponent(Component):
    node: TextNode
    game: GameManager

    def __init__(self) -> None:
        super().__init__()

        self.game = GameManager.get_instance()
        self.game.ticks.register(1, self.update_fps)

    def update_fps(self) -> None:
        fps = self.game.fps

        if math.isfinite(fps):
            fps = int(fps)

        self.node.text = f"{fps} fps"
