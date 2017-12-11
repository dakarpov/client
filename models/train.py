class Train(object):

    def __init__(self, json_train):
        self.idx = json_train['idx']
        self.line_idx = json_train['line_idx']
        self.position = json_train['position']
        self.speed = json_train['speed']
        self.player_id = json_train['player_id']
        #self.capacity = json_train['capacity']
        #self.product = json_train['product']

    def get_position(self):
        return self.position

    def get_line(self):
        return self.line_idx
