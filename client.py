# NOTES
# logout doesn't send result of operation.
# no information about how world is simulated and how player should communicate with it.
# sometimes server returns just code instead of code and data length. For example when you login if you already have been logined.

import json
import asyncio
import struct
import time


class COMMANDS(object):
    LOGIN = 1
    LOGOUT = 2
    MOVE = 3
    UPDATE = 4
    TURN = 5
    MAP = 10


class RESULT(object):
    OK = 0
    BAD_COMMAND = 1
    RESOURCE_NOT_FOUND = 2
    PATH_NOT_FOUND = 3
    ACCESS_DENIED = 5


def makeCommand(id, data):
    return struct.pack('<II', id, len(data)) + bytearray(data, encoding='utf8')


def loginCommand(name):
    return makeCommand(COMMANDS.LOGIN, json.dumps({'name': name}))


class Client(object):
    def __init__(self, loop):
        self.loop = loop
        self.reader, self.writer = None, None

    async def connect(self, host, port):
        self.reader, self.writer = await asyncio.open_connection(host, port, loop=self.loop)

    async def login(self, name):
        cmd = makeCommand(COMMANDS.LOGIN, json.dumps({'name': name}))
        await self.__sendCommand(cmd)
        res, msg = await self.__receiveResponse()
        return res, msg

    async def logout(self):
        cmd = makeCommand(COMMANDS.LOGOUT, '')
        await self.__sendCommand(cmd)
        return RESULT.OK, {}

    async def getMap(self, layer=0):
        cmd = makeCommand(COMMANDS.MAP, json.dumps({'layer': layer}))
        await self.__sendCommand(cmd)
        res, msg = await self.__receiveResponse()
        return res, msg

    async def move(self, line_idx, speed, train_idx):
        cmd = makeCommand(COMMANDS.MOVE, json.dumps({'line_idx': line_idx, "speed": speed, "train_idx": train_idx}))
        await self.__sendCommand(cmd)
        res, msg = await self.__receiveResponse()
        return res, msg

    async def __sendCommand(self, command):
        self.writer.write(command)

    async def __receiveResponse(self):
        res_ = struct.unpack('<I', await self.reader.read(4))[0]
        len_ = struct.unpack('<I', await self.reader.read(4))[0]
        msg = ''
        if res_ == RESULT.OK and len_ > 0:
            tmp = await self.reader.read(len_)
            while len(tmp) != len_:
                tmp += await self.reader.read(len_ - len(tmp))
            msg = json.loads(tmp)
        return res_, msg


class Player:
    def __init__(self):
        self.loop = asyncio.get_event_loop()
        self.client = Client(self.loop)
        self.loop.run_until_complete(self.client.connect('wgforge-srv.wargaming.net', 443)) #'127.0.0.1', 2000)) #('wgforge-srv.wargaming.net', 443))
        self.loop.run_until_complete(self.client.login('test-client'))
        self.G = {}
        self.build_graph()

    def build_graph(self):
        res_map_layer_0 = self.loop.run_until_complete(self.client.getMap(0))[1]
        line = {x['idx']: x for x in res_map_layer_0['line']}
        point = {x['idx']: x for x in res_map_layer_0['point']}

        # build graph
        for point_ in point.keys():
            self.G[point_] = {}
            for line_ in line.values():
                if point_ in line_['point']:
                    self.G[point_][[x for x in line_['point'] if x != point_][0]] = \
                        {
                            'length': line_['length'],
                            'idx': line_['idx'],
                            'direction': 1 if line_['point'][0] == point_ else -1
                        }

    def find(self, type_):
        # type = 1 home
        # type = 2 shop
        assert type(type_) is int
        res_map_layer_0 = self.loop.run_until_complete(self.client.getMap(0))[1]
        res_map_layer_1 = self.loop.run_until_complete(self.client.getMap(1))[1]
        post = {x['idx']: x for x in res_map_layer_1['post']}
        train = {x['idx']: x for x in res_map_layer_1['train']}
        line = {x['idx']: x for x in res_map_layer_0['line']}
        point = {x['idx']: x for x in res_map_layer_0['point']}
        home = dict()
        for post_ in post.values():
            if post_['type'] == type_:
                home['post'] = post_['idx']
                for point_ in point.values():
                    if point_.get('post_id', None) == home['post']:
                        home['point'] = point_['idx']
                        break
                break
        description = 'Home' if type_ == 1 else 'Shop' if type_ == 2 else 'Unknown'
        print("{} post is {} point is {}".format(description, home['post'], home['point']))
        return home

    def find_way(self, point1, point2):
        # find way
        cost, path = Player.dijsktra(self.G, point1)
        # build post array
        s = [point2]
        lines = []
        while s[-1] != point1:
            s.append(path[s[-1]])
        s = s[::-1]
        # format it to lines and directions
        for p1, p2 in zip(s[:-1], s[1:]):
            lines.append((self.G[p1][p2]['idx'], self.G[p1][p2]['direction']))
        return lines

    @staticmethod
    def dijsktra(graph, initial):
        visited = {initial: 0}
        path = {}

        nodes = set(graph.keys())

        while nodes:
            min_node = None
            for node in nodes:
                if node in visited:
                    if min_node is None:
                        min_node = node
                    elif visited[node] < visited[min_node]:
                        min_node = node

            if min_node is None:
                break

            nodes.remove(min_node)
            current_weight = visited[min_node]

            for edge in graph[min_node].keys():
                weight = current_weight + graph[min_node][edge]['length']
                if edge not in visited or weight < visited[edge]:
                    visited[edge] = weight
                    path[edge] = min_node

        return visited, path

    def send_train(self, line, direction, train):
        self.loop.run_until_complete(self.client.move(line, direction, train))
        finish = 0 if direction == -1 else 10
        while self.check_train_status(train)[1] != finish:
            time.sleep(1)
            print(str(self.check_train_status(train)[0:2]))

    def check_train_status(self, train_idx):
        res_map_layer_1 = self.loop.run_until_complete(self.client.getMap(1))[1]
        train = {x['idx']: x for x in res_map_layer_1['train']}
        return train[train_idx]['line_idx'], train[train_idx]['position'], train[train_idx]['speed']

    def check_town_status(self, town_idx):
        res_map_layer_1 = self.loop.run_until_complete(self.client.getMap(1))[1]
        posts = {x['idx']: x for x in res_map_layer_1['post']}
        return posts[town_idx]['population'], posts[town_idx]['product']

    def lab_1(self):
        # send train from town to shop and back. Check that product is shipped to the town
        home = self.find(1)
        shop = self.find(2)

        print(str(self.check_town_status(home['post'])))
        way_to_shop = self.find_way(home['point'], shop['point'])
        way_to_home = self.find_way(shop['point'], home['point'])
        print(way_to_shop)
        print(way_to_home)
        for s in way_to_shop:
            self.send_train(*s, 0)
        for s in way_to_home:
            self.send_train(*s, 0)
        print("population: {} product: {}".format(*self.check_town_status(home['post'])))

    def lab_2(self):
        # population 3 people
        pass


#player = Player()
#player.lab_1()
