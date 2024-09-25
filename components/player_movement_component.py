import pygame as pg
from pygame.key import get_pressed

from kit import Component, GameManager

from tile import TileEntitySpriteNode


class PlayerMovementComponent(Component):
    node: TileEntitySpriteNode
    game: GameManager

    def __init__(self) -> None:
        super().__init__()

        self.game = GameManager.get_instance()
        self.game.ticks.register(1, self.movement)

    def movement(self) -> None:
        state = get_pressed()
        speed = 1
        x, y = 0, 0

        if state[pg.K_d]:
            x += speed
        if state[pg.K_a]:
            x -= speed
        if state[pg.K_w]:
            y -= speed
        if state[pg.K_s]:
            y += speed

        nx, ny = self.node.position

        self.node.position = x + nx, y + ny
