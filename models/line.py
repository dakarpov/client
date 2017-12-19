from models.point import Point

class Line(object):
    def __init__(self, json_line):
        self.idx = json_line['idx']
        self.length = json_line['length']
        self.point_idx = json_line['point']
        self.point = None

    def set_points(self, point1, point2):
        self.point = [point1, point2]
