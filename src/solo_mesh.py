from recast.base_object import BaseObject
from recast.context import Context
from recast.build_config import BuildConfig
from recast.geom import Geom
from recast.height_field import HeightField


class SoloMesh(BaseObject):
    """
    基本的build mesh流程
    """
    def __init__(self, context: Context, config: BuildConfig, geom: Geom):
        self.context = context
        self.config = config
        self.geom = geom

        self.height_field = None
        self.compact_height_field = None

    def build_navmesh(self):
        if (not self.geom) or (not self.geom.get_mesh()):
            self.context.log(Context.LOG_LEVEL.ERROR, "buildNavigation: Input mesh is not specified.")
            return False

        self.init() # 初始化
        self.rasterize_triangles()  # 体素化
        self.filter_walkable_surfaces() # 筛选可行走表面
        self.build_region() # 转化为region
        self.build_contours() # 转化为轮廓线
        self.build_polygon_mesh() # 多边形mesh
        self.build_poly_mesh_detail() # 修正height
        self.create_navmesh_data()  # (optional) step8

    def init(self):
        self.clean_up()
        self.context.init()
        self.config.init()
        self.geom.init()

    def rasterize_triangles(self):
        self.geom.mark_walkable_triangles(self.config.walkable_slope_angle) # 一定角度的三角面才是walkable的
        self.height_field = HeightField(config=self.config)
        for tri in self.geom.get_tris():
            self.height_field.add_triangle(triangle=tri)

    def filter_walkable_surfaces(self):
        pass

    def build_region(self):
        # build_compact_height_field()
        # erode_walkable_area()
        # TODO: (optional) mark areas
        # build_region的3个方法
        # build_distance_field
        # build_region_detail
        pass

    def build_contours(self):
        pass

    def build_polygon_mesh(self):
        pass

    def build_poly_mesh_detail(self):
        pass

    def create_navmesh_data(self):
        pass

    def clean_up(self):
        pass



