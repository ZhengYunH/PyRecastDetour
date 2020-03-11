from recast.base_object import BaseObject
from util.math.grid import Grid
from util.math.triangle import Triangle


class HeightField(BaseObject):
    def __init__(self, owner):
        self.owner = owner
        self.span = Grid(depth=owner.config.depth, width=owner.config.width, data_type=int)

    def rasterize_triangle(self, triangle: Triangle):
        pass