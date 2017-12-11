from models.point import Point
from models.line import Line

class Map(object):
    def __init__(self, json_l0):
        self.point = set()
        self.line = set()
        for point in json_l0['point']:
            self.point.add(Point(point))
        for line in json_l0['line']:
            self.line.add(Line(line))

    def add_layer_10(self, json_l10):
        if not len(json_l10):
            return
        coordinate = {x['idx']: (x['x'], x['y']) for x in json_l10['coordinate']}
        for point in self.point:
            point.set_coordinates(coordinate[point.idx][0], coordinate[point.idx][1])
        self.size = json_l10['size']
