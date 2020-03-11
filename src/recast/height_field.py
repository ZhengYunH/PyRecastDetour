from recast.base_object import BaseObject
from util.math.grid import Grid
from util.math.triangle import Triangle
from util.math.vector3 import Vector3
from util.math import math_common


class HeightField(BaseObject):
    def __init__(self, config):
        self.grid = Grid(depth=config.depth, width=config.width, data_type=int)
        self.bmin = config.bmin
        self.bmax = config.bmax
        self.cell_size = config.cell_size
        self.cell_height = config.cell_height

    def add_triangle(self, triangle: Triangle):
        height_field_bbox = [self.bmin, self.bmax]
        triangle_bbox = triangle.get_bbox()

        # 判断当前三角形是否在当前的heightfield的bbox中
        if not math_common.overlap_bounds(height_field_bbox, triangle_bbox):
            return

        # 将三角形转换到height field的grid中
        triangle_bbox_min, triangle_bbox_max = triangle_bbox
        hf_zmin = self.real_value_to_grid(triangle_bbox_min.z, axis=Vector3.AXIS.Z)
        hf_zmax = self.real_value_to_grid(triangle_bbox_max.z,  axis=Vector3.AXIS.Z)

        remain = triangle.get_data()

        for hf_z in range(hf_zmin, hf_zmax):
            # 切割多边形。保存剩下的多边形在remain中，下次循环使用
            real_cell_z =  self.grid_to_real_value(hf_z, axis=Vector3.AXIS.Z)
            inrow = self.divide_poly(remain, real_cell_z, Vector3.AXIS.Z)
            if len(inrow) < 3:
                continue

            # 找到当前待光栅化部分的上下届 并住转换到grid
            xmin = Vector3.min(*inrow).x
            xmax = Vector3.max(*inrow).x
            hf_xmin = self.real_value_to_grid(xmin, axis=Vector3.AXIS.X)
            hf_xmax = self.real_value_to_grid(xmax, axis=Vector3.AXIS.X)

            for hf_x in range(hf_xmin, hf_xmax):
                real_cell_x = self.grid_to_real_value(hf_x, axis=Vector3.AXIS.X)
                p1 = self.divide_poly(inrow, real_cell_x, Vector3.AXIS.X)
                if len(p1) < 3:
                    continue

                # 找到当前column对应span的上下届
                ymin = Vector3.min(*p1).y
                ymax = Vector3.max(*p1).y
                if ymax < self.bmin.y: continue
                if ymin > self.bmax.y: continue
                hf_ymin = self.real_value_to_grid(ymin, axis=Vector3.AXIS.Y)
                hf_ymax = self.real_value_to_grid(ymax, axis=Vector3.AXIS.Y)
                if hf_ymax <= hf_ymin:
                    hf_ymax = hf_ymin + 1
                
                self.add_span(hf_x, hf_z, hf_ymin, hf_ymax)



        # TODO

    def real_value_to_grid(self, real_value, axis: Vector3.AXIS):
        if axis == Vector3.AXIS.X:
            max_value = self.grid.width
        elif axis == Vector3.AXIS.Z:
            max_value = self.grid.depth
        else:
            max_value = 0xffff # TODO: 大数
        divisor = self.cell_size if axis != Vector3.AXIS.Y else self.cell_height
        hf_value = float(real_value - self.bmin[axis]) / divisor
        hf_value = math_common.clamp(hf_value, 0, max_value-1)
        return hf_value

    def grid_to_real_value(self, grid_value, axis: Vector3.AXIS):
        multiplier = self.cell_size if axis != Vector3.AXIS.Y else self.cell_height
        base = self.bmin[axis]
        return base + grid_value * multiplier

    def divide_poly(self, be_divided, dividing_value, axis: Vector3.AXIS):
        inrow = []
        return inrow

    def add_span(self, hf_x, hf_z, hf_ymin, hf_ymax):
        pass






