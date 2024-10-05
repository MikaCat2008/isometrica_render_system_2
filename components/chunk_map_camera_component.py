import random
from queue import Queue
from typing import Optional
from threading import Thread

from kit import Component, GameManager
from chunk_map import Chunk, ChunkMapNode, ChunkEntityNode, ChunkEntitySpriteNode


class ChunkMapCameraComponent(Component):
    node: Optional[ChunkMapNode]

    game: GameManager
    player: Optional[ChunkEntityNode]

    _busy: bool
    _load_thread: Optional[Thread]
    _input_queue: Queue

    def __init__(self) -> None:
        super().__init__()

        self.game = GameManager.get_instance()
        self.game.ticks.register(1, self.update_player)
        self.game.ticks.register(1, self.update_camera_position)
        self.game.ticks.register(20, self.update_chunks)
        self.player = None

        self._busy = False
        self._input_queue = Queue()
        self._load_thread = Thread(target=self._load_chunks)
        self._load_thread.start()

    def update_player(self) -> None:
        if self.player is None and self.node is not None:
            self.player = self.node.scene.get_node_by_tag("MainPlayer")

    def update_camera_position(self) -> None:
        player = self.player
        chunk_map = self.node
        
        if player is None or chunk_map is None:
            return

        x, y = player.position
        screen_w, screen_h = self.game.screen.get_size()
        chunk_map.render_offset = screen_w / 2 - x, screen_h / 2 - y

    def _load_chunks(self) -> None:
        while 1:
            for position in self._input_queue.get():
                cx, cy = position

                if position in self.node.chunks:
                    continue

                self.node.add_chunk(Chunk(position))
                self.node.add_nodes(
                    ChunkEntitySpriteNode().update_fields(
                        position=(
                            random.randint(cx * 128, (cx + 1) * 128 - 1), 
                            random.randint(cy * 128, (cy + 1) * 128 - 1)
                        ),
                        texture_name=f"tree-{random.randint(0, 1)}"
                    )
                    for _ in range(random.randint(10, 20))
                )

            self._busy = False

    def update_chunks(self) -> None:
        player = self.player
        chunk_map = self.node

        if player is None or chunk_map is None:
            return

        x, y = player.position
        x, y = x // 128, y // 128

        if self._busy:
            return
        
        positions = {
            (x + ox, y + oy)
            for ox in range(-3, 4)
            for oy in range(-2, 3)
        }

        for position, chunk in list(chunk_map.chunks.items()):
            if position not in positions:
                self.node.remove_chunk(chunk)

        self._busy = True
        self._input_queue.put(positions)
