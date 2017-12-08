from models.point import Point
from models.train import Train


class Player(object):
    def __init__(self, json_player):
        self.home = Point(json_player['home'])
        self.idx = json_player['idx']
        self.name = json_player['name']
        self.trains = [Train(json_train) for json_train in json_player['train']]
