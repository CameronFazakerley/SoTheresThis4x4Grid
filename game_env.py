from __future__ import annotations

import bge

from players import Player


class GameEnv:
    no_of_players = 2
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
        obs = ["SolidBlackTile", "SolidWhiteTile"]
        self.dying_blocks = []
        self.killables = ["FadingFloorTile.000", "FadingFloorTile.001", "FadingFloorTile.002", "FadingFloorTile.003"]

        self.map = [[None for _ in range(cls.grid_size)] for _ in range(cls.grid_size)]

        for n in range(cls.grid_size):
            for i in range(cls.grid_size):
                col = (n % 2 + i) % 2
                ob = cls.sce.addObject(obs[col])
                ob.worldPosition = [n * cls.pos_mult - cls.offsetter, i * cls.pos_mult - cls.offsetter, 0.0]
        return bge.logic.__dict__.setdefault("game_env", self)

    def shift_position(self, pos: float):
        return pos * self.pos_mult - self.offsetter

    def update(self):
        for player in self.players:
            player.update()

    def tile_death(self, coords):
        self.map[coords[0]][coords[1]].endObject()
        nu_block = self.sce.addObject(self.get_next_killable(True))
        nu_block.worldPosition = [coords[0] * self.pos_mult - self.offsetter, coords[1] * self.pos_mult - self.offsetter, 0.0]
        self.map[coords[0]][coords[1]] = nu_block

    def get_next_killable(self, is_for_spawning):
        name = self.killables[-1]
        if is_for_spawning:
            self.dying_blocks.append(name)
            del self.killables[-1]
        return name
