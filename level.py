import random

import pygame as pg
import constants as const
from elf import Elf
from reindeer import Reindeer
from santa_claus import SantaClaus


class Level():
    def __init__(self, level_img):
        self.opponent_list = []
        self.image = level_img
        self.level = 1
        self.spawned = 0
        self.killed = 0
        self.missed = 0
        self.health = const.HEALTH
        self.money = const.MONEY

    def draw(self, surface):
        surface.blit(self.image, (0, 0))

    def spawn_opponents(self):
        opponents = const.WAVES_DATA[self.level - 1]
        for name in opponents:
            wave = opponents[name]
            for opp in range(wave):
                self.opponent_list.append(name)
        random.shuffle(self.opponent_list)

    def get_opponent(self, name, routes, sprite_sheet):
        if name == "elf":
            return Elf(routes, sprite_sheet)
        elif name == "reindeer":
            return Reindeer(routes, sprite_sheet)
        elif name == "santa_claus":
            return SantaClaus(routes, sprite_sheet)

    def level_up(self):
        if len(self.opponent_list) == self.killed + self.missed:
            return True

    def reset_stats(self):
        self.opponent_list = []
        self.spawned = 0
        self.killed = 0
        self.missed = 0