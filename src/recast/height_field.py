from recast.base_object import BaseObject
from util.math.grid import Grid
from util.math.triangle import Triangle
from util.math.vector3 import Vector3
from util.math import math_common


class Span(BaseObject):
    def __init__(self, smin, smax, area):
        self.smin = smin
        self.smax = smax
        self.area = area


class HeightField(BaseObject):
    def __init__(self, config):
        self.grid = Grid(depth=config.depth, width=config.width, data_type=list)
        self.bmin = config.bmin
        self.bmax = config.bmax
        self.cell_size = config.cell_size
        self.cell_height = config.cell_height
        self.flag_merge_threshold = config.flag_merge_threshold

    def add_triangle(self, triangle: Triangle):
        height_field_bbox = [self.bmin, self.bmax]
        triangle_bbox = triangle.get_bbox()

        # 判断当前三角形是否在当前的heightfield的bbox中
        if not math_common.overlap_bounds(height_field_bbox, triangle_bbox):
            return

        # 将三角形转换到height field的grid空间中
        triangle_bbox_min, triangle_bbox_max = triangle_bbox
        hf_zmin = self.real_value_to_grid(triangle_bbox_min.z, axis=Vector3.AXIS.Z)
        hf_zmax = self.real_value_to_grid(triangle_bbox_max.z,  axis=Vector3.AXIS.Z)

        remain = triangle.get_data()

        for hf_z in range(hf_zmin, hf_zmax):
            # 切割多边形。保存剩下的多边形在remain中，下次循环使用
            real_cell_z = self.grid_to_real_value(hf_z, axis=Vector3.AXIS.Z)
            inrow, remain = self.divide_poly(remain, real_cell_z, Vector3.AXIS.Z)
            if len(inrow) < 3:
                continue

            # 找到当前待光栅化部分的上下届 并住转换到grid
            xmin = Vector3.min(*inrow).x
            xmax = Vector3.max(*inrow).x
            hf_xmin = self.real_value_to_grid(xmin, axis=Vector3.AXIS.X)
            hf_xmax = self.real_value_to_grid(xmax, axis=Vector3.AXIS.X)

            for hf_x in range(hf_xmin, hf_xmax):
                real_cell_x = self.grid_to_real_value(hf_x, axis=Vector3.AXIS.X)
                p1, _ = self.divide_poly(inrow, real_cell_x, Vector3.AXIS.X)
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
                
                self.add_span(hf_x, hf_z, hf_ymin, hf_ymax, triangle.area)

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
        """切割多边形，返回切出去的部分和剩余部分；切割线由value和axis决定（切割线只能平行于坐标轴）

        :param be_divided: 待切割的多边形
        :param dividing_value: 切割线值
        :param axis: 切割线平行轴
        :return: inrow, remain -> 切出去的部分和剩余部分
        """
        inrow = []
        remain = []

        # 计算所有的点到分割线的距离
        distances = []
        for point in be_divided:
            distances.append(dividing_value - point.get_axis_value(axis))

        for index in range(len(be_divided)):
            cur_point = be_divided[index]
            prev_point = be_divided[index-1]
            ina = distances[index] >= 0
            inb = distances[index-1] >= 0

            if ina != inb:
                factor = distances[index] / distances[index] - distances[index-1]
                point_on_dividing_line = prev_point.add(cur_point.sub(prev_point).mul(factor))
                inrow.append(point_on_dividing_line)
                if distances[index] > 0:
                    remain.append(cur_point)
                else:
                    inrow.append(cur_point)
            else:
                if distances[index] >= 0:
                    remain.append(cur_point)
                    if distances[index] != 0:
                        continue
                inrow.append(cur_point)
        return inrow, remain

    def add_span(self, hf_x, hf_z, hf_ymin, hf_ymax, area):
        spans_column = self.grid[hf_z][hf_x]
        span_handle = Span(hf_ymin, hf_ymax, area)
        insert_index = -1
        inserted = False
        for index, cur_span in enumerate(spans_column):
            if cur_span.smin > span_handle.smax:
                if not inserted:  # 还没有被合并，需要加到列表中
                    insert_index = index
                    inserted = True
                break
            elif cur_span.smax < span_handle.smin:
                continue
            else:   # overlap
                # merge span
                span_handle.smin = min(span_handle.smin, cur_span.smin)
                span_handle.smax = max(span_handle.smax, cur_span.smax)
                if span_handle.smax - cur_span.smax < self.flag_merge_threshold:
                    span_handle.area = cur_span.area
                inserted = True
        if inserted:
            if insert_index >= 0:
                self.grid[hf_z][hf_x] = spans_column.insert(insert_index, span_handle)
        else:
            self.grid[hf_z][hf_x].append(span_handle)

