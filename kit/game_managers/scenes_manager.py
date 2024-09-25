from __future__ import annotations

from typing import Optional

from ..scene import Scene
from ..manager import Manager


class ScenesManager(Manager, init=False):
    scenes: dict[str, Scene]
    current_scene: Optional[Scene]

    def __init__(self) -> None:
        super().__init__()
        
        self.scenes = {}
        self.current_scene = None

    def create_scene(self, name: str) -> Scene:
        scene = Scene()
        
        self.scenes[name] = scene

        return scene
    
    def set_current(self, name: str) -> None:
        self.current_scene = self.scenes[name]

    def check_current_scene(self) -> None:
        if self.current_scene is None:
            raise ValueError("Current scene has not yet been set")
 
    def draw(self) -> None:
        self.check_current_scene()
        self.current_scene.draw()
