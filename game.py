import asyncio
import client
from models.player import Player
from models.map import Map
import pygame
from pygame.locals import *
import sys

import time

BACKGROUND_COLOR = "#004400"
PLATFORM_WIDTH = 32
PLATFORM_HEIGHT = 32
PLATFORM_COLOR = "#FF6262"
CITY_COLOR = "#FF00FF"
SHOP_COLOR = "#00FF00"
multiplier = 3


# 'wgforge-srv.wargaming.net', 443
# '127.0.0.1', 2000

class Game(object):
    def __init__(self, playername):
        """
        Initialization of the game. Initializes connection, player and map
        :param playername: string
        """
        self.loop = asyncio.get_event_loop()
        self.cl = client.Client(self.loop)
        self.loop.run_until_complete(self.cl.connect('wgforge-srv.wargaming.net', 443))
        _, msg = self.loop.run_until_complete(self.cl.login(playername))
        self.player = Player(msg)
        # print(str(player.trains))
        # print(str(msg))
        _, msg = self.loop.run_until_complete(self.cl.getMap(0))
        self.map = Map(msg)
        _, msg = self.loop.run_until_complete(self.cl.getMap(1))
        self.map.add_layer_1(msg)
        _, msg = self.loop.run_until_complete(self.cl.getMap(10))
        self.map.add_layer_10(msg)
        # print(msg)

        pygame.init()
        self.WIN_WIDTH = self.map.size[0] * multiplier
        self.WIN_HEIGHT = self.map.size[1] * multiplier
        self.DISPLAY = (self.WIN_WIDTH, self.WIN_HEIGHT)
        self.screen = pygame.display.set_mode(self.DISPLAY)
        pygame.display.set_caption("Super Mario Boy")
        self.bg = pygame.Surface((self.WIN_WIDTH, self.WIN_HEIGHT))
        self.bg.fill(Color(BACKGROUND_COLOR))

    def update(self, n):
        self.draw()

    def draw(self):
        if not self.map.size:
            return 1
        for point in self.map.point:
            COLOR = PLATFORM_COLOR if not point.post else CITY_COLOR if point.post.type == 1 else SHOP_COLOR
            pf = pygame.Surface((multiplier, multiplier))
            pf.fill(Color(COLOR))
            self.screen.blit(pf, (point.x * multiplier, point.y * multiplier))
        pygame.display.update()

    def __del__(self):
        self.loop.run_until_complete(self.cl.logout())
        print("logout")


game = Game('test-client20')
n = 10
while n:
    game.update(n)
    n -= 1
    time.sleep(1)

del game
