from kit import serialize_field, GameManager
from textures_manager import TexturesManager

from .sprite_node import SpriteNode


class AnimatedSpriteNode(SpriteNode):
    _animation_name: str = serialize_field(str, lambda: "", "animation_name")

    frame_index: int
    _frame_rate: int

    def __init__(self) -> None:
        super().__init__()

        self.frame_rate = 30
        self.frame_index = 0
    
    def on_next_frame(self) -> None:
        if not self.animation.frames:
            return
        
        self.frame_index = (self.frame_index + 1) % len(self.animation.frames)
        self.texture_name = self.animation.frames[self.frame_index]

    @property
    def frame_rate(self) -> int:
        return self._frame_rate
    
    @frame_rate.setter
    def frame_rate(self, frame_rate: int) -> None:
        game = GameManager.get_instance()
        game.ticks.unregister(self.on_next_frame)
        game.ticks.register(frame_rate, self.on_next_frame)

    @property
    def animation_name(self) -> str:
        return self._animation_name

    @animation_name.setter
    def animation_name(self, animation_name: str) -> None:
        if self._animation_name == animation_name:
            return

        texture_manager = TexturesManager.get_instance()
        
        self.animation = texture_manager.get_animation(animation_name)
        self.frame_index = 0

        self._animation_name = animation_name
