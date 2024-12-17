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
    (128, 0), #start
    (128, 303), #down
    (832, 303), #right
    (832, 113), #up
    (1152, 113), #right
    (1152, 815), #down
    (638, 815), #left
    (638, 554), #up
    (386, 554), #left
    (386, 815), #down
    (192, 815), #left
    (192, 618), #up
    (0, 618) #left
]

MAX_LEVEL = 3
TOWER_LEVEL = [
    {
        "range": 115,
        "cooldown": 1500,
    },
    {
        "range": 150,
        "cooldown": 1000,
    },
    {
        "range": 200,
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