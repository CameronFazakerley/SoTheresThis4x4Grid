import bge

no_of_players = 2
sce = bge.logic.getCurrentScene()
grid_size = 4
tile_scale = 2
gaps = 0.1
pos_mult = tile_scale * (1 + gaps)
offsetter = grid_size * pos_mult / 2 - pos_mult / 2
mov_speed = 2


class Player:
    def __init__(self, n):
        play_ob = ["Player1", "Player2"]
        self.player_number = n
        play_spawns = [[0, 0], [3, 3]]
        self.game_object = sce.addObject(play_ob[self.player_number])
        p_pos = play_spawns[n]
        self.game_object.worldPosition = [p_pos[0] * pos_mult - offsetter, p_pos[1] * pos_mult - offsetter, 1.0]

    def update(self):
        kb = bge.logic.keyboard.activeInputs
        keys = [[[45, 1, 1], [23, 0, -1], [41, 1, -1], [26, 0, 1]], [[72, 1, 1], [69, 0, -1], [70, 1, -1], [71, 0, 1]]]
        keys = keys[self.player_number]
        mov = [0.0, 0.0, self.game_object.worldLinearVelocity[2]]  # self.game_object.localLinearVelocity
        for key, axis, mode in keys:
            if key in kb:
                mov[axis] += mov_speed * mode
        floor_collision = self.game_object.sensors["FloorCollision"]
        player_jump_key = [8, 53]
        if len(floor_collision.hitObjectList) != 0:
            if player_jump_key[self.player_number] in kb:
                mov[2] += mov_speed
        self.game_object.localLinearVelocity = mov


class GameEnv:
    def __new__(cls, *args, **kwargs):
        if hasattr(bge.logic, "game_env"):
            bge.logic.game_env.update()
            return bge.logic.game_env
        new = super().__new__(cls)
        return bge.logic.__dict__.setdefault("game_env", new)

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


GameEnv()
