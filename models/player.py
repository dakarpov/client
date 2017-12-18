from models.point import Point
from models.train import Train
from models.post import Post


class Player(object):
    """
    Player is the object that contain all player's property and who is making moves
    """
    def __init__(self, json_player):
        """
        Initialization of player. Player have got only one city and some trains
        :param json_player: json object received from server
        """
        self.home = Point(json_player['home'])
        self.town = Post(json_player['town'])
        self.idx = json_player['idx']
        self.name = json_player['name']
        self.trains = [Train(json_train) for json_train in json_player['train']]
