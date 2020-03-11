from util.math.triangle import Triangle


class Geom(object):
    class AREA_TYPE(object):
        WALKABLE = 63
        NULL = 0

    def __init__(self, verts, tris_index):
        self.verts = verts
        self.tris_index = tris_index
        self.tris = []
        self.areas = []

    def init(self):
        self.tris.clear()
        self.areas.clear()
        for v_index in self.tris_index:
            self.tris.append(Triangle([
                self.verts[v_index[0]],
                self.verts[v_index[1]],
                self.verts[v_index[2]]
            ]))
        self.areas = [Geom.AREA_TYPE.NULL] * len(self.tris)


    def get_tris(self):
        return self.tris

    def get_mesh(self):
        pass

    def mark_walkable_triangles(self, walkable_slope_angle):
        import math
        walkable_threshold = math.cos(walkable_slope_angle / 180.0 * math.pi)
        for index, tri in enumerate(self.get_tris()):
            if tri.get_normal()[1] > walkable_threshold:
                self.areas[index] = Geom.AREA_TYPE.WALKABLE