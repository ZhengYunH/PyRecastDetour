class Vector3(object):
    class AXIS(object):
        X = 0
        Y = 1
        Z = 2

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

    def get_axis_value(self, axis):
        return self.data[axis % 3]

    def add(self, v):
        data = []
        for i, d in enumerate(self.data):
            data.append(d + v[i])
        return Vector3(data)

    def sub(self, v):
        data = []
        for i, d in enumerate(self.data):
            data.append(d - v[i])
        return Vector3(data)

    def mul(self, factor):
        data = []
        for d in self.data:
            data.append(d * factor)
        return Vector3(data)

    @staticmethod
    def compare(op, restrict, *args):
        OP_FUNC_DICT = {
            'min': lambda x, y: x < y,
            'max': lambda x, y: x > y,
        }

        data = []
        for index in range(args[0]):
            cur = args[0][index]
            for v in args[1:]:
                if OP_FUNC_DICT[op](v[index], cur):
                    cur = v[index]
            data.append(cur)
        return data

    @staticmethod
    def min(*args, **kwargs): # TODO: 加一下restrict
        return Vector3.compare('min', None, *args)

    @staticmethod
    def max(*args, **kwargs):
        return Vector3.compare('max', None, *args)

    def equal(self, v):
        if not isinstance(v, Vector3):
            return False
        for index, num in enumerate(self.data):
            if num != v[index] :
                return False
        return True

