import pygame as pg
from pygame.key import get_pressed

from kit import Component, GameManager
from chunk_map import ChunkEntityAnimatedSpriteNode


class PlayerMovementComponent(Component):
    node: ChunkEntityAnimatedSpriteNode
    game: GameManager

    def __init__(self) -> None:
        super().__init__()

        self.game = GameManager.get_instance()
        self.game.ticks.register(1, self.movement)

    def movement(self) -> None:
        player = self.node

        if player is None:
            return

        x, y = 0, 0
        state = get_pressed()
        speed = 1

        if state[pg.K_d]:
            x += speed
        if state[pg.K_a]:
            x -= speed
        if state[pg.K_w]:
            y -= speed
        if state[pg.K_s]:
            y += speed

        if x == 0 and y == 0:
            player.animation_name = "player-0-stay"
            
            return
        
        if x > 0:
            player.flip_x = False
        if x < 0:
            player.flip_x = True
        
        player.animation_name = "player-0-walk"

        nx, ny = player.position
        player.position = x + nx, y + ny
