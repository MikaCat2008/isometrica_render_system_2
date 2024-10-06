from __future__ import annotations

from kit import Node, GameConfig, GameManager

from nodes import TextNode
from tile_map import TileMapNode
from chunk_map import ChunkMapNode, ChunkEntityAnimatedSpriteNode
from components import (
    UpsTextComponent, 
    FpsTextComponent, 
    ChunkMapCameraComponent,
    PlayerMovementComponent
)
from textures_manager import TexturesManager


class Game(GameManager, init=False):
    def __init__(self, config: GameConfig) -> None:
        super().__init__(config)

        TexturesManager()

        main_scene = self.scenes.create_scene("main_scene")
        self.scenes.set_current("main_scene")

        main_scene.update_fields(
            root_node=Node().update_fields(
                nodes=[
                    ChunkMapNode().update_fields(
                        tag="ChunkMap",
                        nodes=[
                            ChunkEntityAnimatedSpriteNode().update_fields(
                                tag="MainPlayer",
                                position=(16, 32),
                                frame_rate=10,
                                animation_name="player-0-stay",
                                components=[
                                    PlayerMovementComponent()
                                ]
                            )
                        ],
                        components=[
                            ChunkMapCameraComponent()
                        ]
                    ),
                    TileMapNode().update_fields(
                        tag="InventoryMenu",
                        size=(3, 3)
                    ),
                    TextNode().update_fields(
                        position=(0, 0),
                        components=[
                            UpsTextComponent()
                        ]
                    ),
                    TextNode().update_fields(
                        position=(0, 14),
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
