class Point(object):
    def __init__(self, json_point):
        self.idx = json_point['idx']
        self.post_id = json_point['post_id']
        self.x = None
        self.y = None

    def set_coordinates(self, x, y):
        self.x = x
        self.y = y
