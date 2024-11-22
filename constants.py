
ROWS = 40
COLS = 30
TILE_SIZE = 32

WINDOW_WIDTH = ROWS * TILE_SIZE
WINDOW_HEIGHT = COLS * TILE_SIZE
CONTROL_PANEL = 500
FPS = 60

HEALTH = 100
MONEY = 1100

TOWER_PRICE = 100
TOWER_UPGRADE = 100

DAMAGE = 20
BOUNTY = 50
PUNISH = 100
REWARD = 100

LEVELS = 1

routes = [
    (128, 0),
    (128, 283),
    (832, 283),
    (832, 123),
    (1152, 123),
    (1152, 795),
    (608, 795),
    (608, 539),
    (416, 539),
    (416, 795),
    (192, 795),
    (192, 603),
    (0, 603)
]

MAX_LEVEL = 3
TOWER_LEVEL = [
    {
        "range": 90,
        "cooldown": 1500,
    },
    {
        "range": 100,
        "cooldown": 1300,
    },
    {
        "range": 120,
        "cooldown": 1000,
    },
]

SPAWN_COOLDOWN = 400
WAVES_DATA = [
    {
        "elf": 1,
        "reindeer": 1,
        "santa_claus": 0
    },
    {
        "elf": 20,
        "reindeer": 4,
        "santa_claus": 2
    },
    {
        "elf": 20,
        "reindeer": 8,
        "santa_claus": 2
    },
    {
        "elf": 20,
        "reindeer": 8,
        "santa_claus": 4
    },
    {
        "elf": 20,
        "reindeer": 10,
        "santa_claus": 5
    }
]