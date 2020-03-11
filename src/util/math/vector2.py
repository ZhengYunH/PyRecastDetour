class Vector2(object):
    def __init__(self, x=0, y=0):
        self.data = [x, y]

    def __getitem__(self, item: int):
        return self.data[item % 2]

