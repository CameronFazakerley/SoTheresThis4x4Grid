from __future__ import annotations
from typing import TYPE_CHECKING

import bge

if TYPE_CHECKING:
    from game_env import GameEnv


class Player:
    play_ob = ["Player1", "Player2"]
    play_spawns = [[0, 0], [3, 3]]

    def __init__(self, n, game_env: GameEnv):
        self.game_env = game_env
        self.player_number = n
        self.game_object = game_env.sce.addObject(self.play_ob[self.player_number])
        self.game_object.worldPosition = [*map(game_env.shift_position, self.play_spawns[n]), 1.0]
        self.mov_speed = 2

    def update(self):
        kb = bge.logic.keyboard.activeInputs
        keys = [[[45, 1, 1], [23, 0, -1], [41, 1, -1], [26, 0, 1]], [[72, 1, 1], [69, 0, -1], [70, 1, -1], [71, 0, 1]]]
        keys = keys[self.player_number]
        mov = [0.0, 0.0, self.game_object.worldLinearVelocity[2]]  # self.game_object.localLinearVelocity
        for key, axis, mode in keys:
            if key in kb:
                mov[axis] += self.mov_speed * mode
        floor_collision = self.game_object.sensors["FloorCollision"]
        player_jump_key = [8, 53]
        if len(floor_collision.hitObjectList) != 0:
            if player_jump_key[self.player_number] in kb:
                mov[2] += self.mov_speed
        self.game_object.localLinearVelocity = mov