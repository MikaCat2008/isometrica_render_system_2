from __future__ import annotations

import random

from kit import Node, Component, GameConfig, GameManager, DrawableNode

from nodes import TextNode
from tile_map import Sprite, TileMapNode
# from chunk_map import ChunkMapNode, ChunkEntityAnimatedSpriteNode
from components import (
    UpsTextComponent, 
    FpsTextComponent, 
    # ChunkMapCameraComponent,
    # PlayerMovementComponent
)
from textures_manager import TexturesManager


def destroy(node: Node, timeout: float = 0) -> None:
    if node.scene:
        node.scene.destroy(node, timeout)
    else:
        node.destroy()


class EntityNode(Node):
    sprite: Sprite

    def __init__(self) -> None:
        super().__init__()

        game = GameManager.get_instance()
        game.ticks.register(1, self._find_tile_map)
        self.sprite = Sprite(
            texture_name="player-0-0", 
            flip_x=False, 
            flip_y=False 
        )
        self.sprite.position = random.randint(0, 522), random.randint(0, 288)
        
    def _find_tile_map(self) -> None:
        tile_map: TileMapNode = self.scene.root_node.get_node_by_tag("TileMap")

        if tile_map is None:
            return
        
        game = GameManager.get_instance()
        game.ticks.unregister(self._find_tile_map)
        tile_map.add_sprites([self.sprite])

        # destroy(self, 6)

    def update(self) -> bool:
        self.sprite.position = random.randint(0, 522), random.randint(0, 288)
        self.sprite.rotation = random.randint(0, 360)
        self.sprite.texture_name = random.choice(("player-0-0", "player-0-1"))

        return super().update()

    def destroy(self) -> None:
        self.is_alive = False
        self.sprite.is_alive = False


class EntityManagerComponent(Component):
    def __init__(self):
        super().__init__()

        game = GameManager.get_instance()
        game.ticks.register(1, self.summon_entities)

    def summon_entities(self) -> None:
        self.node.add_nodes(
            EntityNode()
            for _ in range(4)
        )


class TileMapTilesComponent(Component):
    node: TextNode
    
    def __init__(self):
        super().__init__()

        self.game = GameManager.get_instance()
        self.game.ticks.register(10, self._find_tile_map)
    
    def _find_tile_map(self) -> None:
        self.tile_map: TileMapNode = self.node.scene.root_node.get_node_by_tag("TileMap")

        if self.tile_map is None:
            return
        
        self.game.ticks.unregister(self._find_tile_map)
        self.game.ticks.register(5, self.update_sprite)

    def update_sprite(self) -> None:
        self.node.text = f"{len(self.tile_map.tile_map.tiles)} tiles"
        self.node.position = self.game.screen.get_width() - self.node.image.get_width(), 0


class TileMapChunksComponent(Component):
    node: TextNode
    
    def __init__(self):
        super().__init__()

        self.game = GameManager.get_instance()
        self.game.ticks.register(10, self._find_tile_map)
    
    def _find_tile_map(self) -> None:
        self.tile_map: TileMapNode = self.node.scene.root_node.get_node_by_tag("TileMap")

        if self.tile_map is None:
            return
        
        self.game.ticks.unregister(self._find_tile_map)
        self.game.ticks.register(5, self.update_sprite)

    def update_sprite(self) -> None:
        self.node.text = f"{len(self.tile_map.tile_map.chunks)} chunks"
        self.node.position = self.game.screen.get_width() - self.node.image.get_width(), 14


class TileMapSpritesComponent(Component):
    node: TextNode
    
    def __init__(self):
        super().__init__()

        self.game = GameManager.get_instance()
        self.game.ticks.register(10, self._find_tile_map)
    
    def _find_tile_map(self) -> None:
        self.tile_map: TileMapNode = self.node.scene.root_node.get_node_by_tag("TileMap")

        if self.tile_map is None:
            return
        
        self.game.ticks.unregister(self._find_tile_map)
        self.game.ticks.register(5, self.update_sprite)

    def update_sprite(self) -> None:
        self.node.text = f"{len(self.tile_map.sprites)} sprites"
        self.node.position = self.game.screen.get_width() - self.node.image.get_width(), 28


class Game(GameManager, init=False):
    def __init__(self, config: GameConfig) -> None:
        super().__init__(config)

        TexturesManager()

        main_scene = self.scenes.create_scene("main_scene")
        self.scenes.set_current("main_scene")

        main_scene.update_fields(
            root_node=DrawableNode().update_fields(
                nodes=[
                    Node().update_fields(
                        nodes=[
                            EntityNode()
                            for _ in range(1000)
                        ]
                    ),
                    TileMapNode().update_fields(
                        tag="TileMap"
                    ),
                    TextNode().update_fields(
                        color=(255, 0, 0),
                        position=(0, 0),
                        components=[
                            UpsTextComponent()
                        ]
                    ),
                    TextNode().update_fields(
                        color=(255, 0, 0),
                        position=(0, 14),
                        components=[
                            FpsTextComponent()
                        ]
                    ),
                    TextNode().update_fields(
                        color=(0, 255, 0),
                        components=[
                            TileMapTilesComponent()
                        ]
                    ),
                    TextNode().update_fields(
                        color=(0, 255, 0),
                        components=[
                            TileMapChunksComponent()
                        ]
                    ),
                    TextNode().update_fields(
                        color=(0, 255, 0),
                        components=[
                            TileMapSpritesComponent()
                        ]
                    )
                ]
            )
        )

    def draw(self) -> None:
        self.scenes.draw()

        super().draw()
