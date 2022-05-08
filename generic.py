import bge

no_of_players = 2
sce = bge.logic.getCurrentScene()
grid_size = 4
tile_scale = 2
gaps = 0.1
pos_mult = tile_scale * (1 + gaps)
offsetter = grid_size * pos_mult / 2 - pos_mult / 2


class Player:
    def __init__(self, n):
        play_ob = ["Player1", "Player2"]
        self.player_number = n
        play_spawns = [[0, 0], [3, 3]]
        self.game_object = sce.addObject(play_ob[self.player_number])
        p_pos = play_spawns[n]
        self.game_object.worldPosition = [p_pos[0] * pos_mult - offsetter, p_pos[1] * pos_mult - offsetter, 1.0]

    def update(self):
        pass


class GameEnv:
    def __init__(self):
        self.players = [Player(n) for n in range(no_of_players)]
        obs = ["SolidBlackTile", "SolidWhiteTile"]
        self.dying_blocks = []
        self.killables = ["FadingFloorTile.000", "FadingFloorTile.001", "FadingFloorTile.002", "FadingFloorTile.003"]

        self.map = [[None for _ in range(grid_size)] for _ in range(grid_size)]

        for n in range(grid_size):
            for i in range(grid_size):
                col = (n % 2 + i) % 2
                ob = sce.addObject(obs[col])
                ob.worldPosition = [n * pos_mult - offsetter, i * pos_mult - offsetter, 0.0]

    def update(self):
        for player in self.players:
            player.update()

    def tile_death(self, coords):
        self.map[coords[0]][coords[1]].endObject()
        nu_block = sce.addObject(self.get_next_killable(True))
        nu_block.worldPosition = [coords[0] * pos_mult - offsetter, coords[1] * pos_mult - offsetter, 0.0]
        self.map[coords[0]][coords[1]] = nu_block

    def get_next_killable(self, is_for_spawning):
        name = self.killables[-1]
        if is_for_spawning:
            self.dying_blocks.append(name)
            del self.killables[-1]
        return name


if hasattr(bge.logic, "GameEnv"):
    bge.logic.GameEnv.update()
else:
    bge.logic.GameEnv = GameEnv()
