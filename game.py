from __future__ import annotations

import random
from math import sin
from typing import Optional

import pygame as pg
from pygame.key import get_pressed

from kit import Node, Component, GameConfig, GameManager, DrawableNode

from nodes import TextNode
from tile_map import Sprite, TileMapNode, AnimatedSprite
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
    tile_map: Optional[TileMapNode]

    def __init__(self) -> None:
        super().__init__()

        game = GameManager.get_instance()
        game.ticks.register(1, self._find_tile_map)

        self.tile_map = None

    def _find_tile_map(self) -> None:
        self.tile_map = self.scene.root_node.get_node_by_tag("TileMap")

        if self.tile_map is None:
            return
        
        game = GameManager.get_instance()
        game.ticks.unregister(self._find_tile_map)
        self.tile_map.add_sprites([self.sprite])

    def destroy(self) -> None:
        self.is_alive = False
        self.sprite.is_alive = False


class TreeNode(EntityNode):
    speed: int
    offset: int

    def __init__(self):
        super().__init__()

        self.sprite = Sprite(
            "tree-0", 
            flip_x=False, 
            flip_y=False 
        )
        self.speed = random.randint(20, 40)
        self.offset = random.randint(0, 30)
        self.sprite.position = random.randint(0, 522), random.randint(32, 288 + 128)

    def update(self) -> bool:
        self.sprite.rotation = int(
            sin((self.scene.game.ticks.ticks + self.offset) / self.speed) * 2
        )

        return super().update()


class PlayerNode(EntityNode):
    sprite: AnimatedSprite

    def __init__(self):
        super().__init__()

        self.sprite = AnimatedSprite(
            "player-0-walk", 
            position=(16, 32),
            flip_x=False, 
            flip_y=False 
        )

    def update(self) -> bool:
        super().update()

        x, y = 0, 0
        speed = 1
        state = get_pressed()

        if state[pg.K_a]:
            x -= speed
        if state[pg.K_d]:
            x += speed
        if state[pg.K_w]:
            y -= speed
        if state[pg.K_s]:
            y += speed

        if x or y:
            if x < 0:
                self.sprite.flip_x = True
            elif x > 0:
                self.sprite.flip_x = False

            sx, sy = self.sprite.position

            self.sprite.position = sx + x, sy + y
            self.sprite.animation_name = "player-0-walk"
        else:
            self.sprite.animation_name = "player-0-stay"

        if self.tile_map is None:
            return self.is_alive

        w, h = self.scene.game.screen.get_size()
        sx, sy = self.sprite.position

        self.tile_map.offset = sx - w // 2, sy - h // 2

        return self.is_alive


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
                        nodes=[PlayerNode()] + [
                            TreeNode()
                            for _ in range(1500)
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
