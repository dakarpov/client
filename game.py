import asyncio
import client
from models.player import Player

import time

loop = asyncio.get_event_loop()
cl = client.Client(loop)

# 'wgforge-srv.wargaming.net', 443
# '127.0.0.1', 2000
loop.run_until_complete(cl.connect('127.0.0.1', 2000))
res, msg = loop.run_until_complete(cl.login('test-client'))
player = Player(msg)
print(str(player.trains))
print(str(msg))
res, msg = loop.run_until_complete(cl.getMap(0))
time.sleep(1)
loop.run_until_complete(cl.logout())
print("logout")
