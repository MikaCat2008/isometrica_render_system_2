from .nodes import (
    Node as Node,
    Scene as Scene,
    Component as Component,
    DrawableNode as DrawableNode
)
from .game_managers import (
    GameManager as GameManager,
    TicksManager as TicksManager,
    EventsManager as EventsManager,
    ScenesManager as ScenesManager,
    ResourcesManager as ResourcesManager
)
from .serialization import (
    serialize_field as serialize_field,
    Serializable as Serializable,
    SerializeField as SerializeField
)

from .manager import Manager as Manager
from .animation import Animation as Animation
from .game_config import GameConfig as GameConfig


def destroy(node: Node, timeout: float = 0) -> None:
    if node.scene:
        node.scene.destroy(node, timeout)
    else:
        node.destroy()
