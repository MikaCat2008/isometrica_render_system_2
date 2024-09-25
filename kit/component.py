from __future__ import annotations

from typing import TYPE_CHECKING

from .serialization import Serializable

if TYPE_CHECKING:
    from .node import Node


class Component(Serializable):   
    node: Node
