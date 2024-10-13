from kit import Animation, ResourcesManager


class Resources(ResourcesManager, init=False):    
    def __init__(self) -> None:
        super().__init__()

        self.textures = {
            "tree-0": self.load_texture("tree-0.png"),
            "tree-1": self.load_texture("tree-1.png"),

            "player-0-0": self.load_texture("player-0-0.png"),
            "player-0-1": self.load_texture("player-0-1.png"),
            "player-1": self.load_texture("player-1.png"),

            "grass-tile": self.load_texture("grass-tile.png"),
        }
        self.animations = {
            "": Animation(),
            "player-0-stay": [
                "player-0-0"
            ],
            "player-0-walk": [
                "player-0-0",
                "player-0-1"
            ]
        }
