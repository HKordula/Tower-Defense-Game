ROWS = 20
COLS = 15
TILE_SIZE = 64

WINDOW_WIDTH = ROWS * TILE_SIZE
WINDOW_HEIGHT = COLS * TILE_SIZE
CONTROL_PANEL = 500
FPS = 60

HEALTH = 100
MONEY = 500

TOWER_PRICE = 100
TOWER_UPGRADE = 200

DAMAGE = 20
BOUNTY = 25
PUNISH = 10
REWARD = 50

LEVELS = 5

routes = [
    (128, 0), # start
    (128, 303), # dół
    (832, 303), # prawo
    (832, 113), # góra
    (1152, 113), # prawo
    (1152, 815), # dół
    (638, 815), # lewo
    (638, 559), # góra
    (386, 559), # lewo
    (386, 815), # dół
    (192, 815), # lewo
    (192, 623), # góra
    (0, 623) # meta
]

MAX_LEVEL = 3
TOWER_LEVEL = [
    {
        "range": 115,
        "cooldown": 1500,
    },
    {
        "range": 150,
        "cooldown": 1200,
    },
    {
        "range": 185,
        "cooldown": 1000,
    },
]

SPAWN_COOLDOWN = 300
WAVES_DATA = [
    {
        "elf": 10,
        "reindeer": 5,
        "santa_claus": 1
    },
    {
        "elf": 20,
        "reindeer": 10,
        "santa_claus": 2
    },
    {
        "elf": 30,
        "reindeer": 15,
        "santa_claus": 3
    },
    {
        "elf": 40,
        "reindeer": 20,
        "santa_claus": 4
    },
    {
        "elf": 50,
        "reindeer": 25,
        "santa_claus": 5
    }
]

DIRECTION_MAP = {
            'down': 0,
            'left': 1,
            'right': 2,
            'up': 3
        }