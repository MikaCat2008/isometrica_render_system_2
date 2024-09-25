import pygame as pg

from kit import GameConfig
from game import Game

pg.init()


if __name__ == "__main__":
    config = GameConfig()
    config.update_fields(
        flags=pg.SCALED | pg.DOUBLEBUF | pg.FULLSCREEN,
        screen_size=(512, 288)
    )
    
    game = Game(config)
    game.run()
