class Vector3(object):
    def __init__(self, raw_data=None, data_type=None):
        self.inited = False
        if not raw_data: # 留个placeHolder，到时候set的时候再初始化
            return
        self.data_type = data_type if data_type else type(raw_data[0])
        self.data = self.init_data(raw_data)

    def init_data(self, raw_data):
        data_type = self.data_type
        data = []
        for i, d in enumerate(raw_data):
            if i > 2: # TODO: add WARNING info
                break
            # d_copy = d
            if not isinstance(d, data_type):
                d = data_type(d)
            data.append(d)
        self.inited = True
        return data

    def __getitem__(self, item: int):
        return self.data[item % 3]

    def __setitem__(self, key, value):
        self.data[key % 3] = value

