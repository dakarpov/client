from models.point import Point
from models.line import Line
from models.post import Post


class Map(object):
    def __init__(self, json_l0):
        self.point = set()
        self.line = set()
        for point in json_l0['point']:
            self.point.add(Point(point))
            print(point)
        for line in json_l0['line']:
            self.line.add(Line(line))
        self.size = None

    def add_layer_10(self, json_l10):
        if not len(json_l10):
            return
        coordinate = {x['idx']: (x['x'], x['y']) for x in json_l10['coordinate']}
        for point in self.point:
            point.set_coordinates(coordinate[point.idx][0], coordinate[point.idx][1])
        self.size = json_l10['size']

    def add_layer_1(self, json_l1):
        post = {x['idx']: x for x in json_l1['post']}
        for point in self.point:
            if point.post_id:
                point.set_post(Post(post[point.post_id]))
