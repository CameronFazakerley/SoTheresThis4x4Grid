from __future__ import annotations

import bge

from players import Player
from tiles import Grid


class GameEnv:
    no_of_players = 2
    no_of_dying_tiles = 3
    sce = bge.logic.getCurrentScene()
    grid_size = 4
    tile_scale = 2
    gaps = 0.1
    pos_mult = tile_scale * (1 + gaps)
    offsetter = grid_size * pos_mult / 2 - pos_mult / 2

    def __new__(cls, *args, **kwargs):
        if hasattr(bge.logic, "game_env"):
            bge.logic.game_env.update()
            return bge.logic.game_env
        self = super().__new__(cls)
        self.players = [Player(n, self) for n in range(cls.no_of_players)]
        self.grid = Grid(self)
        return bge.logic.__dict__.setdefault("game_env", self)

    def shift_position(self, pos: float):
        return pos * self.pos_mult - self.offsetter

    def update(self):
        for player in self.players:
            player.update()
        self.grid.update()
