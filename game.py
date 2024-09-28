from __future__ import annotations

import random

from kit import Node, GameConfig, GameManager
from textures_manager import TexturesManager

from tile import TileMapNode, TileEntitySpriteNode
from nodes import TextNode
from components import FpsTextComponent, PlayerMovementComponent


class Game(GameManager, init=False):
    def __init__(self, config: GameConfig) -> None:
        super().__init__(config)

        TexturesManager()

        main_scene = self.scenes.create_scene("main_scene")
        self.scenes.set_current("main_scene")

        tile_map = TileMapNode()

        for x in range(4):
            for y in range(5):
                tile_map.create_chunk((x, y))

        player = TileEntitySpriteNode().update_fields(
            position=(0, 32),
            texture_name="player-1",
            components=[
                PlayerMovementComponent().update_fields(
                    tile_map=tile_map
                )
            ]
        )
        player.tile_map = tile_map

        for _ in range(1_000):
            tree = TileEntitySpriteNode().update_fields(
                position=(random.randint(0, 512), random.randint(0, 288)),
                texture_name=f"tree-{random.randint(0, 1)}"
            )
            tree.tile_map = tile_map

        main_scene.update_fields(
            root_node=Node().update_fields(
                nodes=[
                    tile_map,
                    TextNode().update_fields(
                        position=(0, 0),
                        components=[
                            FpsTextComponent()
                        ]
                    )
                ]
            )
        )

    def draw(self) -> None:
        self.scenes.draw()

        super().draw()
