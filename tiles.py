from __future__ import annotations

from random import random, choice
from math import pi
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from game_env import GameEnv


class Grid:
    def __init__(self, game_env: GameEnv):
        self.game_env = game_env
        self.map = {(n, i): Tile([n, i], game_env) for i in range(game_env.grid_size) for n in range(game_env.grid_size)}

    def update(self):
        count = 0
        for count, tile in enumerate(Tile.dying_tiles):
            tile.destabilize()
            if tile.is_fully_destabilized:
                self.map.pop(tile.coords)
        if count + 1 < self.game_env.no_of_dying_tiles:
            new_dying_tile = self.select_tile_to_kill()
            if new_dying_tile:
                Tile.dying_tiles.append(new_dying_tile)

    def select_tile_to_kill(self) -> Tile:
        choose_from = tuple(t for t in self.map.values() if t not in Tile.dying_tiles)
        if len(choose_from) > 1:
            return choice(choose_from)


class Tile:
    dying_tiles = []
    dying_tile_object = "FadingFloorTile.000"
    solid_tile_objects = ["SolidBlackTile", "SolidWhiteTile"]

    def __init__(self, coords: [int, int], game_env: GameEnv):
        self.game_env = game_env
        self.game_object = game_env.sce.addObject(self.solid_tile_objects[sum(coords) % 2])
        self.game_object.worldPosition = [*map(game_env.shift_position, coords), 0.0]
        self.coords = tuple(coords)
        self._is_fully_destabilized = 0.0

    def destabilize(self):
        self._is_fully_destabilized += 0.0003
        self.game_object.worldOrientation = [pi + self._is_fully_destabilized * (random() - 0.5) * 2,
                                             self._is_fully_destabilized * (random() - 0.5) * 2,
                                             self._is_fully_destabilized * (random() - 0.5) * 2]
        if self.is_fully_destabilized:
            self.dying_tiles.remove(self)
        if 0.16 > self._is_fully_destabilized > 0.15:
            self.game_object.worldScale = [(0.16 - self._is_fully_destabilized) * 100 for _ in range(3)]
        elif self._is_fully_destabilized > 0.16:
            self.game_object.worldPosition.z += 100
            self.game_object.worldOrientation = [0, 0, 0]

    @property
    def is_fully_destabilized(self):
        return self._is_fully_destabilized > 0.16
