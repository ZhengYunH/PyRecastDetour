class Grid(object):
    def __init__(self, depth, width, data_type):
        self.depth = depth
        self.width = width
        self.data_type = data_type
        self.data = self.init_data()

    def init_data(self):
        data = []
        for d in range(self.depth):
            row_lst = []
            for w in range(self.width):
                row_lst.append(self.data_type())
            data.append(row_lst)
        return data

    def __getitem__(self, item):
        item = item % self.depth
        return self.data[item]

