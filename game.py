import random

from kit import Node, Scene, GameConfig, GameManager
from textures_manager import TexturesManager

from nodes import TextNode
from components import FpsTextComponent, RandomizedTextComponent


class Game(GameManager, init=False):
    def __init__(self, config: GameConfig) -> None:
        super().__init__(config)

        TexturesManager()

        main_scene = self.scenes.create_scene("main_scene")
        self.scenes.set_current("main_scene")

        main_scene.update_fields(
            root_node=Node().update_fields(
                nodes=[
                    TextNode().update_fields(
                        position=(0, 0),
                        components=[
                            FpsTextComponent()
                        ]
                    ),
                    *[
                        TextNode().update_fields(
                            position=(random.randint(0, 512), random.randint(0, 288)),
                            components=[
                                RandomizedTextComponent()
                            ]
                        )
                        for _ in range(3_000)
                    ]
                ]
            )
        )

    def draw(self) -> None:
        self.scenes.draw()

        super().draw()
