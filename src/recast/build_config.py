from util.math.vector3 import Vector3


class BuildConfig(object):
    def __init__(self):
        self.cell_size = 10
        self.cell_height = 10

        self.bmin = Vector3([0,0,0])
        self.bmax = Vector3([0,0,0])

        self.width = 0
        self.depth = 0

        self.walkable_slope_angle = 70
        self.walkable_height = 0

        self.flag_merge_threshold = 1

    def init(self):
        self.calc_grid_size()

    def calc_grid_size(self):
        self.width = int((self.bmax[0] - self.bmin[0])/self.cell_size + 0.5)
        self.depth = int((self.bmax[2] - self.bmin[2])/self.cell_size + 0.5)
