class Type:
    TOWN = 1
    MARKET = 2


class Post(object):
    def __init__(self, json_post):
        self.idx = json_post['idx']
        self.name = json_post['name']
        self.type = json_post['type']
        if self.type == Type.TOWN:
            self.population = json_post['population']
            self.armor = json_post['armor']
            self.product = json_post['product']
        if self.type == Type.MARKET:
            self.product_capacity = json_post['product']
            self.replenishment = json_post['replenishment']
