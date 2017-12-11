class Line(object):
    def __init__(self, json_line):
        self.idx = json_line['idx']
        self.length = json_line['length']
        self.point = json_line['point']