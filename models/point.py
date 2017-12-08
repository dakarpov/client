class Point(object):
    def __init__(self, json_point):
        self.idx = json_point['idx']
        self.post_id = json_point['post_id']
