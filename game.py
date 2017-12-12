import asyncio
import client
from models.player import Player
from models.map import Map

import time


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
        _, msg = self.loop.run_until_complete(self.cl.getMap(10))
        self.map.add_layer_10(msg)
        # print(msg)

    def __del__(self):
        self.loop.run_until_complete(self.cl.logout())
        print("logout")


game = Game('test-client18')
del game
