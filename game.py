import asyncio
import client
from models.player import Player
from models.map import Map

import time

loop = asyncio.get_event_loop()
cl = client.Client(loop)

# 'wgforge-srv.wargaming.net', 443
# '127.0.0.1', 2000
loop.run_until_complete(cl.connect('wgforge-srv.wargaming.net', 443))
_, msg = loop.run_until_complete(cl.login('test-client14'))
player = Player(msg)
print(str(player.trains))
print(str(msg))
_, msg = loop.run_until_complete(cl.getMap(0))
map = Map(msg)
_, msg = loop.run_until_complete(cl.getMap(10))
map.add_layer_10(msg)
print(msg)
loop.run_until_complete(cl.logout())
print("logout")
