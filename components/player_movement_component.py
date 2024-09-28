import pygame as pg
from pygame.key import get_pressed

from kit import serialize_field, Component, GameManager
from tile import TileMapNode, TileEntitySpriteNode


class PlayerMovementComponent(Component):
    tile_map: TileMapNode = serialize_field(TileMapNode)

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

        if x == 0 and y == 0:
            return

        nx, ny = self.node.position
        nx, ny = self.node.position = x + nx, y + ny

        self.update_tile_map_chunks()
        self.update_tile_map_position(nx, ny)

    def update_tile_map_chunks(self) -> None:
        ...

    def update_tile_map_position(self, nx: int, ny: int) -> None:
        screen_w, screen_h = self.game.screen.get_size()

        self.tile_map.inner_position = screen_w / 2 - nx, screen_h / 2 - ny
