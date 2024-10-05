from __future__ import annotations

from kit import Node, GameConfig, GameManager
from textures_manager import TexturesManager

from nodes import TextNode
from chunk_map import ChunkMapNode, ChunkEntitySpriteNode
from components import (
    UpsTextComponent, 
    FpsTextComponent, 
    ChunkMapCameraComponent,
    PlayerMovementComponent
)


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
                            ChunkEntitySpriteNode().update_fields(
                                tag="MainPlayer",
                                position=(16, 32),
                                texture_name="player-1",
                                components=[
                                    PlayerMovementComponent()
                                ]
                            )
                        ],
                        components=[
                            ChunkMapCameraComponent()
                        ]
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
