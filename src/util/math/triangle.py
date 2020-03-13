from util.math.vector3 import Vector3

class Triangle(Vector3):
    def __init__(self, v0=None, v1=None, v2=None, data_type=Vector3):
        super(Triangle, self).__init__([v0, v1, v2], data_type=data_type)
        self.area = None

    def set_data(self, v0=None, v1=None, v2=None):
        if v0: self.data[0] = v0
        if v1: self.data[1] = v1
        if v2: self.data[2] = v2
        # v0 and (self.data[0]=v0)
        # v1 and (self.data[1]=v1)
        # v2 and (self.data[2]=v2)

    def set_area(self, area):
        self.area = area

    def get_data(self):
        return self.data

    def get_normal(self):
        return Vector3()

    def get_bbox(self):
        bbox_min = Vector3.min(*self.data)
        bbox_max = Vector3.max(*self.data)
        return bbox_min, bbox_max
